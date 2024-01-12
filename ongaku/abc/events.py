from __future__ import annotations

import attrs
import typing as t

import hikari

from .. import enums
from .lavalink import ExceptionError
from .track import Track
from .base import PayloadBaseApp, PayloadBase

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
    "PlayerQueueEmptyEvent",
)

@attrs.define
class OngakuEvent(hikari.Event):
    """
    Ongaku Event

    The base event, that all events are attached too.

    Parameters
    ----------
    _app : hikari.RESTAware
        The application, or bot, that ongaku is running on.
    """

    _app: hikari.RESTAware
    """THIS APP POO"""

    @property
    def app(self) -> hikari.RESTAware:
        return self._app


@attrs.define
class ReadyEvent(OngakuEvent, PayloadBaseApp[dict[str, t.Any]]):
    """
    Ready Event

    The event that is dispatched, when lavalink is ready for discord connections.

    Parameters
    ----------
    _app : hikari.RESTAware
        The application, or bot, that ongaku is running on.
    resumed : bool
        Whether or not the session has been resumed, or is a new session.
    session_id : str
        The lavalink session id, for the current session.
    """

    resumed: bool
    session_id: str

    @classmethod
    def _from_payload(cls, payload: dict[str, t.Any], *, app: hikari.RESTAware) -> ReadyEvent:
        resumed = payload["resumed"]
        session_id = payload["sessionId"]

        return cls(app, resumed, session_id)


@attrs.define
class StatsMemory(PayloadBase[dict[str, t.Any]]):
    """
    All of the Statistics Memory information.

    Find out more [here](https://lavalink.dev/api/websocket.html#memory).

    Parameters
    ----------
    free : int
        The amount of free memory in bytes
    used : int
        The amount of used memory in bytes
    allocated : int
        The amount of allocated memory in bytes
    reservable : int
        The amount of reservable memory in bytes
    """

    free: int
    used: int
    allocated: int
    reservable: int

    @classmethod
    def _from_payload(cls, payload: dict[str, t.Any]) -> StatsMemory:
        free = payload["free"]
        used = payload["used"]
        allocated = payload["allocated"]
        reservable = payload["reservable"]

        return cls(free, used, allocated, reservable)


@attrs.define
class StatsCpu(PayloadBase[dict[str, t.Any]]):
    """
    All of the Statistics CPU information.

    Find out more [here](https://lavalink.dev/api/websocket.html#cpu).

    Parameters
    ----------
    cores : int
        The amount of cores the node has
    system_load : float
        The system load of the node
    lavalink_load : float
        The load of Lavalink on the node
    """

    cores: int
    system_load: float
    lavalink_load: float

    @classmethod
    def _from_payload(cls, payload: dict[str, t.Any]) -> StatsCpu:
        cores = payload["cores"]
        system_load = payload["systemLoad"]
        lavalink_load = payload["lavalinkLoad"]

        return cls(cores, system_load, lavalink_load)


@attrs.define
class StatsFrameStatistics(PayloadBase[dict[str, t.Any]]):
    """
    All of the Statistics frame statistics information.

    Find out more [here](https://lavalink.dev/api/websocket.html#frame-stats).

    Parameters
    ----------
    sent : int
        The amount of frames sent to Discord
    nulled : int
        The amount of frames that were nulled
    deficit : int
        The difference between sent frames and the expected amount of frames
    """

    sent: int
    nulled: int
    deficit: int

    @classmethod
    def _from_payload(cls, payload: dict[str, t.Any]) -> StatsFrameStatistics:
        sent = payload["sent"]
        nulled = payload["nulled"]
        deficit = payload["deficit"]

        return cls(sent, nulled, deficit)


@attrs.define
class StatisticsEvent(OngakuEvent, PayloadBaseApp[dict[str, t.Any]]):
    """
    All of the Statistics information.

    Find out more [here](https://lavalink.dev/api/websocket.html#stats-object).

    Parameters
    ----------
    players : int
        The amount of players connected to the node
    playing_players : int
        The amount of players playing a track
    uptime : int
        The uptime of the node in milliseconds
    memory : StatsMemory | None
        The memory stats of the node
    cpu : StatsCpu | None
        The cpu stats of the node
    frame_statistics : StatsFrameStatistics | None
        The frame stats of the node.
    """

    _app: hikari.RESTAware
    players: int
    playing_players: int
    uptime: int
    memory: StatsMemory
    cpu: StatsCpu
    frame_statistics: t.Optional[StatsFrameStatistics]

    @classmethod
    def _from_payload(cls, payload: dict[str, t.Any], *, app: hikari.RESTAware):
        players = payload["players"]
        playing_players = payload["playingPlayers"]
        uptime = payload["uptime"]
        memory = StatsMemory._from_payload(payload["memory"])
        cpu = StatsCpu._from_payload(payload["cpu"])
        frame_statistics = None
        if payload.get("frameStats", None) is not None:
            try:
                frame_statistics = StatsFrameStatistics._from_payload(
                    payload["frameStats"]
                )
            except Exception:
                frame_statistics = None

        return cls(app, players, playing_players, uptime, memory, cpu, frame_statistics)


