from .track import Track
import hikari
import typing as t
import dataclasses

@dataclasses.dataclass
class State:
    """
    The player state.
    """

    time: int
    position: int
    connected: bool
    ping: int

    @classmethod
    def as_payload(cls, payload: dict[t.Any, t.Any]):
        time = payload["time"]
        position = payload["position"]
        connected = payload["connected"]
        ping = payload["ping"]

        return cls(time, position, connected, ping)
    
    @property
    def raw(self) -> dict[str, t.Any]:
        return dataclasses.asdict(self)

@dataclasses.dataclass
class Voice:
    """
    The voice connection data.
    """

    token: str
    endpoint: str
    session_id: str

    @classmethod
    def as_payload(cls, payload: dict[t.Any, t.Any]):
        token = payload["token"]
        endpoint = payload["endpoint"]
        session_id = payload["sessionId"]

        return cls(token, endpoint, session_id)
    
    @property
    def raw(self) -> dict[str, t.Any]:
        return dataclasses.asdict(self)

@dataclasses.dataclass
class Player:
    """
    The player data returned from lavalink.
    """

    guild_id: hikari.Snowflake
    track: t.Optional[Track]
    volume: int
    paused: bool
    state: State
    voice: Voice

    @classmethod
    def as_payload(cls, payload: dict[t.Any, t.Any]):
        guild_id = payload["guildId"]
        try:
            track = Track.as_payload(payload["track"])
        except:
            track = None
        volume = payload["volume"]
        paused = payload["paused"]
        state = State.as_payload(payload["state"])
        voice = Voice.as_payload(payload["voice"])

        return cls(guild_id, track, volume, paused, state, voice)
    
    @property
    def raw(self) -> dict[str, t.Any]:
        return dataclasses.asdict(self)