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
"""Session and entities related to Lavalink session objects."""

from __future__ import annotations

import asyncio
import enum
import http
import logging
import typing

import aiohttp
from hikari import undefined

from ongaku import errors
from ongaku import events
from ongaku.internal import types
from ongaku.internal.about import __version__
from ongaku.internal.logging import TRACE_LEVEL

if typing.TYPE_CHECKING:
    import hikari

    from ongaku.abc import handlers
    from ongaku.client import Client
    from ongaku.internal import routes
    from ongaku.player import ControllablePlayer


__all__: typing.Sequence[str] = (
    "ControllableSession",
    "Session",
    "SessionStatus",
)


_logger: typing.Final[logging.Logger] = logging.getLogger("ongaku.session")


class Session:
    __slots__: typing.Sequence[str] = ("_resuming", "_timeout")

    def __init__(self, *, resuming: bool, timeout: int) -> None:
        self._resuming = resuming
        self._timeout = timeout

    @property
    def resuming(self) -> bool:
        return self._resuming

    @property
    def timeout(self) -> int:
        return self._timeout

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Session):
            return False

        return self.resuming == other.resuming and self.timeout == other.timeout


class ControllableSession:
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
        Whether the server is `https` or just `http`.
    host
        The host of the lavalink server.
    port
        The port of the lavalink server.
    password
        The password of the lavalink server.
    """

    __slots__: typing.Sequence[str] = (
        "_base_uri",
        "_client",
        "_client_session",
        "_extensions",
        "_host",
        "_name",
        "_password",
        "_players",
        "_port",
        "_session_id",
        "_session_task",
        "_ssl",
        "_status",
    )

    def __init__(
        self,
        client: Client,
        *,
        name: str,
        ssl: bool,
        host: str,
        port: int,
        password: str,
    ) -> None:
        self._client = client
        self._name = name
        self._ssl = ssl
        self._host = host
        self._port = port
        self._password = password
        self._base_uri = f"http{'s' if ssl else ''}://{host}:{port}"
        self._session_id: str | None = None
        self._session_task: asyncio.Task[None] | None = None
        self._status = SessionStatus.NOT_CONNECTED
        self._players: typing.MutableMapping[hikari.Snowflake, ControllablePlayer] = {}
        self._client_session = None
        self._extensions = client._extensions  # noqa: SLF001 FIXME: Maybe find a smarter way to do this.

    @property
    def client(self) -> Client:
        """The client this session is included in."""
        return self._client

    @property
    def app(self) -> hikari.GatewayBotAware:
        """The application this session is included in."""
        return self.client.app

    @property
    def name(self) -> str:
        """The name of the session."""
        return self._name

    @property
    def ssl(self) -> bool:
        """Whether the server uses `https` or just `http`."""
        return self._ssl

    @property
    def host(self) -> str:
        """The host or domain of the site."""
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
        """The base URI for the server."""
        return self._base_uri

    @property
    def status(self) -> SessionStatus:
        """The current status of the session."""
        return self._status

    @property
    def session_id(self) -> str | None:
        """
        The current session id.

        !!! note
            Shows up as none if the current session failed to connect,
            or has not connected yet.
        """
        return self._session_id

    async def start(self, client_session: aiohttp.ClientSession) -> None:
        """
        Start the session.

        Starts up the session, to receive events.
        """
        self._client_session = client_session

        bot = self.app.get_me()

        if not bot:
            raise errors.SessionStartError("Could not fetch the bot information.")

        bot_name = "unknown"
        if bot.global_name is not None:
            bot_name = bot.global_name
        elif bot.display_name not in (None, undefined.UNDEFINED):
            bot_name = bot.display_name

        headers = {
            "User-Id": str(int(bot.id)),
            "Client-Name": f"{bot_name}/{__version__}",
            "Authorization": self.password,
        }

        self._session_task = asyncio.create_task(
            self._websocket(client_session, headers),
        )

    async def stop(self) -> None:
        """
        Stop the session.

        Stops the current session, if it is running.
        """
        _logger.log(
            TRACE_LEVEL,
            "Shutting down session %s",
            self.name,
        )
        if self._session_task:
            self._session_task.cancel()

            try:
                await self._session_task
            except asyncio.CancelledError:
                self._session_task = None

        _logger.log(
            TRACE_LEVEL,
            "Successfully shut down session %s",
            self.name,
        )

    async def _websocket(
        self,
        client_session: aiohttp.ClientSession,
        headers: typing.Mapping[str, typing.Any],
    ) -> None:
        while True:
            try:
                ws = await client_session.ws_connect(
                    self.base_uri + "/v4/websocket",
                    headers=headers,
                    autoclose=False,
                )

                _logger.log(
                    TRACE_LEVEL,
                    "Successfully made connection to session %s",
                    self.name,
                )

                self._status = SessionStatus.CONNECTED

                event = events.SessionConnectedEvent.from_session(self)

                self._client.app.event_manager.dispatch(event, return_tasks=False)

                async for msg in ws:
                    match msg.type:
                        case aiohttp.WSMsgType.TEXT:
                            payload_event = events.PayloadEvent.from_session(
                                self,
                                payload=msg.data,
                            )
                            event = self._handle_payload(msg.data)

                            self.app.event_manager.dispatch(
                                payload_event,
                                return_tasks=False,
                            )
                            if event:
                                self.app.event_manager.dispatch(
                                    event,
                                    return_tasks=False,
                                )
                            else:
                                _logger.warning(
                                    "Received unknown payload: %s",
                                    msg.data,
                                )

                        case aiohttp.WSMsgType.ERROR:
                            _logger.warning(
                                "An error occurred, data: %s, extra: %s",
                                msg.data,
                                msg.extra,
                            )

                            event = events.SessionErrorEvent.from_session(self)

                            self.app.event_manager.dispatch(
                                event,
                                return_tasks=False,
                            )

                        case aiohttp.WSMsgType.CLOSED:
                            event = events.SessionDisconnectedEvent.from_session(
                                self,
                                code=msg.data,
                                reason=msg.extra,
                            )

                            self.app.event_manager.dispatch(
                                event,
                                return_tasks=False,
                            )

                        case msg_type:
                            _logger.log(
                                TRACE_LEVEL,
                                "Received unknown message type: %s",
                                msg_type,
                                msg.data,
                                msg.extra,
                            )

            except Exception as err:  # noqa: BLE001, PERF203
                timeout_delay = 60

                _logger.warning(
                    "Websocket connection failure: %s reattempting in %ss",
                    err,
                    timeout_delay,
                )
                self._status = SessionStatus.NOT_CONNECTED
                await asyncio.sleep(timeout_delay)

    def _handle_payload(self, data: str) -> hikari.Event | None:
        mapped_data = types.json_loads(data)

        if isinstance(mapped_data, typing.Sequence):
            raise errors.BuildError(
                "Expected 'typing.Mapping' but received 'typing.Sequence'",
            )

        op_code = mapped_data["op"]

        event: hikari.Event | None = None

        op_code_mapping: dict[
            str,
            typing.Any,
        ] = {  # FIXME: I hate that this uses typing.Any, it should technically be a callable
            "ready": self.client.builder.deserialize_ready_event,
            "playerUpdate": self.client.builder.deserialize_player_update_event,
            "stats": self.client.builder.deserialize_statistics_event,
        }

        if (deserializer := op_code_mapping.get(op_code)) is not None:
            event = deserializer(
                mapped_data,
                session=self,
            )

        if op_code == "ready":
            self._session_id = mapped_data["sessionId"]

        elif op_code == "event":
            event_type = mapped_data["type"]

            event_type_mapping: dict[str, typing.Any] = {
                "TrackStartEvent": self.client.builder.deserialize_track_start_event,
                "TrackEndEvent": self.client.builder.deserialize_track_end_event,
                "TrackExceptionEvent": self.client.builder.deserialize_track_exception_event,
                "TrackStuckEvent": self.client.builder.deserialize_track_stuck_event,
                "WebSocketClosedEvent": self.client.builder.deserialize_websocket_closed_event,
            }

            if (deserializer := event_type_mapping.get(event_type)) is not None:
                event = deserializer(
                    mapped_data,
                    session=self,
                )

        for e in self._extensions.copy():
            try:
                ext = self.client.injector.get_type_dependency(e)
            except KeyError:
                self._extensions.discard(e)
                continue

            event = ext.event_handler(mapped_data, self)

            if event:
                return event

        return event

    @typing.overload
    async def request(
        self,
        route: routes.BuiltRoute,
        *,
        headers: typing.Mapping[str, typing.Any] | None = None,
        body: types.RequestBodyT = None,
        params: typing.Mapping[str, str | int | float | bool] | None = None,
        ignore_default_headers: bool = False,
        optional: typing.Literal[False] = False,
    ) -> typing.Sequence[str] | typing.Mapping[str, typing.Any] | str: ...

    @typing.overload
    async def request(
        self,
        route: routes.BuiltRoute,
        *,
        headers: typing.Mapping[str, typing.Any] | None = None,
        body: types.RequestBodyT = None,
        params: typing.Mapping[str, str | int | float | bool] | None = None,
        ignore_default_headers: bool = False,
        optional: typing.Literal[True] = True,
    ) -> typing.Sequence[str] | typing.Mapping[str, typing.Any] | str | None: ...

    async def request(
        self,
        route: routes.BuiltRoute,
        *,
        headers: typing.Mapping[str, typing.Any] | None = None,
        body: types.RequestBodyT = None,
        params: typing.Mapping[str, str | int | float | bool] | None = None,
        ignore_default_headers: bool = False,
        optional: bool = False,
    ) -> typing.Sequence[str] | typing.Mapping[str, typing.Any] | str | None:
        """Request.

        Make a http(s) request to the current session

        Parameters
        ----------
        route
            The route to make the request to.
        headers
            The headers to send.
        body
            The body to send.
        params
            The parameters to send.
        ignore_default_headers
            Whether to ignore the default headers or not.
        optional
            Whether the response is optional.

        Returns
        -------
        types.RequestT | None
            Your requested type of data.

        Raises
        ------
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the response is 204, or 404.
        RestStatusError
            Raised when a request fails.
        BuildError
            Raised when the mapping or sequence could not be built.
        RestRequestError
            Raised when a request fails, but Lavalink has more information.
        RestError
            Raised when an unknown error is caught.
        """
        if self._client_session is None:
            raise errors.SessionStartError

        new_headers: typing.MutableMapping[str, typing.Any] = dict(headers or {})

        if ignore_default_headers is False:
            new_headers["Authorization"] = self.password

        new_params: typing.MutableMapping[str, str] | None = None

        if params and params != {}:
            new_params = {}
            for key, value in params.items():
                if isinstance(value, bool):
                    new_params.update({key: "true" if value else "false"})

                new_params.update({key: str(value)})

        if _logger.isEnabledFor(TRACE_LEVEL):
            if new_params is not None:
                new_params.update({"trace": "true"})
            else:
                new_params = {"trace": "true"}

        _logger.log(
            TRACE_LEVEL,
            "Making request to %s with headers: %s and json: %s and params: %s",
            route,
            new_headers,
            body,
            new_params,
        )

        response = await self._client_session.request(
            route.method,
            f"{self.base_uri}{route.path}",
            headers=new_headers,
            json=body,
            params=new_params,
        )

        if response.status in (http.HTTPStatus.NO_CONTENT, http.HTTPStatus.NOT_FOUND):
            if optional:
                return None
            raise errors.RestEmptyError

        if response.status >= http.HTTPStatus.BAD_REQUEST:
            payload = await response.text()

            if len(payload) == 0:
                raise errors.RestStatusError(response.status, response.reason)

            try:
                rest_error = self.client.builder.deserialize_rest_error(payload)
            except Exception as err:
                raise errors.RestStatusError(response.status, response.reason) from err
            raise rest_error

        payload = await response.text()

        if response.content_type == "application/json":
            try:
                json_payload = types.json_loads(payload)
            except Exception as e:
                raise errors.BuildError(str(e)) from e

            return json_payload

        return payload

    async def transfer(self, handler: handlers.Handler, /) -> None:
        """
        Transfer.

        Transfer all the players from this session, to a different one.

        !!! warning
            This will close the current sessions connection.

        Parameters
        ----------
        handler
            The session handler, that will allow this session to move its players too.
        """
        session = handler.get_session()

        _logger.log(
            TRACE_LEVEL,
            "Attempting transfer players from session %s to %s",
            self.name,
            session.name,
        )

        for player in self._players.values():
            handler.add_player(player=await player.transfer(session=session))

        await self.stop()

        _logger.log(
            TRACE_LEVEL,
            "Successfully transferred players from %s to %s",
            self.name,
            session.name,
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ControllableSession):
            return False

        return (
            self.name == other.name
            and self.ssl == other.ssl
            and self.host == other.host
            and self.port == other.port
            and self.password == other.password
            and self.base_uri == other.base_uri
            and self.status == other.status
        )


class SessionStatus(int, enum.Enum):
    """
    Session Status.

    The status of the session.
    """

    NOT_CONNECTED = 0
    """Not connected to the lavalink server."""
    CONNECTED = 1
    """Successfully connected to the lavalink server."""
    FAILURE = 2
    """A failure occurred connecting to the lavalink server."""
