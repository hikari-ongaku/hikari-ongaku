from __future__ import annotations

import attrs
import typing as t

import hikari

from .. import enums
from .lavalink import ExceptionError
from .track import Track
from .base import PayloadBaseApp, PayloadBase, PayloadT

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
    "PlayerQueueEmptyEvent"
)

class OngakuEvent(hikari.Event):
    """
    The base Ongaku events.
    """


@attrs.define
class ReadyEvent(OngakuEvent, PayloadBaseApp[PayloadT]):
    """
    Gotta do the docs for me
    """

    _app: hikari.RESTAware
    resumed: bool
    session_id: str

    @property
    def app(self) -> hikari.RESTAware:
        return self._app

    @classmethod
    def from_payload(cls, payload:  PayloadT, *, app: hikari.RESTAware) -> ReadyEvent[PayloadT]:
        """
        Ready Event parser

        parse a payload of information, to receive a [ReadyEvent][ongaku.abc.events.ReadyEvent] dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        ReadyEvent
            The [ReadyEvent][ongaku.abc.events.ReadyEvent] payload you parsed.
        """
        if isinstance(payload, list):
            raise TypeError("Payload is of wrong expected type.")

        resumed = payload["resumed"]
        session_id = payload["sessionId"]

        return cls(app, resumed, session_id)


@attrs.define
class StatsMemory(PayloadBase[PayloadT]):
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
    def from_payload(cls, payload: PayloadT) -> StatsMemory[PayloadT]:
        """
        Statistics Event, Memory parser

        parse a payload of information, to receive a [StatsMemory][ongaku.abc.events.StatsMemory] dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        StatsMemory
            The [StatsMemory][ongaku.abc.events.StatsMemory] payload you parsed.
        """

        if isinstance(payload, list):
            raise TypeError(f"Payload is of wrong expected type. {type(payload)}")
        
        free = payload["free"]
        used = payload["used"]
        allocated = payload["allocated"]
        reservable = payload["reservable"]

        return cls(free, used, allocated, reservable)


@attrs.define
class StatsCpu(PayloadBase[PayloadT]):
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
    def from_payload(cls, payload: PayloadT) -> StatsCpu[PayloadT]:
        """
        Statistics Event, CPU parser

        parse a payload of information, to receive a [StatsCpu][ongaku.abc.events.StatsCpu] dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        StatsCpu
            The [StatsCpu][ongaku.abc.events.StatsCpu] payload you parsed.
        """

        if isinstance(payload, list):
            raise TypeError(f"Payload is of wrong expected type. {type(payload)}")

        cores = payload["cores"]
        system_load = payload["systemLoad"]
        lavalink_load = payload["lavalinkLoad"]

        return cls(cores, system_load, lavalink_load)


@attrs.define
class StatsFrameStatistics(PayloadBase[PayloadT]):
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
    def from_payload(cls, payload: PayloadT) -> StatsFrameStatistics[PayloadT]:
        """
        Statistics Event, Frame Statistics parser

        parse a payload of information, to receive a [StatsFrameStatistics][ongaku.abc.events.StatsFrameStatistics] dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        StatsFrameStatistics
            The [StatsFrameStatistics][ongaku.abc.events.StatsFrameStatistics] payload you parsed.
        """

        if isinstance(payload, list):
            raise TypeError(f"Payload is of wrong expected type. {type(payload)}")
        
        sent = payload["sent"]
        nulled = payload["nulled"]
        deficit = payload["deficit"]

        return cls(sent, nulled, deficit)


