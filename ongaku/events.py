"""
Events.

All ongaku related events.
"""

from __future__ import annotations

import typing

import attrs
import hikari

if typing.TYPE_CHECKING:
    from ongaku.abc.error import ExceptionError
    from ongaku.abc.player import PlayerState
    from ongaku.abc.statistics import StatsCpu
    from ongaku.abc.statistics import StatsFrameStatistics
    from ongaku.abc.statistics import StatsMemory
    from ongaku.abc.track import Track
    from ongaku.client import Client
    from ongaku.enums import TrackEndReasonType
    from ongaku.session import Session

__all__ = (
    "OngakuEvent",
    "PayloadEvent",
    "ReadyEvent",
    "PlayerUpdateEvent",
    "StatisticsEvent",
    "WebsocketClosedEvent",
    "TrackStartEvent",
    "TrackEndEvent",
    "TrackExceptionEvent",
    "TrackStuckEvent",
    "QueueEmptyEvent",
    "QueueNextEvent",
)


@attrs.define
class OngakuEvent(hikari.Event):
    """The base ongaku event, that all events subclass."""

    _app: hikari.RESTAware
    _client: Client
    _session: Session

    @property
    def app(self) -> hikari.RESTAware:
        """The application attached to the event."""
        return self._app

    @property
    def client(self) -> Client:
        """The ongaku client attached to the event."""
        return self._client

    @property
    def session(self) -> Session:
        """The session attached to the event."""
        return self._session


@attrs.define
class PayloadEvent(OngakuEvent):
    """
    Payload Event.

    The event that is dispatched each time a message is received from the lavalink websocket.
    """

    payload: str
    """The payload received."""


@attrs.define
class ReadyEvent(OngakuEvent):
    """
    Ready Event.

    The event that is dispatched when the lavalink server is ready for connections.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#ready-op)
    """

    resumed: bool
    """Whether the session has been resumed, or is a new session."""
    session_id: str
    """The lavalink session id, for the current session."""


@attrs.define
class PlayerUpdateEvent(OngakuEvent):
    """
    Player Update Event.

    The event that is dispatched when a players state has been updated.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#player-update-op)
    """

    guild_id: hikari.Snowflake
    """The guild related to this event."""
    state: PlayerState
    """The player state."""


@attrs.define
class StatisticsEvent(OngakuEvent):
    """
    Statistics Event.

    All of the statistics about the current session.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#stats-op)
    """

    players: int
    """The amount of players connected to the session."""
    playing_players: int
    """The amount of players playing a track."""
    uptime: int
    """The uptime of the session in milliseconds."""
    memory: StatsMemory
    """The memory stats of the session."""
    cpu: StatsCpu
    """The cpu stats of the session."""
    frame_statistics: StatsFrameStatistics | None
    """The frame stats of the session."""


@attrs.define
class WebsocketClosedEvent(OngakuEvent):
    """
    Websocket Closed Event.

    The event that is dispatched, when a websocket to discord gets closed.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#websocketclosedevent)
    """

    guild_id: hikari.Snowflake
    """The guild related to this event."""
    code: int
    """The discord error code that [discord](https://discord.com/developers/docs/topics/opcodes-and-status-codes#voice-voice-close-event-codes) responded with."""
    reason: str
    """The close reason."""
    by_remote: bool
    """Whether the connection was closed by Discord."""


@attrs.define
class TrackStartEvent(OngakuEvent):
    """
    Track start event.

    The event that is dispatched when a track starts playing.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#trackstartevent)
    """

    guild_id: hikari.Snowflake
    """The guild related to this event."""
    track: Track
    """The track related to this event."""


@attrs.define
class TrackEndEvent(OngakuEvent):
    """
    Track end event.

    The event that is dispatched when a track ends.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#trackendevent)
    """

    guild_id: hikari.Snowflake
    """The guild related to this event."""
    track: Track
    """The track related to this event."""
    reason: TrackEndReasonType
    """The reason for the track ending."""


@attrs.define
class TrackExceptionEvent(OngakuEvent):
    """
    Track exception event.

    The event that is dispatched when an exception happens with a track.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#trackexceptionevent)
    """

    guild_id: hikari.Snowflake
    """The guild related to this event."""
    track: Track
    """The track related to this event."""
    exception: ExceptionError
    """The exception error that was returned."""


@attrs.define
class TrackStuckEvent(OngakuEvent):
    """
    Track stuck event.

    The event that is dispatched when a track gets stuck.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#trackstuckevent)
    """

    guild_id: hikari.Snowflake
    """The guild related to this event."""
    track: Track
    """The track related to this event."""
    threshold_ms: int
    """The threshold in milliseconds that was exceeded."""


@attrs.define
class QueueEmptyEvent(OngakuEvent):
    """
    Queue empty event.

    The event that is dispatched, when a players queue is empty.
    """

    guild_id: hikari.Snowflake
    """The guild related to this event."""


@attrs.define
class QueueNextEvent(OngakuEvent):
    """
    Queue next event.

    The event that is dispatched when a queue is playing the next song.
    """

    guild_id: hikari.Snowflake
    """The guild related to this event."""
    track: Track
    """The track that is now playing."""
    old_track: Track
    """The track that was playing."""


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
