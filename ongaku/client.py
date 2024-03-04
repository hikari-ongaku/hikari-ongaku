"""Ongaku Client.

Ongaku base client where everything is started from.
"""

from __future__ import annotations

import typing as t

import aiohttp
import hikari

from . import internal
from .abc import Server
from .enums import ConnectionType
from .enums import VersionType
from .handlers import BaseSessionHandler
from .handlers import ShardSessionHandler
from .player import Player
from .rest import RESTClient
from .session import Session

_logger = internal.logger

__all__ = ("Client",)


class Client:
    """Base Ongaku class.

    The base Ongaku class, where everything starts from.

    !!! WARNING
        Do not change `max_retries` unless you know what you are doing. If your websocket does not stay connected/doesn't connect on the first try, do not use this as a fix. Try and solve the issue first.

    Parameters
    ----------
    bot : hikari.GatewayBot
        The bot that ongaku will attach to.
    max_retries : int
        The maximum amount of retries for the Websocket or a rest actions.
    session_handler : typing.Type[BaseSessionHandler]
        The session handler that handles your sessions.
    logs : str | int
        The log level of ongaku. Setting this to `TRACE_ONGAKU` will give you trace messages.
    """

    def __init__(
        self,
        bot: hikari.GatewayBot,
        *,
        max_retries: int = 3,
        session_handler: t.Type[BaseSessionHandler] = ShardSessionHandler,
        logs: str | int = "INFO",
    ) -> None:
        _logger.setLevel(logs)

        # bot that the client is attached too.
        self._bot = bot

        # rest client for all rest actions.
        self._rest = RESTClient(self)

        # aiohttp client session.
        self._session: aiohttp.ClientSession | None = None

        # The server to use for all currently.
        self._current_server: Server | None = None

        # A list of all provided servers for ongaku.
        self._servers: list[Server] = []

        self._retries: t.Final[int] = max_retries

        _logger.log(internal.Trace.LEVEL, "Creating starting event...")
        bot.subscribe(hikari.StartingEvent, self._handle_startup)
        _logger.log(internal.Trace.LEVEL, "Creating stopping event...")
        bot.subscribe(hikari.StoppingEvent, self._handle_shutdown)
        _logger.log(internal.Trace.LEVEL, "Successfully setup events.")

        if not session_handler:
            self._session_handler = ShardSessionHandler(self)
        else:
            self._session_handler = session_handler(self)

    @property
    def sessions(self) -> t.Sequence[Session]:
        """The sessions, that are attached to the lavalink server."""
        return self._session_handler.sessions

    @property
    def players(self) -> t.Sequence[Player]:
        """The players, from all sessions attached to the lavalink server."""
        return self._session_handler.players

    @property
    def rest(self) -> RESTClient:
        """The REST access. For the lavalink server."""
        return self._rest

    @property
    def bot(self) -> hikari.GatewayBot:
        """The App or Bot that lavalink is connected too."""
        return self._bot

    def _get_server(self) -> Server:
        if len(self._servers) == 0:
            raise Exception("No servers have been added yet.")

        if (
            self._current_server
            and self._current_server.status == ConnectionType.CONNECTED
        ):
            return self._current_server

        for server in self._servers:
            if server.status is ConnectionType.CONNECTED:
                self._current_server = server
                return server

            if server.status is ConnectionType.NOT_CONNECTED:
                self._current_server = server
                return server

        raise Exception("All servers have failed.")

    def _strike_server(self, server: Server, reason: str) -> None:
        s_index = self._servers.index(server)

        self._servers[s_index].remaining_attempts -= 1

        _logger.warning(
            f"server: {self._servers[s_index].host}:{self._servers[s_index].port} has failed to load properly. Remaining attempts: {self._servers[s_index].remaining_attempts}. Reason: {reason}."
        )

        if self._servers[s_index].remaining_attempts == 0:
            _logger.critical(
                f"server: {self._servers[s_index].host}:{self._servers[s_index].port} has completely failed. Reason: {reason}."
            )

            self._servers[s_index].status = ConnectionType.FAILURE

            self._get_server()

    async def _get_session(self) -> aiohttp.ClientSession:
        if not self._session:
            self._session = aiohttp.ClientSession()

        return self._session

    async def _handle_startup(self, event: hikari.StartingEvent):
        await self._session_handler.start()

    async def _handle_shutdown(self, event: hikari.StoppingEvent):
        _logger.info("Shutting down handler...")
        await self._session_handler.stop()

        _logger.info("shutting down client session...")

        if self._session:
            await self._session.close()

        _logger.info("Shutdown complete.")

    def add_server(
        self,
        *,
        host: str = "localhost",
        port: int = 2333,
        password: str | None = "youshallnotpass",
        version: VersionType = VersionType.V4,
        ssl: bool = False,
    ) -> None:
        """Add a new server.

        Add a new server to the list of servers you allow. You must have at least one.
        """
        new_server = Server.build(ssl, host, port, password, version, self._retries)

        self._servers.append(new_server)

        if self._current_server is None:
            self._current_server = new_server

    async def create_player(self, guild_id: hikari.Snowflake) -> Player:
        """Create a player.
        
        Create a new player, for a specified guild.

        Parameters
        ----------
        guild_id : hikari.Snowflake
            The guild id you wish to add a player to.

        Raises
        ------
        #TODO: add raises things.
        """
        return await self._session_handler.create_player(guild_id)

    async def fetch_player(self, guild_id: hikari.Snowflake) -> Player:
        """Fetch a player.
        
        Fetch a player, for a specified guild.

        Parameters
        ----------
        guild_id : hikari.Snowflake
            The guild id you wish to fetch the player from.

        Raises
        ------
        #TODO: add raises things.
        """
        return await self._session_handler.fetch_player(guild_id)

    async def delete_player(self, guild_id: hikari.Snowflake) -> None:
        """Delete a player.
        
        Delete a player, for a specified guild.

        Parameters
        ----------
        guild_id : hikari.Snowflake
            The guild id you wish to delete the player from.

        Raises
        ------
        #TODO: add raises things.
        """
        await self._session_handler.delete_player(guild_id)


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
