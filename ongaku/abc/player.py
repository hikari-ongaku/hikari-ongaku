"""
Player ABC's.

The player Abstract classes.
"""

from __future__ import annotations

import typing

import pydantic

from ongaku.abc.bases import PayloadBase
from ongaku.abc.track import Track

if typing.TYPE_CHECKING:
    from ongaku.internal.types import GuildIdT

__all__ = (
    "PlayerState",
    "PlayerVoice",
    "Player",
)


class PlayerState(PayloadBase):
    """
    Players State.

    All the information for the players current state.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/websocket.html#player-state)
    """

    time: int
    """Unix timestamp in milliseconds."""
    position: int
    """The position of the track in milliseconds."""
    connected: bool
    """Whether Lavalink is connected to the voice gateway."""
    ping: int
    """The ping of the session to the Discord voice server in milliseconds (-1 if not connected)."""


class PlayerVoice(PayloadBase):
    """
    Players Voice state.

    All of the Player Voice information.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest.html#voice-state)
    """

    token: str
    """The Discord voice token to authenticate with."""
    endpoint: str
    """The Discord voice endpoint to connect to."""
    session_id: typing.Annotated[str, pydantic.Field(alias="sessionId")]
    """The Discord voice session id to authenticate with."""


class Player(PayloadBase):
    """
    Player information.

    All of the information about the player, for the specified guild.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest.html#player)
    """

    guild_id: GuildIdT
    """The guild id this player is currently in."""
    track: typing.Annotated[Track | None, pydantic.Field(default=None)]
    """The track the player is currently playing. None means its not currently playing any track."""
    volume: int
    """The volume of the player."""
    is_paused: typing.Annotated[bool, pydantic.Field(alias="paused")]
    """Whether the player is paused or not."""
    state: PlayerState
    """The [PlayerState][ongaku.abc.player.PlayerState] object."""
    voice: PlayerVoice
    """the [PlayerVoice][ongaku.abc.player.PlayerVoice] object."""
    filters: dict[typing.Any, typing.Any]
    """The filter object."""


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
