"""
Simple macOS console pixel recorder, output GIF directly.
Usage Examples::

    record_window(['echo', 'hello, world!'], 'out.gif', window_titles=['Terminal'])
"""

# pyright: reportUnknownVariableType=false
from __future__ import annotations

import os
import subprocess
import sys
import time
from typing import cast

import mss
from PIL import Image
from contextlib import suppress


def _run_applescript(script: str) -> str:
    # Run osascript and return stdout (text). Do not raise on nonzero; we parse output ourselves.
    try:
        proc = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, check=False)
        return proc.stdout or ""
    except Exception:
        return ""


def _list_windows() -> list[dict[str, str | int]]:
    """
    Return list of window info dicts with keys:
      owner: application process name (str)
      pid: unix pid of the application process (int)
      name: window name (str)
      x, y, width, height: ints (position and size)
    The AppleScript uses System Events to enumerate visible windows.
    """
    applescript = r"""
    set out to ""
    tell application "System Events"
      set procs to application processes
      repeat with p in procs
        try
          set pname to name of p
          set pid to unix id of p
        on error
          set pname to ""
          set pid to 0
        end try
        repeat with w in windows of p
          try
            set wname to name of w
          on error
            set wname to ""
          end try
          try
            set pos to position of w
            set sz to size of w
            set out to out & pname & "\t" & (pid as string) & "\t" & wname & "\t" & (item 1 of pos as string) & "\t" & (item 2 of pos as string) & "\t" & (item 1 of sz as string) & "\t" & (item 2 of sz as string) & "\n"
          end try
        end repeat
      end repeat
    end tell
    return out
    """
    raw: str = _run_applescript(applescript)
    lines: list[str] = [ln for ln in raw.splitlines() if ln.strip()]
    results: list[dict[str, str | int]] = []
    for ln in lines:
        parts: list[str] = ln.split("\t")
        if len(parts) < 7:
            continue
        owner, pid_s, name, x_s, y_s, w_s, h_s = parts[:7]
        try:
            pid: int = int(pid_s)
            x: int = int(float(x_s))
            y: int = int(float(y_s))
            w: int = int(float(w_s))
            h: int = int(float(h_s))
        except Exception:
            continue
        results.append(
            {
                "owner": owner,
                "pid": pid,
                "name": name,
                "x": x,
                "y": y,
                "width": w,
                "height": h,
            }
        )
    return results


def record_window(
    cmdlist: list[str],
    out_path: str,
    /,
    window_titles: list[str] | None = None,
    win_pid: int | None = None,
    fps: int = 10,
) -> None:
    """Record a macOS Terminal console window and export it as an animated GIF.

    The command is launched inside Terminal.app with a unique injected window title.
    The recorder then enumerates visible windows via AppleScript, selects the target
    window (by PID, injected unique title, or title hints), captures pixel frames,
    and saves them as a GIF.

    Positional-only Parameters
    --------------------------
    cmdlist : list[str]
        Split command arguments to run.
    out_path : str
        Output path for the GIF file.

    Other Parameters
    ----------------
    window_titles : list[str] | None, optional
        Title hints used to locate the target window (e.g. `Terminal`, `iTerm2`).
        If `None`, defaults to `["Terminal", "iTerm2"]`.
    win_pid : int | None, optional
        Exact process PID for precise matching.
        If provided, it takes priority over title matching.
    fps : int, default=10
        Frames per second.

    Returns
    -------
    None
        The GIF is saved directly to `out_path`.

    Raises
    ------
    NotImplementedError
        If called on a non-macOS platform.
    RuntimeError
        If the target window cannot be found.

    Notes
    -----
    - Recording continues until `Ctrl+C` is pressed.
    """
    if sys.platform != "darwin":
        raise NotImplementedError("Only supports macOS platform")
    prompt: str = """
WARNING: Please don't record personal informations or secrets on the window.
WARNING: Please enable the access of your editor before recording.
"""
    print(f"\x1b[93m{prompt}\033[0m")

    cmd: str = " ".join(cmdlist)
    if window_titles is None:
        window_titles = ["Terminal", "iTerm2"]

    # Create a unique title we can reliably search for.
    unique_title: str = f"__RECORDER_{int(time.time() * 1000)}__"

    # Build inner shell command that sets the terminal window title (via escape sequence) then execs the user's command.
    # Use literal backslashes so the terminal receives the escape sequence.
    inner_cmd: str = f'printf "\\\\033]0;{unique_title}\\\\007"; exec {cmd}'

    # Escape double quotes for embedding into AppleScript string
    inner_cmd_escaped = inner_cmd.replace('"', '\\"')

    # Ask Terminal to run bash -lc "<inner_cmd>"
    applescript_launch: str = f'tell application "Terminal" to do script "bash -lc \\"{inner_cmd_escaped}\\""'
    print("Launching AppleScript...")
    proc: subprocess.Popen[bytes] = subprocess.Popen(
        ["osascript", "-e", applescript_launch],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    # Give Terminal a short time to open the window and apply title
    time.sleep(0.5)

    # Find new console window (match the specified title roughly or by PID or by our unique title)
    all_wins: list[dict[str, int | str]] = _list_windows()
    console_win: dict[str, int | str] | None = None

    print("Finding window...")

    # If win_pid provided, match application pid first
    if win_pid is not None:
        for w in all_wins:
            if w.get("pid") == win_pid:
                console_win = w
                break

    # Prefer matching the unique title we injected
    if console_win is None:
        for w in all_wins:
            name = str(w.get("name") or "")
            if unique_title in name:
                console_win = w
                break

    # If still not found, fallback to matching owner/title hints
    if console_win is None:
        for w in all_wins:
            name: str = str(w.get("name") or "")
            owner: str = str(w.get("owner") or "")
            found = False
            for title in window_titles:
                if title and (title in name or title in owner):
                    console_win = w
                    found = True
                    break
            if found:
                break

    if console_win is None:
        with suppress(Exception):
            proc.terminate()
        raise RuntimeError("Cannot find target console window")

    # Extract region from window info
    x: int = int(console_win.get("x", 0))
    y: int = int(console_win.get("y", 0))
    width: int = int(console_win.get("width", 0))
    height: int = int(console_win.get("height", 0))

    region: dict[str, float] = {"top": float(y), "left": float(x), "width": float(width), "height": float(height)}

    frames: list[Image.Image] = []
    frame_delay: float = 1 / fps
    print(f"Recording console window, Ctrl+C to stop and save GIF: {out_path}")
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
        try:
            proc.terminate()
        except Exception:
            pass

        # Best-effort: if win_pid was passed, try to terminate it.
        if win_pid is not None:
            try:
                os.kill(win_pid, 15)
            except Exception:
                pass

        if frames:
            frames[0].save(
                fp=out_path,
                save_all=True,
                append_images=frames[1:],
                duration=int(frame_delay * 1000),
                loop=0,
                optimize=True,
            )
            print(f"Saved GIF to {out_path}, total frames: {len(frames)}")
            return
        else:
            print("No frames recorded")
            return
