"""Sessions.

The base hikari session.
"""

from __future__ import annotations

import asyncio
import typing as t

import aiohttp
import hikari

from . import internal
from .about import __version__
from .exceptions import PlayerMissingException
from .exceptions import RequiredException
from .exceptions import SessionConnectionException
from .exceptions import SessionException
from .handlers import _WSHandler
from .player import Player

if t.TYPE_CHECKING:
    from .client import Client

__all__ = ("Session",)

_logger = internal.logger.getChild("session")


class Session:
    """Session.

    A base session item, for sharding the sets of players.

    Parameters
    ----------
    client : Client
        The Ongaku client that it will be connected too.
    name : str
        The name of the session. This can be anything.
    """

    def __init__(self, client: Client, name: str) -> None:
        self._client = client
        self._name = name

        self._players: dict[hikari.Snowflake, Player] = {}

        self._handler = _WSHandler(self)

        self._connection: asyncio.Task[t.Any] | None = None

        self._session_id: str | None = None

    @property
    def name(self) -> str:
        """The name of the session."""
        return self._name

    @property
    def client(self) -> Client:
        """The [client][ongaku.Client] object that this session has attached to."""
        return self._client

    @property
    def players(self) -> t.Sequence[Player]:
        """The players, that are attached to this session."""
        return list(self._players.values())

    def _get_session_id(self) -> str:
        if self._session_id:
            return self._session_id

        raise Exception("Session id missing")

    async def _websocket(self, new_headers: dict[str, t.Any]):
        server = self._client._get_server()

        while server.remaining_attempts > 0:
            if server.remaining_attempts < self.client._retries:
                await asyncio.sleep(3)

            session = await self.client._get_session()

            headers = server.default_headers.copy()

            headers.update(new_headers)

            print(headers)

            try:
                async with session.ws_connect(
                    server.base_uri + server.version.value + "/websocket",
                    headers=headers,
                    timeout=5,
                ) as ws:
                    _logger.log(
                        internal.Trace.LEVEL,
                        f"Websocket connection on session {self.name} successful.",
                    )
                    async for msg in ws:
                        await self._handler.handle_message(msg)
            except aiohttp.ClientConnectionError:
                self.client._strike_server(server, "Client Timeout")

            except Exception as e:
                self.client._strike_server(server, str(e))

            server = self._client._get_server()

    async def connect(self):
        """Connect to the lavalink websocket."""
        try:
            bot = self._client.bot.get_me()
        except Exception:
            reason = f"Session: {self.name} could not start, due to the bot ID not being found."
            _logger.warning(reason)
            raise SessionConnectionException(None, reason)

        if bot is None:
            reason = f"Session: {self.name} could not start, due to the bot ID not being found."
            _logger.warning(reason)
            raise SessionConnectionException(None, reason)

        new_headers = {
            "User-Id": str(bot.id),
            "Client-Name": f"{bot.username.replace(' ', '_').strip()}::{__version__}",
        }

        _logger.log(internal.Trace.LEVEL, "Starting websocket connection...")
        task = asyncio.create_task(self._websocket(new_headers))

        self._connection = task

    async def disconnect(self) -> None:
        """Disconnect from lavalink websocket."""
        _logger.log(internal.Trace.LEVEL, "Destroying connection...")
        if self._connection:
            self._connection.cancel()

        _logger.log(internal.Trace.LEVEL, f"successfully destroyed connection.")

    async def create_player(self, guild_id: hikari.Snowflake) -> Player:
        _logger.log(
            internal.Trace.LEVEL,
            f"bot player: {guild_id} in node: {self.name}",
        )
        bot = self.client.bot.get_me()

        if bot is None:
            raise RequiredException("The bot is required to be able to connect.")

        bot_state = self.client.bot.cache.get_voice_state(guild_id, bot.id)

        if bot_state is not None and bot_state.channel_id is not None:
            try:
                self._players.pop(guild_id)
            except KeyError:
                raise SessionException("This session has not yet been started.")

        new_player = Player(self, guild_id)

        self._players.update({guild_id: new_player})

        _logger.log(
            internal.Trace.LEVEL,
            f"successfully created player: {guild_id} in node: {self.name}",
        )

        return new_player

    async def fetch_player(self, guild_id: hikari.Snowflake) -> Player:
        _logger.log(
            internal.Trace.LEVEL,
            f"finding player: {guild_id} in node: {self.name}",
        )

        for player in self._players.values():
            if player.guild_id == guild_id:
                _logger.log(
                    internal.Trace.LEVEL,
                    f"successfully found player: {guild_id} in node: {self.name}",
                )
                return player

        raise PlayerMissingException(guild_id)

    async def delete_player(self, guild_id: hikari.Snowflake) -> None:
        _logger.log(
            internal.Trace.LEVEL,
            f"deleting player: {guild_id} in node: {self.name}",
        )

        player = await self.fetch_player(guild_id)

        await player.disconnect()

        self._players.pop(guild_id)

        _logger.log(
            internal.Trace.LEVEL,
            f"successfully deleted player: {guild_id} in node: {self.name}",
        )


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
