<!-- API REFERENCE

*** This is the reference of most public APIs.
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
### `record_window(cmdlist: list[str], out_path: str, /, window_titles: list[str] | None = None, win_pid: int | None = None, fps: int = 10, timeout: float = 3.0) -> None`
Record a native Windows console window running the specified command and save the capture as an animated GIF file.
- `cmdlist`: List of split command arguments to launch the target Windows console process.
- `out_path`: File path to save the final animated GIF output.
- `window_titles`: List of window title patterns used to match the target console window for recording.
- `win_pid`: Exact target console process ID (PID) for precise window matching; takes priority over title matching if provided.
- `fps`: Frames per second for the exported GIF animation (default: 10). Lower values reduce file size.
- `timeout`: Maximum time (seconds) allowed to locate the target console window before timing out (default: 3.0).
- Returns: `None` (GIF file is written directly to the specified path).

---
### `make_gif(cmd: str | list[str], output: str, /, win_name: str | list[str] | None = None, win_pid: int | None = None, fps: int = 10) -> None`
Launch a new Windows native console, record interactive terminal sessions, and export the recording as an animated GIF file.
- `cmd`: Full command string OR list of split command arguments to execute in the new Windows console window.
- `output`: File path for the final GIF output (`.gif` extension recommended).
- `win_name`: Single or multiple window title patterns for matching the target console window. Defaults to `["cmd", "PowerShell"]` when `None`.
- `win_pid`: Exact target console process ID (PID) for precise window matching (takes priority over title matching if specified).
- `fps`: Frames per second for the exported GIF animation (default: 10). Lower values reduce file size.
- Returns: `None` (GIF file is written directly to the specified path).
