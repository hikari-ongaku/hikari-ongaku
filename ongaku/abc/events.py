import abc
import hikari
from . import track
from .. import enums
import typing as t
import dataclasses


class OngakuEvent(hikari.Event, abc.ABC):
    """
    The base Ongaku events.
    """


class Ready(abc.ABC):
    """
    Gotta do the docs for me
    """

    def __init__(self, app: hikari.RESTAware, resumed: bool, session_id: str) -> None:
        self._app = app
        self._resumed = resumed
        self._session_id = session_id

    @classmethod
    def from_payload(cls, app: hikari.RESTAware, payload: dict[t.Any, t.Any]):
        resumed = payload["resumed"]
        session_id = payload["sessionId"]

        return cls(app, resumed, session_id)

    @property
    def app(self) -> hikari.RESTAware:
        return self._app

    @property
    def resumed(self) -> bool:
        return self._resumed

    @property
    def session_id(self) -> str:
        return self._session_id


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
class Statistics(abc.ABC):
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

    players: int
    playing_players: int
    uptime: int
    memory: StatsMemory
    cpu: StatsCpu
    frame_statistics: t.Optional[StatsFrameStatistics]

    @classmethod
    def as_payload(cls, payload: dict[t.Any, t.Any]):
        players = payload["players"]
        playing_players = payload["playingPlayers"]
        uptime = payload["uptime"]
        memory = StatsMemory.as_payload(payload["memory"])
        cpu = StatsCpu.as_payload(payload["cpu"])
        frame_statistics = None
        if payload.get("frameStats", None) != None:
            try:
                frame_statistics = StatsFrameStatistics.as_payload(
                    payload["frameStats"]
                )
            except:
                frame_statistics = None

        return cls(players, playing_players, uptime, memory, cpu, frame_statistics)

    @property
    def raw(self) -> dict[str, t.Any]:
        return dataclasses.asdict(self)


class WebsocketClosed(abc.ABC):
    """
    Gotta do the docs for me
    """

    @property
    @abc.abstractmethod
    def app(self) -> hikari.RESTAware:
        ...

    @property
    @abc.abstractmethod
    def code(self) -> int:
        ...

    @property
    @abc.abstractmethod
    def reason(self) -> str:
        ...

    @property
    @abc.abstractmethod
    def by_remote(self) -> bool:
        ...

    @property
    @abc.abstractmethod
    def guild_id(self) -> int:
        ...


# Track Events:


class TrackBase(abc.ABC):
    """
    Gotta do the docs for me
    """

    @property
    @abc.abstractmethod
    def app(self) -> hikari.RESTAware:
        ...

    @property
    @abc.abstractmethod
    def track(self) -> track.Track:
        ...

    @property
    @abc.abstractmethod
    def guild_id(self) -> int:
        ...


class TrackStart(TrackBase, abc.ABC):
    """
    Gotta do the docs for me
    """


class TrackEnd(TrackBase, abc.ABC):
    """
    Gotta do the docs for me
    """

    @property
    @abc.abstractmethod
    def reason(self) -> enums.TrackEndReasonType:
        ...


class TrackExceptionReason(abc.ABC):
    """
    Gotta do the docs for me
    """

    @property
    def message(self) -> str:
        ...

    @property
    def severity(self) -> enums.LavalinkSeverityType:
        ...

    @property
    def cause(self) -> str:
        ...


class TrackException(TrackBase, abc.ABC):
    """
    Gotta do the docs for me
    """

    @property
    @abc.abstractmethod
    def reason(self) -> TrackExceptionReason:
        ...


class TrackStuck(TrackBase, abc.ABC):
    """
    Gotta do the docs for me
    """

    @property
    @abc.abstractmethod
    def threshold_ms(self) -> int:
        ...


# Player Events:


class PlayerBase(abc.ABC):
    """
    Gotta do the docs for me
    """

    @property
    @abc.abstractmethod
    def app(self) -> hikari.RESTAware:
        ...

    @property
    @abc.abstractmethod
    def guild_id(self) -> int:
        ...


class PlayerQueueEmpty(PlayerBase, abc.ABC):
    """
    Gotta do the docs for me
    """
