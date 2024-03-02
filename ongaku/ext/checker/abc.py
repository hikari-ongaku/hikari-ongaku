"""
Checker.

A extension, that checks if your query, is a track/playlist, or just a query.
"""

from __future__ import annotations

import enum

import attrs


@attrs.define
class Checked:
    """
    Checked value.

    The checked, and confirmed value, with its specific type attached.
    """

    value: str
    """The value.
    
    This is the value, based on the [type][ongaku.ext.checker.abc.CheckedType] it is.
    """
    type: CheckedType
    """The type of the checked value."""


class CheckedType(enum.IntEnum):
    """
    Checked type.

    The type of result you have received.
    """

    QUERY = 0
    """The result was a query."""
    TRACK = 1
    """The result was a track."""
    PLAYLIST = 2
    """The result was a playlist."""


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
