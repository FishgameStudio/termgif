"""termgif.convert

Convert a cast JSON (as produced by record_win.py) to a GIF.

Usage:
  python convert.py session.cast demo.gif --fps 12 --font-size 14
"""

# pyright: reportUnusedCallResult=false, reportExplicitAny=false
# pyright: reportAny=false, reportUnknownVariableType=false
# pyright: reportUnknownArgumentType=false

from __future__ import annotations

import argparse
import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from pyte.screens import Char, StaticDefaultDict
from typing import Any, cast as _typing_cast
from collections.abc import Sequence
import pyte
from PIL import Image, ImageChops, ImageDraw, ImageFont

CURDIR: str = os.path.dirname(__file__)


logger = logging.getLogger("termgif.convert")
logger.addHandler(logging.NullHandler())

DEFAULT_FONTS: list[str] = [
    f"{CURDIR}/assets/UbuntuMono-r.ttf",
    "C:\\Windows\\Fonts\\Consola.ttf",
    "C:\\Windows\\Fonts\\vgasyst.fon",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/Library/Fonts/Andale Mono.ttf",
]


@dataclass
class Frame:
    image: Image.Image  # palette mode
    duration_ms: int


def _char_size(font: ImageFont.ImageFont) -> tuple[int, int]:
    """Return (char_width, char_height) for monospace font."""
    # try:
    bbox: tuple[int, int, int, int] = font.getbbox("M")
    cw: int = bbox[2] - bbox[0]
    ch: int = bbox[3] - bbox[1]
    print(f"cw: {cw}, ch: {ch}")
    if cw > 0 and ch > 0:
        return cw, ch
    # except Exception as e:
    #    print(f"Exception: {e}, pass")
    #    pass

    # Fallback; different Pillow versions expose different APIs
    try:
        # font.getsize is deprecated
        left, top, right, bottom = font.getbbox("M")
        w: int = right - left
        h: int = bottom - top
        return w, h
    except Exception:
        return 8, 16


