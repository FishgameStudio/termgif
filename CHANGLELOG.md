# CHANGELOG
All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## \[0.2.2\] - 2026-07-15

### ♻️ Changed
- **Package name**: PyPI package renamed from `termgif` to `term2gif` to resolve naming conflicts and align with project branding.
- **Version bump**: Updated version from `0.2.0` to `0.2.2` across `pyproject.toml`, `setup.py`, and `__init__.py`.
- **Platform detection**: Refactored platform-specific imports in `wrap.py` to use `match/case` syntax for cleaner cross-platform dispatching.
- **Type annotations**: Added explicit type hints (`Path`, `str`) in `setup.py` for better code clarity.
- **macOS recorder**: Improved user-facing warnings and added AppleScript launch feedback message.
- **Error handling**: Replaced bare `try/except` with `contextlib.suppress(Exception)` in macOS recorder cleanup.

### 🔥 Removed
- **Windows-specific dependency**: Removed `pywin32>=312` from core dependencies in both `pyproject.toml` and `setup.py`.
- **Platform submodules from public API**: Removed `linux`, `macos`, and `record_window` from `__all__` in `__init__.py`. The cross-platform `make_gif()` is now the sole public entry point.
- **Keyword cleanup**: Removed `"termgif"` from package keywords to reflect the rename.

### 🐛 Fixed
- **API documentation**: Fixed glob pattern reference in `docs/api_reference.md` (`__init__.py` → `**/__init__.py`).
- **Package discovery**: Updated `find_packages()` call in `setup.py` to use keyword argument `where="termgif"`.
- **Platform validation**: Added explicit platform check at module load time, raising `NotImplementedError` for unsupported platforms.
- **macOS window detection**: Expanded default window title search to include `"Terminal"` alongside `"cmd"` and `"PowerShell"`.

### ✨ Added
- **macOS test**: Added `tests/macos_test.py` for local macOS window recording validation.

---

## \[v0.2.0\] - 2026-07-14

### ✨ New Features
- add official **macOS backend** (`termgif.macos.record_window`):
  - Use AppleScript + System Events to enumerate terminal windows (Terminal.app / iTerm2)
  - Inject unique dynamic window title for reliable target window matching
  - PID + title matching + mss pixel capture for precise terminal GIF recording
  - Yellow warning prompt + Ctrl+C stop & GIF export workflow consistent with Windows
- Add official **Linux fallback backend** (`termgif.linux.record_window`):
  - Pure `mss` + Pillow implementation (no external CLI tools / ffmpeg / Xlib dependencies)
  - Wayland global restriction handling: full primary monitor capture mode
  - Explicit warning for Wayland auto-single-window limitation
  - Basic command launching + full-screen pixel capture + GIF export
- Cross-platform entry point: update `make_gif()` to auto-detect OS and dispatch platform backends
- API extensions: add `win_pid` (PID exact matching) & `fps` parameters to core functions for frame rate control
- Expose new modules: `termgif.linux`, `termgif.macos` in `__init__.py` public API
- Add structured public API documentation (`docs/api_reference.md`) with parameter spec, platform notes, exceptions

### 📚 Documentation & Spec Updates
- Rewrite commit convention docs (`COMMIT_CONVENTION.md`, `CONTRIBUTING.md`) to markdown table format
  - Add emoji / type reference table + optional scope syntax `type-emoji type(scope): desc`
  - Add alignment comment for consistent formatting
- Complete API reference documentation with parameters, returns, raises, platform tags
- Improve docstrings across all core modules (record\_win, linux, macos, wrap)
- Update root package docstring for cross-platform overview
- Update example GIF assets, remove old redundant screenshot files

### 🔧 Dependencies & Packaging
- Update `pyproject.toml` + `setup.py` dependencies: add `pywin32>=312`, align `PyGetWindow`, `mss`, `pillow` versions
- Remove legacy unused dependencies (pyte, pywinpty)
- Version bump to `0.1.1`

### 🐛 Improvements & Refactors
- Windows recorder (`record_win.py`):
  - Add PID lookup via `win32process` for precise console matching
  - Add `win_pid` and `fps` parameters, configurable frame rate
  - Standard yellow ANSI warning prompt
  - Improve window polling logic, fix GIF save parameter (`fp=`)
  - Add type annotations, `from __future__ import annotations`
