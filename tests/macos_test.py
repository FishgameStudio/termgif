import termgif
import os

# Record a vscode window
# The title of VSCode is different between macOS and Windows.
# Use the name of the current folder instead.
termgif.make_gif("", f"{os.path.dirname(__file__)}/macos_o.gif", win_name="termgif")