def choose_font(font_path: str | None, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    if font_path:
        try:
            return ImageFont.truetype(font_path, size)
        except Exception as exc:
            logger.warning("Failed to load font %s: %s", font_path, exc)

    for p in DEFAULT_FONTS:
        try:
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
        except Exception:
            continue

    logger.warning("No TTF font found; falling back to default bitmap font.")
    return ImageFont.load_default()


def _screen_line(screen: pyte.Screen, row: int) -> str:
    # Preferred API: screen.display
    if hasattr(screen, "display"):
        try:
            return screen.display[row]
        except Exception:
            pass

    # Fallback: screen.buffer
    try:
        row_buf: StaticDefaultDict[int, Char] | list[Any] = screen.buffer.get(row, [])
    except Exception:
        try:
            row_buf = screen.buffer[row]
        except Exception:
            return ""

    out: list[str] = []
    for cell in row_buf:
        if isinstance(cell, str):
            out.append(cell)
        else:
            out.append(getattr(cell, "data", None) or getattr(cell, "char", None) or "")
    return "".join(out)


def render_screen_to_image(
    screen: pyte.Screen,
    font: ImageFont.ImageFont,
    fg: tuple[int, int, int] = (255, 255, 255),
    bg: tuple[int, int, int] = (0, 0, 0),
) -> Image.Image:
    cw, ch = _char_size(font)
    width_px = screen.columns * cw
    height_px = screen.lines * ch

    img = Image.new("RGB", (width_px, height_px), bg)
    draw = ImageDraw.Draw(img)

    for r in range(screen.lines):
        line = _screen_line(screen, r)
        draw.text(xy=(0, r * ch), text=line, font=font, fill=fg)

    return img


def _images_equal(a: Image.Image, b: Image.Image) -> bool:
    if a.size != b.size:
        return False
    diff = ImageChops.difference(a.convert("RGBA"), b.convert("RGBA"))
    return diff.getbbox() is None


def convert_cast_to_gif(
    cast_path: str | Path,
    out_gif: str | Path,
    font_path: str | None = None,
    font_size: int = 14,
    fps: int = 12,
    dedupe_identical_frames: bool = False,
    min_frame_ms: int = 80,
) -> None:
    cast_file: Path = Path(cast_path)
    if not cast_file.exists():
        raise FileNotFoundError(f"Cast file not found: {cast_file}")

    with cast_file.open("r", encoding="utf-8") as f:
        cast: dict[str, Any] = json.load(f)

    cols = int(cast.get("width", 80))
    lines = int(cast.get("height", 24))
    events: list[Any] = cast.get("events", [])

    screen: pyte.Screen = pyte.Screen(cols, lines)
    stream: pyte.Stream = pyte.Stream(screen)
    font: ImageFont.ImageFont = _typing_cast(ImageFont.ImageFont, choose_font(font_path, font_size))

    # Ensure stable ordering
    def _key(e: Any) -> float:
        try:
            return float(e[0])
        except Exception:
            return 0.0

    events = sorted(events, key=_key)

    frames: list[Frame] = []
    last_t: float = 0.0
    last_img_rgb: Image.Image | None = None

    if not events:
        img = render_screen_to_image(screen, font)
        frames.append(
            Frame(image=img.convert("P", palette=Image.Palette.ADAPTIVE), duration_ms=max(1, int(1000 / fps)))
        )
    else:
        for ev in events:

            if not isinstance(ev, (list, tuple)) or len(ev) < 2:
                continue

            t_raw: Any = ev[0]
            data: str = ev[1]

            t: float
            try:
                t = float(t_raw)
            except Exception:
                t = last_t

            try:
                stream.feed(data)
            except Exception:
                # If pyte can't parse some escape sequences, keep going
                continue

            img_rgb: Image.Image = render_screen_to_image(screen, font)
            duration_ms: int
            if last_t == 0.0:
                duration_ms = max(1, int(1000 / fps))
            else:
                duration_ms = max(1, int((t - last_t) * 1000))
            last_t = t

            if dedupe_identical_frames and last_img_rgb is not None:
                try:
                    if _images_equal(img_rgb, last_img_rgb) and frames:
                        frames[-1].duration_ms += duration_ms
                        continue
                except Exception:
                    pass

            duration_ms = max(duration_ms, min_frame_ms)
            frames.append(Frame(image=img_rgb.convert("P", palette=Image.Palette.ADAPTIVE), duration_ms=duration_ms))
            last_img_rgb = img_rgb

    if not frames:
        raise RuntimeError("No frames were produced from cast.")

    out_path = Path(out_gif)
    if out_path.parent and not out_path.parent.exists():
        out_path.parent.mkdir(parents=True, exist_ok=True)

    durations = [max(1, int(f.duration_ms)) for f in frames]
    images = [f.image for f in frames]

    images[0].save(
        str(out_path),
        save_all=True,
        append_images=images[1:],
        duration=durations,
        loop=0,
        disposal=2,
    )

    logger.info("Wrote GIF %s (%d frames)" % (out_path, len(frames)))


def _parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="convert", description="Convert cast JSON to GIF")
    p.add_argument("infile", help="Input cast JSON path")
    p.add_argument("outfile", help="Output GIF path")
    p.add_argument("--font", help="Path to TTF font")
    p.add_argument("--font-size", type=int, default=14, help="Font size")
    p.add_argument("--fps", type=int, default=12, help="Fallback FPS")
    p.add_argument("--debug", action="store_true", help="Enable debug logging")
    return p.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args: argparse.Namespace = _parse_args(argv)
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO, format="%(levelname)s: %(message)s")
    convert_cast_to_gif(
        args.infile,
        args.outfile,
        font_path=args.font,
        font_size=args.font_size,
        fps=args.fps,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
