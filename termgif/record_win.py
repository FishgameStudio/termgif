"""
Simple Windows console pixel recorder, output GIF directly.
Usage Examples::
    
    record_window(['echo', 'hello, world!'], 'out.gif')
"""

# pyright: reportMissingTypeStubs=false, reportUnknownMemberType=false, reportAny=false
# pyright: reportUnusedCallResult=false, reportUnknownVariableType=false
import time
import sys
import mss
import pygetwindow
from PIL import Image
import subprocess
from typing import cast


def record_window(cmdlist: list[str], out_path: str, /, window_titles: list[str] | None = None) -> None:
    if sys.platform != "win32":
        raise NotImplementedError("Only supports Windows platform")

    cmd: str = " ".join(cmdlist)
    if window_titles is None:
        window_titles = ["cmd", "PowerShell"]
    # Launch target command in new console
    proc: subprocess.Popen[bytes] = subprocess.Popen(
        cmd,
        creationflags=subprocess.CREATE_NEW_CONSOLE,
        shell=True
    )
    time.sleep(0.3)

    # Find new console window (match cmd/powershell roughly)
    all_wins: list[pygetwindow.Win32Window] = cast(list[pygetwindow.Win32Window], pygetwindow.getAllWindows())
    console_win: pygetwindow.Win32Window | None = None
    print("Finding window...")
    for w in all_wins:
        if w.title:
            for title in window_titles:
                if title in w.title:
                    console_win = w
                    break
    if console_win is None:
        proc.terminate()
        raise RuntimeError("Cannot find target console window")

    region: dict[str, float] = {
        "top": console_win.top,
        "left": console_win.left,
        "width": console_win.width,
        "height": console_win.height
    }

    frames: list[Image.Image] = []
    fps = 10
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
            frames[0].save(
                out_path,
                save_all=True,
                append_images=frames[1:],
                duration=int(frame_delay * 1000),
                loop=0,
                optimize=True
            )
            print(f"Saved GIF to {out_path}, total frames: {len(frames)}")
            return
        else:
            print("No frames recorded")
            return
