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


# Main Events:


class Ready(abc.ABC):
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
class Memory:
    free: int
    used: int
    allocated: int
    reservable: int
        

    @classmethod
    def as_payload(cls, payload: dict[t.Any, t.Any]):
        free = payload["free"]
        used = payload["used"]
        allocated = payload["allocated"]
        reservable = payload["reservable"]

        return cls(free, used, allocated, reservable)

    @property
    def raw(self) -> dict[str, t.Any]:
        return dataclasses.asdict(self)

@dataclasses.dataclass
class Cpu:
    cores: int
    system_load: float
    lavalink_load: float

    @classmethod
    def as_payload(cls, payload: dict[t.Any, t.Any]):
        cores = payload["cores"]
        system_load = payload["systemLoad"]
        lavalink_load = payload["lavalinkLoad"]

        return cls(cores, system_load, lavalink_load)

    @property
    def raw(self) -> dict[str, t.Any]:
        return dataclasses.asdict(self)

@dataclasses.dataclass
class FrameStatistics:
    sent: int
    nulled: int
    deficit: int

    @classmethod
    def as_payload(cls, payload: dict[t.Any, t.Any]):
        sent = payload["sent"]
        nulled = payload["nulled"]
        deficit = payload["deficit"]

        return cls(sent, nulled, deficit)

@dataclasses.dataclass
class Statistics(abc.ABC):
    players: int
    playing_players: int
    uptime: int
    memory: t.Optional[Memory]
    cpu: t.Optional[Cpu]
    try:
        frame_statistics: t.Optional[FrameStatistics]
    except:
        frame_statistics = None

    @classmethod
    def as_payload(cls, payload: dict[t.Any, t.Any]):
        players = payload["players"]
        playing_players = payload["playingPlayers"]
        uptime = payload["uptime"]
        try:
            memory = Memory.as_payload(payload["memory"])
        except:
            memory = None
        try:
            cpu = Cpu.as_payload(payload["cpu"])
        except:
            cpu = None
        try:
            frame_statistics = FrameStatistics.as_payload(payload["frameStatistics"])
        except:
            frame_statistics = None

        return cls(players, playing_players, uptime, memory, cpu, frame_statistics)

    @property
    def raw(self) -> dict[str, t.Any]:
        return dataclasses.asdict(self)


class WebsocketClosed(abc.ABC):
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
    Base Track Start event.
    """


class TrackEnd(TrackBase, abc.ABC):
    @property
    @abc.abstractmethod
    def reason(self) -> enums.TrackEndReasonType:
        ...


class TrackExceptionReason(abc.ABC):
    @property
    def message(self) -> str:
        ...

    @property
    def severity(self) -> enums.TrackSeverityType:
        ...

    @property
    def cause(self) -> str:
        ...


class TrackException(TrackBase, abc.ABC):
    @property
    @abc.abstractmethod
    def reason(self) -> TrackExceptionReason:
        ...


class TrackStuck(TrackBase, abc.ABC):
    @property
    @abc.abstractmethod
    def threshold_ms(self) -> int:
        ...


# Player Events:


class PlayerBase(abc.ABC):
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
    When the player queue is empty, this is called.
    """
