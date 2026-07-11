# Contributing Guide
Thank you for your interest in contributing to **termgif**! All forms of contributions are **welcome**, including bug reports, feature requests, documentation improvements and code pull requests. Please read this guide before submitting issues or PRs.

## 1. Prerequisites
1. `main` is the primary development branch. All changes **must be created on a new feature branch** based on `main`. Direct commits to `main` are forbidden.
2. Search existing issues first to avoid duplicates. If a relevant ticket exists, leave your comments under the original issue.
3. Before submission, ensure your code compiles and runs without errors. Add **corresponding tests or examples** for newly added logic.

## 2. Branch Naming Convention
Format: `type/short-description`
Available types:
- `feat/`: New features
- `fix/`: Bug fixes
- `docs/`: Documentation updates (README, CONTRIBUTING, code comments, etc.)
- `refactor/`: Code refactoring with no functional changes
- `perf/`: Performance optimization
- `test/`: Unit tests or demo examples
- `ci/`: CI workflows, build scripts and configuration

Examples:
`feat/add-ui-demo`
`fix/resolve-path-error`
`docs/update-examples-docs`

## 3. Commit Message Standard
Format: `type-emoji type: short-description`
Types of emoji:
* ✨ `:sparkles:` **feat**: New feature
* 🐛 `:bug:` **fix**: Bug fixes
* 📚 `:books:` **docs**: Documentation update
* ♻️ `:recycle:` **refactor**: Restructure logic
* ⚡️ `:zap:` **perf**: Performance optimization
* 🧪 `:test_tube:` **test**: Add test instance
* 🤖 `:robot:` **ci**: Configure CI
* 🔧 `:wrench:` **config**: Update configuration files
* 📸 `:camera_flash:` **media**: Add media files
* 🔥 `:fire:` **chore**: Remove files
* 🔒 `:lock:` **security**: Security fixes
* 🌐 `:globe_with_meridians:` **i18n**: Internationalization
* 🎨 `:art:` **style**: Change code style


Examples:
```plaintext
✨ feat: new function
🐛 fix: bug repair
📚 docs: document update
♻️ refactor: code refactor
⚡️ perf: performance optimize
🧪 test: test cases
🔧 chore: config/build
🎨 style: code format
🔥 remove: delete old code
🤖 ci: workflow adjust
```

## 4. Pull Request Rules
1. Use a **clear** PR title. Fill the description with:
   - Problems solved or new capabilities added
   - Related issue number (e.g. Fix #12)
   - Test environment and key modifications
2. One PR should only cover one single feature or bug fix. Mixed irrelevant changes will be asked to split.
3. If you modify APIs, directory structures or UI components, update documents under `docs/` and demos under `examples/` synchronously.
4. All CI checks must pass. Fix style lint failures before review.
5. At least one maintainer’s approval is required before merging.

## 5. Code Style Requirements
1. Follow the existing indentation, naming and comment styles of the project.
2. Add inline comments for key logic and block comments for complex implementations.
3. Do not commit debug print logs, hardcoded test addresses, secret keys or other sensitive data.
4. Add demo code to the `examples/` folder for every new feature.

## 6. Issue Template Rules
### Bug Report
Include these details:
1. Environment info: OS version, compiler toolchain, project version
2. Step-by-step reproduction steps
3. Expected behavior vs actual error behavior
4. Error logs or screenshots (if available)

### Feature Request
1. Describe your usage scenario and pain points
2. Briefly explain your ideal implementation
3. Attach sample code snippets for reference if possible

## 7. Directory Structure Rules
- Demo samples: `examples/` (do not scatter samples inside `src/`)
- Unit tests: `tests/`
- Documentation: `docs/`
- Core source code: `src/`

## 8. Open Source License Notice
By submitting any code, document or asset to this repository, you agree that:
1. All your contributions are licensed under the license file (`LICENSE`) in the project root.
2. You own **full copyright of your submissions**, with no infringing or proprietary third-party code.
3. If you import third-party open-source code, mark its source and corresponding license in code comments.

## 9. Code of Conduct
1. Communicate **politely and respectfully** to all contributors. Personal attacks and sarcasm are prohibited.
2. Discussions shall focus on code and requirements, avoid irrelevant arguments.
3. Maintainers reserve the right to close duplicate, low-quality or off-topic issues and PRs.

## 10. Standard Contribution Workflow
1. Fork this repository
2. Clone your forked repo locally
3. Create a new branch from `main`: `git checkout -b feat/amazing-feature`
4. Modify code and test locally
5. Commit changes with standardized commit messages
6. Push to your personal fork and open a PR targeting the original repo’s `main` branch
7. Revise code based on review feedback and wait for merge