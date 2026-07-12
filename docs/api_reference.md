<!-- API REFERENCE

*** This is the reference of most APIs.
*** To edit this file please follow this format:

---
### `module_name_if_has.function_name(param1: type, param2: type = default_value) -> return_type`
function-usage.
- `param1`: param-usage.
- `param2`: param-usage.
- Returns: return-content-description


*** This api_reference.md only refer to the Python public APIs,
*** Do not add private APIs to this file.
*** For clarity, please only document APIs explicitly listed in __all__ in __init__.py.

-->

# API Reference
All public APIs are documented here.

---
### `def make_gif(cmd: str | list[str], output: str, /, width: int = 80, height: int = 24, font: str = "Consolas", font_size: int = 30, fps: int = 60) -> None`
Make a GIF file including the output of the specified command.
- `cmd`: the command to execute. Captures the output of the execution. Join by whitespace if is instance of `list`, like the command of `subprocess.run`.
- `output`: output path of the GIF file. Create if not exists.
- `width`: the width (pixel) of the GIF file.
- `height`: the height (pixel) of the GIF file.
- `font`: the font path. For example `termgif/UbuntuMono-r.ttf`.
- `font_size`: the size (pixel) of the font. The text may appear cramped if too big.
- `fps`: the number of frames per second. Higher frame rate means smoother playback.

- Returns: `None` (GIF is written directly to `out_gif`).

---
### `def convert_cast_to_gif(cast_path: str | Path, out_gif: str | Path, font_path: str | None = None, font_size: int = 14, fps: int = 12, dedupe_identical_frames: bool = False, min_frame_ms: int = 80) -> None`
Convert a cast JSON (as produced by `record_with_winpty`) to a GIF file.
- `cast_path`: Input cast JSON path (must exist). The cast contains terminal events, plus `width`/`height`.
- `out_gif`: Output GIF file path. The parent directory will be created if it does not exist.
- `font_path`: Optional TTF font path used for rendering text.
- `font_size`: Font size (pixel) used when rendering frames.
- `fps`: Fallback frame rate used when cast timestamps are not available (also used for the first-frame duration).
- `dedupe_identical_frames`: If `True`, identical consecutive frames may be merged by extending the previous frame duration.
- `min_frame_ms`: Minimum duration (in milliseconds) for each produced frame.

- Returns: `None` (GIF is written directly to `out_gif`).

---
### `def choose_font(font_path: str | None, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont`
Choose a font for rendering terminal text into GIF frames.
- `font_path`: Optional path to a TTF font file. If provided but loading fails, the function falls back to other fonts.
- `size`: Font size (pixel) used when loading/rendering.

If `font_path` is not given (or cannot be loaded), this function tries a set of default font locations and finally falls back to Pillow's default font.

- Returns: a loaded Pillow font object (`PIL.ImageFont.FreeTypeFont` or `PIL.ImageFont.ImageFont`).

---
### `def render_screen_to_image(screen: pyte.Screen, font: ImageFont.ImageFont, fg: tuple[int, int, int] = (255, 255, 255), bg: tuple[int, int, int] = (0, 0, 0)) -> Image.Image`
Render a `pyte.Screen` into a Pillow image using a monospace font.
- `screen`: The terminal screen buffer to render (`pyte.Screen`).
- `font`: The font used to draw each row.
- `fg`: Foreground color as an RGB tuple.
- `bg`: Background color as an RGB tuple.

- Returns: a Pillow `PIL.Image.Image` representing the current screen contents.

---
### `def record_with_winpty(cmdlist: list[str], out_path: str, width: int = 80, height: int = 24) -> None`
Record the output of the command and store it as json cast file.
- `cmdlist`: Command tokens to execute (joined into a command line string for `winpty`).
- `out_path`: Output path of the cast JSON file.
- `width`: Virtual terminal column count.
- `height`: Virtual terminal row count.

- Returns: `None` (the cast JSON is written directly to `out_path`).
