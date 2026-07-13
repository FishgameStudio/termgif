# CHANGELOG
All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

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

