"""
Handlers.

All the handlers for Lavalink.
"""

from __future__ import annotations

import abc
import asyncio
import typing

import hikari

from ongaku import enums
from ongaku import errors
from ongaku.player import Player
from ongaku.session import Session

if typing.TYPE_CHECKING:
    from ongaku.client import Client


class SessionHandlerBase(abc.ABC):
    """
    Session handler base.

    The base session handler object.

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
        """
        ...

    @abc.abstractmethod
    async def fetch_player(self, guild: hikari.SnowflakeishOr[hikari.Guild]) -> Player:
        """
        Fetch a player.

        Fetches an existing player.
        """
        ...

    @abc.abstractmethod
    async def delete_player(self, guild: hikari.SnowflakeishOr[hikari.Guild]) -> None:
        """
        Delete a player.

        Delete a pre-existing player.
        """
        ...


class BasicSessionHandler(SessionHandlerBase):
    """
    Basic Session Handler.

    The basic session handler.

    This session handler simply fetches the first working session, and returns it. If it dies, it switches to the next available one.
    """

    def __init__(self, client: Client) -> None:
        self._client = client
        self._is_alive = False
        self._current_session: Session | None = None
        self._sessions: typing.MutableMapping[str, Session] = {}
        self._players: typing.MutableMapping[hikari.Snowflake, Player] = {}

    @property
    def sessions(self) -> typing.Sequence[Session]:
        """The sessions attached to this handler."""
        return tuple(self._sessions.values())

    @property
    def players(self) -> typing.Sequence[Player]:
        """The players attached to this handler."""
        return tuple(self._players.values())

    @property
    def is_alive(self) -> bool:
        """Whether the handler is alive or not."""
        return self._is_alive

    async def start(self) -> None:
        """Start the session handler."""
        self._is_alive = True

        for session in self.sessions:
            if session.status == enums.SessionStatus.NOT_CONNECTED:
                await session.start()

    async def stop(self) -> None:
        """Stop the session handler."""
        for session in self.sessions:
            await session.stop()

        for player in self.players:
            await player.disconnect()

    def fetch_session(self) -> Session:
        """Fetch a current session."""
        if self._current_session:
            return self._current_session

        for session in self.sessions:
            if session.status == enums.SessionStatus.CONNECTED:
                self._current_session = session
                return session

        raise errors.SessionException(None)

    def add_session(
        self, ssl: bool, host: str, port: int, password: str, attempts: int
    ) -> None:
        """Add a session."""
        new_session = Session(
            self._client, str(len(self.sessions)), ssl, host, port, password, attempts
        )

        if self.is_alive:
            asyncio.create_task(new_session.start())

        self._sessions.update({new_session.name: new_session})

    async def create_player(self, guild: hikari.SnowflakeishOr[hikari.Guild]) -> Player:
        """
        Create a player.

        Create a new player for this session.
        """
        try:
            return await self.fetch_player(hikari.Snowflake(guild))
        except Exception:
            pass

        session = self.fetch_session()

        new_player = Player(session, hikari.Snowflake(guild))

        self._players.update({hikari.Snowflake(guild): new_player})

        return new_player

    async def fetch_player(self, guild: hikari.SnowflakeishOr[hikari.Guild]) -> Player:
        """
        Fetch a player.

        Fetches an existing player.
        """
        player = self._players.get(hikari.Snowflake(guild))

        if player:
            return player

        raise errors.PlayerMissingException(hikari.Snowflake(guild))

    async def delete_player(self, guild: hikari.SnowflakeishOr[hikari.Guild]) -> None:
        """
        Delete a player.

        Delete a pre-existing player.
        """
        self._players.pop(hikari.Snowflake(guild))


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