- Consistent error handling & explicit `NotImplementedError` per platform backends
- Standardize Ctrl+C keyboard interrupt flow, process cleanup, GIF saving logic
- Add pyright type checking rules across source files

### ⚠️ Known Limitations
- Linux: Pure Wayland environments cannot auto-select individual terminal windows (security protocol restriction), uses full-monitor fallback mode
- Linux: No per-window/PID targeted capture (X11-specific implementation not included in this base version)
- macOS: Requires Terminal/iTerm2 + AppleScript permissions for window enumeration

### 📝 Developer
- Update CONTRIBUTING.md commit message format & add table layout
- Add consistent code formatting & pyright lint configuration

---

## \[v0.1.1\] - 2026-07-13
### ✨ Added
- GitHub community templates: commit convention, discussion templates, bug/feature issue templates, PR template, release template
- GitHub support guide (SUPPORT.md), issue config (ISSUE_TEMPLATE/config.yml)
- Basic test scripts (import_test.py, record_test.py)
- New screenshot GIF assets for documentation
- Direct native Windows console pixel capture workflow using `mss` + `PyGetWindow`
- New public API: `record_window()` for raw window GIF recording
- `win_name` parameter for `make_gif()` to customize target console window matching

### ♻️ Changed
- **Core workflow refactor**: remove legacy `.cast` JSON + pyte virtual terminal rendering, switch to direct pixel recording
- Dependencies updated: replace `pyte`, `pywinpty` with `mss`, `PyGetWindow`; keep `Pillow`
- Project package name updated to `term2gif`, version bumped to 0.1.1
- Public API surface updated in `__init__.py`; removed legacy cast-related functions
- API documentation (`api_reference.md`) rewritten to reflect new public functions
- README rewritten to document pixel recording flow, update installation instructions and examples
- `NOTICE` third-party attribution updated for mss/PyGetWindow, remove winpty/pyte legacy entries
- `.gitignore`: add wildcard *.gif ignore rule (preserve screenshots folder)
- `pyproject.toml` & `setup.py`: update dependencies, version, formatting rules
- `wrap.py` (`make_gif`): rewrite implementation for direct GIF generation, update docstring
- `record_win.py`: completely rewritten from winpty cast recorder to pixel-based GIF recorder
- Window matching logic: fix reversed substring check for console title detection
- Parameter default pattern: use `None` instead of mutable list defaults to resolve linter warnings
- Code formatting & lint rules updated in `pyproject.toml`

### 🔥 Removed
- Legacy `convert.py` cast-to-gif renderer
- Legacy `record_with_winpty` winpty-based .cast recorder
- Legacy monospace font asset `UbuntuMono-r.ttf`
- Virtual terminal text rendering logic and related utilities
- Old font rendering parameters (width/height/font/font_size) from main API

### 🐛 Fixed
- Mutable list parameter default linter error (reportCallInDefaultInitializer)
- Incorrect window title substring matching logic
- Legacy winpty/pyte architecture compatibility issues
- Incorrect third-party license attribution

### 📚 Docs
- Updated API reference documentation
- Updated README main flow, examples, dependencies and credits
- Added contribution guidelines, commit message convention
- Added community support & issue reporting templates

---

## \[v0.1.0\] - 2026-07-12
### Added
- Core public API functions: `make_gif`, `convert_cast_to_gif`, `choose_font`, `render_screen_to_image`, `record_with_winpty`
- Windows terminal recording via winpty and cast JSON format export
- GIF rendering based on pyte terminal emulator and Pillow
- Project structure & package configuration (`pyproject.toml`, `setup.py`, `py.typed`)
- Official public API declaration via `__all__` in `termgif/__init__.py`
- Documentation: `README.md`, `docs/api_reference.md`, `docs/quickstart.md`
- Example code under `examples/basic/`
- Font asset: UbuntuMono-r.ttf
- Repository config: `.gitignore`, `.mailmap`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`, `NOTICE`
- Linting & formatting config (Ruff, Black, mypy)
- MIT license & third-party dependency attribution
- Basic CLI entrypoints for recording and conversion

### Changed
- N/A (initial release)

### Fixed
- N/A (initial release)

