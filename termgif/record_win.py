"""Record a native Windows console window and export it as an animated GIF.

The provided command is launched in a new Windows console. The recorder then locates
the console window (by PID or by matching one of the given title patterns), captures
screen frames using pixel-based screen grabbing, and saves them to `out_path`.

Positional-only Parameters
--------------------------
cmdlist : list[str]
    Split command arguments to run in the new console.
out_path : str
    Output path for the GIF file.

Other Parameters
----------------
window_titles : list[str] | None, optional
    Title patterns used to match the target console window.
    If `None`, defaults to `["cmd", "PowerShell"]`.
win_pid : int | None, optional
    Exact target process PID for precise window matching.
    If provided, it takes priority over `window_titles`.
fps : int, default=10
    Frames per second for the captured animation.

Returns
-------
None
    The GIF is saved directly to `out_path`.

Raises
------
NotImplementedError
    If called on a non-Windows platform.
RuntimeError
    If the target console window cannot be found.

Notes
-----
- This is a pixel-based recorder (not a text/capture-format recorder).
- Recording continues until `Ctrl+C` is pressed.
"""

# pyright: reportMissingTypeStubs=false, reportUnknownMemberType=false, reportAny=false
# pyright: reportUnusedCallResult=false, reportUnknownVariableType=false
from __future__ import annotations

import subprocess
import sys
import time
from typing import cast

import mss
import pygetwindow
import win32process as win32ps
from PIL import Image


def _get_pid(w: pygetwindow.Win32Window) -> int:
    return win32ps.GetWindowThreadProcessId(w._hWnd)[1]  # pyright: ignore[reportPrivateUsage]


def record_window(
    cmdlist: list[str],
    out_path: str,
    /,
    window_titles: list[str] | None = None,
    win_pid: int | None = None,
    fps: int = 10,
) -> None:
    if sys.platform != "win32":
        raise NotImplementedError("Only supports Windows platform")
    prompt: str = "WARNING: Please don't record personal informations or secrets on the window."
    print(f"\x1b[93m{prompt}\033[0m")

    cmd: str = " ".join(cmdlist)
    if window_titles is None:
        window_titles = ["cmd", "PowerShell"]
    # Launch target command in new console
    proc: subprocess.Popen[bytes] = subprocess.Popen(
        cmd,
        creationflags=subprocess.CREATE_NEW_CONSOLE,
        shell=True,
    )
    time.sleep(0.5)

    # Find new console window (match the specified title roughly)
    all_wins: list[pygetwindow.Win32Window] = cast(list[pygetwindow.Win32Window], pygetwindow.getAllWindows())
    console_win: pygetwindow.Win32Window | None = None

    print("Finding window...")

    # Search by the PID if specified.
    if win_pid is not None:
        for w in all_wins:
            if _get_pid(w) == win_pid:
                console_win = w
                break
    # Search by the specified title.
    else:
        for w in all_wins:
            if w.title:
                for title in window_titles:
                    if title in w.title:
                        console_win = w
                        break
                if console_win is not None:
                    break  # Jumps out of the outermost for loop.

    if console_win is None:
        proc.terminate()
        raise RuntimeError("Cannot find target console window")

    region: dict[str, float] = {
        "top": console_win.top,
        "left": console_win.left,
        "width": console_win.width,
        "height": console_win.height,
    }

    frames: list[Image.Image] = []
    frame_delay: float = 1 / fps
    print(f"Recording console window, Ctrl+C to stop and save GIF: {out_path}")
    try:
        with mss.mss() as sct:
            sct: mss.MSS = cast(mss.MSS, sct)
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
