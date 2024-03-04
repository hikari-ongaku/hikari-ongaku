"""Errors.

All of the ongaku errors.
"""

from __future__ import annotations

import aiohttp
import attrs
import hikari

from .enums import WebsocketEventType
from .enums import WebsocketOPCodeType

__all__ = (
    "OngakuException",
    "WebsocketException",
    "WebsocketClosureException",
    "WebsocketTypeException",
    "SessionException",
    "SessionConnectionException",
    "PlayerException",
    "PlayerConnectException",
    "PlayerQueueException",
    "PlayerMissingException",
    "BuildException",
    "RequiredException",
    "SessionHandlerException",
)


class OngakuException(Exception):
    """The base ongaku exception."""


# Websocket related:


class WebsocketException(OngakuException):
    """Base websocket exception."""


@attrs.define
class WebsocketClosureException(WebsocketException):
    """When a websocket has closed."""

    reason: aiohttp.WSCloseCode
    extra: str | None


@attrs.define
class WebsocketTypeException(WebsocketException):
    """When a event has an issue decoding."""

    op: WebsocketOPCodeType | WebsocketEventType | None
    """The op code or event type that this event error is attached too. If unknown, this will be none."""
    reason: str
    """The reason for the events error."""


# Session related:


@attrs.define
class SessionException(OngakuException):
    """Base session exception."""

    session_id: str | None


@attrs.define
class SessionConnectionException(SessionException):
    """Raised when the session has either failed to connect, or is not connected."""

    reason: str = "Session is missing."


# Player related:


@attrs.define
class PlayerException(OngakuException):
    """Base player exception."""

    guild_id: hikari.Snowflake


@attrs.define
class PlayerConnectException(PlayerException):
    """raised when the player fails to connect to a channel."""

    reason: str


@attrs.define
class PlayerQueueException(PlayerException):
    """Raised when an issue occurs within the queue of a player."""

    reason: str

    # Old errors:

    # class GatewayRequiredException(OngakuBaseException):
    """Raised when Gateway bot is not used. [more info](https://ongaku.mplaty.com/getting_started/#qs-and-as)."""

    # class BuildException(OngakuBaseException):
    """Raised when a model fails to build correctly."""

    # class TimeoutException(OngakuBaseException):
    """Raised when a timeout has exceed its timer."""

    # class RequiredException(OngakuBaseException):
    """Raised when a value is required, but is None, or missing."""


class PlayerMissingException(PlayerException):
    """Raised when the player was unable to be found."""


# Other:


@attrs.define
class BuildException(OngakuException):
    """Raised when something fails to be built."""

    reason: str


@attrs.define
class RequiredException(OngakuException):
    """Raised when something is required, but does not exist."""

    required_item: str


class LavalinkException(OngakuException):
    """Raised when an issue occurs with lavalink or rest actions."""


@attrs.define
class SessionHandlerException(OngakuException):
    """Raised when an issue occurs within a session handler."""

    reason: str


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
