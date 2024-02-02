"""Events.

All of the hikari events for ongaku, are here!
"""

from __future__ import annotations

import hikari
import pydantic
import typing as t

from .. import enums
from .base import PayloadBase
from .base import PayloadBaseApp
from .lavalink import ExceptionError
from .track import Track

__all__ = (
    "OngakuEvent",
    "ReadyEvent",
    "StatsMemory",
    "StatsCpu",
    "StatsFrameStatistics",
    "StatisticsEvent",
    "WebsocketClosedEvent",
    "TrackStartEvent",
    "TrackEndEvent",
    "TrackExceptionEvent",
    "TrackStuckEvent",
    "QueueEmptyEvent",
    "QueueNextEvent",
)



class OngakuEvent(hikari.Event):
    """Ongaku Event.

    The base event, that all other Ongaku events are attached too.
    """

    _app: hikari.RESTAware

    @property
    def app(self) -> hikari.RESTAware:
        """The application the event is attached too."""
        return self._app


class ReadyEvent(OngakuEvent, PayloadBaseApp):
    """Ready event.

    The event that is dispatched, when lavalink is ready for new players, discord connections, and song requests.
    """

    resumed: bool
    """Whether or not the session has been resumed, or is a new session."""
    session_id: t.Annotated[str, pydantic.Field(alias="sessionId")]
    """The lavalink session id, for the current session."""



class StatsMemory(PayloadBase):
    """
    All of the Statistics Memory information.

    Find out more [here](https://lavalink.dev/api/websocket.html#memory).
    """

    free: int
    """The amount of free memory in bytes"""
    used: int
    """The amount of used memory in bytes"""
    allocated: int
    """The amount of allocated memory in bytes"""
    reservable: int
    """The amount of reservable memory in bytes"""



class StatsCpu(PayloadBase):
    """
    All of the Statistics CPU information.

    Find out more [here](https://lavalink.dev/api/websocket.html#cpu).
    """

    cores: int
    """The amount of cores the server has."""
    system_load: t.Annotated[float | int, pydantic.Field(alias="systemLoad")]
    """The system load of the server."""
    lavalink_load: t.Annotated[float | int, pydantic.Field(alias="systemLoad")]
    """The load of Lavalink on the server."""




class StatsFrameStatistics(PayloadBase):
    """
    All of the Statistics frame statistics information.

    Find out more [here](https://lavalink.dev/api/websocket.html#frame-stats).
    """

    sent: int
    """The amount of frames sent to Discord."""
    nulled: int
    """The amount of frames that were nulled."""
    deficit: int
    """The difference between sent frames and the expected amount of frames."""




class StatisticsEvent(OngakuEvent, PayloadBaseApp):
    """
    All of the Statistics information.

    Find out more [here](https://lavalink.dev/api/websocket.html#stats-object).
    """

    _app: hikari.RESTAware

    players: int
    """The amount of players connected to the session."""
    playing_players: t.Annotated[int, pydantic.Field(alias="playingPlayers")]
    """The amount of players playing a track."""
    uptime: int
    """The uptime of the session in milliseconds."""
    memory: StatsMemory
    """The memory stats of the session."""
    cpu: StatsCpu
    """The cpu stats of the session."""
    frame_statistics: t.Annotated[StatsFrameStatistics | None, pydantic.Field(default=None, alias="frameStats")]
    """The frame stats of the session."""


class WebsocketClosedEvent(OngakuEvent, PayloadBaseApp):
    """Websocket closed event.

    The event that is sent out, when a websocket closes.
    """

    _app: hikari.RESTAware

    guild_id: t.Annotated[hikari.Snowflake, pydantic.Field(alias="guildId")]
    """The guild that had their websocket closed in."""
    code: int
    """The discord error code that [discord](https://discord.com/developers/docs/topics/opcodes-and-status-codes#voice-voice-close-event-codes) responded with."""
    reason: str
    """	The close reason."""
    by_remote: t.Annotated[bool, pydantic.Field(alias="byRemote")]
    """Whether the connection was closed by Discord."""

    



class TrackBase(OngakuEvent, PayloadBaseApp):
    """Base track class.

    The class that all Track based classes, inherit.
    """

    guild_id: t.Annotated[hikari.Snowflake, pydantic.Field(alias="guildId")]
    """The guild the track is playing in."""
    track: Track
    """The track that the event is attached too."""




class TrackStartEvent(TrackBase, OngakuEvent):
    """Track start event.

    The track start event that is dispatched when a track starts on a player.
    """


class TrackEndEvent(TrackBase, OngakuEvent):
    """Track end event.

    The track end event that is dispatched when a track ends.
    """

    reason: enums.TrackEndReasonType
    """The reason for the track ending."""



class TrackExceptionEvent(TrackBase, OngakuEvent):
    """Track exception event.

    This event is dispatched when a track gets stuck.
    """

    exception: ExceptionError
    """The exception error that was returned."""



class TrackStuckEvent(TrackBase, OngakuEvent):
    """Track stuck event.

    This event is dispatched when a track gets stuck.
    """

    threshold_ms: t.Annotated[int, pydantic.Field(alias="thresholdMs")]
    """The threshold in milliseconds that was exceeded."""



class PlayerBase(OngakuEvent, PayloadBaseApp):
    """Player base.

    This is the base player object for all Ongaku player events.
    """

    guild_id: t.Annotated[hikari.Snowflake, pydantic.Field(alias="guildId")]
    """The guild id of the player."""



class QueueEmptyEvent(PlayerBase, OngakuEvent):
    """Queue empty event.

    This event is dispatched when the player queue is empty, and no more songs are available.
    """



class QueueNextEvent(PlayerBase, OngakuEvent):
    """Queue next event.

    The event that is dispatched, when a new song is played in a player, from the queue.
    """

    track: Track
    """The track that is now playing."""
    old_track:  t.Annotated[Track, pydantic.Field(alias="oldTrack")]
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
