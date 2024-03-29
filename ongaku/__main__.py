"""CLI for ongaku."""

import os
import sys

import hikari

import ongaku

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


# MIT License

# Copyright (c) 2023 MPlatypus

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
