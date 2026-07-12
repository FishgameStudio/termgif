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
### `def record_window(cmdlist: list[str], out_path: str) -> None`
Record a Windows native console window executing the specified command and save directly as an animated GIF file.
- `cmdlist`: Command token list to launch the Windows console process.
- `out_path`: Output path for the generated GIF file.

- Returns: `None` (GIF file saved directly to the specified path).

---
### `def make_gif(cmd: str | list[str], output: str, /) -> None`
Launch a Windows native console, record the command interaction, and export as an animated GIF file.
- `cmd`: Command string or token list to run in the Windows native console.
- `output`: Output path of the final GIF file.

- Returns: `None` (GIF file saved directly to the specified path).