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
    """The ping of the node to the Discord voice server in milliseconds (-1 if not connected)."""

    @classmethod
    def _from_payload(cls, payload: t.Mapping[str, t.Any]) -> PlayerState:
        time = payload["time"]
        position = payload["position"]
        connected = payload["connected"]
        ping = payload["ping"]

        return cls(time, position, connected, ping)


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
        token = payload["token"]
        endpoint = payload["endpoint"]
        session_id = payload["sessionId"]

        return cls(token, endpoint, session_id)


@attrs.define
class Player(PayloadBase[dict[str, t.Any]]):
    """Player information.

    All of the information about the player, for the specified guild.

    Find out more [here](https://lavalink.dev/api/rest.html#player).
    """

    guild_id: hikari.Snowflake
    """The guild id this player is currently in."""
    track: t.Optional[Track]
    """The track the player is currently playing. None means its not currently playing any track."""
    volume: int
    """The volume of the player."""
    paused: bool
    """Whether the player is paused or not."""
    state: PlayerState
    """The [PlayerState][ongaku.abc.player.PlayerState] object."""
    voice: PlayerVoice
    """the [PlayerVoice][ongaku.abc.player.PlayerVoice] object."""
    filters: dict[t.Any, t.Any] | None = None
    """The filters object."""

    @classmethod
    def _from_payload(cls, payload: t.Mapping[str, t.Any]) -> Player:
        guild_id = hikari.Snowflake(payload["guildId"])
        try:
            track = Track._from_payload(payload["track"])
        except Exception:
            track = None
        volume = payload["volume"]
        paused = payload["paused"]
        state = PlayerState._from_payload(payload["state"])
        voice = PlayerVoice._from_payload(payload["voice"])
        filters = payload["filters"]

        return cls(guild_id, track, volume, paused, state, voice, filters)


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
