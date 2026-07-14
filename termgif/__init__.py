# The MIT License (MIT)
#
# Copyright (c) 2026 FishgameStudio
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
``termgif`` can record the specified window and output GIF files.
For complete informations see docs.

# Main API
- ``make_gif(...)``: Record a specified window context and output a GIF file to
the path, returns None. This is the wrapped cross-platform API.
- ``record_window(...)``: Windows raw API for targeted window recording.
- ``linux.record_window(...)``: Linux Wayland fallback recorder (full monitor capture only, no precise single-window tracking).

"""

from .record_win import record_window
from .wrap import make_gif
from . import linux
from . import macos

__version__ = "0.1.1"
__author__ = "FishgameStudio"
__all__ = [
    "make_gif",
    "record_window",
    "linux", 
    "macos"
]
