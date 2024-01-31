"""# Player ABC's.

The player Abstract classes. [more here](https://ongaku.mplaty.com/api/abc/player)
"""

from __future__ import annotations

import typing as t

import attrs
import hikari

from .base import PayloadBase
from .track import Track

__all__ = (
    "PlayerState",
    "PlayerVoice",
    "Player",
)


@attrs.define
class PlayerState(PayloadBase[t.Mapping[str, t.Any]]):
    """Players State.

    All the information for the players current state.
    Find out more [here](https://lavalink.dev/api/websocket.html#player-state).
    """

    time: int
    """Unix timestamp in milliseconds."""
    position: int
    """The position of the track in milliseconds."""
    connected: bool
    """Whether Lavalink is connected to the voice gateway."""
    ping: int
    """The ping of the session to the Discord voice server in milliseconds (-1 if not connected)."""

    @classmethod
    def _from_payload(cls, payload: t.Mapping[str, t.Any]) -> PlayerState:
        time = payload.get("time")
        if time is None:
            raise ValueError("time cannot be none.")
        if not isinstance(time, int):
            raise TypeError("time must be a integer.")
        
        position = payload.get("position")
        if position is None:
            raise ValueError("position cannot be none.")
        if not isinstance(position, int):
            raise TypeError("position must be a integer.")
        
        connected = payload.get("connected")
        if connected is None:
            raise ValueError("connected cannot be none.")
        if not isinstance(connected, bool):
            raise TypeError("connected must be a integer.")
        
        ping = payload.get("ping")
        if ping is None:
            raise ValueError("ping cannot be none.")
        if not isinstance(ping, int):
            raise TypeError("ping must be a integer.")

        return cls(
            time, 
            position, 
            connected, 
            ping,
        )


@attrs.define
class PlayerVoice(PayloadBase[t.Mapping[str, t.Any]]):
    """Players Voice state.

    All of the Player Voice information.
    Find out more [here](https://lavalink.dev/api/rest.html#voice-state).
    """

    token: str
    """The Discord voice token to authenticate with."""
    endpoint: str
    """The Discord voice endpoint to connect to."""
    session_id: str
    """The Discord voice session id to authenticate with."""

    @classmethod
    def _from_payload(cls, payload: t.Mapping[str, t.Any]) -> PlayerVoice:
        token = payload.get("token")
        if token is None:
            raise ValueError("token cannot be none.")
        if not isinstance(token, str):
            raise TypeError("token must be a string.")
        
        endpoint = payload.get("endpoint")
        if endpoint is None:
            raise ValueError("endpoint cannot be none.")
        if not isinstance(endpoint, str):
            raise TypeError("endpoint must be a string.")
        
        session_id = payload.get("sessionId")
        if session_id is None:
            raise ValueError("sessionId cannot be none.")
        if not isinstance(session_id, str):
            raise TypeError("sessionId must be a string.")

        return cls(token, endpoint, session_id)


@attrs.define
class Player(PayloadBase[dict[str, t.Any]]):
    """Player information.

    All of the information about the player, for the specified guild.

    Find out more [here](https://lavalink.dev/api/rest.html#player).
    """

    guild_id: hikari.Snowflake
    """The guild id this player is currently in."""
    track: Track | None
    """The track the player is currently playing. None means its not currently playing any track."""
    volume: int
    """The volume of the player."""
    is_paused: bool
    """Whether the player is paused or not."""
    state: PlayerState
    """The [PlayerState][ongaku.abc.player.PlayerState] object."""
    voice: PlayerVoice
    """the [PlayerVoice][ongaku.abc.player.PlayerVoice] object."""
    filters: dict[t.Any, t.Any]
    """The filters object."""

    @classmethod
    def _from_payload(cls, payload: t.Mapping[str, t.Any]) -> Player:
        guild_id = payload.get("guildId")
        if guild_id is None:
            raise ValueError("guildId cannot be none.")
        if isinstance(guild_id, (str, int)):
            guild_id = int(guild_id)
        else:
            raise TypeError("guildId must be a integer.")
        
        track = payload.get("track")
        if track is not None:
            try:
                track = Track._from_payload(track)
            except TypeError:
                raise
            except ValueError:
                raise

        volume = payload.get("volume")
        if volume is None:
            raise ValueError("volume cannot be none.")
        if not isinstance(volume, int):
            raise TypeError("volume must be a integer.")

        paused = payload.get("paused")
        if paused is None:
            raise ValueError("paused cannot be none.")
        if not isinstance(paused, bool):
            raise TypeError("paused must be a boolean.")

        state = payload.get("state")
        if state is None:
            raise ValueError("state cannot be none.")

        try:
            state = PlayerState._from_payload(state)
        except TypeError:
            raise
        except ValueError:
            raise

        voice = payload.get("voice")
        if voice is None:
            raise ValueError("voice cannot be none.")

        try:
            voice = PlayerVoice._from_payload(voice)
        except TypeError:
            raise
        except ValueError:
            raise

        #TODO: These might need checks, however, I am unsure.
        filters = payload.get("filters", {})

        return cls(hikari.Snowflake(guild_id), track, volume, paused, state, voice, filters)


# MIT License

# Copyright (c) 2023 MPlatypus

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
