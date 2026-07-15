from pathlib import Path

from setuptools import find_packages, setup

BASE_DIR: Path = Path(__file__).parent
README: str = (BASE_DIR / "README.md").read_text(encoding="utf-8")

_ = setup(
    name="term2gif",
    version="0.2.2",
    author="Fishgame Studio",
    author_email="popxh@outlook.com",
    description="Lightweight GUI framework written in Python",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/FishgameStudio/termgif",
    license="MIT",
    python_requires=">=3.10",
    packages=find_packages(where="termgif"),
    package_dir={"termgif": "termgif"},
    package_data={
        "ohmygui": [
            "termgif/assets/*", "assets/*"
        ]
    },
    keywords=["term2gif", "gif", "gif-generator", "terminal"],
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS",
        "License :: OSI Approved :: MIT License",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Multimedia :: Graphics :: Capture",
        "Topic :: Utilities",
    ],
    install_requires=[
        "pillow>=12.3.0", 
        "PyGetWindow>=0.0.9", 
        "mss>=10.2.0", 
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "mypy>=1.8",
            "build",
            "twine"
        ],
        "examples": [
            "pillow>=10.0"
        ]
    }
)
