"""
Event ABC's and Events.

The session abstract classes and hikari events.
"""

from __future__ import annotations

import abc
import enum
import typing

import hikari

if typing.TYPE_CHECKING:
    from ongaku.client import Client
    from ongaku.session import Session

__all__ = (
    "OngakuEvent",
    "TrackEndReasonType",
)


class OngakuEvent(hikari.Event, abc.ABC):
    """Ongaku Event.

    The base ongaku event, that adds the client and session to all events.
    """

    __slots__: typing.Sequence[str] = ("_app", "_client", "_session")

    @property
    def client(self) -> Client:
        """The ongaku client attached to the event."""
        return self._client

    @property
    def session(self) -> Session:
        """The session attached to the event."""
        return self._session

    @property
    def app(self) -> hikari.RESTAware:
        return self._app

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, OngakuEvent):
            return False

        if self.client != other.client:
            return False

        return self.session == other.session


class TrackEndReasonType(str, enum.Enum):
    """
    Track end reason type.

    The track end reason type for the track that was just playing.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket#track-end-reason)
    """

    FINISHED = "finished"
    """The track finished playing."""
    LOADFAILED = "loadFailed"
    """The track failed to load."""
    STOPPED = "stopped"
    """The track was stopped."""
    REPLACED = "replaced"
    """The track was replaced."""
    CLEANUP = "cleanup"
    """The track was cleaned up."""


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
