"""
Simple Linux cross-platform fallback recorder (no external CLI tools: pure mss + Pillow).
- Wayland: full primary monitor recording only (cannot auto-locate single native Wayland windows)
- X11: can add manual fixed rect for precise capture
Usage Examples::
    record_window(['echo', 'hello, world!'], 'out.gif')
"""

# pyright: reportUnusedCallResult=false, reportUnknownVariableType=false
# pyright: reportAny=false

from __future__ import annotations

import subprocess
import sys
import time
from dataclasses import dataclass
from typing import cast

import mss
from mss.models import Monitor
from PIL import Image


@dataclass(frozen=True)
class _Rect:
    top: int
    left: int
    width: int
    height: int


def _get_primary_monitor_rect() -> _Rect:
    with mss.mss() as sct:
        sct = cast(mss.MSS, sct)
        mon: Monitor = sct.monitors[1]
        return _Rect(
            top=int(mon["top"]),
            left=int(mon["left"]),
            width=int(mon["width"]),
            height=int(mon["height"]),
        )


def record_window(cmdlist: list[str], out_path: str, /, fps: int = 10) -> None:
    """Record an animated GIF using a Linux fallback (full primary monitor capture).

    This backend is intended for environments where precise per-window tracking is not
    available (notably Wayland).

    Positional-only Parameters
    --------------------------
    cmdlist : list[str]
        Split command arguments to run.
    out_path : str
        Output path for the GIF file.

    Other Parameters
    ----------------
    fps : int, default=10
        Frames per second.

    Returns
    -------
    None
        The GIF is saved directly to `out_path` when recording stops.

    Raises
    ------
    NotImplementedError
        If called on a non-Linux platform.
    """
    if sys.platform not in ("linux", "linux2"):
        raise NotImplementedError("This fallback version is for Linux only")

    prompt: str = """WARNING:\n
    Wayland cannot auto-locate single terminal window; recording full primary monitor (static mode only).\n
    Please don't record personal informations or secrets on the window."""
    print(f"\x1b[93m{prompt}\033[0m")

    cmd: str = " ".join(cmdlist)
    # Launch shell command (generic terminal, no auto window tracking for Wayland)
    proc: subprocess.Popen[bytes] = subprocess.Popen(cmd, shell=True, start_new_session=True)
    time.sleep(0.3)

    # Fallback: whole primary monitor
    rect = _get_primary_monitor_rect()
    region: dict[str, int] = {"top": rect.top, "left": rect.left, "width": rect.width, "height": rect.height}

    frames: list[Image.Image] = []
    frame_delay: float = 1 / fps
    print(f"Recording full monitor, Ctrl+C to stop and save GIF: {out_path}")

    try:
        with mss.mss() as sct:
            sct = cast(mss.MSS, sct)
            while True:
                sshot: mss.ScreenShot = sct.grab(region)
                img: Image.Image = Image.frombytes("RGB", sshot.size, sshot.rgb)
                frames.append(img)
                time.sleep(frame_delay)
    except KeyboardInterrupt:
        print("Start saving GIF files...")
        proc.terminate()
        proc.wait()
        if frames:
            from tqdm import tqdm
            frames[0].save(
                fp=out_path,
                save_all=True,
                append_images=tqdm(frames[1:], desc="Encoding GIF frames", unit="frame"),
                duration=int(frame_delay * 1000),
                loop=0,
                optimize=True,
            )
            print(f"Saved GIF to {out_path}, total frames: {len(frames)}")
            return
        else:
            print("No frames recorded")
            return
