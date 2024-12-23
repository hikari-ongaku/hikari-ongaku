"""
Types.

All types for ongaku.
"""

from __future__ import annotations

import typing

import hikari

__all__ = ("PayloadMappingT", "PayloadSequenceT", "RequestT", "RequestorT")

# Type Variables.

RequestT = typing.TypeVar(
    "RequestT",
    str,
    int,
    bool,
    float,
    dict[str, typing.Any],
    list[typing.Any],
    tuple[typing.Any, ...],
)
"""Request Type.

The types you can request for.
"""


# Type Aliases

RequestorT: typing.TypeAlias = (
    hikari.SnowflakeishOr[hikari.User] | hikari.SnowflakeishOr[hikari.Member]
)
"""Requestor Type.

The types to set for a requestor of a track.s
"""

PayloadMappingT: typing.TypeAlias = typing.Mapping[str, typing.Any] | str | bytes
"""Payload Mapping Type. 

Supports string, bytes, or a mapping.
"""
PayloadSequenceT: typing.TypeAlias = typing.Sequence[typing.Any] | str | bytes
"""Payload Sequence Type. 

Supports string, bytes, or a sequence.
"""

# MIT License

# Copyright (c) 2023-present MPlatypus

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
