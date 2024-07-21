"""
Client.

The base client for ongaku.
"""

from __future__ import annotations

import typing

import aiohttp
import hikari

from ongaku import errors
from ongaku.builders import EntityBuilder
from ongaku.impl.handlers import BasicSessionHandler
from ongaku.internal.logger import TRACE_LEVEL
from ongaku.internal.logger import logger
from ongaku.player import Player
from ongaku.rest import RESTClient
from ongaku.session import Session

if typing.TYPE_CHECKING:
    import arc
    import lightbulb
    import tanjun

    from ongaku.abc.handler import SessionHandler

_logger = logger.getChild("client")


__all__ = ("Client",)


class Client:
    """
    Client.

    The client for ongaku.

    !!! note
        The lowest log level for ongaku is `TRACE_ONGAKU` which will result in all traces being printed to the terminal.

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
    session_handler
        The session handler to use for the current client.
    logs
        The log level for ongaku.
    attempts
        The amount of attempts a session will try to connect to the server.
    """

    __slots__: typing.Sequence[str] = (
        "_attempts",
        "_app",
        "_client_session",
        "_rest_client",
        "_is_alive",
        "_session_handler",
        "_entity_builder",
    )

    def __init__(
        self,
        app: hikari.GatewayBotAware,
        *,
        session_handler: typing.Type[SessionHandler] = BasicSessionHandler,
        logs: str | int = "INFO",
        attempts: int = 3,
    ) -> None:
        _logger.setLevel(logs)

        self._attempts = attempts
        self._app = app
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
        logs: str | int = "INFO",
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
        session_handler
            The session handler to use for the current client.
        logs
            The log level for ongaku.
        attempts
            The amount of attempts a session will try to connect to the server.
        """
        cls = cls(
            client.app, session_handler=session_handler, logs=logs, attempts=attempts
        )

        client.set_type_dependency(Client, cls)

        client.add_injection_hook(cls._arc_player_injector)

        return cls

    @classmethod
    def from_tanjun(
        cls,
        client: tanjun.abc.Client,
        *,
        session_handler: typing.Type[SessionHandler] = BasicSessionHandler,
        logs: str | int = "INFO",
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
        session_handler
            The session handler to use for the current client.
        logs
            The log level for ongaku.
        attempts
            The amount of attempts a session will try to connect to the server.
        """
        try:
            app = client.get_type_dependency(hikari.GatewayBotAware)
        except KeyError:
            raise Exception("The gateway bot requested was not found.")

        cls = cls(app, session_handler=session_handler, logs=logs, attempts=attempts)

        client.set_type_dependency(Client, cls)

        return cls

    @classmethod
    def from_lightbulb(
        cls,
        client: lightbulb.GatewayEnabledClient,
        *,
        session_handler: typing.Type[SessionHandler] = BasicSessionHandler,
        logs: str | int = "INFO",
        attempts: int = 3,
    ) -> Client:
        """From Lightbulb.

        This supports `client` and `player` [injection](../gs/injection.md) for [Lightbulb](https://github.com/tandemdude/hikari-lightbulb)

        Example
        -------
        ```py
        bot = hikari.GatewayBot(...)
        client = lightbulb.Client(bot)
        ongaku_client = ongaku.Client.from_arc(client)
        ```

        Parameters
        ----------
        client
            Your Gateway client for lightbulb.
        session_handler
            The session handler to use for the current client.
        logs
            The log level for ongaku.
        attempts
            The amount of attempts a session will try to connect to the server.
        """
        cls = cls(
            client._app, session_handler=session_handler, logs=logs, attempts=attempts
        )

        client.di.register_for(lightbulb.di.Contexts.DEFAULT).register_value(Client, cls)

        client.di.register_for(lightbulb.di.Contexts.COMMAND).register_factory(Player, cls._lightbulb_player_injector)

        return cls

    @property
    def app(self) -> hikari.GatewayBotAware:
        """The application this client is included in."""
        return self._app

    @property
    def rest(self) -> RESTClient:
        """The rest client for calling rest actions."""
        return self._rest_client

    @property
    def is_alive(self) -> bool:
        """
        Whether the session handler is alive.

        !!! note
            If the `hikari.StartedEvent` has occurred, and this is False, ongaku is no longer running and has crashed. Check your logs.
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

    async def _start_event(self, event: hikari.StartedEvent) -> None:
        _logger.log(TRACE_LEVEL, "Starting up ongaku.")
        await self.session_handler.start()
        _logger.log(TRACE_LEVEL, "Successfully started ongaku.")

    async def _stop_event(self, event: hikari.StoppingEvent) -> None:
        _logger.log(TRACE_LEVEL, "Shutting down ongaku.")
        await self.session_handler.stop()

        if self._client_session:
            await self._client_session.close()

        _logger.log(TRACE_LEVEL, "Successfully shut down ongaku.")

    async def _arc_player_injector(
        self, ctx: arc.GatewayContext, inj_ctx: arc.InjectorOverridingContext
    ) -> None:
        _logger.log(TRACE_LEVEL, "Attempting to inject player.")

        if ctx.guild_id is None:
            _logger.log(TRACE_LEVEL, "Player ignored, not in guild.")
            return

        try:
            player = self.fetch_player(ctx.guild_id)
        except errors.PlayerMissingError:
            _logger.log(TRACE_LEVEL, "Player not found for context.")
            return

        _logger.log(TRACE_LEVEL, "Successfully injected player into context.")

        inj_ctx.set_type_dependency(Player, player)

    async def _lightbulb_player_injector(
        self, ctx: lightbulb.Context
    ) -> Player:
        _logger.log(TRACE_LEVEL, "Attempting to inject player.")

        if ctx.guild_id is None:
            _logger.log(TRACE_LEVEL, "Player missing, not in guild.")
            raise errors.PlayerMissingError

        try:
            player = self.fetch_player(ctx.guild_id)
        except errors.PlayerMissingError:
            _logger.log(TRACE_LEVEL, "Player missing, does not exist.")
            raise errors.PlayerMissingError

        _logger.log(TRACE_LEVEL, "Successfully returned player.")

        return player

    def create_session(
        self,
        name: str,
        ssl: bool = False,
        host: str = "127.0.0.1",
        port: int = 2333,
        password: str = "youshallnotpass",
    ) -> Session:
        """
        Create Session.

        Create a new session for the session handler.

        Example
        -------
        ```py
        client = ongaku.Client(...)

        client.add_session(host="192.168.68.69")
        ```

        !!! warning
            The name set must be unique, otherwise an error will be raised.

        Parameters
        name
            The name of the session
        ssl
            Whether the server uses `https` or just `http`.
        host
            The host of the lavalink server.
        port
            The port of the lavalink server.
        password
            The password of the lavalink server.
        attempts
            The attempts that the session is allowed to use, before completely shutting down.

        Returns
        -------
        Session
            The session that was added to the handler.

        Raises
        ------
        UniqueError
        """
        new_session = Session(
            self,
            name,
            ssl,
            host,
            port,
            password,
            self._attempts,
        )

        return self.session_handler.add_session(new_session)

    def fetch_session(self, name: str) -> Session:
        """Fetch a session.

        Fetch a session from the session handler.

        Parameters
        ----------
        name
            The name of the session

        Returns
        -------
        Session
            The session that was requested.

        Raises
        ------
        SessionMissingError
            Raised when the session does not exist.
        """
        return self.session_handler.fetch_session(name)

    async def delete_session(self, name: str) -> None:
        """Delete a session.

        Delete a session from the session handler.

        Parameters
        ----------
        name
            The name of the session

        Raises
        ------
        SessionMissingError
            Raised when the session does not exist.
        """
        await self.session_handler.delete_session(name)

    def create_player(self, guild: hikari.SnowflakeishOr[hikari.Guild]) -> Player:
        """
        Create a player.

        Create a new player to play songs on.

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
            The `guild`, or `guild id` you wish to create a player for.

        Returns
        -------
        Player
            The player that was created.

        Raises
        ------
        NoSessionsError
            When there is no available sessions.
        """
        try:
            return self.fetch_player(hikari.Snowflake(guild))
        except errors.PlayerMissingError:
            pass

        session = self.session_handler.fetch_session()

        new_player = Player(session, hikari.Snowflake(guild))

        return self.session_handler.add_player(new_player)

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
            The `guild`, or `guild id` you wish to fetch the player for.

        Raises
        ------
        PlayerMissingError
            Raised when the player for the specified guild does not exist.
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
            The `guild`, or `guild id` you wish to delete the player from.

        Raises
        ------
        PlayerMissingError
            Raised when the player for the specified guild does not exist.
        """
        await self.session_handler.delete_player(guild)


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
