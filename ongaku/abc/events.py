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
        Stats Memory parser

        parse a payload of information, to receive a `StatsMemory` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        StatsMemory
            The Stats Memory you parsed.
        """
        free = payload["free"]
        used = payload["used"]
        allocated = payload["allocated"]
        reservable = payload["reservable"]

        return cls(free, used, allocated, reservable)

    @property
    def raw(self) -> dict[str, t.Any]:
        return dataclasses.asdict(self)


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
        Stats CPU parser

        parse a payload of information, to receive a `StatsCpu` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        StatsCpu
            The Stats Cpu you parsed.
        """
        cores = payload["cores"]
        system_load = payload["systemLoad"]
        lavalink_load = payload["lavalinkLoad"]

        return cls(cores, system_load, lavalink_load)

    @property
    def raw(self) -> dict[str, t.Any]:
        return dataclasses.asdict(self)


@dataclasses.dataclass
class StatsFrameStatistics:
    """
    All of the Statistics Memory information.

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
        Stats Frame Statistics parser

        parse a payload of information, to receive a `StatsFrameStatistics` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        StatsFrameStatistics
            The Stats Frame Statistics you parsed.
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

    @property
    def raw(self) -> dict[str, t.Any]:
        return dataclasses.asdict(self)


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
        Stats CPU parser

        parse a payload of information, to receive a `StatsCpu` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        StatsCpu
            The Stats Cpu you parsed.
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
        Stats CPU parser

        parse a payload of information, to receive a `StatsCpu` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        StatsCpu
            The Stats Cpu you parsed.
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
        Stats CPU parser

        parse a payload of information, to receive a `StatsCpu` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        StatsCpu
            The Stats Cpu you parsed.
        """
        base = TrackBase.as_payload(app, payload)
        reason = enums.TrackEndReasonType(payload["reason"])

        return cls(base.app, base.track, base.guild_id, reason)


@dataclasses.dataclass
class TrackExceptionEvent(TrackBase, OngakuEvent):
    """
    Gotta do the docs for me
    """

    exception: ExceptionError

    @classmethod
    def as_payload(cls, app: hikari.RESTAware, payload: dict[t.Any, t.Any]):
        """
        Stats CPU parser

        parse a payload of information, to receive a `StatsCpu` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        StatsCpu
            The Stats Cpu you parsed.
        """
        track = Track.as_payload(payload["track"])
        guild_id = hikari.Snowflake(payload["guildId"])
        reason = ExceptionError.as_payload(payload["exception"])

        return cls(app, track, guild_id, reason)


@dataclasses.dataclass
class TrackStuckEvent(TrackBase, OngakuEvent):
    """
    Gotta do the docs for me
    """

    threshold_ms: int

    @classmethod
    def as_payload(cls, app: hikari.RESTAware, payload: dict[t.Any, t.Any]):
        """
        Stats CPU parser

        parse a payload of information, to receive a `StatsCpu` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        StatsCpu
            The Stats Cpu you parsed.
        """
        base = TrackBase.as_payload(app, payload)
        threshold_ms = payload["thresholdMs"]

        return cls(base.app, base.track, base.guild_id, threshold_ms)


# Player Events:


@dataclasses.dataclass
class PlayerBase:
    """
    Gotta do the docs for me
    """

    _app: hikari.RESTAware
    guild_id: hikari.Snowflake

    @property
    def app(self) -> hikari.RESTAware:
        return self._app

    @classmethod
    def as_payload(cls, app: hikari.RESTAware, payload: dict[t.Any, t.Any]):
        """
        Stats CPU parser

        parse a payload of information, to receive a `StatsCpu` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        StatsCpu
            The Stats Cpu you parsed.
        """
        guild_id = hikari.Snowflake(payload["guildId"])

        return cls(app, guild_id)


class PlayerQueueEmptyEvent(PlayerBase, OngakuEvent):
    """
    Gotta do the docs for me
    """

    @classmethod
    def as_payload(cls, app: hikari.RESTAware, payload: dict[t.Any, t.Any]):
        """
        Stats CPU parser

        parse a payload of information, to receive a `StatsCpu` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        StatsCpu
            The Stats Cpu you parsed.
        """
        base = PlayerBase.as_payload(app, payload)

        return cls(base.app, base.guild_id)
