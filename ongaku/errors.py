"""
Errors.

All of the ongaku errors.
"""

from __future__ import annotations

import typing

import attrs

from ongaku.abc.errors import ExceptionError

if typing.TYPE_CHECKING:
    from ongaku.abc.errors import RestError

__all__ = (
    "OngakuException",
    "RestException",
    "RestStatusException",
    "RestErrorException",
    "RestEmptyException",
    "RestTrackException",
    "ClientException",
    "ClientAliveException",
    "SessionException",
    "SessionStartException",
    "SessionHandlerException",
    "NoSessionsException",
    "PlayerException",
    "PlayerConnectException",
    "PlayerQueueException",
    "PlayerMissingException",
    "BuildException",
    "TimeoutException",
)


@attrs.define
class OngakuException(Exception):
    """The base ongaku exception."""


# Rest:


@attrs.define
class RestException(OngakuException):
    """The base rest exception for all rest action errors."""


@attrs.define
class RestStatusException(RestException):
    """Raised when the status is 4XX or 5XX."""

    status: int
    """The status of the response."""
    response: str | None
    """The response of the exception."""


@attrs.define
class RestErrorException(RestException):
    """Raised when a rest error is received from the response."""

    rest_error: RestError
    """The rest error object."""


@attrs.define
class RestEmptyException(RestException):
    """Raised when the request was 204, but required data."""


@attrs.define
class RestTrackException(RestException):
    """Raised when a track search results in a error result."""

    exception_error: ExceptionError
    """The exception error."""


# Client


@attrs.define
class ClientException(OngakuException):
    """The base for all client exceptions."""


@attrs.define
class ClientAliveException(ClientException):
    """Raised when the client is not currently alive, or has crashed."""

    reason: str
    """The reason this exception occurred."""


# Sessions


@attrs.define
class SessionException(OngakuException):
    """The base session exception for all session related exceptions."""


@attrs.define
class SessionStartException(SessionException):
    """Raised when the session has not started. (has not received the ready payload)."""


# Session Handler


@attrs.define
class SessionHandlerException(OngakuException):
    """The base for all session handler related exceptions."""


@attrs.define
class NoSessionsException(SessionHandlerException):
    """Raised when there is no available sessions for the handler to return."""


# Player


@attrs.define
class PlayerException(OngakuException):
    """The base for all player related exceptions."""


@attrs.define
class PlayerConnectException(PlayerException):
    """Raised when the player cannot connect to lavalink, or discord."""

    reason: str
    """The reason for failure of connection."""


@attrs.define
class PlayerQueueException(PlayerException):
    """Raised when the players queue is empty."""

    reason: str
    """Reason for the queue exception."""


@attrs.define
class PlayerMissingException(PlayerException):
    """Raised when the player is missing."""


# Others:


@attrs.define
class BuildException(OngakuException):
    """Raised when a abstract class fails to build."""

    reason: str | None
    """The reason for the failure of the build."""


@attrs.define
class TimeoutException(OngakuException):
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
