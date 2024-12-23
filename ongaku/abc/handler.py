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

    __slots__: typing.Sequence[str] = (
        "_client",
        "_is_alive",
    )

    @abc.abstractmethod
    def __init__(self, *, client: Client): ...

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
    def is_alive(self) -> bool:
        """Whether the handler is alive or not."""
        return self._is_alive

    @abc.abstractmethod
    async def start(self) -> None:
        """Start the session handler.

        Starts up the session handler and attempts to connect all sessions to their websocket.
        """
        ...

    @abc.abstractmethod
    async def stop(self) -> None:
        """Stop the session handler.

        Stops the session handler and kills all players and sessions.
        """
        ...

    @abc.abstractmethod
    def add_session(self, *, session: Session) -> Session:
        """Add a session.

        Add a new session to the session handler.

        Parameters
        session
            The session to add to the session handler.

        Returns
        -------
        Session
            The session that was added to the handler.
        """
        ...

    @abc.abstractmethod
    def fetch_session(self, *, name: str | None = None) -> Session:
        """Fetch a session.

        Returns a valid session.

        !!! note
            If a name is provided, only that session will be attempted to be returned.

        Parameters
        ----------
        name
            The name of the session.

        Returns
        -------
        Session
            The session to use.

        Raises
        ------
        NoSessionError
            Raised when there is no available sessions for the handler to return.
        SessionMissingError
            Raised when a session is requested, but does not exist.
        """
        ...

    @abc.abstractmethod
    async def delete_session(self, *, name: str) -> None:
        """Delete a session.

        Delete a session from the session handler.

        Parameters
        name
            The name of the session to delete.

        Returns
        -------
        Session
            The session that was added to the handler.

        Raises
        ------
        SessionMissingError
            Raised when the session does not exist.
        """
        ...

    @abc.abstractmethod
    def add_player(self, *, player: Player) -> Player:
        """Add a player.

        Add a new player to the session handler.

        Parameters
        ----------
        player
            The player to add to the session handler.

        Returns
        -------
        Player
            The player you added to the session handler.
        """
        ...

    @abc.abstractmethod
    def fetch_player(self, *, guild: hikari.SnowflakeishOr[hikari.Guild]) -> Player:
        """
        Fetch a player.

        Fetches an existing player.

        Parameters
        ----------
        guild
            The `guild`, or `guild id` you wish to fetch the player for.

        Raises
        ------
        PlayerMissingError
            Raised when the player for the specified guild does not exist.
        """
        ...

    @abc.abstractmethod
    async def delete_player(
        self, *, guild: hikari.SnowflakeishOr[hikari.Guild]
    ) -> None:
        """
        Delete a player.

        Delete a pre-existing player.

        Parameters
        ----------
        guild
            The `guild`, or `guild id` you wish to delete the player from.

        Raises
        ------
        PlayerMissingError
            Raised when the player for the specified guild does not exist.
        """
        ...


# MIT License

# Copyright (c) 2023-present MPlatypus

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
