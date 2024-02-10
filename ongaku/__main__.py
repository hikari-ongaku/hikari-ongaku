"""CLI for ongaku."""

import os
import sys

import hikari

import ongaku

# Support color on Windows
if sys.platform == "win32":
    import colorama

    colorama.init()


WATERMELON = "\x1b[91m"
WHITE = "\x1b[37m"

if "--version" in sys.argv or "-v" in sys.argv:
    sys.stderr.write(f"{WATERMELON}Ongaku version: {WHITE}{ongaku.__version__}")
    exit(1)

if "--about" in sys.argv or "-a" in sys.argv:
    sys.stderr.write(
        f"""{WATERMELON}About Ongaku
{WHITE}------------
Ongaku is a voice library, designed to work with hikari (https://hikari-py.dev/).
It's a super simple to setup library, whilst also having all features for advanced users as well.
"""
    )
    exit(1)

sys.stderr.write(
    f"""
{WATERMELON}ongaku - package information
{WHITE}--------------------------------
{WATERMELON}Ongaku version: {WHITE}{ongaku.__version__}
{WATERMELON}Hikari version: {WHITE}{hikari.__version__}
{WATERMELON}Install path: {WHITE}{os.path.abspath(os.path.dirname(__file__))}\n\n"""
)
