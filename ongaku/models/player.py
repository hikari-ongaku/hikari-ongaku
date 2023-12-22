from . import track
import hikari

import typing as t


class State:
    """
    The player state.
    """

    def __init__(self, data: dict) -> None:
        self._time = data["time"]
        self._position = data["position"]
        self._connected = data["connected"]
        self._ping = data["ping"]

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

    def __init__(self, data: dict) -> None:
        self._raw = data
        self._token = data["token"]
        self._endpoint = data["endpoint"]
        self._session_id = data["sessionId"]

    @property
    def token(self) -> str:
        return self._token

    @property
    def endpoint(self) -> str:
        return self._endpoint

    @property
    def session_id(self) -> str:
        return self._session_id

    @property
    def raw(self) -> dict:
        return self._raw


class Player:
    """
    The player data returned from lavalink.
    """

    def __init__(self, data: dict) -> None:
        self._guild_id = data["guildId"]
        try:
            self._track = track.Track(data["track"])
        except:
            self._track = None

        self._volume = data["volume"]
        self._paused = data["paused"]
        try:
            self._state = State(data["state"])
        except Exception as e:
            raise e

        try:
            self._voice = Voice(data["voice"])
        except Exception as e:
            raise e

    @property
    def guild_id(self) -> hikari.Snowflake:
        return self._guild_id

    @property
    def track(self) -> t.Optional[track.Track]:
        return self._track

    @property
    def volume(self) -> float:
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
