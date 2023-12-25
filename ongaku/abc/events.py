import abc
import hikari
from . import track
from .. import enums
import typing as t


class OngakuEvent(hikari.Event, abc.ABC):
    """
    The base Ongaku events.
    """


# Main Events:


class Ready(abc.ABC):
    @property
    @abc.abstractmethod
    def app(self) -> hikari.RESTAware:
        ...

    @property
    @abc.abstractmethod
    def resumed(self) -> bool:
        ...

    @property
    @abc.abstractmethod
    def session_id(self) -> int:
        ...


class Memory(abc.ABC):
    @property
    @abc.abstractmethod
    def free(self) -> int:
        ...

    @property
    @abc.abstractmethod
    def used(self) -> int:
        ...

    @property
    @abc.abstractmethod
    def allocated(self) -> int:
        ...

    @property
    @abc.abstractmethod
    def reservable(self) -> int:
        ...


class Cpu(abc.ABC):
    @property
    @abc.abstractmethod
    def cores(self) -> int:
        ...

    @property
    @abc.abstractmethod
    def system_load(self) -> float:
        ...

    @property
    @abc.abstractmethod
    def lavalink_load(self) -> float:
        ...


class FrameStatistics(abc.ABC):
    @property
    @abc.abstractmethod
    def sent(self) -> int:
        ...

    @property
    @abc.abstractmethod
    def nulled(self) -> int:
        ...

    @property
    @abc.abstractmethod
    def deficit(self) -> int:
        ...


class Statistics(abc.ABC):
    @property
    @abc.abstractmethod
    def players(self) -> int:
        ...

    @property
    @abc.abstractmethod
    def playing_players(self) -> int:
        ...

    @property
    @abc.abstractmethod
    def uptime(self) -> int:
        ...

    @property
    @abc.abstractmethod
    def memory(self) -> t.Optional[Memory]:
        ...

    @property
    @abc.abstractmethod
    def cpu(self) -> t.Optional[Cpu]:
        ...

    @property
    @abc.abstractmethod
    def frame_statistics(self) -> t.Optional[FrameStatistics]:
        ...


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
