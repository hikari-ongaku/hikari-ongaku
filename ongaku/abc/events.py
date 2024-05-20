"""
Event ABC's and Events.

The session abstract classes and hikari events.
"""

from __future__ import annotations

import hikari
import attrs

from ongaku.abc.error import ExceptionError
from ongaku.abc.player import State
from ongaku.abc.track import Track
from ongaku.enums import TrackEndReasonType

__all__ = (
    "Ready",
    "PlayerUpdate",
    "WebsocketClosed",
    "TrackStart",
    "TrackEnd",
    "TrackException",
    "TrackStuck",
)

@attrs.define
class Ready:
    """
    Ready Event Base.

    The base for the ready event.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#ready-op)
    """

    _resumed: bool = attrs.field(alias="resumed")
    _session_id: str = attrs.field(alias="session_id")
    
    @property
    def resumed(self) -> bool:
        """Whether or not the session has been resumed, or is a new session."""
        return self._resumed

    @property
    def session_id(self) -> str:
        """The lavalink session id, for the current session."""
        return self._session_id
    

@attrs.define
class PlayerUpdate:
    """
    Player update event base.

    The base for the player update event.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#player-update-op)
    """

    _guild_id: hikari.Snowflake = attrs.field(alias="guild_id")
    _state: State = attrs.field(alias="state")

    @property
    def guild_id(self) -> hikari.Snowflake:
        """The guild related to this event."""
        return self._guild_id
    
    @property
    def state(self) -> State:
        """The player state."""
        ...


@attrs.define
class WebsocketClosed:
    """
    Websocket closed event base.

    The base for the websocket closed event.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#websocketclosedevent)
    """

    _guild_id: hikari.Snowflake = attrs.field(alias="guild_id")
    _code: int = attrs.field(alias="code")
    _reason: str = attrs.field(alias="reason")
    _by_remote: bool = attrs.field(alias="by_remote")

    @property
    def guild_id(self) -> hikari.Snowflake:
        """The guild related to this event."""
        return self._guild_id

    @property
    def code(self) -> int:
        """The error code that [discord](https://discord.com/developers/docs/topics/opcodes-and-status-codes#voice-voice-close-event-codes) responded with."""
        return self._code

    @property
    def reason(self) -> str:
        """The close reason."""
        return self._reason
    
    @property
    def by_remote(self) -> bool:
        """Whether the connection was closed by Discord."""
        return self._by_remote
    

@attrs.define
class TrackStart:
    """
    Track start event base.

    The base for the track start event.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#trackstartevent)
    """

    _guild_id: hikari.Snowflake = attrs.field(alias="guild_id")
    _track: Track = attrs.field(alias="track")

    @property
    def guild_id(self) -> hikari.Snowflake:
        """The guild related to this event."""
        return self._guild_id
    
    @property
    def track(self) -> Track:
        """The track related to this event."""
        return self._track
    

@attrs.define
class TrackEnd:
    """
    Track end event base.

    The base for the track end event.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#trackendevent)
    """

    _guild_id: hikari.Snowflake = attrs.field(alias="guild_id")
    _track: Track = attrs.field(alias="track")
    _reason: TrackEndReasonType = attrs.field(alias="reason")

    @property
    def guild_id(self) -> hikari.Snowflake:
        """The guild related to this event."""
        return self._guild_id
    
    @property
    def track(self) -> Track:
        """The track related to this event."""
        return self._track
    
    @property
    def reason(self) -> TrackEndReasonType:
        """The reason for the track ending."""
        return self._reason

@attrs.define
class TrackException:
    """
    Track exception event base.

    The base for track exception event.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#trackexceptionevent)
    """

    _guild_id: hikari.Snowflake = attrs.field(alias="guild_id")
    _track: Track = attrs.field(alias="track")
    _exception: ExceptionError = attrs.field(alias="exception")

    @property
    def guild_id(self) -> hikari.Snowflake:
        """The guild related to this event."""
        return self._guild_id
    
    @property
    def track(self) -> Track:
        """The track related to this event."""
        return self._track

    @property
    def exception(self) -> ExceptionError:
        """The exception error that was returned."""
        return self._exception

@attrs.define
class TrackStuck:
    """
    Track stuck event base.

    The base for track stuck event.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#trackstuckevent)
    """

    _guild_id: hikari.Snowflake = attrs.field(alias="guild_id")
    _track: Track = attrs.field(alias="track")
    _threshold_ms: int = attrs.field(alias="threshold_ms")

    @property
    def guild_id(self) -> hikari.Snowflake:
        """The guild related to this event."""
        return self._guild_id
    
    @property
    def track(self) -> Track:
        """The track related to this event."""
        return self._track

    @property
    def threshold_ms(self) -> int:
        """The threshold in milliseconds that was exceeded."""
        return self._threshold_ms
    
@attrs.define
class QueueEmpty:
    """
    Queue empty event.

    The event that is dispatched, when a players queue is empty.
    """

    _guild_id: hikari.Snowflake = attrs.field(alias="guild_id")

    @property
    def guild_id(self) -> hikari.Snowflake:
        """The guild related to this event."""
        return self._guild_id


@attrs.define
class QueueNext:
    """
    Queue next event.

    The event that is dispatched when a queue is playing the next song.
    """

    _guild_id: hikari.Snowflake = attrs.field(alias="guild_id")
    _track: Track = attrs.field(alias="track")
    _old_track: Track = attrs.field(alias="old_track")

    @property
    def guild_id(self) -> hikari.Snowflake:
        """The guild related to this event."""
        return self._guild_id
    
    @property
    def track(self) -> Track:
        """The track related to this event."""
        return self._track
    
    @property
    def old_track(self) -> Track:
        """The track that was previously playing."""
        return self._old_track



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
