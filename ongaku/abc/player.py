import abc
from . import track
import hikari
import typing as t

class State(abc.ABC):
    """
    The player state.
    """

    _time: int
    _position: int
    _connected: bool
    _ping: int

    @property
    def time(self) -> int:
        return self._time

    @property
    def position(self) -> int:
        return self._position

    @property
    def connected(self) -> bool:
        return self._connected

    @property
    def ping(self) -> int:
        return self._ping

class Voice:
    """
    The voice connection data.
    """
    _token: str
    _endpoint: str
    _session_id: str

    @property
    def token(self) -> str:
        return self._token

    @property
    def endpoint(self) -> str:
        return self._endpoint

    @property
    def session_id(self) -> str:
        return self._session_id


class Player(abc.ABC):
    """
    The player data returned from lavalink.
    """

    def __init__(self, payload: dict[t.Any, t.Any]) -> None:
        self._guild_id = payload["guildId"]
        self._track = track.Track(payload)

    _guild_id: hikari.Snowflake
    _track: t.Optional[track.Track]
    _volume: int
    _paused: bool
    _state: State
    _voice: Voice

    @property
    def guild_id(self) -> hikari.Snowflake:
        return self._guild_id

    @property
    def track(self) -> t.Optional[track.Track]:
        return self._track

    @property
    def volume(self) -> int:
        return self._volume

    @property
    def paused(self) -> bool:
        return self._paused

    @property
    def state(self) -> State:
        return self._state

    @property
    def voice(self) -> Voice:
        return self._voice
    