@attrs.define
class StatisticsEvent(OngakuEvent):
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
    memory: StatsMemory[t.Any]
    cpu: StatsCpu[t.Any]
    frame_statistics: t.Optional[StatsFrameStatistics[t.Any]]

    @property
    def app(self) -> hikari.RESTAware:
        return self._app

    @classmethod
    def from_payload(cls, payload: dict[str, t.Any], *, app: hikari.RESTAware):
        """
        Statistics Event parser

        parse a payload of information, to receive a [StatisticsEvent][ongaku.abc.events.StatisticsEvent] dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        StatisticsEvent
            The [StatisticsEvent][ongaku.abc.events.StatisticsEvent] payload you parsed.
        """
        players = payload["players"]
        playing_players = payload["playingPlayers"]
        uptime = payload["uptime"]
        memory = StatsMemory.from_payload(payload["memory"])
        cpu = StatsCpu.from_payload(payload["cpu"])
        frame_statistics = None
        if payload.get("frameStats", None) is not None:
            try:
                frame_statistics = StatsFrameStatistics.from_payload(
                    payload["frameStats"]
                )
            except Exception:
                frame_statistics = None

        return cls(app, players, playing_players, uptime, memory, cpu, frame_statistics)


@attrs.define
class WebsocketClosedEvent(OngakuEvent, PayloadBaseApp[PayloadT]):
    """
    Gotta do the docs for me
    """

    _app: hikari.RESTAware
    guild_id: hikari.Snowflake
    code: int
    reason: str
    by_remote: bool

    @property
    def app(self) -> hikari.RESTAware:
        return self._app

    @classmethod
    def from_payload(cls, payload: PayloadT, *, app: hikari.RESTAware):
        """
        Websocket Closed Event parser

        parse a payload of information, to receive a [WebsocketClosedEvent][ongaku.abc.events.WebsocketClosedEvent] dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        WebsocketClosedEvent
            The [WebsocketClosedEvent][ongaku.abc.events.WebsocketClosedEvent] payload you parsed.
        """

        if isinstance(payload, list):
            raise TypeError(f"Payload is of wrong expected type. {type(payload)}")
        
        guild_id = payload["guildId"]
        code = payload["code"]
        reason = payload["reason"]
        by_remote = payload["byRemote"]

        return cls(app, guild_id, code, reason, by_remote)


# Track Events:


@attrs.define
class TrackBase(PayloadBaseApp[PayloadT]):
    """
    Base track class

    The class that all tracks inherit.

    Parameters
    ----------
    app : hikari.RESTAware
        The app or bot, that the event is attached to.
    track : Track
        The track that the event is attached too.
    guild_id : hikari.Snowflake
        The guild the track is playing in.
    """

    _app: hikari.RESTAware
    track: Track
    guild_id: hikari.Snowflake

    @property
    def app(self) -> hikari.RESTAware:
        return self._app

    @classmethod
    def from_payload(cls, payload: PayloadT, *, app: hikari.RESTAware):
        """
        Track Base parser

        parse a payload of information, to receive a [TrackBase][ongaku.abc.events.TrackBase] dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        TrackBase
            The [TrackBase][ongaku.abc.events.TrackBase] payload you parsed.
        """

        if isinstance(payload, list):
            raise TypeError(f"Payload is of wrong expected type. {type(payload)}")
        
        track = Track.from_payload(payload["track"])
        guild_id = hikari.Snowflake(payload["guildId"])

        return cls(app, track, guild_id)


@attrs.define
class TrackStartEvent(TrackBase[PayloadT], OngakuEvent):
    """
    Gotta do the docs for me
    """

    @classmethod
    def from_payload(cls, payload: PayloadT, *, app: hikari.RESTAware):
        """
        Track Start Event parser

        parse a payload of information, to receive a [TrackStartEvent][ongaku.abc.events.TrackStartEvent] dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        TrackStartEvent
            The [TrackStartEvent][ongaku.abc.events.TrackStartEvent] payload you parsed.
        """

        if isinstance(payload, list):
            raise TypeError(f"Payload is of wrong expected type. {type(payload)}")
        
        base = TrackBase.from_payload(payload, app=app)

        return cls(base.app, base.track, base.guild_id)


