"""
Session ABC's.

The session abstract classes.
"""

from __future__ import annotations

import abc
import enum
import typing

__all__ = (
    "Session",
    "SessionStatus",
)


class Session(abc.ABC):
    """
    Session information.

    All of the specified session information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#update-session)
    """

    __slots__: typing.Sequence[str] = ("_resuming", "_timeout")

    @property
    def resuming(self) -> bool:
        """Whether resuming is enabled for this session or not."""
        return self._resuming

    @property
    def timeout(self) -> int:
        """The timeout in seconds."""
        return self._timeout

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Session):
            return False

        if self.resuming != other.resuming:
            return False

        if self.timeout != other.timeout:
            return False

        return True


class SessionStatus(int, enum.Enum):
    """
    Session Status.

    The status of the session.
    """

    NOT_CONNECTED = 0
    """Not connected to the lavalink server."""
    CONNECTED = 1
    """Successfully connected to the lavalink server."""
    FAILURE = 2
    """A failure occurred connecting to the lavalink server."""


class WebsocketOPCode(str, enum.Enum):
    READY = "ready"
    PLAYER_UPDATE = "playerUpdate"
    STATS = "stats"
    EVENT = "event"


class WebsocketEvent(str, enum.Enum):
    TRACK_START_EVENT = "TrackStartEvent"
    TRACK_END_EVENT = "TrackEndEvent"
    TRACK_EXCEPTION_EVENT = "TrackExceptionEvent"
    TRACK_STUCK_EVENT = "TrackStuckEvent"
    WEBSOCKET_CLOSED_EVENT = "WebSocketClosedEvent"


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
