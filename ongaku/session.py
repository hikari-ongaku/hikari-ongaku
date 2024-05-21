"""
Session.

Session related objects.
"""

from __future__ import annotations

import asyncio
import typing

import aiohttp

from ongaku import enums
from ongaku import errors
from ongaku import events
from ongaku.abc import events as abc_events
from ongaku.abc import statistics
from ongaku.internal.about import __version__
from ongaku.internal.converters import json_loads
from ongaku.internal.logger import logger

_logger = logger.getChild("session")

if typing.TYPE_CHECKING:
    import hikari

    from ongaku.client import Client
    from ongaku.handlers import SessionHandlerBase
    from ongaku.player import Player

__all__ = ("Session",)


class Session:
    """
    Session.

    The base session object.

    Parameters
    ----------
    client
        The ongaku client attached to this session.
    name
        The name of the session.
    ssl
        Whether the server is https or just http.
    host
        The host of the lavalink server.
    port
        The port of the lavalink server.
    password
        The password of the lavalink server.
    attempts
        The attempts that the session is allowed to use, before completely shutting down.
    """

    def __init__(
        self,
        client: Client,
        name: str,
        ssl: bool,
        host: str,
        port: int,
        password: str,
        attempts: int,
    ) -> None:
        self._client = client
        self._name = name
        self._ssl = ssl
        self._host = host
        self._port = port
        self._password = password
        self._attempts = attempts
        self._remaining_attempts = attempts
        self._base_uri = f"http{'s' if ssl else ''}://{host}:{port}"
        self._session_id = None
        self._session_task: asyncio.Task[None] | None = None
        self._status = enums.SessionStatus.NOT_CONNECTED
        self._players: typing.MutableMapping[hikari.Snowflake, Player] = {}
        self._base_headers: typing.MutableMapping[str, typing.Any]

    @property
    def client(self) -> Client:
        """The client attached to the bot."""
        return self._client

    @property
    def app(self) -> hikari.GatewayBotAware:
        """The application attached to this bot."""
        return self.client.app

    @property
    def name(self) -> str:
        """The name of the session."""
        return self._name

    @property
    def ssl(self) -> bool:
        """Whether the server uses https or just http."""
        return self._ssl

    @property
    def host(self) -> str:
        """The host, or domain of the site."""
        return self._host

    @property
    def port(self) -> int:
        """The port of the server."""
        return self._port

    @property
    def password(self) -> str:
        """The password for the server."""
        return self._password

    @property
    def base_uri(self) -> str:
        """The base uri for the server."""
        return self._base_uri

    @property
    def status(self) -> enums.SessionStatus:
        """The current status of the server."""
        return self._status

    @property
    def session_id(self) -> str | None:
        """
        The current session id.

        !!! note
            Shows up as none if the current session failed to connect, or has not connected yet.
        """
        return self._session_id

    async def _handle_op_code(self, data: str) -> None:
        mapped_data = json_loads(data)

        if isinstance(mapped_data, typing.Sequence):
            raise errors.BuildException(
                "Invalid data received. Must be of type 'typing.Mapping' and not 'typing.Sequence'"
            )

        op_code = enums.WebsocketOPCode(mapped_data["op"])

        if op_code == enums.WebsocketOPCode.READY:
            parser = abc_events.Ready._from_payload(data)

            event = events.ReadyEvent(
                self.app,
                self.client,
                self,
                parser.resumed,
                parser.session_id,
            )

            self._session_id = parser.session_id

        elif op_code == enums.WebsocketOPCode.PLAYER_UPDATE:
            parser = abc_events.PlayerUpdate._from_payload(data)

            event = events.PlayerUpdateEvent(
                self.app,
                self.client,
                self,
                parser.guild_id,
                parser.state,
            )

        elif op_code == enums.WebsocketOPCode.STATS:
            parser = statistics.Statistics._from_payload(data)

            event = events.StatisticsEvent(
                self.app,
                self.client,
                self,
                parser.players,
                parser.playing_players,
                parser.uptime,
                parser.memory,
                parser.cpu,
                parser.frame_statistics,
            )

        else:
            event_type = enums.WebsocketEvent(mapped_data["type"])

            if event_type == enums.WebsocketEvent.TRACK_START_EVENT:
                parser = abc_events.TrackStart._from_payload(data)

                event = events.TrackStartEvent(
                    self.app,
                    self.client,
                    self,
                    parser.guild_id,
                    parser.track,
                )

            elif event_type == enums.WebsocketEvent.TRACK_END_EVENT:
                parser = abc_events.TrackEnd._from_payload(data)

                event = events.TrackEndEvent(
                    self.app,
                    self.client,
                    self,
                    parser.guild_id,
                    parser.track,
                    parser.reason,
                )

            elif event_type == enums.WebsocketEvent.TRACK_EXCEPTION_EVENT:
                parser = abc_events.TrackException._from_payload(data)

                event = events.TrackExceptionEvent(
                    self.app,
                    self.client,
                    self,
                    parser.guild_id,
                    parser.track,
                    parser.exception,
                )

            elif event_type == enums.WebsocketEvent.TRACK_STUCK_EVENT:
                parser = abc_events.TrackStuck._from_payload(data)

                event = events.TrackStuckEvent(
                    self.app,
                    self.client,
                    self,
                    parser.guild_id,
                    parser.track,
                    parser.threshold_ms,
                )

            else:
                parser = abc_events.WebsocketClosed._from_payload(data)

                event = events.WebsocketClosedEvent(
                    self.app,
                    self.client,
                    self,
                    parser.guild_id,
                    parser.code,
                    parser.reason,
                    parser.by_remote,
                )

        self.app.event_manager.dispatch(event)

    async def _handle_ws_message(self, msg: aiohttp.WSMessage) -> None:
        if msg.type == aiohttp.WSMsgType.TEXT:
            event = events.PayloadEvent(self.app, self.client, self, msg.data)
            self.app.event_manager.dispatch(event)

            await self._handle_op_code(msg.data)

        elif msg.type == aiohttp.WSMsgType.ERROR:
            self._status = enums.SessionStatus.FAILURE
            _logger.warning("An error occurred.")
            await self.transfer(self.client._session_handler)

        elif msg.type == aiohttp.WSMsgType.CLOSED:
            self._status = enums.SessionStatus.FAILURE
            _logger.warning(
                f"Told to close. Code: {msg.data.name}. Message: {msg.extra}"
            )
            await self.transfer(self.client._session_handler)

    async def _websocket(self) -> None:
        bot = self.app.get_me()

        if not bot:
            if self._remaining_attempts > 0:
                self._status = enums.SessionStatus.NOT_CONNECTED

                _logger.warning(
                    "Attempted fetching the bot, but failed as it does not exist."
                )
            else:
                self._status = enums.SessionStatus.FAILURE

            _logger.warning(
                "Attempted fetching the bot, but failed as it does not exist."
            )

            raise errors.SessionStartException

        headers: typing.MutableMapping[str, typing.Any] = {
            "Authorization": self.password,
            "User-Id": str(int(bot.id)),
            "Client-Name": f"{bot.global_name if bot.global_name else 'invalid'}/{__version__}",
        }

        self._base_headers = headers

        while self._remaining_attempts >= 1:
            if self._remaining_attempts != self._attempts:
                await asyncio.sleep(2.5)
            self._remaining_attempts -= 1
            try:
                async with self.client._get_client_session() as session:
                    async with session.ws_connect(
                        self.base_uri + "/v4/websocket",
                        headers=headers,
                        autoclose=False,
                    ) as ws:
                        self._status = enums.SessionStatus.CONNECTED
                        async for msg in ws:
                            await self._handle_ws_message(msg)

            except Exception as e:
                _logger.warning(f"Websocket connection failure: {e}")
                self._status = enums.SessionStatus.NOT_CONNECTED

        else:
            _logger.critical(f"Server has no more attempts.")
            self._status = enums.SessionStatus.NOT_CONNECTED

    def _get_session_id(self) -> str:
        if self._session_id:
            return self._session_id

        raise errors.SessionStartException

    async def transfer(self, session_handler: SessionHandlerBase) -> None:
        """
        Transfer.

        Transfer all the players from this session, to a different one.

        Parameters
        ----------
        session_handler
            The session handler, that will allow this session to move its players too.
        """
        for id, player in self._players.items():
            await player.disconnect()

            new_player = await session_handler.create_player(id)

            if player.channel_id:
                await new_player.connect(player.channel_id)

            new_player.add(player.queue)

            new_player.set_autoplay(player.autoplay)

        await self.stop()

    async def start(self) -> None:
        """
        Start the session.

        Starts up the session, to receive events.
        """
        self._session_task = asyncio.create_task(self._websocket())

    async def stop(self) -> None:
        """
        Stop the session.

        Stops the current session, if it is running.
        """
        if self._session_task:
            self._session_task.cancel()

        for guild_id, player in self._players.items():
            await player.disconnect()

            self._players.pop(guild_id)


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
