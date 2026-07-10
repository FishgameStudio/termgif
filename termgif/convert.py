#!/usr/bin/env python3
"""termgif.convert

Convert a cast JSON (as produced by record_win.py) to a GIF.

Usage:
  python convert.py session.cast demo.gif --fps 12 --font-size 14
"""

from __future__ import annotations

import argparse
import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Optional, Sequence, Tuple

import pyte
from PIL import Image, ImageChops, ImageDraw, ImageFont

logger = logging.getLogger("termgif.convert")
logger.addHandler(logging.NullHandler())

DEFAULT_FONTS: List[str] = [
    "assets/DejaVuSansMono.ttf",
    "C:\\Windows\\Fonts\\Consola.ttf",
    "C:\\Windows\\Fonts\\DejaVuSansMono.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/Library/Fonts/Andale Mono.ttf",
]


@dataclass
class Frame:
    image: Image.Image  # palette mode
    duration_ms: int


def _char_size(font: ImageFont.ImageFont) -> Tuple[int, int]:
    """Return (char_width, char_height) for monospace font."""
    try:
        bbox = font.getbbox("M")
        cw = bbox[2] - bbox[0]
        ch = bbox[3] - bbox[1]
        if cw > 0 and ch > 0:
            return cw, ch
    except Exception:
        pass

    # Fallback; different Pillow versions expose different APIs
    try:
        w, h = font.getsize("M")  # type: ignore[attr-defined]
        return int(w), int(h)
    except Exception:
        return 8, 16


def choose_font(font_path: Optional[str], size: int) -> ImageFont.ImageFont:
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
        row_buf = screen.buffer.get(row, [])  # type: ignore[union-attr]
    except Exception:
        try:
            row_buf = screen.buffer[row]  # type: ignore[index]
        except Exception:
            return ""

    out: List[str] = []
    for cell in row_buf:
        if isinstance(cell, str):
            out.append(cell)
        else:
            out.append(getattr(cell, "data", None) or getattr(cell, "char", None) or "")
    return "".join(out)


def render_screen_to_image(
    screen: pyte.Screen,
    font: ImageFont.ImageFont,
    fg: Tuple[int, int, int] = (255, 255, 255),
    bg: Tuple[int, int, int] = (0, 0, 0),
) -> Image.Image:
    cw, ch = _char_size(font)
    width_px = screen.columns * cw
    height_px = screen.lines * ch

    img = Image.new("RGB", (width_px, height_px), bg)
    draw = ImageDraw.Draw(img)

    for r in range(screen.lines):
        line = _screen_line(screen, r)
        draw.text((0, r * ch), line, font=font, fill=fg)

    return img


def _images_equal(a: Image.Image, b: Image.Image) -> bool:
    if a.size != b.size:
        return False
    diff = ImageChops.difference(a.convert("RGBA"), b.convert("RGBA"))
    return diff.getbbox() is None


def convert_cast_to_gif(
    cast_path: str | Path,
    out_gif: str | Path,
    font_path: Optional[str] = None,
    font_size: int = 14,
    fps: int = 12,
    dedupe_identical_frames: bool = False,
    min_frame_ms: int = 80,
) -> None:
    cast_file = Path(cast_path)
    if not cast_file.exists():
        raise FileNotFoundError(f"Cast file not found: {cast_file}")

    with cast_file.open("r", encoding="utf-8") as f:
        cast = json.load(f)

    cols = int(cast.get("width", 80))
    lines = int(cast.get("height", 24))
    events: List[Any] = cast.get("events", [])

    screen = pyte.Screen(cols, lines)
    stream = pyte.Stream(screen)
    font = choose_font(font_path, font_size)

    # Ensure stable ordering
    def _key(e: Any) -> float:
        try:
            return float(e[0])
        except Exception:
            return 0.0

    events = sorted(events, key=_key)

    frames: List[Frame] = []
    last_t: float = 0.0
    last_img_rgb: Optional[Image.Image] = None

    if not events:
        img = render_screen_to_image(screen, font)
        frames.append(Frame(image=img.convert("P", palette=Image.ADAPTIVE), duration_ms=max(1, int(1000 / fps))))
    else:
        for idx, ev in enumerate(events):

            if not isinstance(ev, (list, tuple)) or len(ev) < 2:
                continue

            t_raw, data = ev[0], ev[1]



            try:
                t = float(t_raw)
            except Exception:
                t = last_t

            try:
                stream.feed(data)
            except Exception:
                # If pyte can't parse some escape sequences, keep going
                continue

            img_rgb = render_screen_to_image(screen, font)

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
            frames.append(Frame(image=img_rgb.convert("P", palette=Image.ADAPTIVE), duration_ms=duration_ms))
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

    logger.info("Wrote GIF %s (%d frames)", out_path, len(frames))




def _parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="convert", description="Convert cast JSON to GIF")
    p.add_argument("infile", help="Input cast JSON path")
    p.add_argument("outfile", help="Output GIF path")
    p.add_argument("--font", help="Path to TTF font")
    p.add_argument("--font-size", type=int, default=14, help="Font size")
    p.add_argument("--fps", type=int, default=12, help="Fallback FPS")
    p.add_argument("--debug", action="store_true", help="Enable debug logging")
    return p.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = _parse_args(argv)
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

