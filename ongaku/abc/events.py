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

    def __eq__(self, other: object) -> bool:  # noqa: D105
        if not isinstance(other, OngakuEvent):
            return False

        if self.client != other.client:
            return False

        if self.session != other.session:
            return False

        return True


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

    def __eq__(self, other: object) -> bool:  # noqa: D105
        if not isinstance(other, Ready):
            return False

        if self.resumed != other.resumed:
            return False

        if self.session_id != other.session_id:
            return False

        return True


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

    def __eq__(self, other: object) -> bool:  # noqa: D105
        if not isinstance(other, PlayerUpdate):
            return False

        if self.guild_id != other.guild_id:
            return False

        if self.state != other.state:
            return False

        return True


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

    def __eq__(self, other: object) -> bool:  # noqa: D105
        if not isinstance(other, WebsocketClosed):
            return False

        if self.guild_id != other.guild_id:
            return False

        if self.code != other.code:
            return False

        if self.reason != other.reason:
            return False

        if self.by_remote != other.by_remote:
            return False

        return True


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

    def __eq__(self, other: object) -> bool:  # noqa: D105
        if not isinstance(other, TrackStart):
            return False

        if self.guild_id != other.guild_id:
            return False

        if self.track != other.track:
            return False

        return True


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

    def __eq__(self, other: object) -> bool:  # noqa: D105
        if not isinstance(other, TrackEnd):
            return False

        if self.guild_id != other.guild_id:
            return False

        if self.track != other.track:
            return False

        if self.reason != other.reason:
            return False

        return True


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

    def __eq__(self, other: object) -> bool:  # noqa: D105
        if not isinstance(other, TrackException):
            return False

        if self.guild_id != other.guild_id:
            return False

        if self.track != other.track:
            return False

        if self.exception != other.exception:
            return False

        return True


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

    def __eq__(self, other: object) -> bool:  # noqa: D105
        if not isinstance(other, TrackStuck):
            return False

        if self.guild_id != other.guild_id:
            return False

        if self.track != other.track:
            return False

        if self.threshold_ms != other.threshold_ms:
            return False

        return True


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

    def __eq__(self, other: object) -> bool:  # noqa: D105
        if not isinstance(other, QueueEmpty):
            return False

        if self.guild_id != other.guild_id:
            return False

        if self.old_track != other.old_track:
            return False

        return True


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

    def __eq__(self, other: object) -> bool:  # noqa: D105
        if not isinstance(other, QueueNext):
            return False

        if self.guild_id != other.guild_id:
            return False

        if self.track != other.track:
            return False

        if self.old_track != other.old_track:
            return False

        return True


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