@attrs.define
class TrackEndEvent(TrackBase[PayloadT], OngakuEvent):
    """
    Gotta do the docs for me
    """

    reason: enums.TrackEndReasonType

    @classmethod
    def from_payload(cls, payload: PayloadT, *, app: hikari.RESTAware):
        """
        Track End Event parser

        parse a payload of information, to receive a [TrackEndEvent][ongaku.abc.events.TrackEndEvent] dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        TrackEndEvent
            The [TrackEndEvent][ongaku.abc.events.TrackEndEvent] payload you parsed.
        """

        if isinstance(payload, list):
            raise TypeError(f"Payload is of wrong expected type. {type(payload)}")
        
        base = TrackBase.from_payload(payload, app=app)
        reason = enums.TrackEndReasonType(payload["reason"])

        return cls(base.app, base.track, base.guild_id, reason)


@attrs.define
class TrackExceptionEvent(TrackBase[PayloadT], OngakuEvent):
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

    exception: ExceptionError

    @classmethod
    def from_payload(cls, payload: PayloadT, *, app: hikari.RESTAware):
        """
        Track Exception Event parser

        parse a payload of information, to receive a [TrackExceptionEvent][ongaku.abc.events.TrackExceptionEvent] dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        TrackExceptionEvent
            The [TrackExceptionEvent][ongaku.abc.events.TrackExceptionEvent] payload you parsed.
        """

        if isinstance(payload, list):
            raise TypeError(f"Payload is of wrong expected type. {type(payload)}")
        
        track = Track.from_payload(payload["track"])
        guild_id = hikari.Snowflake(payload["guildId"])
        reason = ExceptionError.from_payload(payload["exception"])

        return cls(app, track, guild_id, reason)


@attrs.define
class TrackStuckEvent(TrackBase[PayloadT], OngakuEvent):
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
    def from_payload(cls, payload: PayloadT, *, app: hikari.RESTAware):
        """
        Track Stuck Event parser

        parse a payload of information, to receive a [TrackStuckEvent][ongaku.abc.events.TrackStuckEvent] dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        TrackStuckEvent
            The [TrackStuckEvent][ongaku.abc.events.TrackStuckEvent] payload you parsed.
        """

        if isinstance(payload, list):
            raise TypeError(f"Payload is of wrong expected type. {type(payload)}")
        
        base = TrackBase.from_payload(payload, app=app)
        threshold_ms = payload["thresholdMs"]

        return cls(base.app, base.track, base.guild_id, threshold_ms)


# Player Events:


@attrs.define
class PlayerBase(PayloadBaseApp[PayloadT]):
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

    _app: hikari.RESTAware
    guild_id: hikari.Snowflake

    @property
    def app(self) -> hikari.RESTAware:
        return self._app

    @classmethod
    def from_payload(cls, payload: PayloadT, *, app: hikari.RESTAware):
        """
        Player Base parser

        parse a payload of information, to receive a [PlayerBase][ongaku.abc.events.PlayerBase] dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        PlayerBase
            The [PlayerBase][ongaku.abc.events.PlayerBase] payload you parsed.
        """

        if isinstance(payload, list):
            raise TypeError(f"Payload is of wrong expected type. {type(payload)}")
        
        guild_id = hikari.Snowflake(payload["guildId"])

        return cls(app, guild_id)


class PlayerQueueEmptyEvent(PlayerBase[PayloadT], OngakuEvent):
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
    def from_payload(cls, payload: PayloadT, *, app: hikari.RESTAware):
        """
        Player Queue parser

        parse a payload of information, to receive a [PlayerQueueEmptyEvent][ongaku.abc.events.PlayerQueueEmptyEvent] dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        PlayerQueueEmptyEvent
            The [PlayerQueueEmptyEvent][ongaku.abc.events.PlayerQueueEmptyEvent] payload you parsed.
        """

        if isinstance(payload, list):
            raise TypeError(f"Payload is of wrong expected type. {type(payload)}")
        
        base = PlayerBase.from_payload(payload, app=app)

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
