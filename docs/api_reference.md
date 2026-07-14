<!-- API REFERENCE

*** This is the reference of most public APIs.
*** To edit this file please follow this format:

---
### `module_name_if_has.function_name(param1: type, param2: type = default_value) -> return_type`
function-usage.
- `param1`: param-usage.
- `param2`: param-usage.
- Returns: return-content-description.
*** Optional notes:
- Platform: platform-only.
- Raises: `exception` when something-happend
- Notes: notes


*** This api_reference.md only refer to the Python public APIs,
*** Do not add private APIs to this file.
*** For clarity, please only document APIs explicitly listed in __all__ in __init__.py.

-->

# API Reference

All public APIs are documented here.

---

### `record_window(cmdlist: list[str], out_path: str, /, window_titles: list[str] | None = None, win_pid: int | None = None, fps: int = 10) -> None`

Record a native Windows console window and save the capture as an animated GIF file.

- `cmdlist`: Split command arguments to run in the new console.
- `out_path`: Output path for the resulting GIF file.
- `window_titles`: Title patterns used to match the target console window (used when `win_pid` is not provided).
- `win_pid`: Exact target console process PID for precise matching (takes priority over `window_titles`).
- `fps`: Frames per second for the exported GIF animation.
- Returns: `None` (GIF is written directly to `out_path`).
- Platform: **Windows only**

---

### `make_gif(cmd: str | list[str], output: str, /, win_name: str | list[str] | None = None, win_pid: int | None = None, fps: int = 10) -> None`

Launch a new Windows native console, record interactive terminal sessions, and export the recording as an animated GIF file.

- `cmd`: Full command string OR list of split command arguments to execute in the new Windows console window.
- `output`: File path for the final GIF output (`.gif` extension recommended).
- `win_name`: Single or multiple window title patterns for matching the target console window. Defaults to `["cmd", "PowerShell"]` when `None`.
- `win_pid`: Exact target console process ID (PID) for precise window matching (takes priority over title matching if specified).
- `fps`: Frames per second for the exported GIF animation (default: 10). Lower values reduce file size.
- Returns: `None` (GIF file is written directly to the specified path).
- Platform: **Windows only**

---

### `linux.record_window(cmdlist: list[str], out_path: str, /, fps: int = 10) -> None`

Linux Wayland fallback recorder (full primary monitor capture only), saves screen recording as an animated GIF file.
Wayland does not support precise individual terminal window selection, so this implementation records the entire primary monitor instead of a single specific window.

- `cmdlist`: List of split command arguments to launch the target shell/terminal process to record.
- `out_path`: File path to save the final animated GIF output.
- `fps`: Frames per second for the exported GIF animation (default: 10). Lower values reduce file size.
- Returns: `None` (GIF file is written directly to the specified path when recording stops via Ctrl+C; no GIF saved if zero frames are captured).
- Raises: `NotImplementedError` when running on non-Linux systems
- Platform: **Linux only (Wayland fallback mode, full monitor capture)**


