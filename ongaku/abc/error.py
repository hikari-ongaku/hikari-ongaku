"""
Error ABC's.

The error abstract classes.
"""

from __future__ import annotations

import typing as t

import pydantic

from ..enums import SeverityType
from .bases import PayloadBase

__all__ = (
    "RestError",
    "ExceptionError",
)


class RestError(PayloadBase):
    """
    Rest error information.

    This is the error that is formed, when a call to a rest method fails.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest.html#error-responses)
    """

    timestamp: int
    """The timestamp of the error in milliseconds since the Unix epoch."""
    status: int
    """The HTTP status code."""
    error: str
    """The HTTP status code message."""
    trace: t.Annotated[str | None, pydantic.Field(default=None)] = None
    """The stack trace of the error."""
    message: str
    """The error message."""
    path: str
    """The request path."""


class ExceptionError(PayloadBase):
    """
    Exception error.

    The exception error lavalink returns when a track has an exception.
    """

    message: str
    """The message of the exception."""
    severity: SeverityType
    """The severity of the exception."""
    cause: str
    """The cause of the exception."""


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
