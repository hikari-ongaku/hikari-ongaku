import dataclasses
import typing as t

import hikari

from .. import enums
from .lavalink import ExceptionError
from .track import Track


class OngakuEvent(hikari.Event):
    """
    The base Ongaku events.
    """


@dataclasses.dataclass
class ReadyEvent(OngakuEvent):
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
    def as_payload(cls, app: hikari.RESTAware, payload: dict[t.Any, t.Any]):
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
        resumed = payload["resumed"]
        session_id = payload["sessionId"]

        return cls(app, resumed, session_id)


@dataclasses.dataclass
class StatsMemory:
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
    def as_payload(cls, payload: dict[t.Any, t.Any]):
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
        free = payload["free"]
        used = payload["used"]
        allocated = payload["allocated"]
        reservable = payload["reservable"]

        return cls(free, used, allocated, reservable)


@dataclasses.dataclass
class StatsCpu:
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
    def as_payload(cls, payload: dict[t.Any, t.Any]):
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
        cores = payload["cores"]
        system_load = payload["systemLoad"]
        lavalink_load = payload["lavalinkLoad"]

        return cls(cores, system_load, lavalink_load)


@dataclasses.dataclass
class StatsFrameStatistics:
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
    def as_payload(cls, payload: dict[t.Any, t.Any]):
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
        sent = payload["sent"]
        nulled = payload["nulled"]
        deficit = payload["deficit"]

        return cls(sent, nulled, deficit)


@dataclasses.dataclass
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
    memory: StatsMemory
    cpu: StatsCpu
    frame_statistics: t.Optional[StatsFrameStatistics]

    @property
    def app(self) -> hikari.RESTAware:
        return self._app

    @classmethod
    def as_payload(cls, app: hikari.RESTAware, payload: dict[t.Any, t.Any]):
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
        memory = StatsMemory.as_payload(payload["memory"])
        cpu = StatsCpu.as_payload(payload["cpu"])
        frame_statistics = None
        if payload.get("frameStats", None) is not None:
            try:
                frame_statistics = StatsFrameStatistics.as_payload(
                    payload["frameStats"]
                )
            except Exception:
                frame_statistics = None

        return cls(app, players, playing_players, uptime, memory, cpu, frame_statistics)


@dataclasses.dataclass
class WebsocketClosedEvent(OngakuEvent):
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
    def as_payload(cls, app: hikari.RESTAware, payload: dict[t.Any, t.Any]):
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
        guild_id = payload["guildId"]
        code = payload["code"]
        reason = payload["reason"]
        by_remote = payload["byRemote"]

        return cls(app, guild_id, code, reason, by_remote)


# Track Events:


@dataclasses.dataclass
class TrackBase:
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
    def as_payload(cls, app: hikari.RESTAware, payload: dict[t.Any, t.Any]):
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
        track = Track.as_payload(payload["track"])
        guild_id = hikari.Snowflake(payload["guildId"])

        return cls(app, track, guild_id)


@dataclasses.dataclass
class TrackStartEvent(TrackBase, OngakuEvent):
    """
    Gotta do the docs for me
    """

    @classmethod
    def as_payload(cls, app: hikari.RESTAware, payload: dict[t.Any, t.Any]):
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
        base = TrackBase.as_payload(app, payload)

        return cls(base.app, base.track, base.guild_id)


@dataclasses.dataclass
class TrackEndEvent(TrackBase, OngakuEvent):
    """
    Gotta do the docs for me
    """

    reason: enums.TrackEndReasonType

    @classmethod
    def as_payload(cls, app: hikari.RESTAware, payload: dict[t.Any, t.Any]):
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
        base = TrackBase.as_payload(app, payload)
        reason = enums.TrackEndReasonType(payload["reason"])

        return cls(base.app, base.track, base.guild_id, reason)


@dataclasses.dataclass
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
    threshold_ms : int
        The threshold in milliseconds that was exceeded.
    """

    exception: ExceptionError

    @classmethod
    def as_payload(cls, app: hikari.RESTAware, payload: dict[t.Any, t.Any]):
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
        track = Track.as_payload(payload["track"])
        guild_id = hikari.Snowflake(payload["guildId"])
        reason = ExceptionError.as_payload(payload["exception"])

        return cls(app, track, guild_id, reason)


@dataclasses.dataclass
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
    def as_payload(cls, app: hikari.RESTAware, payload: dict[t.Any, t.Any]):
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
        base = TrackBase.as_payload(app, payload)
        threshold_ms = payload["thresholdMs"]

        return cls(base.app, base.track, base.guild_id, threshold_ms)


# Player Events:


@dataclasses.dataclass
class PlayerBase:
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
    def as_payload(cls, app: hikari.RESTAware, payload: dict[t.Any, t.Any]):
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
        guild_id = hikari.Snowflake(payload["guildId"])

        return cls(app, guild_id)


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
    def as_payload(cls, app: hikari.RESTAware, payload: dict[t.Any, t.Any]):
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
        base = PlayerBase.as_payload(app, payload)

        return cls(base.app, base.guild_id)