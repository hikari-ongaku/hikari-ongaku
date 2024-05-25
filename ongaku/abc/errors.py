"""
Error ABC's.

The error abstract classes.
"""

from __future__ import annotations

import abc
import datetime

from ongaku.enums import SeverityType

__all__ = (
    "RestError",
    "ExceptionError",
)


class RestError(abc.ABC):
    """
    Rest error information.

    This is the error that is formed, when a call to a rest method fails.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#error-responses)
    """

    @property
    @abc.abstractmethod
    def timestamp(self) -> datetime.datetime:
        """The timestamp of the error in milliseconds since the Unix epoch."""
        ...

    @property
    @abc.abstractmethod
    def status(self) -> int:
        """The HTTP status code."""
        ...

    @property
    @abc.abstractmethod
    def error(self) -> str:
        """The HTTP status code message."""
        ...

    @property
    @abc.abstractmethod
    def message(self) -> str:
        """The error message."""
        ...

    @property
    @abc.abstractmethod
    def path(self) -> str:
        """The request path."""
        ...

    @property
    @abc.abstractmethod
    def trace(self) -> str | None:
        """The stack trace of the error."""
        ...


class ExceptionError(abc.ABC):
    """
    Exception error.

    The exception error lavalink returns when a track has an exception.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#exception-object)
    """

    @property
    @abc.abstractmethod
    def message(self) -> str:
        """The message of the exception."""
        ...

    @property
    @abc.abstractmethod
    def severity(self) -> SeverityType:
        """The severity of the exception."""
        ...

    @property
    @abc.abstractmethod
    def cause(self) -> str:
        """The cause of the exception."""
        ...


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
