"""
Record a native Windows console session and export the recording as an animated GIF.

Launches the target command in a separate Windows console window, captures real-time
screen frames of the matched console window, and compiles the frames directly into a GIF file.
Preserves the original console appearance, cursor state, and manual interactive input.
Press Ctrl+C to stop recording early and finalize the GIF output.

Positional-only Parameters
--------------------------
cmd : str | list[str]
    Target command to run in a new Windows native console window.
    A full command string, or a list of split command arguments.
output : str
    Path to save the final animated GIF file (recommended suffix: .gif).

Other Parameters
----------------
win_name : str | list[str] | None, optional
    Window title(s) to help match the target console window, e.g. "cmd", "PowerShell".
    If None, defaults to ["cmd", "PowerShell"].
win_pid : int | None, optional
    Exact process ID (PID) of the target console process for precise window matching.
    If specified, PID matching takes priority over title matching.
fps : int, default=10
    Frames per second for the exported GIF animation.
    Lower FPS reduces file size, higher FPS improves playback smoothness.

Returns
-------
None
    No return value; the GIF file is saved directly to the specified output path.

Notes
-----
- Windows-only, depends on mss, pygetwindow, and Pillow libraries.
- Uses real-time pixel capture of the raw Windows console window (not text-based .cast format).
- Timeout for window discovery is fixed at 3 seconds.
- Positional-only arguments (cmd, output) cannot be passed via keyword syntax.
"""
def make_gif(
    cmd: str | list[str],
    output: str,
    /,
    win_name: str | list[str] | None = None,
    win_pid: int | None = None,
    fps: int = 10
) -> None:
    # Build command list.
    cmdlist: list[str] = cmd if isinstance(cmd, list) else cmd.split(" ")
    window_name: list[str] = win_name if isinstance(win_name, list) else \
        [win_name] if win_name is not None else ["cmd", "PowerShell"]

    # Record window and generate .gif file.
    from sys import platform
    if platform == "win32":
        from .record_win import record_window
        record_window(cmdlist, output, window_titles=window_name, win_pid=win_pid, fps=fps)
    elif platform == "darwin":
        from .macos import record_window
        record_window(cmdlist, output, window_titles=window_name, win_pid=win_pid, fps=fps)
    elif platform in ("linux", "linux2"):
        from .linux import record_window
        record_window(cmdlist, output, fps=fps)  # No title and pid specification
