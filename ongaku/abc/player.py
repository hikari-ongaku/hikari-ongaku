"""
Player ABC's.

The player Abstract classes.
"""

from __future__ import annotations

import typing

import hikari
import datetime
import attrs
from ongaku.abc.track import Track

__all__ = (
    "State",
    "Voice",
    "Player",
)

@attrs.define
class State:
    """
    Players State.

    All the information for the players current state.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#player-state)
    """

    _time: datetime.datetime = attrs.field(alias="time")
    _position: int = attrs.field(alias="position")
    _connection: bool = attrs.field(alias="connection")
    _ping: int = attrs.field(alias="ping")

    @property
    def time(self) -> datetime.datetime:
        """Unix timestamp in milliseconds."""
        return self._time
    
    @property
    def position(self) -> int:
        """The position of the track in milliseconds."""
        return self._position
    
    @property
    def connected(self) -> bool:
        """Whether Lavalink is connected to the voice gateway."""
        return self._connection

    @property
    def ping(self) -> int:
        """The ping of the session to the Discord voice server in milliseconds (-1 if not connected)."""
        return self._ping


@attrs.define
class Voice:
    """
    Players Voice state.

    All of the Player Voice information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#voice-state)
    """

    _token: str = attrs.field(alias="token")
    _endpoint: str = attrs.field(alias="endpoint")
    _session_id: str = attrs.field(alias="session_id")

    @property
    def token(self) -> str:
        """The Discord voice token to authenticate with."""
        return self._token

    @property
    def endpoint(self) -> str:
        """The Discord voice endpoint to connect to."""
        return self._endpoint

    @property
    def session_id(self) -> str:
        """The Discord voice session id to authenticate with."""
        return self._session_id
    

@attrs.define
class Player:
    """
    Player information.

    All of the information about the player, for the specified guild.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#player)
    """

    _guild_id: hikari.Snowflake = attrs.field(alias="guild_id")
    _track: Track | None = attrs.field(alias="track")
    _volume: int = attrs.field(alias="volume")
    _is_paused: bool = attrs.field(alias="is_paused")
    _state: State = attrs.field(alias="state")
    _voice: Voice = attrs.field(alias="voice")
    _filters: typing.Mapping[str, typing.Any] = attrs.field(alias="filters")

    @property
    def guild_id(self) -> hikari.Snowflake:
        """The guild id this player is attached too."""
        return self._guild_id
    
    @property
    def track(self) -> Track | None:
        """The track the player is currently playing.
        
        !!! note
            If the track is `None` then there is no current track playing.
        """
        return self._track
    
    @property
    def volume(self) -> int:
        """The volume of the player."""
        return self._volume
    
    @property
    def is_paused(self) -> bool:
        """Whether the player is paused or not."""
        return self._is_paused

    @property
    def state(self) -> State:
        """The [PlayerState][ongaku.abc.player.PlayerState] object."""
        return self._state

    @property
    def voice(self) -> Voice:
        """The [PlayerVoice][ongaku.abc.player.Voice] object."""
        return self._voice

    @property
    def filters(self) -> typing.Mapping[str, typing.Any]:
        """The filter object."""
        return self._filters
        # FIXME: This should return a filter object. (or at least  try to parse one.)


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
