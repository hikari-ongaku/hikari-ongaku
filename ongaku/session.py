"""
Session.

Session related objects.
"""

from __future__ import annotations

import asyncio
import typing

import aiohttp

from ongaku import errors
from ongaku import events
from ongaku.abc import session as session_
from ongaku.internal.about import __version__
from ongaku.internal.converters import json_loads
from ongaku.internal.logger import logger

_logger = logger.getChild("session")

if typing.TYPE_CHECKING:
    import hikari

    from ongaku.abc import handler as handler_
    from ongaku.client import Client
    from ongaku.internal import types
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
        self._session_id: str | None = None
        self._session_task: asyncio.Task[None] | None = None
        self._status = session_.SessionStatus.NOT_CONNECTED
        self._players: typing.MutableMapping[hikari.Snowflake, Player] = {}
        self._websocket_headers: typing.MutableMapping[str, typing.Any]
        self._authorization_headers: typing.Mapping[str, typing.Any] = {
            "Authorization": password
        }

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
    def auth_headers(self) -> typing.Mapping[str, typing.Any]:
        """The headers required for authorization. This is automatically added."""
        return self._authorization_headers

    @property
    def status(self) -> session_.SessionStatus:
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

    async def request(
        self,
        method: str,
        path: str,
        return_type: typing.Type[types.RequestT] | None,
        *,
        headers: typing.Mapping[str, typing.Any] = {},
        json: typing.Mapping[str, typing.Any] | typing.Sequence[typing.Any] = {},
        params: typing.Mapping[str, typing.Any] = {},
        ignore_default_headers: bool = False,
        version: bool = True,
    ) -> types.RequestT | None:
        """Request.

        Make a http(s) request to the current session

        Parameters
        ----------
        method
            The method to send the request as. `GET`, `POST`, `PATCH`, `DELETE`, `PUT`
        path
            The path to the url. e.g. `/v4/info`
        return_type
            The response type you expect.
        headers
            The headers you wish to send.
        json
            The json data you wish to send.
        params
            The parameters you wish to send.
        ignore_default_headers
            Whether to ignore the default headers or not.
        version
            Whether or not to include the version in the path.

        Returns
        -------
        types.RequestT
            Your requested type of data.

        Raises
        ------
        errors.TimeoutException
            Raised when the request takes too long to respond.
        errors.RestEmptyException
            Raised when the request required a return type, but received nothing, or a 204 response.
        errors.RestStatusException
            Raised when a 4XX or a 5XX status is received.
        errors.BuildException
            Raised when a mapping or sequence is requested, but could not be created from the response.
        errors.RestErrorException
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        errors.RestException
            Raised when an unknown exception is caught.
        """
        session = self.client._get_client_session()

        new_headers: typing.MutableMapping[str, typing.Any] = dict(headers)

        if ignore_default_headers is False:
            new_headers.update(self.auth_headers)

        new_params: typing.MutableMapping[str, typing.Any] = dict(params)

        trace = True

        if trace is True:
            new_params.update({"trace": "true"})

        response = await session.request(
            method,
            f"{self.base_uri}{'/v4' if version else ''}{path}",
            headers=new_headers,
            json=json,
            params=new_params,
        )

        if response.status == 204 and return_type is not None:
            raise errors.RestEmptyError

        if response.status >= 400:
            payload = await response.text()

            if len(payload) == 0:
                raise errors.RestStatusError(response.status, response.reason)

            try:
                rest_error = self.client.entity_builder.build_rest_error(payload)
            except Exception:
                raise errors.RestStatusError(response.status, response.reason)
            raise errors.RestRequestError.from_error(rest_error)

        if return_type is None:
            return

        payload = await response.text()

        if issubclass(return_type, str | int | bool | float):
            return return_type(payload)

        try:
            json_payload = json_loads(payload)
        except Exception as e:
            raise errors.BuildError(str(e))

        return return_type(json_payload)

    def _handle_op_code(self, data: str) -> hikari.Event:
        mapped_data = json_loads(data)

        if isinstance(mapped_data, typing.Sequence):
            raise errors.BuildError(
                "Invalid data received. Must be of type 'typing.Mapping' and not 'typing.Sequence'"
            )

        op_code = session_.WebsocketOPCode(mapped_data["op"])

        if op_code == session_.WebsocketOPCode.READY:
            parser = self.client.entity_builder.build_ready(mapped_data)
            event = events.ReadyEvent.from_session(
                self, parser.resumed, parser.session_id
            )

            self._session_id = parser.session_id

        elif op_code == session_.WebsocketOPCode.PLAYER_UPDATE:
            parser = self.client.entity_builder.build_player_update(mapped_data)
            event = events.PlayerUpdateEvent.from_session(
                self,
                parser.guild_id,
                parser.state,
            )

        elif op_code == session_.WebsocketOPCode.STATS:
            parser = self.client.entity_builder.build_statistics(mapped_data)

            event = events.StatisticsEvent.from_session(
                self,
                parser.players,
                parser.playing_players,
                parser.uptime,
                parser.memory,
                parser.cpu,
                parser.frame_stats,
            )

        else:
            event_type = session_.WebsocketEvent(mapped_data["type"])

            if event_type == session_.WebsocketEvent.TRACK_START_EVENT:
                parser = self.client.entity_builder.build_track_start(mapped_data)

                event = events.TrackStartEvent.from_session(
                    self,
                    parser.guild_id,
                    parser.track,
                )

            elif event_type == session_.WebsocketEvent.TRACK_END_EVENT:
                parser = self.client.entity_builder.build_track_end(mapped_data)

                event = events.TrackEndEvent.from_session(
                    self,
                    parser.guild_id,
                    parser.track,
                    parser.reason,
                )

            elif event_type == session_.WebsocketEvent.TRACK_EXCEPTION_EVENT:
                parser = self.client.entity_builder.build_track_exception(mapped_data)

                event = events.TrackExceptionEvent.from_session(
                    self,
                    parser.guild_id,
                    parser.track,
                    parser.exception,
                )

            elif event_type == session_.WebsocketEvent.TRACK_STUCK_EVENT:
                parser = self.client.entity_builder.build_track_stuck(mapped_data)

                event = events.TrackStuckEvent.from_session(
                    self,
                    parser.guild_id,
                    parser.track,
                    parser.threshold_ms,
                )

            else:
                parser = self.client.entity_builder.build_websocket_closed(mapped_data)

                event = events.WebsocketClosedEvent.from_session(
                    self,
                    parser.guild_id,
                    parser.code,
                    parser.reason,
                    parser.by_remote,
                )
        return event

    async def _handle_ws_message(self, msg: aiohttp.WSMessage) -> None:
        if msg.type == aiohttp.WSMsgType.TEXT:
            payload_event = events.PayloadEvent.from_session(self, msg.data)
            event = self._handle_op_code(msg.data)

            await self.app.event_manager.dispatch(payload_event)
            await self.app.event_manager.dispatch(event)

        elif msg.type == aiohttp.WSMsgType.ERROR:
            self._status = session_.SessionStatus.FAILURE
            _logger.warning("An error occurred.")
            await self.transfer(self.client.session_handler)

        elif msg.type == aiohttp.WSMsgType.CLOSED:
            self._status = session_.SessionStatus.FAILURE
            _logger.warning(
                f"Told to close. Code: {msg.data.name}. Message: {msg.extra}"
            )
            await self.transfer(self.client.session_handler)

    async def _websocket(self) -> None:
        bot = self.app.get_me()

        if not bot:
            if self._remaining_attempts > 0:
                self._status = session_.SessionStatus.NOT_CONNECTED

                _logger.warning(
                    "Attempted fetching the bot, but failed as it does not exist."
                )
            else:
                self._status = session_.SessionStatus.FAILURE

            _logger.warning(
                "Attempted fetching the bot, but failed as it does not exist."
            )

            raise errors.SessionStartError

        self._websocket_headers = {
            "User-Id": str(int(bot.id)),
            "Client-Name": f"{bot.global_name if bot.global_name else 'unknown'}/{__version__}",
        }

        new_headers: typing.MutableMapping[str, typing.Any] = {}

        new_headers.update(self._websocket_headers)

        new_headers.update(self.auth_headers)

        while self._remaining_attempts >= 1:
            if self._remaining_attempts != self._attempts:
                await asyncio.sleep(2.5)
            self._remaining_attempts -= 1
            try:
                async with (
                    self.client._get_client_session() as session,
                    session.ws_connect(
                        self.base_uri + "/v4/websocket",
                        headers=new_headers,
                        autoclose=False,
                    ) as ws,
                ):
                    self._status = session_.SessionStatus.CONNECTED
                    async for msg in ws:
                        await self._handle_ws_message(msg)

            except Exception as e:
                _logger.warning(f"Websocket connection failure: {e}")
                self._status = session_.SessionStatus.NOT_CONNECTED

        else:
            _logger.critical("Server has no more attempts.")
            self._status = session_.SessionStatus.NOT_CONNECTED

    def _get_session_id(self) -> str:
        if self.session_id:
            return self.session_id

        raise errors.SessionStartError

    async def transfer(self, session_handler: handler_.SessionHandler) -> None:
        """
        Transfer.

        Transfer all the players from this session, to a different one.

        Parameters
        ----------
        session_handler
            The session handler, that will allow this session to move its players too.
        """
        for player in self._players.values():
            player = await player.transfer(session_handler.fetch_session())

            session_handler.add_player(player)

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

            try:
                await self._session_task
            except asyncio.CancelledError:
                self._session_task = None


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
