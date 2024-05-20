"""
Error ABC's.

The error abstract classes.
"""

from __future__ import annotations

import datetime
import attrs

from ongaku.enums import SeverityType

__all__ = (
    "RestError",
    "ExceptionError",
)

@attrs.define
class RestError:
    """
    Rest error information.

    This is the error that is formed, when a call to a rest method fails.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#error-responses)
    """

    _timestamp: datetime.datetime = attrs.field(alias="timestamp")
    _status: int = attrs.field(alias="status")
    _error: str = attrs.field(alias="error")
    _message: str = attrs.field(alias="message")
    _path: str = attrs.field(alias="path")
    _trace: str | None = attrs.field(alias="trace")

    @property
    def timestamp(self) -> datetime.datetime:
        """The timestamp of the error in milliseconds since the Unix epoch."""
        return self._timestamp
    
    @property
    def status(self) -> int:
        """The HTTP status code."""
        return self._status

    @property
    def error(self) -> str:
        """The HTTP status code message."""
        return self._error
    

    @property
    def message(self) -> str:
        """The error message."""
        return self._message
    

    @property
    def path(self) -> str:
        """The request path."""
        return self._path

    @property
    def trace(self) -> str | None:
        """The stack trace of the error."""
        return self._trace
    

@attrs.define
class ExceptionError:
    """
    Exception error.

    The exception error lavalink returns when a track has an exception.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#exception-object)
    """

    _message: str = attrs.field(alias="message")
    _severity: SeverityType = attrs.field(alias="severity")
    _cause: str = attrs.field(alias="cause")

    @property
    def message(self) -> str:
        """The message of the exception."""
        return self._message

    @property
    def severity(self) -> SeverityType:
        """The severity of the exception."""
        return self._severity
    
    @property
    def cause(self) -> str:
        """The cause of the exception."""
        return self._cause


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
