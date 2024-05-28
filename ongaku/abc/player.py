"""
Player ABC's.

The player Abstract classes.
"""

from __future__ import annotations

import abc
import typing

if typing.TYPE_CHECKING:
    import datetime

    import hikari

    from ongaku.abc.track import Track

__all__ = (
    "State",
    "Voice",
    "Player",
)


class Player(abc.ABC):
    """
    Player information.

    All of the information about the player, for the specified guild.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#player)
    """

    @property
    @abc.abstractmethod
    def guild_id(self) -> hikari.Snowflake:
        """The guild id this player is attached too."""
        ...

    @property
    @abc.abstractmethod
    def track(self) -> Track | None:
        """The track the player is currently playing.

        !!! note
            If the track is `None` then there is no current track playing.
        """
        ...

    @property
    @abc.abstractmethod
    def volume(self) -> int:
        """The volume of the player."""
        ...

    @property
    @abc.abstractmethod
    def is_paused(self) -> bool:
        """Whether the player is paused or not."""
        ...

    @property
    @abc.abstractmethod
    def state(self) -> State:
        """The [State][ongaku.abc.player.State] object."""
        ...

    @property
    @abc.abstractmethod
    def voice(self) -> Voice:
        """The [Voice][ongaku.abc.player.Voice] object."""
        ...

    @property
    @abc.abstractmethod
    def filters(self) -> typing.Mapping[str, typing.Any]:
        """The filter object."""
        ...
        # FIXME: This should return a filter object. (or at least  try to parse one.)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Player):
            return False

        if self.guild_id != other.guild_id:
            return False

        if self.track != other.track:
            return False

        if self.volume != other.volume:
            return False

        if self.is_paused != other.is_paused:
            return False

        if self.state != other.state:
            return False

        if self.voice != other.voice:
            return False

        if self.filters != other.filters:
            return False

        return True


class State(abc.ABC):
    """
    Players State.

    All the information for the players current state.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#player-state)
    """

    @property
    @abc.abstractmethod
    def time(self) -> datetime.datetime:
        """Unix timestamp in milliseconds."""
        ...

    @property
    @abc.abstractmethod
    def position(self) -> int:
        """The position of the track in milliseconds."""
        ...

    @property
    @abc.abstractmethod
    def connected(self) -> bool:
        """Whether Lavalink is connected to the voice gateway."""
        ...

    @property
    @abc.abstractmethod
    def ping(self) -> int:
        """The ping of the session to the Discord voice server in milliseconds (-1 if not connected)."""
        ...

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, State):
            return False

        if self.time != other.time:
            return False

        if self.position != other.position:
            return False

        if self.connected != other.connected:
            return False

        if self.ping != other.ping:
            return False

        return True


class Voice(abc.ABC):
    """
    Players Voice state.

    All of the Player Voice information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#voice-state)
    """

    @property
    @abc.abstractmethod
    def token(self) -> str:
        """The Discord voice token to authenticate with."""
        ...

    @property
    @abc.abstractmethod
    def endpoint(self) -> str:
        """The Discord voice endpoint to connect to."""
        ...

    @property
    @abc.abstractmethod
    def session_id(self) -> str:
        """The Discord voice session id to authenticate with."""
        ...

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Voice):
            return False

        if self.token != other.token:
            return False

        if self.endpoint != other.endpoint:
            return False

        if self.session_id != other.session_id:
            return False

        return True


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
