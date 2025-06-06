"""
Errors.

All of the ongaku errors.
"""

from __future__ import annotations

import typing

from ongaku.abc import errors as errors_

if typing.TYPE_CHECKING:
    import datetime

    from ongaku.abc.errors import SeverityType

__all__ = (
    "BuildError",
    "ClientAliveError",
    "ClientError",
    "NoSessionsError",
    "OngakuError",
    "PlayerConnectError",
    "PlayerError",
    "PlayerMissingError",
    "PlayerQueueError",
    "RestEmptyError",
    "RestError",
    "RestExceptionError",
    "RestRequestError",
    "RestStatusError",
    "SessionError",
    "SessionHandlerError",
    "SessionStartError",
    "TimeoutError",
)


class OngakuError(Exception):
    """The base ongaku error."""


# Rest:


class RestError(OngakuError):
    """The base rest error for all rest action errors."""


class RestStatusError(RestError):
    """Raised when the status is 4XX or 5XX."""

    __slots__: typing.Sequence[str] = ("_reason", "_status")

    def __init__(self, status: int, reason: str | None) -> None:
        self._status = status
        self._reason = reason

    @property
    def status(self) -> int:
        """The status of the response."""
        return self._status

    @property
    def reason(self) -> str | None:
        """The response of the error."""
        return self._reason


class RestRequestError(RestError):
    """Raised when a rest error is received from the response."""

    __slots__: typing.Sequence[str] = (
        "_error",
        "_message",
        "_path",
        "_status",
        "_timestamp",
        "_trace",
    )

    def __init__(
        self,
        timestamp: datetime.datetime,
        status: int,
        error: str,
        message: str,
        path: str,
        trace: str | None,
    ) -> None:
        self._timestamp = timestamp
        self._status = status
        self._error = error
        self._message = message
        self._path = path
        self._trace = trace

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


class RestEmptyError(RestError):
    """Raised when the request was 204, but data was requested."""


class RestExceptionError(RestError, errors_.ExceptionError):
    """Raised when a track search results in a error result."""

    __slots__: typing.Sequence[str] = ()

    def __init__(
        self,
        message: str | None,
        severity: SeverityType,
        cause: str,
    ):
        self._message = message
        self._severity = severity
        self._cause = cause

    @classmethod
    def from_error(cls, error: errors_.ExceptionError):
        return cls(error.message, error.severity, error.cause)

    @property
    def message(self) -> str | None:
        return self._message

    @property
    def severity(self) -> errors_.SeverityType:
        return self._severity

    @property
    def cause(self) -> str:
        return self._cause


# Client


class ClientError(OngakuError):
    """The base for all client errors."""


class ClientAliveError(ClientError):
    """Raised when the client is not currently alive, or has crashed."""

    __slots__: typing.Sequence[str] = ("_reason",)

    def __init__(self, reason: str) -> None:
        self._reason = reason

    @property
    def reason(self) -> str:
        """The reason this error occurred."""
        return self._reason


# Sessions


class SessionError(OngakuError):
    """The base session error for all session related errors."""


class SessionStartError(SessionError):
    """Raised when the session has not started. (has not received the ready payload)."""


class SessionMissingError(SessionError):
    """Raised when the session could not be found."""


# Session Handler


class SessionHandlerError(OngakuError):
    """The base for all session handler related errors."""


class NoSessionsError(SessionHandlerError):
    """Raised when there is no available sessions for the handler to return."""


# Player


class PlayerError(OngakuError):
    """The base for all player related errors."""


class PlayerConnectError(PlayerError):
    """Raised when the player cannot connect to lavalink, or discord."""

    __slots__: typing.Sequence[str] = "_reason"

    def __init__(self, reason: str) -> None:
        self._reason = reason

    @property
    def reason(self) -> str:
        """The reason for failure of connection."""
        return self._reason


class PlayerQueueError(PlayerError):
    """Raised when the players queue is empty."""

    __slots__: typing.Sequence[str] = "_reason"

    def __init__(self, reason: str) -> None:
        self._reason = reason

    @property
    def reason(self) -> str:
        """Reason for the queue error."""
        return self._reason


class PlayerMissingError(PlayerError):
    """Raised when the player could not be found."""


# Others:


class BuildError(OngakuError):
    """Raised when a abstract class fails to build."""

    __slots__: typing.Sequence[str] = ("_exception", "_reason")

    def __init__(self, exception: Exception | None, reason: str | None = None) -> None:
        self._exception = exception
        self._reason = reason

    @property
    def exception(self) -> Exception | None:
        """The exception raised to receive the build error."""
        return self._exception

    @property
    def reason(self) -> str | None:
        """The reason this error occurred."""
        return self._reason


class TimeoutError(OngakuError):
    """Raised when an event times out."""


class UniqueError(OngakuError):
    """Raised when a value should be unique, but is not."""

    __slots__: typing.Sequence[str] = "_reason"

    def __init__(self, reason: str | None) -> None:
        self._reason = reason

    @property
    def reason(self) -> str | None:
        """The reason for the unique error."""
        return self._reason


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
