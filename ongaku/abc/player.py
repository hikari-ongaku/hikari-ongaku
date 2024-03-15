"""
Player ABC's.

The player Abstract classes.
"""

from __future__ import annotations

import typing as t

from hikari import Snowflake
from pydantic import Field
from pydantic import WrapSerializer
from pydantic import WrapValidator

from .bases import PayloadBase
from .bases import _snowflake_to_string
from .bases import _string_to_snowflake
from .track import Track

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
    session_id: t.Annotated[str, Field(alias="sessionId")]
    """The Discord voice session id to authenticate with."""


class Player(PayloadBase):
    """
    Player information.

    All of the information about the player, for the specified guild.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest.html#player)
    """

    guild_id: t.Annotated[
        Snowflake,
        WrapValidator(_string_to_snowflake),
        WrapSerializer(_snowflake_to_string),
        Field(alias="guildId"),
    ]
    """The guild id this player is currently in."""
    track: t.Annotated[Track | None, Field(default=None)]
    """The track the player is currently playing. None means its not currently playing any track."""
    volume: int
    """The volume of the player."""
    is_paused: t.Annotated[bool, Field(alias="paused")]
    """Whether the player is paused or not."""
    state: PlayerState
    """The [PlayerState][ongaku.abc.player.PlayerState] object."""
    voice: PlayerVoice
    """the [PlayerVoice][ongaku.abc.player.PlayerVoice] object."""
    filters: dict[t.Any, t.Any]
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
