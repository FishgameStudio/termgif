<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/FishgameStudio/termgif">
    <img src="assets/logo.png" alt="Logo">
  </a>

# termgif
<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
![Contributors](https://img.shields.io/github/contributors/FishgameStudio/termgif)
![Stars](https://img.shields.io/github/stars/FishgameStudio/termgif?style=social)
![Forks](https://img.shields.io/github/forks/FishgameStudio/termgif?style=social)
![Issues](https://img.shields.io/github/issues/FishgameStudio/termgif)
![PRs](https://img.shields.io/github/issues-pr/FishgameStudio/termgif)
[![CommitCount](https://badgen.net/github/commits/FishgameStudio/termgif/main)](https://github.com/FishgameStudio/termgif/commits/main)
<!-- TODO: Unlock this after launched on PyPI:
[![PyPI](https://img.shields.io/pypi/v/termgif?style=color=orange)](https://pypi.com/project/termgif)
-->
![Size](https://img.shields.io/github/repo-size/FishgameStudio/termgif)
![Welcome](https://img.shields.io/badge/PRs%20%26%20Issues-welcome-bluevoilet)
![Version](https://img.shields.io/badge/version-0.1.0-orange)
[![License](https://img.shields.io/github/license/FishgameStudio/termgif)](LICENSE)

  <p align="center">
    A simple and lightweight static GIF generator!
    <br />
    <a href="https://github.com/FishgameStudio/termgif/tree/main/docs"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/FishgameStudio/termgif/tree/main/examples">View Demo</a>
    &middot;
    <a href="https://github.com/FishgameStudio/termgif/issues/new?labels=bug">Report Bug</a>
    &middot;
    <a href="https://github.com/FishgameStudio/termgif/issues/new?labels=enhancement">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>📖 Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">🔹 About The Project</a>
      <ul>
        <li><a href="#built-with">🔹 Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">🔹 Getting Started</a>
      <ul>
        <li><a href="#prerequisites">🔹 Prerequisites</a></li>
        <li><a href="#installation">🔹 Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">🔹 Usage</a></li>
    <li><a href="#roadmap">🔹 Roadmap</a></li>
    <li><a href="#contributing">🔹 Contributing</a></li>
    <li><a href="#license">🔹 License</a></li>
    <li><a href="#contact">🔹 Contact</a></li>
    <li><a href="#acknowledgments">🔹 Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## 🎬 About The Project


> ***"Creating clean, visually appealing demo screenshots for command-line tutorials can often be a tedious hassle—working with asciinema and ffmpeg involves a convoluted workflow. In reality, however, simply feeding it an API will resolve all such issues."***

**termgif** is a lightweight tool for static-build GIF generation. On Windows it records your terminal command execution (producing a cast JSON), then renders the captured output into an animated GIF.

The goal is simple: make command-line demos more visual and lightweight.

Main flow:

1. 🎥 **Record**: run the target command and capture terminal output (record_win.py)
2. 🔄 **Convert**: render the cast JSON into GIF frames (convert_cast_to_gif / convert.py)
3. 🧩 **Generate**: write the GIF to the specified output path

<p align="right"><a href="#readme-top">🔝back to top</a></p>



### 🛠️ Built With

* [![Python3.14](https://img.shields.io/badge/python-3.14-3776AB?logo=python&logoColor=white&style=for-the-badge)](https://python.org)
* [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json&style=for-the-badge)](https://docs.astral.sh/ruff)
* [![Black](https://img.shields.io/badge/code_style-black-000000?style=for-the-badge&logo=black&logoColor=white)](https://black.readthedocs.io)
* [![MyPy](https://img.shields.io/badge/type\_checker-mypy-3178C6?style=for-the-badge&logo=python&logoColor=white)](https://mypy.readthedocs.io)


<p align="right"><a href="#readme-top">🔝back to top</a></p>



<!-- GETTING STARTED -->
## 🚀 Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### ✅ Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* Hatch \(if exists\)
  ```sh
  # print all dependencies
  hatch dep show
  # print dependencies on group dep
  hatch dep show dev
  ```
_See [pyproject.toml](pyproject.toml#L28) for complete content._

### 📦 Installation

1. Clone the repo
   ```sh
   git clone https://github.com/FishgameStudio/termgif.git
   ```
2. Install PIP packages
   ```sh
   pip install .
   ```
3. Change git remote url to avoid accidental pushes to base project
   ```sh
   git remote remove origin
   git remote -v # confirm the changes
   ```

<p align="right"><a href="#readme-top">🔝back to top</a></p>



<!-- USAGE EXAMPLES -->
## 💡 Usage

```python
import termgif
import os
import subprocess

GIF_PATH: str = f"{os.path.dirname(__file__)}/dist.gif"
termgif.make_gif(
    'cmd /c "echo hello world!"', GIF_PATH, width=100, height=25, fps=90  # Specify the command to execute.
)
subprocess.run([GIF_PATH], shell=True)  # Open it with the default program.
```

_For more examples, please refer to the [Documentation](docs) or [Examples](examples)_

<p align="right"><a href="#readme-top">🔝back to top</a></p>



<!-- ROADMAP -->
## 🗺️ Roadmap
- [x] **v0.1.0**: Basic recording for Windows
- [ ] **v0.2.0**:
    - [ ] Support for macOS and Linux
    - [ ] Support for recording live inputting text on console (`stdin`)
    - [ ] Support recording live console (with echo and color)

See the [open issues](https://github.com/FishgameStudio/termgif/issues) for a full list of proposed features (and known issues).

<p align="right"><a href="#readme-top">🔝back to top</a></p>



<!-- CONTRIBUTING -->
## 🤝 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right"><a href="#readme-top">🔝back to top</a></p>

### 🌟 Top contributors:

<a href="https://github.com/FishgameStudio/termgif/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=FishgameStudio/termgif" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## 📃 License

Distributed under the project_license. See `LICENSE` for more information.

<p align="right"><a href="#readme-top">🔝back to top</a></p>



<!-- CONTACT -->
## 📬 Contact

Nicola Grey - [popxh@outlook.com](mailto:popxh@outlook.com)

Project Link: [https://github.com/FishgameStudio/termgif](https://github.com/FishgameStudio/termgif)

<p align="right"><a href="#readme-top">🔝back to top</a></p>



<!-- ACKNOWLEDGMENTS -->
## 🙏 Acknowledgments

* [Best-README-Template](https://github.com/othneildrew/Best-README-Template)
* [Pillow](https://github.com/python-pillow/Pillow)
* [pyte](https://github.com/selectel/pyte)
* [winpty](https://github.com/rprichard/winpty)
* [pywinpty](https://github.com/andfoy/pywinpty)

<p align="right"><a href="#readme-top">🔝back to top</a></p>
