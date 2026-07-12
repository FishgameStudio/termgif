# Example to call the APIs.

import os
import subprocess as sp

import termgif

GIF_PATH: str = f"{os.path.dirname(__file__)}/dist.gif"
termgif.make_gif(
    'cmd /c "echo hello world!"', GIF_PATH # Specify the command to execute.
)
_ = sp.run([GIF_PATH], shell=True)  # Open it with the default program.
