"""
Handler ABC's.

The handler abstract classes.
"""

from __future__ import annotations

import abc
import typing

if typing.TYPE_CHECKING:
    import hikari

    from ongaku.client import Client
    from ongaku.player import Player
    from ongaku.session import Session

__all__ = ("SessionHandler",)


class SessionHandler(abc.ABC):
    """
    Session handler base.

    The base session handler object.

    !!! note
        All custom session handlers **must** subclass this.

    Parameters
    ----------
    client
        The base ongaku client.
    """

    @abc.abstractmethod
    def __init__(self, client: Client): ...

    @property
    @abc.abstractmethod
    def sessions(self) -> typing.Sequence[Session]:
        """The sessions attached to this handler."""
        ...

    @property
    @abc.abstractmethod
    def players(self) -> typing.Sequence[Player]:
        """The players attached to this handler."""
        ...

    @property
    @abc.abstractmethod
    def is_alive(self) -> bool:
        """Whether the handler is alive or not."""
        ...

    @abc.abstractmethod
    async def start(self) -> None:
        """Start the session handler."""
        ...

    @abc.abstractmethod
    async def stop(self) -> None:
        """Stop the session handler."""
        ...

    @abc.abstractmethod
    def add_session(
        self, ssl: bool, host: str, port: int, password: str, attempts: int
    ) -> None:
        """Add a session."""
        ...

    @abc.abstractmethod
    def fetch_session(self) -> Session:
        """Return a valid session."""
        ...

    @abc.abstractmethod
    async def create_player(self, guild: hikari.SnowflakeishOr[hikari.Guild]) -> Player:
        """
        Create a player.

        Create a new player for this session.

        Parameters
        ----------
        guild
            The guild, or guild id you wish to delete the player from.
        """
        ...

    @abc.abstractmethod
    def fetch_player(self, guild: hikari.SnowflakeishOr[hikari.Guild]) -> Player:
        """
        Fetch a player.

        Fetches an existing player.

        Parameters
        ----------
        guild
            The guild, or guild id you wish to delete the player from.

        Raises
        ------
        PlayerMissingException
            Raised when the player for the guild, does not exist.
        """
        ...

    @abc.abstractmethod
    async def delete_player(self, guild: hikari.SnowflakeishOr[hikari.Guild]) -> None:
        """
        Delete a player.

        Delete a pre-existing player.

        Parameters
        ----------
        guild
            The guild, or guild id you wish to delete the player from.

        Raises
        ------
        PlayerMissingException
            Raised when the player for the guild, does not exist.
        """
        ...


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
