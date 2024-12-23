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

if typing.TYPE_CHECKING:
    from ongaku.client import Client
    from ongaku.player import Player
    from ongaku.session import Session

__all__ = ("BasicSessionHandler",)


_logger = logger.logger.getChild("handlers")


class BasicSessionHandler(handler_.SessionHandler):
    """
    Basic Session Handler.

    This session handler simply fetches the first working session, and returns it.
    If it closes or fails, it switches to the next available one.
    """

    __slots__: typing.Sequence[str] = ("_current_session", "_players", "_sessions")

    def __init__(self, *, client: Client) -> None:
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
        self._is_alive = True

        await asyncio.gather(*[i.start() for i in self.sessions])

    async def stop(self) -> None:
        for session in self.sessions:
            await session.stop()

        self._players.clear()

        self._is_alive = False

    def add_session(self, *, session: Session) -> Session:
        """Add a session."""
        if self.is_alive:
            asyncio.create_task(session.start())  # noqa: RUF006

        if self._sessions.get(session.name, None) is None:
            self._sessions.update({session.name: session})
            return session

        raise errors.UniqueError(f"The name {session.name} is not unique.")

    def fetch_session(self, *, name: str | None = None) -> Session:
        if name is not None:
            try:
                return self._sessions[name]
            except KeyError:
                raise errors.SessionMissingError

        if self._current_session:
            return self._current_session

        for session in self.sessions:
            if session.status == session_.SessionStatus.CONNECTED:
                self._current_session = session
                return session

        raise errors.NoSessionsError

    async def delete_session(self, *, name: str) -> None:
        try:
            session = self._sessions.pop(name)
        except KeyError:
            raise errors.SessionMissingError

        await session.stop()

    def add_player(self, *, player: Player) -> Player:
        if self._players.get(player.guild_id, None) is not None:
            raise errors.UniqueError(
                f"A player with the guild id {player.guild_id} has already been made."
            )

        self._players.update({player.guild_id: player})

        return player

    def fetch_player(self, *, guild: hikari.SnowflakeishOr[hikari.Guild]) -> Player:
        player = self._players.get(hikari.Snowflake(guild))

        if player:
            return player

        raise errors.PlayerMissingError

    async def delete_player(
        self, *, guild: hikari.SnowflakeishOr[hikari.Guild]
    ) -> None:
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
