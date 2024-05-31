"""
Errors.

All of the ongaku errors.
"""

from __future__ import annotations

import typing

import attrs

from ongaku.abc import errors as errors_

if typing.TYPE_CHECKING:
    import datetime

    from ongaku.abc.errors import SeverityType

__all__ = (
    "OngakuError",
    "RestError",
    "RestStatusError",
    "RestRequestError",
    "RestEmptyError",
    "RestExceptionError",
    "ClientError",
    "ClientAliveError",
    "SessionError",
    "SessionStartError",
    "SessionHandlerError",
    "NoSessionsError",
    "PlayerError",
    "PlayerConnectError",
    "PlayerQueueError",
    "PlayerMissingError",
    "BuildError",
    "TimeoutError",
)


@attrs.define
class OngakuError(Exception):
    """The base ongaku error."""


# Rest:


@attrs.define
class RestError(OngakuError):
    """The base rest error for all rest action errors."""


@attrs.define
class RestStatusError(RestError):
    """Raised when the status is 4XX or 5XX."""

    status: int
    """The status of the response."""
    response: str | None
    """The response of the Error."""


@attrs.define
class RestRequestError(RestError, errors_.RestError):
    """Raised when a rest error is received from the response."""

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

    @classmethod
    def from_error(cls, error: errors_.RestError):
        return cls(
            error.timestamp,
            error.status,
            error.error,
            error.message,
            error.path,
            error.trace,
        )

    @property
    def timestamp(self) -> datetime.datetime:
        return self._timestamp

    @property
    def status(self) -> int:
        return self._status

    @property
    def error(self) -> str:
        return self._error

    @property
    def message(self) -> str:
        return self._message

    @property
    def path(self) -> str:
        return self._path

    @property
    def trace(self) -> str | None:
        return self._trace


@attrs.define
class RestEmptyError(RestError):
    """Raised when the request was 204, but required data."""


@attrs.define
class RestExceptionError(RestError, errors_.ExceptionError):
    """Raised when a track search results in a error result."""

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
    def severity(self) -> SeverityType:
        return self._severity

    @property
    def cause(self) -> str:
        return self._cause


# Client


@attrs.define
class ClientError(OngakuError):
    """The base for all client exception."""


@attrs.define
class ClientAliveError(ClientError):
    """Raised when the client is not currently alive, or has crashed."""

    reason: str
    """The reason this exception occurred."""


# Sessions


@attrs.define
class SessionError(OngakuError):
    """The base session error for all session related errors."""


@attrs.define
class SessionStartError(SessionError):
    """Raised when the session has not started. (has not received the ready payload)."""


# Session Handler


@attrs.define
class SessionHandlerError(OngakuError):
    """The base for all session handler related Errors."""


@attrs.define
class NoSessionsError(SessionHandlerError):
    """Raised when there is no available sessions for the handler to return."""


# Player


@attrs.define
class PlayerError(OngakuError):
    """The base for all player related errors."""


@attrs.define
class PlayerConnectError(PlayerError):
    """Raised when the player cannot connect to lavalink, or discord."""

    reason: str
    """The reason for failure of connection."""


@attrs.define
class PlayerQueueError(PlayerError):
    """Raised when the players queue is empty."""

    reason: str
    """Reason for the queue error."""


@attrs.define
class PlayerMissingError(PlayerError):
    """Raised when the player is missing."""


# Others:


@attrs.define
class BuildError(OngakuError):
    """Raised when a abstract class fails to build."""

    reason: str | None
    """The reason for the failure of the build."""


@attrs.define
class TimeoutError(OngakuError):
    """Raised when an event times out."""


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
