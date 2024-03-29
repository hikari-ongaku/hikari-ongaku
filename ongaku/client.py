"""
# Ongaku Client.

Ongaku base client where all functions like rest, creating/deleting/fetching players and more start from!
"""

from __future__ import annotations

import typing as t

from aiohttp import ClientSession
from hikari import GatewayBot
from hikari import Guild
from hikari import Snowflake
from hikari import SnowflakeishOr
from hikari import StartedEvent
from hikari import StoppingEvent

from ongaku.enums import VersionType
from ongaku.internal import TRACE_LEVEL
from ongaku.internal import logger as _logger
from ongaku.player import Player
from ongaku.rest import RESTClient
from ongaku.session import BaseSessionHandler
from ongaku.session import GeneralSessionHandler
from ongaku.session import Session

__all__ = ("Client",)


class Client:
    """
    Client.

    The client, where everything comes from.

    !!! warning
        Do not change `max_attempts` unless you know what you are doing. If your websocket does not stay connected/doesn't connect on the first try, do not use this as a fix. Try and solve the issue first.

    Parameters
    ----------
    bot : hikari.GatewayBot
        The bot that ongaku will attach to.
    max_attempts : int
        The maximum amount of attempts for the Websocket or rest actions.
    session_handler : typing.Type[BaseSessionHandler]
        The session handler that handles your sessions.
    logs : str | int
        The log level of ongaku. Setting this to `TRACE_ONGAKU` will give you trace messages.
    """

    def __init__(
        self,
        bot: GatewayBot,
        *,
        max_attempts: int = 3,
        session_handler: t.Type[BaseSessionHandler] = GeneralSessionHandler,
        logs: str | int = "INFO",
    ) -> None:
        _logger.setLevel(logs)
        self._bot = bot
        self._rest = RESTClient(self)
        self._session: ClientSession | None = None
        self._attempts: t.Final[int] = max_attempts
        self._session_handler = session_handler(self)
        _logger.log(TRACE_LEVEL, "Creating starting event...")
        bot.subscribe(StartedEvent, self._handle_startup)
        _logger.log(TRACE_LEVEL, "Creating stopping event...")
        bot.subscribe(StoppingEvent, self._handle_shutdown)
        _logger.log(TRACE_LEVEL, "Successfully setup events.")

    @property
    def sessions(self) -> t.Sequence[Session]:
        """All the available sessions."""
        return self._session_handler.sessions

    @property
    def players(self) -> t.Sequence[Player]:
        """The players, attached to all sessions."""
        return self._session_handler.players

    @property
    def rest(self) -> RESTClient:
        """The REST actions, for the lavalink server."""
        return self._rest

    @property
    def bot(self) -> GatewayBot:
        """The App or Bot that lavalink is connected too."""
        return self._bot

    async def _get_session(self) -> ClientSession:
        """
        Get session.

        Get the `aiohttp.ClientSession`, or creates a new one.
        """
        if not self._session:
            self._session = ClientSession()

        return self._session

    async def _handle_startup(self, event: StartedEvent):
        """
        Handle startup.

        Handles startup for the session handler.
        """
        await self._session_handler.start()

    async def _handle_shutdown(self, event: StoppingEvent):
        """
        Handle shutdown.

        Handles shutdown for both the session handler, and the client session.
        """
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
        """
        Add a new server.

        Add a new server to the list of servers you allow. You must have at least one.
        """
        self._session_handler.add_server(
            ssl=ssl, host=host, port=port, password=password, version=version
        )

    async def create_player(self, guild: SnowflakeishOr[Guild]) -> Player:
        """
        Create a player.

        Create a new player, for a guild.

        Parameters
        ----------
        guild : hikari.SnowflakeishOr[Guild]
            The guild or guild ID you wish to set the new player to.

        Raises
        ------
        SessionConnectionException
            Raised when no available sessions exist, to create the player on.
        """
        return await self._session_handler.create_player(Snowflake(guild))

    async def fetch_player(self, guild: SnowflakeishOr[Guild]) -> Player:
        """
        Fetch a player.

        Fetch a player, for a guild.

        Parameters
        ----------
        guild : hikari.SnowflakeishOr[Guild]
            The guild or guild ID you wish to fetch the player for.

        Raises
        ------
        PlayerMissingException
            Raised when no player exists for this guild.
        """
        return await self._session_handler.fetch_player(Snowflake(guild))

    async def delete_player(self, guild: SnowflakeishOr[Guild]) -> None:
        """
        Delete a player.

        Delete a player, for a guild.

        Parameters
        ----------
        guild : hikari.SnowflakeishOr[Guild]
            The guild id you wish to delete the player from.

        Raises
        ------
        PlayerMissingException
            Raised when no player exists for this guild.
        SessionConnectionException
            The session id was null, or empty.
        LavalinkException
            Raise when a invalid response type is received.
        """
        await self._session_handler.delete_player(Snowflake(guild))


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
