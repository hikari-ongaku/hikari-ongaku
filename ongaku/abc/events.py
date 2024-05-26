"""
Event ABC's and Events.

The session abstract classes and hikari events.
"""

from __future__ import annotations

import abc
import enum
import typing

import hikari

from ongaku.abc.errors import ExceptionError
from ongaku.abc.player import State
from ongaku.abc.track import Track

if typing.TYPE_CHECKING:
    from ongaku.client import Client
    from ongaku.session import Session

__all__ = (
    "OngakuEvent",
    "Ready",
    "PlayerUpdate",
    "WebsocketClosed",
    "TrackStart",
    "TrackEnd",
    "TrackException",
    "TrackStuck",
    "QueueEmpty",
    "QueueNext",
    "TrackEndReasonType",
)


class OngakuEvent(hikari.Event, abc.ABC):
    """Ongaku Event.

    The base ongaku event, that adds the client and session to all events.
    """

    @property
    @abc.abstractmethod
    def client(self) -> Client:
        """The ongaku client attached to the event."""
        ...

    @property
    @abc.abstractmethod
    def session(self) -> Session:
        """The session attached to the event."""
        ...


class Ready(abc.ABC):
    """
    Ready Event Base.

    The base for the ready event.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#ready-op)
    """

    @property
    @abc.abstractmethod
    def resumed(self) -> bool:
        """Whether or not the session has been resumed, or is a new session."""
        ...

    @property
    @abc.abstractmethod
    def session_id(self) -> str:
        """The lavalink session id, for the current session."""
        ...


class PlayerUpdate(abc.ABC):
    """
    Player update event base.

    The base for the player update event.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#player-update-op)
    """

    @property
    @abc.abstractmethod
    def guild_id(self) -> hikari.Snowflake:
        """The guild related to this event."""
        ...

    @property
    @abc.abstractmethod
    def state(self) -> State:
        """The player state."""
        ...


class WebsocketClosed(abc.ABC):
    """
    Websocket closed event base.

    The base for the websocket closed event.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#websocketclosedevent)
    """

    @property
    @abc.abstractmethod
    def guild_id(self) -> hikari.Snowflake:
        """The guild related to this event."""
        ...

    @property
    @abc.abstractmethod
    def code(self) -> int:
        """The error code that [discord](https://discord.com/developers/docs/topics/opcodes-and-status-codes#voice-voice-close-event-codes) responded with."""
        ...

    @property
    @abc.abstractmethod
    def reason(self) -> str:
        """The close reason."""
        ...

    @property
    @abc.abstractmethod
    def by_remote(self) -> bool:
        """Whether the connection was closed by Discord."""
        ...


class TrackStart(abc.ABC):
    """
    Track start event base.

    The base for the track start event.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#trackstartevent)
    """

    @property
    @abc.abstractmethod
    def guild_id(self) -> hikari.Snowflake:
        """The guild related to this event."""
        ...

    @property
    @abc.abstractmethod
    def track(self) -> Track:
        """The track related to this event."""
        ...


class TrackEnd(abc.ABC):
    """
    Track end event base.

    The base for the track end event.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#trackendevent)
    """

    @property
    @abc.abstractmethod
    def guild_id(self) -> hikari.Snowflake:
        """The guild related to this event."""
        ...

    @property
    @abc.abstractmethod
    def track(self) -> Track:
        """The track related to this event."""
        ...

    @property
    @abc.abstractmethod
    def reason(self) -> TrackEndReasonType:
        """The reason for the track ending."""
        ...


class TrackException(abc.ABC):
    """
    Track exception event base.

    The base for track exception event.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#trackexceptionevent)
    """

    @property
    @abc.abstractmethod
    def guild_id(self) -> hikari.Snowflake:
        """The guild related to this event."""
        ...

    @property
    @abc.abstractmethod
    def track(self) -> Track:
        """The track related to this event."""
        ...

    @property
    @abc.abstractmethod
    def exception(self) -> ExceptionError:
        """The exception error that was returned."""
        ...


class TrackStuck(abc.ABC):
    """
    Track stuck event base.

    The base for track stuck event.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#trackstuckevent)
    """

    @property
    @abc.abstractmethod
    def guild_id(self) -> hikari.Snowflake:
        """The guild related to this event."""
        ...

    @property
    @abc.abstractmethod
    def track(self) -> Track:
        """The track related to this event."""
        ...

    @property
    @abc.abstractmethod
    def threshold_ms(self) -> int:
        """The threshold in milliseconds that was exceeded."""
        ...


class QueueEmpty(abc.ABC):
    """
    Queue empty event.

    The event that is dispatched, when a players queue is empty.
    """

    @property
    @abc.abstractmethod
    def guild_id(self) -> hikari.Snowflake:
        """The guild related to this event."""
        ...

    @property
    @abc.abstractmethod
    def old_track(self) -> Track:
        """The track that was previously playing."""
        ...


class QueueNext(abc.ABC):
    """
    Queue next event.

    The event that is dispatched when a queue is playing the next song.
    """

    @property
    @abc.abstractmethod
    def guild_id(self) -> hikari.Snowflake:
        """The guild related to this event."""
        ...

    @property
    @abc.abstractmethod
    def track(self) -> Track:
        """The track related to this event."""
        ...

    @property
    @abc.abstractmethod
    def old_track(self) -> Track:
        """The track that was previously playing."""
        ...


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
