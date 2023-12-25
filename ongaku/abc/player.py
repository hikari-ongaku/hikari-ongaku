import abc
from . import track
import hikari
import typing as t

class State(abc.ABC):
    """
    The player state.
    """

    @property
    def time(self) -> int:
        ...

    @property
    def position(self) -> int:
        ...

    @property
    def connected(self) -> bool:
        ...

    @property
    def ping(self) -> int:
        ...


class Voice:
    """
    The voice connection data.
    """

    @property
    def token(self) -> str:
        ...

    @property
    def endpoint(self) -> str:
        ...

    @property
    def session_id(self) -> str:
        ...

    @property
    def raw(self) -> dict[t.Any, t.Any]:
        ...


class Player:
    """
    The player data returned from lavalink.
    """

    @property
    def guild_id(self) -> hikari.Snowflake:
        ...

    @property
    def track(self) -> t.Optional[track.Track]:
        ...

    @property
    def volume(self) -> float | int:
        ...

    @property
    def paused(self) -> bool:
        ...

    @property
    def state(self) -> State:
        ...

    @property
    def voice(self) -> Voice:
        ...
