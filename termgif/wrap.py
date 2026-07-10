"""
Main function wrapper.

Record terminal command execution and convert captured content into a GIF image.

Positional-only Parameters
--------------------------
cmd : str | list[str]
    Target shell command to execute.
    Pass a string for single command, or list of strings for split arguments.
output : str
    Output file path of the generated GIF file.

Keyword Parameters
------------------
width : int, default=80
    Terminal column width for the virtual terminal recording window.
height : int, default=24
    Terminal row height for the virtual terminal recording window.
font : str, default="Consolas"
    Font family name used when rendering text in GIF frames.
font_size : int, default=30
    Pixel size of text font inside output GIF.
fps : int, default=60
    Frame rate of the final exported GIF animation.

Returns
-------
None
    No return value, GIF file is written directly to given output path.

Notes
-----
Uses temporary file to store raw terminal capture data before conversion.
Dependencies: internal record_win for terminal capture, convert for GIF rendering.
This function is Windows-only (depends on pywinpty).
"""


def make_gif(
        cmd: str | list[str], 
        output: str, 
        /, 
        width: int     = 80,
        height: int    = 24, 
        font: str      = "Consolas", 
        font_size: int = 30, 
        fps: int       = 60
    ) -> None:
    # Build finally command.
    command: str = ""
    if isinstance(cmd, str):
        command = cmd
    else:
        command = " ".join(cmd)
    from .convert import convert_cast_to_gif
    from .record_win import record_with_pywinpty
    import tempfile
    # Crerate temp file for .cast file
    with tempfile.TemporaryFile("w", encoding="utf-8") as f:
        record_with_pywinpty([command], f.name, width, height)
        convert_cast_to_gif(f.name, output, font, font_size, fps)
    