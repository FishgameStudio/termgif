"""
Main function wrapper.

Record native Windows console command interaction and export directly to a GIF image.

Positional-only Parameters
--------------------------
cmd : str | list[str]
    Target command to execute in a new Windows native console window.
    Pass a string for a full command, or list of strings for split arguments.
output : str
    Output file path of the generated GIF file (suffix .gif recommended).

Keyword Parameters
------------------
fps : int, default=10
    Frame rate of the final exported GIF animation. Lower value reduces file size.

Returns
-------
None
    No return value, GIF file is written directly to given output path.

Notes
-----
Performs real-time pixel capture of the native Windows console window,
preserving original console visuals, cursor and manual input interactions.
Press Ctrl+C to stop recording and finalize the GIF file.
Windows-only (depends on mss, pygetwindow, Pillow).
No .cast text format is used in this workflow.
"""

def make_gif(
    cmd: str | list[str],
    output: str,
    /
) -> None:
    # Build command list.
    cmdlist: list[str] = cmd if isinstance(cmd, list) else cmd.split(" ")

    from .record_win import record_window

    # Record window and generate .gif file.
    record_window(cmdlist, output)