@attrs.define
class WebsocketClosedEvent(OngakuEvent, PayloadBaseApp[dict[str, t.Any]]):
    """
    Gotta do the docs for me
    """

    _app: hikari.RESTAware
    guild_id: hikari.Snowflake
    code: int
    reason: str
    by_remote: bool

    @classmethod
    def _from_payload(
        cls, payload: dict[str, t.Any], *, app: hikari.RESTAware
    ) -> WebsocketClosedEvent:
        guild_id = payload["guildId"]
        code = payload["code"]
        reason = payload["reason"]
        by_remote = payload["byRemote"]

        return cls(app, guild_id, code, reason, by_remote)


# Track Events:


@attrs.define
class TrackBase(OngakuEvent, PayloadBaseApp[dict[str, t.Any]]):
    """
    Base track class

    The class that all tracks inherit.

    Parameters
    ----------
    _app : hikari.RESTAware
        The app or bot, that the event is attached to.
    track : Track
        The track that the event is attached too.
    guild_id : hikari.Snowflake
        The guild the track is playing in.
    """

    track: Track
    guild_id: hikari.Snowflake

    @classmethod
    def _from_payload(cls, payload: dict[str, t.Any], *, app: hikari.RESTAware):
        track = Track._from_payload(payload["track"])
        guild_id = hikari.Snowflake(payload["guildId"])

        return cls(app, track, guild_id)


@attrs.define
class TrackStartEvent(TrackBase, OngakuEvent):
    """
    Track Start Event

    The track start event that is dispatched when a track starts.

    Parameters
    ----------
    _app : hikari.RESTAware
        The application, or bot that the event was dispatched on.
    track : Track
        The track that the player got stuck on.
    guild_id : hikari.Snowflake
        The guild id of the player, where the track got stuck on.
    """

    @classmethod
    def _from_payload(cls, payload: dict[str, t.Any], *, app: hikari.RESTAware) -> TrackStartEvent:
        base = TrackBase._from_payload(payload, app=app)

        return cls(base.app, base.track, base.guild_id)


@attrs.define
class TrackEndEvent(TrackBase, OngakuEvent):
    """
    Track End Event

    The track end event that is dispatched when a track ends.

    Parameters
    ----------
    _app : hikari.RESTAware
        The application, or bot that the event was dispatched on.
    track : Track
        The track that the player got stuck on.
    guild_id : hikari.Snowflake
        The guild id of the player, where the track got stuck on.
    reason : enums.TrackEndReasonType
        The reason for the track ending.
    """

    reason: enums.TrackEndReasonType

    @classmethod
    def _from_payload(cls, payload: dict[str, t.Any], *, app: hikari.RESTAware):
        base = TrackBase._from_payload(payload, app=app)
        reason = enums.TrackEndReasonType(payload["reason"])

        return cls(base.app, base.track, base.guild_id, reason)


@attrs.define
class TrackExceptionEvent(TrackBase, OngakuEvent):
    """
    Track Stuck Event

    This event is dispatched when a track gets stuck.

    Parameters
    ----------
    _app : hikari.RESTAware
        The application, or bot that the event was dispatched on.
    track : Track
        The track that the player got stuck on.
    guild_id : hikari.Snowflake
        The guild id of the player, where the track got stuck on.
    exception : ExceptionError
        The exception error that was raised.
    """

    exception: ExceptionError

    @classmethod
    def _from_payload(cls, payload: dict[str, t.Any], *, app: hikari.RESTAware):
        track = Track._from_payload(payload["track"])
        guild_id = hikari.Snowflake(payload["guildId"])
        reason = ExceptionError._from_payload(payload["exception"])

        return cls(app, track, guild_id, reason)


@attrs.define
class TrackStuckEvent(TrackBase, OngakuEvent):
    """
    Track Stuck Event

    This event is dispatched when a track gets stuck.

    Parameters
    ----------
    _app : hikari.RESTAware
        The application, or bot that the event was dispatched on.
    track : Track
        The track that the player got stuck on.
    guild_id : hikari.Snowflake
        The guild id of the player, where the track got stuck on.
    threshold_ms : int
        The threshold in milliseconds that was exceeded.
    """

    threshold_ms: int

    @classmethod
    def _from_payload(cls, payload: dict[str, t.Any], *, app: hikari.RESTAware):
        base = TrackBase._from_payload(payload, app=app)
        threshold_ms = payload["thresholdMs"]

        return cls(base.app, base.track, base.guild_id, threshold_ms)


# Player Events:


@attrs.define
class PlayerBase(OngakuEvent, PayloadBaseApp[dict[str, t.Any]]):
    """
    Player Base

    This is the base player object for player events.

    Parameters
    ----------
    _app : hikari.RESTAware
        The application, or bot that the event was dispatched on.
    guild_id : hikari.Snowflake
        The guild id that ran out of tracks.
    """

    guild_id: hikari.Snowflake

    @classmethod
    def _from_payload(
        cls, payload: dict[str, t.Any], *, app: hikari.RESTAware
    ) -> PlayerBase:
        guild_id = hikari.Snowflake(payload["guildId"])

        return cls(app, guild_id)


@attrs.define
class PlayerQueueEmptyEvent(PlayerBase, OngakuEvent):
    """
    Player Queue Empty Event

    This event is dispatched when the player queue is empty, and no more songs are available.

    Parameters
    ----------
    _app : hikari.RESTAware
        The application, or bot that the event was dispatched on.
    guild_id : hikari.Snowflake
        The guild id that ran out of tracks.
    """

    @classmethod
    def _from_payload(cls, payload: dict[str, t.Any], *, app: hikari.RESTAware):
        base = PlayerBase._from_payload(payload, app=app)

        return cls(base.app, base.guild_id)


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
