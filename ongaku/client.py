"""
Client.

The base client for ongaku.
"""

from __future__ import annotations

import typing

import aiohttp
import hikari

from ongaku import enums
from ongaku import errors
from ongaku.handlers import BasicSessionHandler
from ongaku.internal.logger import logger
from ongaku.rest import RESTClient

if typing.TYPE_CHECKING:
    from ongaku.handlers import SessionHandlerBase
    from ongaku.player import Player
    from ongaku.session import Session


_logger = logger.getChild("client")


__all__ = ("Client",)


class Client:
    """
    Client.

    The client for ongaku.

    Example
    -------
    ```py
    bot = hikari.GatewayBot("...")
    client = ongaku.Client(bot)
    ```

    Parameters
    ----------
    app
        The application that the client will attach too.
    attempts
        The amount of attempts a session will try to connect to the server.
    session_handler
        The session handler to use for the current client.
    """

    def __init__(
        self,
        app: hikari.GatewayBot,
        session_handler: typing.Type[SessionHandlerBase] = BasicSessionHandler,
        attempts: int = 3,
    ) -> None:
        self._attempts = attempts
        self._app = app
        self._selected_session: Session | None = None
        self._sessions: typing.MutableSequence[Session] = []
        self._client_session: aiohttp.ClientSession | None = None

        self._rest_client = RESTClient(self)

        self._is_alive = False

        self._session_handler = session_handler(self)

        app.subscribe(hikari.StartedEvent, self._start_event)
        app.subscribe(hikari.StoppingEvent, self._stop_event)

    @property
    def app(self) -> hikari.GatewayBot:
        """The application attached to this bot."""
        return self._app

    @property
    def rest(self) -> RESTClient:
        """The rest client for all the rest actions."""
        return self._rest_client

    @property
    def is_alive(self) -> bool:
        """
        Whether or not the session handler is alive.

        !!! note
            If the hikari.StartedEvent has already happened, and this is False, ongaku is no longer running and has crashed. Check your logs.
        """
        return self._session_handler.is_alive

    def _get_client_session(self) -> aiohttp.ClientSession:
        if not self._client_session:
            self._client_session = aiohttp.ClientSession()

        if self._client_session.closed:
            self._client_session = aiohttp.ClientSession()

        return self._client_session

    def _fetch_live_server(self) -> Session:
        if not self.app.is_alive:
            raise errors.ClientAliveException("Hikari has not started.")

        if not self.is_alive:
            raise errors.ClientAliveException("Ongaku has crashed.")

        if self._selected_session:
            return self._selected_session

        for session in self._sessions:
            if session.status == enums.SessionStatus.CONNECTED:
                self._selected_session = session

        if self._selected_session == None:
            _logger.warning(
                "Ongaku is shutting down, due to no sessions currently working."
            )
            raise errors.NoSessionsException

        return self._selected_session

    async def _start_event(self, event: hikari.StartedEvent) -> None:
        await self._session_handler.start()

    async def _stop_event(self, event: hikari.StoppingEvent) -> None:
        await self._session_handler.stop()

    def add_session(
        self,
        ssl: bool = False,
        host: str = "127.0.0.1",
        port: int = 2333,
        password: str = "youshallnotpass",
    ) -> None:
        """
        Add Session.

        Add a new session to the session pool.

        Example
        -------
        ```py
        client = ongaku.Client(...)

        client.add_session(
            host="192.168.68.69"
        )
        ```

        Parameters
        ----------
        ssl
            Whether the server is https or just http.
        host
            The host of the lavalink server.
        port
            The port of the lavalink server.
        password
            The password of the lavalink server.
        """
        self._session_handler.add_session(ssl, host, port, password, self._attempts)

    async def create_player(self, guild: hikari.SnowflakeishOr[hikari.Guild]) -> Player:
        """
        Create a player.

        Create a new player for this session.

        Example
        -------
        ```py
        client = ongaku.Client(...)

        player = await client.create_player(guild_id)

        await player.connect(channel_id)

        await player.play(track)
        ```

        Parameters
        ----------
        guild
            The guild, or guild id you wish to delete the player from.
        """
        return await self._session_handler.create_player(guild)

    async def fetch_player(self, guild: hikari.SnowflakeishOr[hikari.Guild]) -> Player:
        """
        Fetch a player.

        Fetches an existing player.

        Example
        -------
        ```py
        client = ongaku.Client(...)
        player = await client.fetch_player(guild_id)

        await player.pause()
        ```

        Parameters
        ----------
        guild
            The guild, or guild id you wish to delete the player from.

        Raises
        ------
        PlayerMissingException
            Raised when the player for the guild, does not exist.
        """
        return await self._session_handler.fetch_player(guild)

    async def delete_player(self, guild: hikari.SnowflakeishOr[hikari.Guild]) -> None:
        """
        Delete a player.

        Delete a pre-existing player.

        Example
        -------
        ```py
        client = ongaku.Client(...)
        await client.delete_player(...)
        ```

        Parameters
        ----------
        guild
            The guild, or guild id you wish to delete the player from.

        Raises
        ------
        PlayerMissingException
            Raised when the player for the guild, does not exist.
        """
        player = await self.fetch_player(guild)

        if player.connected:
            await player.disconnect()

        await self._session_handler.delete_player(guild)


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
