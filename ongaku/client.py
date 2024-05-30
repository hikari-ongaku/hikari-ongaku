"""
Client.

The base client for ongaku.
"""

from __future__ import annotations

import typing

import aiohttp
import hikari

from ongaku import errors
from ongaku.abc import session as session_
from ongaku.builders import EntityBuilder
from ongaku.impl.handlers import BasicSessionHandler
from ongaku.internal.logger import logger
from ongaku.player import Player
from ongaku.rest import RESTClient

if typing.TYPE_CHECKING:
    import arc
    import tanjun

    from ongaku.abc.handler import SessionHandler
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
        app: hikari.GatewayBotAware,
        *,
        session_handler: typing.Type[SessionHandler] = BasicSessionHandler,
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

        self._entity_builder = EntityBuilder()

        app.event_manager.subscribe(hikari.StartedEvent, self._start_event)
        app.event_manager.subscribe(hikari.StoppingEvent, self._stop_event)

    @classmethod
    def from_arc(
        cls,
        client: arc.GatewayClient,
        *,
        session_handler: typing.Type[SessionHandler] = BasicSessionHandler,
        attempts: int = 3,
    ) -> Client:
        """From Arc.

        This supports `client` and `player` [injection](../gs/injection.md) for [Arc](https://github.com/hypergonial/hikari-arc)

        Example
        -------
        ```py
        bot = arc.GatewayBot(...)
        client = arc.GatewayClient(bot)
        ongaku_client = ongaku.Client.from_arc(client)
        ```

        Parameters
        ----------
        client
            Your Gateway client for arc.
        attempts
            The amount of attempts a session will try to connect to the server.
        session_handler
            The session handler to use for the current client.
        """
        cls = cls(client.app, session_handler=session_handler, attempts=attempts)

        client.set_type_dependency(Client, cls)

        client.add_injection_hook(cls._arc_player_injector)

        return cls

    @classmethod
    def from_tanjun(
        cls,
        client: tanjun.abc.Client,
        *,
        session_handler: typing.Type[SessionHandler] = BasicSessionHandler,
        attempts: int = 3,
    ) -> Client:
        """From Tanjun.

        This supports `client` [injection](../gs/injection.md) for [Tanjun](https://github.com/FasterSpeeding/Tanjun)

        Example
        -------
        ```py
        bot = arc.GatewayBot(...)
        client = tanjun.Client.from_gateway_bot(bot)
        ongaku_client = ongaku.Client.from_tanjun(client)
        ```

        Parameters
        ----------
        client
            Your Gateway client from tanjun.
        attempts
            The amount of attempts a session will try to connect to the server.
        session_handler
            The session handler to use for the current client.
        """
        try:
            app = client.get_type_dependency(hikari.GatewayBotAware)
        except KeyError:
            raise Exception("The gateway bot requested was not found.")

        cls = cls(app, session_handler=session_handler, attempts=attempts)

        client.set_type_dependency(Client, cls)

        return cls

    @property
    def app(self) -> hikari.GatewayBotAware:
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
        return self.session_handler.is_alive

    @property
    def entity_builder(self) -> EntityBuilder:
        """The entity builder."""
        return self._entity_builder
    
    @property
    def session_handler(self) -> SessionHandler:
        """Session handler.
        
        The session handler that is currently controlling the sessions.

        !!! warning
            This should not be touched, or used if you do not know what you are doing.
            Please use the other methods in client for anything session handler related.
        """
        return self._session_handler

    def _get_client_session(self) -> aiohttp.ClientSession:
        if not self._client_session:
            self._client_session = aiohttp.ClientSession()

        if self._client_session.closed:
            self._client_session = aiohttp.ClientSession()

        return self._client_session

    def _fetch_live_server(self) -> Session:
        if not self.app.is_alive:
            raise errors.ClientAliveError("Hikari has not started.")

        if not self.is_alive:
            raise errors.ClientAliveError("Ongaku has crashed.")

        if self._selected_session:
            return self._selected_session

        for session in self._sessions:
            if session.status == session_.SessionStatus.CONNECTED:
                self._selected_session = session

        if self._selected_session is None:
            _logger.warning(
                "Ongaku is shutting down, due to no sessions currently working."
            )
            raise errors.NoSessionsError

        return self._selected_session

    async def _start_event(self, event: hikari.StartedEvent) -> None:
        await self.session_handler.start()

    async def _stop_event(self, event: hikari.StoppingEvent) -> None:
        await self.session_handler.stop()

        if self._client_session:
            await self._client_session.close()

    async def _arc_player_injector(
        self, ctx: arc.GatewayContext, inj_ctx: arc.InjectorOverridingContext
    ) -> None:
        if ctx.guild_id is None:
            return

        try:
            player = self.fetch_player(ctx.guild_id)
        except errors.PlayerMissingError:
            return

        inj_ctx.set_type_dependency(Player, player)

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
        self.session_handler.add_session(ssl, host, port, password, self._attempts)

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
        return await self.session_handler.create_player(guild)

    def fetch_player(self, guild: hikari.SnowflakeishOr[hikari.Guild]) -> Player:
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
        return self.session_handler.fetch_player(guild)

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
        player = self.fetch_player(guild)

        if player.connected:
            await player.disconnect()

        await self.session_handler.delete_player(guild)


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
