"""
Handler Impl's.

The handler implemented classes.
"""

from __future__ import annotations

import asyncio
import typing

import hikari

from ongaku import errors
from ongaku.abc import handler as handler_
from ongaku.abc import session as session_
from ongaku.internal import logger
from ongaku.player import Player

if typing.TYPE_CHECKING:
    from ongaku.client import Client
    from ongaku.session import Session

__all__ = ("BasicSessionHandler",)


_logger = logger.logger.getChild("handlers")


class BasicSessionHandler(handler_.SessionHandler):
    """
    Basic Session Handler.

    This session handler simply fetches the first working session, and returns it.
    If it closes or fails, it switches to the next available one.
    """

    def __init__(self, client: Client) -> None:
        self._client = client
        self._is_alive = False
        self._current_session: Session | None = None
        self._sessions: typing.MutableMapping[str, Session] = {}
        self._players: typing.MutableMapping[hikari.Snowflake, Player] = {}

    @property
    def sessions(self) -> typing.Sequence[Session]:
        return tuple(self._sessions.values())

    @property
    def players(self) -> typing.Sequence[Player]:
        return tuple(self._players.values())

    @property
    def is_alive(self) -> bool:
        return self._is_alive

    async def start(self) -> None:
        self._is_alive = True

        for session in self.sessions:
            if session.status == session_.SessionStatus.NOT_CONNECTED:
                await session.start()

    async def stop(self) -> None:
        for session in self.sessions:
            await session.stop()

        for player in self.players:
            await player.disconnect()

        self._is_alive = False

    def fetch_session(self) -> Session:
        if self._current_session:
            return self._current_session

        for session in self.sessions:
            if session.status == session_.SessionStatus.CONNECTED:
                self._current_session = session
                return session

        raise errors.NoSessionsError

    def add_session(self, session: Session) -> Session:
        """Add a session."""
        if self.is_alive:
            asyncio.create_task(session.start())  # noqa: RUF006

        self._sessions.update({session.name: session})

        return session

    def add_player(
        self,
        player: Player,
    ) -> Player:
        self._players.update({player.guild_id: player})

        return player

    async def create_player(self, guild: hikari.SnowflakeishOr[hikari.Guild]) -> Player:
        try:
            return self.fetch_player(hikari.Snowflake(guild))
        except Exception:
            pass

        session = self.fetch_session()

        new_player = Player(session, hikari.Snowflake(guild))

        self._players.update({hikari.Snowflake(guild): new_player})

        return new_player

    def fetch_player(self, guild: hikari.SnowflakeishOr[hikari.Guild]) -> Player:
        player = self._players.get(hikari.Snowflake(guild))

        if player:
            return player

        raise errors.PlayerMissingError

    async def delete_player(self, guild: hikari.SnowflakeishOr[hikari.Guild]) -> None:
        try:
            player = self._players.pop(hikari.Snowflake(guild))
        except KeyError:
            raise errors.PlayerMissingError

        await player.disconnect()


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
