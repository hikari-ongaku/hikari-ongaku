import dataclasses
import typing as t

import hikari

from .track import Track


@dataclasses.dataclass
class PlayerState:
    """
    Player State

    All of the Player State information.

    Find out more [here](https://lavalink.dev/api/websocket.html#player-state).

    Parameters
    ----------
    time : int
        Unix timestamp in milliseconds
    position : int
        The position of the track in milliseconds
    connected : bool
        Whether Lavalink is connected to the voice gateway
    ping : int
        The ping of the node to the Discord voice server in milliseconds (-1 if not connected)
    """

    time: int
    position: int
    connected: bool
    ping: int

    @classmethod
    def as_payload(cls, payload: dict[t.Any, t.Any]):
        """
        Player State parser

        parse a payload of information, to receive a `PlayerState` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        PlayerState
            The Player State you parsed.
        """
        time = payload["time"]
        position = payload["position"]
        connected = payload["connected"]
        ping = payload["ping"]

        return cls(time, position, connected, ping)

    @property
    def raw(self) -> dict[str, t.Any]:
        return dataclasses.asdict(self)


@dataclasses.dataclass
class PlayerVoice:
    """
    Player Voice

    All of the Player Voice information.

    Find out more [here](https://lavalink.dev/api/rest.html#voice-state).

    Parameters
    ----------
    token : str
        The Discord voice token to authenticate with
    endpoint : str
        The Discord voice endpoint to connect to
    session_id : str
        The Discord voice session id to authenticate with
    """

    token: str
    endpoint: str
    session_id: str

    @classmethod
    def as_payload(cls, payload: dict[t.Any, t.Any]):
        """
        Player Voice parser

        parse a payload of information, to receive a `PlayerVoice` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        PlayerVoice
            The Player Voice you parsed.
        """
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
    Player Voice

    All of the Player Voice information.

    Find out more [here](https://lavalink.dev/api/rest.html#player).

    Parameters
    ----------
    guild_id : hikari.Snowflake
        The guild id this player is currently in.
    track : abc.Track | None
        The track the player is currently playing. None means its not currently playing any track.
    volume : int
        The volume of the player.
    paused : int
        Whether the player is paused or not.
    state : PlayerState
        The `PlayerState` object
    voice : PlayerVoice
        The `PlayerVoice` object
    """

    guild_id: hikari.Snowflake
    track: t.Optional[Track]
    volume: int
    paused: bool
    state: PlayerState
    voice: PlayerVoice
    filters: dict[t.Any, t.Any] | None = None

    @classmethod
    def as_payload(cls, payload: dict[t.Any, t.Any]):
        """
        Player parser

        parse a payload of information, to receive a `Player` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        Player
            The Player you parsed.
        """
        guild_id = hikari.Snowflake(payload["guildId"])
        try:
            track = Track.as_payload(payload["track"])
        except Exception:
            track = None
        volume = payload["volume"]
        paused = payload["paused"]
        state = PlayerState.as_payload(payload["state"])
        voice = PlayerVoice.as_payload(payload["voice"])
        filters = payload["filters"]

        return cls(guild_id, track, volume, paused, state, voice, filters)

    @property
    def raw(self) -> dict[str, t.Any]:
        return dataclasses.asdict(self)
