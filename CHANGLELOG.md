# CHANGELOG
All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## \[v0.1.0\] - 2026-7-12
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

