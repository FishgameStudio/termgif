"""Create an animated GIF recording of an interactive terminal session.

This is the cross-platform entry point. Internally it dispatches to a platform-specific
implementation:
- Windows: targeted console window recording.
- macOS: Terminal.app window recording by matching an injected unique window title.
- Linux: Wayland/X11 fallback recording (full primary monitor capture).

Positional-only Parameters
--------------------------
cmd : str | list[str]
    Command to run in a new terminal/console.
    - If `str`, it is split on spaces into arguments.
    - If `list[str]`, it is treated as already-split arguments.
output : str
    Path to write the resulting GIF file (typically ends with `.gif`).

Other Parameters
----------------
win_name : str | list[str] | None, optional
    Window title(s) used to locate the target window.
    - If `None`, defaults to `["cmd", "PowerShell"]`.
    - For macOS, common defaults are `Terminal` and `iTerm2`.
win_pid : int | None, optional
    Exact process ID (PID) of the target console process.
    If provided, PID matching takes priority over title matching.
fps : int, default=10
    Frames per second for the exported GIF.

Returns
-------
None
    The GIF is written directly to `output`.

Raises
------
NotImplementedError
    When the active platform is not supported by the selected backend.
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
