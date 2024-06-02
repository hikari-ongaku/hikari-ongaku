# ruff: noqa: D100, D101, D102, D103

import datetime
import logging
import typing

import aiohttp
import mock
import orjson
import pytest
from hikari import OwnUser
from hikari.impl import gateway_bot as gateway_bot_
from hikari.snowflakes import Snowflake

from ongaku import Player
from ongaku import errors
from ongaku import events
from ongaku.abc.handler import SessionHandler
from ongaku.abc.session import SessionStatus
from ongaku.client import Client
from ongaku.impl.handlers import BasicSessionHandler
from ongaku.internal import __version__
from ongaku.session import Session
from tests import payloads


@pytest.fixture
def gateway_bot() -> gateway_bot_.GatewayBot:
    return mock.Mock()


@pytest.fixture
def ongaku_client(gateway_bot: gateway_bot_.GatewayBot) -> Client:
    return Client(gateway_bot)


@pytest.fixture
def ongaku_session(ongaku_client: Client) -> Session:
    session = Session(
        ongaku_client, "test_session", False, "127.0.0.1", 2333, "youshallnotpass", 3
    )
    session._authorization_headers = {"Authorization": session.password}

    return session


@pytest.fixture
def bot_user() -> OwnUser:
    return mock.Mock(
        global_name="test_username", username="test_username", id=Snowflake(1234567890)
    )


class TestSession:
    def test_properties(self, ongaku_client: Client):
        session = Session(
            ongaku_client, "test_name", False, "127.0.0.1", 2333, "youshallnotpass", 3
        )

        assert session.client == ongaku_client
        assert session.app == ongaku_client.app
        assert session.name == "test_name"
        assert session.ssl is False
        assert session.host == "127.0.0.1"
        assert session.port == 2333
        assert session.password == "youshallnotpass"
        if session.ssl:
            assert session.base_uri == f"https://{session.host}:{session.port}"
        else:
            assert session.base_uri == f"http://{session.host}:{session.port}"
        assert session.status == SessionStatus.NOT_CONNECTED

    @pytest.mark.asyncio
    async def test_get_session_id(self, ongaku_session: Session):
        # Test valid session id:

        with mock.patch.object(
            ongaku_session,
            "_session_id",
            new_callable=mock.PropertyMock(return_value="session_id"),
        ):
            session_id = ongaku_session._get_session_id()

            assert session_id == "session_id"

        with pytest.raises(errors.SessionStartError):
            session_id = ongaku_session._get_session_id()

    @pytest.mark.asyncio
    async def test_transfer(self, ongaku_client: Client, ongaku_session: Session):
        handler = BasicSessionHandler(ongaku_client)

        player_1 = Player(ongaku_session, Snowflake(1234567891))
        player_2 = Player(ongaku_session, Snowflake(1234567890))

        new_session = Session(
            ongaku_client,
            "test_session_1",
            False,
            "127.0.0.1",
            2333,
            "youshallnotpass",
            3,
        )

        ongaku_session._players = {
            player_1.guild_id: player_1,
            player_2.guild_id: player_2,
        }

        with (
            mock.patch.object(handler, "fetch_session", return_value=new_session),
            mock.patch.object(
                player_1,
                "transfer",
                new_callable=mock.AsyncMock,
                return_value=player_1,
            ) as patched_player_1,
            mock.patch.object(
                player_2,
                "transfer",
                new_callable=mock.AsyncMock,
                return_value=player_2,
            ) as patched_player_2,
        ):
            await ongaku_session.transfer(handler)

            patched_player_1.assert_called_once_with(handler.fetch_session())
            patched_player_2.assert_called_once_with(handler.fetch_session())

            logging.warning(handler.players)

            assert len(handler.players) == 2

            assert handler.players[0].guild_id == player_1.guild_id
            assert handler.players[1].guild_id == player_2.guild_id

    @pytest.mark.asyncio
    async def test_websocket(
        self,
        gateway_bot: gateway_bot_.GatewayBot,
        ongaku_client: Client,
        bot_user: OwnUser,
    ):
        cs = aiohttp.ClientSession()

        # Test working

        with (
            mock.patch.object(gateway_bot, "get_me", return_value=bot_user),
            mock.patch.object(ongaku_client, "_client_session", cs),
            mock.patch.object(
                cs, "ws_connect", new_callable=mock.AsyncMock, return_value=None
            ) as patched_ws_connect,
        ):
            session = Session(
                ongaku_client,
                "test_name",
                False,
                "127.0.0.1",
                2333,
                "youshallnotpass",
                3,
            )
            session._authorization_headers = {"Authorization": session.password}

            me = gateway_bot.get_me()

            assert me is not None

            logging.warning(me.id)
            logging.warning(type(me.id))

            await session._websocket()

            headers = {
                "User-Id": "1234567890",
                "Client-Name": f"test_username/{__version__}",
            }

            headers.update(session.auth_headers)

            patched_ws_connect.assert_called_once_with(
                session.base_uri + "/v4/websocket", headers=headers, autoclose=False
            )

        # Test no bot

        with (
            mock.patch.object(gateway_bot, "get_me", return_value=None),
            pytest.raises(errors.SessionStartError),
        ):
            await session._websocket()

    @pytest.mark.asyncio
    async def test_start(self, ongaku_session: Session):
        with mock.patch.object(
            ongaku_session, "_websocket", new_callable=mock.AsyncMock
        ) as patched_websocket:
            await ongaku_session.start()

            patched_websocket.assert_called_once()

            assert ongaku_session._session_task is not None

    @pytest.mark.asyncio
    async def test_stop(self, ongaku_session: Session):
        with mock.patch.object(
            ongaku_session, "_websocket", new_callable=mock.AsyncMock
        ) as patched_websocket:
            await ongaku_session.start()

            patched_websocket.assert_called_once()

            assert ongaku_session._session_task is not None

            await ongaku_session.stop()

            assert ongaku_session._session_task is None


class TestRequest:
    @pytest.mark.asyncio
    async def test_string(self, ongaku_session: Session):
        cs = aiohttp.ClientSession()

        with (
            mock.patch.object(ongaku_session.client, "_client_session", cs),
            mock.patch.object(
                cs,
                "request",
                new_callable=mock.AsyncMock,
                return_value=mock.AsyncMock(
                    status=200, text=mock.AsyncMock(return_value="text")
                ),
            ) as patched_request,
        ):
            response = await ongaku_session.request("GET", "/string", str)

            patched_request.assert_called_once_with(
                "GET",
                "http://127.0.0.1:2333/v4/string",
                headers=ongaku_session.auth_headers,
                json={},
                params={},
            )

            assert response == "text"

        await cs.close()

    @pytest.mark.asyncio
    async def test_integer(self, ongaku_session: Session):
        cs = aiohttp.ClientSession()

        with (
            mock.patch.object(ongaku_session.client, "_client_session", cs),
            mock.patch.object(
                cs,
                "request",
                new_callable=mock.AsyncMock,
                return_value=mock.AsyncMock(
                    status=200, text=mock.AsyncMock(return_value=1234567890)
                ),
            ) as patched_request,
        ):
            response = await ongaku_session.request("GET", "/integer", int)

            patched_request.assert_called_once_with(
                "GET",
                "http://127.0.0.1:2333/v4/integer",
                headers=ongaku_session.auth_headers,
                json={},
                params={},
            )

            assert isinstance(response, int)
            assert response == 1234567890

        await cs.close()

    @pytest.mark.asyncio
    async def test_float(self, ongaku_session: Session):
        cs = aiohttp.ClientSession()

        with (
            mock.patch.object(ongaku_session.client, "_client_session", cs),
            mock.patch.object(
                cs,
                "request",
                new_callable=mock.AsyncMock,
                return_value=mock.AsyncMock(
                    status=200, text=mock.AsyncMock(return_value=4.2)
                ),
            ) as patched_request,
        ):
            response = await ongaku_session.request("GET", "/float", float)

            patched_request.assert_called_once_with(
                "GET",
                "http://127.0.0.1:2333/v4/float",
                headers=ongaku_session.auth_headers,
                json={},
                params={},
            )

            assert isinstance(response, float)
            assert response == 4.2

        await cs.close()

    @pytest.mark.asyncio
    async def test_boolean(self, ongaku_session: Session):
        cs = aiohttp.ClientSession()

        with (
            mock.patch.object(ongaku_session.client, "_client_session", cs),
            mock.patch.object(
                cs,
                "request",
                new_callable=mock.AsyncMock,
                return_value=mock.AsyncMock(
                    status=200, text=mock.AsyncMock(return_value=True)
                ),
            ) as patched_request,
        ):
            response = await ongaku_session.request("GET", "/boolean", bool)

            patched_request.assert_called_once_with(
                "GET",
                "http://127.0.0.1:2333/v4/boolean",
                headers=ongaku_session.auth_headers,
                json={},
                params={},
            )

            assert isinstance(response, bool)
            assert response is True

        await cs.close()

    @pytest.mark.asyncio
    async def test_dict(self, ongaku_session: Session):
        cs = aiohttp.ClientSession()

        return_dict = {"beanos": "Very cool."}

        with (
            mock.patch.object(ongaku_session.client, "_client_session", cs),
            mock.patch.object(
                cs,
                "request",
                new_callable=mock.AsyncMock,
                return_value=mock.AsyncMock(
                    status=200,
                    text=mock.AsyncMock(
                        return_value=orjson.dumps(return_dict).decode()
                    ),
                ),
            ) as patched_request,
        ):
            response = await ongaku_session.request("GET", "/dict", dict)

            patched_request.assert_called_once_with(
                "GET",
                "http://127.0.0.1:2333/v4/dict",
                headers=ongaku_session.auth_headers,
                json={},
                params={},
            )

            assert isinstance(response, dict)
            assert response == return_dict

        await cs.close()

    @pytest.mark.asyncio
    async def test_list(self, ongaku_session: Session):
        cs = aiohttp.ClientSession()

        return_list = ["beanos", "are", "very", "cool"]

        with (
            mock.patch.object(ongaku_session.client, "_client_session", cs),
            mock.patch.object(
                cs,
                "request",
                new_callable=mock.AsyncMock,
                return_value=mock.AsyncMock(
                    status=200,
                    text=mock.AsyncMock(
                        return_value=orjson.dumps(return_list).decode()
                    ),
                ),
            ) as patched_request,
        ):
            response = await ongaku_session.request("GET", "/list", list)

            patched_request.assert_called_once_with(
                "GET",
                "http://127.0.0.1:2333/v4/list",
                headers=ongaku_session.auth_headers,
                json={},
                params={},
            )

            assert isinstance(response, list)
            assert response == return_list

        await cs.close()

    @pytest.mark.asyncio
    async def test_tuple(self, ongaku_session: Session):
        cs = aiohttp.ClientSession()

        return_tuple = ("beanos", "are", "very", "cool")

        with (
            mock.patch.object(ongaku_session.client, "_client_session", cs),
            mock.patch.object(
                cs,
                "request",
                new_callable=mock.AsyncMock,
                return_value=mock.AsyncMock(
                    status=200,
                    text=mock.AsyncMock(
                        return_value=orjson.dumps(return_tuple).decode()
                    ),
                ),
            ) as patched_request,
        ):
            response = await ongaku_session.request("GET", "/tuple", tuple)

            patched_request.assert_called_once_with(
                "GET",
                "http://127.0.0.1:2333/v4/tuple",
                headers=ongaku_session.auth_headers,
                json={},
                params={},
            )

            assert isinstance(response, tuple)
            assert response == return_tuple

        await cs.close()

    @pytest.mark.asyncio
    async def test_none(self, ongaku_session: Session):
        cs = aiohttp.ClientSession()

        with (
            mock.patch.object(ongaku_session.client, "_client_session", cs),
            mock.patch.object(
                cs,
                "request",
                new_callable=mock.AsyncMock,
                return_value=mock.AsyncMock(
                    status=204, text=mock.AsyncMock(return_value="")
                ),
            ) as patched_request,
        ):
            response = await ongaku_session.request("GET", "/none", None)

            patched_request.assert_called_once_with(
                "GET",
                "http://127.0.0.1:2333/v4/none",
                headers=ongaku_session.auth_headers,
                json={},
                params={},
            )

            assert response is None

        await cs.close()

    @pytest.mark.asyncio
    async def test_extra_args(self, ongaku_session: Session):
        cs = aiohttp.ClientSession()

        test_dict = {"fruit": "banana"}

        with (
            mock.patch.object(ongaku_session.client, "_client_session", cs),
            mock.patch.object(
                cs,
                "request",
                new_callable=mock.AsyncMock,
                return_value=mock.AsyncMock(
                    status=204, text=mock.AsyncMock(return_value="")
                ),
            ) as patched_request,
        ):
            # Test extra headers

            response = await ongaku_session.request(
                "GET", "/headers", None, headers=test_dict
            )

            headers = dict(test_dict)

            headers.update(ongaku_session.auth_headers)

            patched_request.assert_called_with(
                "GET",
                "http://127.0.0.1:2333/v4/headers",
                headers=headers,
                json={},
                params={},
            )

            assert response is None

            # Test json payload.

            response = await ongaku_session.request(
                "GET", "/json", None, json=test_dict
            )

            patched_request.assert_called_with(
                "GET",
                "http://127.0.0.1:2333/v4/json",
                headers=ongaku_session.auth_headers,
                json=test_dict,
                params={},
            )

            assert response is None

            # Test extra params

            response = await ongaku_session.request(
                "GET", "/params", None, params=test_dict
            )

            params = dict(test_dict)

            params.update({})

            patched_request.assert_called_with(
                "GET",
                "http://127.0.0.1:2333/v4/params",
                headers=ongaku_session.auth_headers,
                json={},
                params=params,
            )

            assert response is None

        await cs.close()

    @pytest.mark.asyncio
    async def test_errors(self, ongaku_session: Session):
        cs = aiohttp.ClientSession()

        # Return type is a value, but received 204.

        with (
            mock.patch.object(ongaku_session.client, "_client_session", cs),
            mock.patch.object(
                cs,
                "request",
                new_callable=mock.AsyncMock,
                return_value=mock.AsyncMock(
                    status=204, text=mock.AsyncMock(return_value="")
                ),
            ),
            pytest.raises(errors.RestEmptyError),
        ):
            await ongaku_session.request("GET", "/none", str)

        # Response status is 400, and no text.

        with (
            mock.patch.object(ongaku_session.client, "_client_session", cs),
            mock.patch.object(
                cs,
                "request",
                new_callable=mock.AsyncMock,
                return_value=mock.AsyncMock(
                    status=400, reason="reason", text=mock.AsyncMock(return_value="")
                ),
            ),
            pytest.raises(errors.RestStatusError) as rest_status_error_1,
        ):
            await ongaku_session.request("GET", "/none", str)

        assert isinstance(rest_status_error_1.value, errors.RestStatusError)

        assert rest_status_error_1.value.status == 400
        assert rest_status_error_1.value.reason == "reason"

        # Response status is 400, body included, but not a rest error payload.

        with (
            mock.patch.object(ongaku_session.client, "_client_session", cs),
            mock.patch.object(
                cs,
                "request",
                new_callable=mock.AsyncMock,
                return_value=mock.AsyncMock(
                    status=400,
                    reason="reason",
                    text=mock.AsyncMock(return_value="not a rest error payload"),
                ),
            ),
            pytest.raises(errors.RestStatusError) as rest_status_error_2,
        ):
            await ongaku_session.request("GET", "/none", str)

        assert isinstance(rest_status_error_2.value, errors.RestStatusError)

        assert rest_status_error_2.value.status == 400
        assert rest_status_error_2.value.reason == "reason"

        # Response status is 400, body included, and is a rest error.

        with (
            mock.patch.object(ongaku_session.client, "_client_session", cs),
            mock.patch.object(
                cs,
                "request",
                new_callable=mock.AsyncMock,
                return_value=mock.AsyncMock(
                    status=400,
                    reason="reason",
                    text=mock.AsyncMock(
                        return_value=orjson.dumps(payloads.REST_ERROR_PAYLOAD).decode()
                    ),
                ),
            ),
            pytest.raises(errors.RestRequestError) as rest_error_error,
        ):
            await ongaku_session.request("GET", "/none", str)

        assert isinstance(rest_error_error.value, errors.RestRequestError)

        assert rest_error_error.value.timestamp == datetime.datetime.fromtimestamp(
            1 / 1000, datetime.timezone.utc
        )
        assert rest_error_error.value.status == 2
        assert rest_error_error.value.error == "error"
        assert rest_error_error.value.message == "message"
        assert rest_error_error.value.path == "path"
        assert rest_error_error.value.trace == "trace"

        # Response was ok, however a malformed json document was received.

        with (
            mock.patch.object(ongaku_session.client, "_client_session", cs),
            mock.patch.object(
                cs,
                "request",
                new_callable=mock.AsyncMock,
                return_value=mock.AsyncMock(
                    status=200, text=mock.AsyncMock("I am malformed.")
                ),
            ),
            pytest.raises(errors.BuildError) as build_error,
        ):
            await ongaku_session.request("GET", "/none", dict)

        assert isinstance(build_error.value, errors.BuildError)

        await cs.close()


class TestHandleOPCode:
    @pytest.mark.asyncio
    async def test_ready_event(self, ongaku_session: Session):
        event = ongaku_session._handle_op_code(
            orjson.dumps(payloads.READY_PAYLOAD).decode()
        )

        assert isinstance(event, events.ReadyEvent)

    @pytest.mark.asyncio
    async def test_player_update_event(self, ongaku_session: Session):
        event = ongaku_session._handle_op_code(
            orjson.dumps(payloads.PLAYER_UPDATE_PAYLOAD).decode()
        )

        assert isinstance(event, events.PlayerUpdateEvent)

    @pytest.mark.asyncio
    async def test_statistics_event(self, ongaku_session: Session):
        payload = dict(payloads.STATISTICS_PAYLOAD)

        payload.update({"op": "stats"})

        event = ongaku_session._handle_op_code(orjson.dumps(payload).decode())

        assert isinstance(event, events.StatisticsEvent)

    @pytest.mark.asyncio
    async def test_track_start_event(self, ongaku_session: Session):
        event = ongaku_session._handle_op_code(
            orjson.dumps(payloads.TRACK_START_PAYLOAD).decode()
        )

        assert isinstance(event, events.TrackStartEvent)

    @pytest.mark.asyncio
    async def test_track_end_event(self, ongaku_session: Session):
        event = ongaku_session._handle_op_code(
            orjson.dumps(payloads.TRACK_END_PAYLOAD).decode()
        )

        assert isinstance(event, events.TrackEndEvent)

    @pytest.mark.asyncio
    async def test_track_exception_event(self, ongaku_session: Session):
        event = ongaku_session._handle_op_code(
            orjson.dumps(payloads.TRACK_EXCEPTION_PAYLOAD).decode()
        )

        assert isinstance(event, events.TrackExceptionEvent)

    @pytest.mark.asyncio
    async def test_track_stuck_event(self, ongaku_session: Session):
        event = ongaku_session._handle_op_code(
            orjson.dumps(payloads.TRACK_STUCK_PAYLOAD).decode()
        )

        assert isinstance(event, events.TrackStuckEvent)

    @pytest.mark.asyncio
    async def test_websocket_closed_event(self, ongaku_session: Session):
        event = ongaku_session._handle_op_code(
            orjson.dumps(payloads.WEBSOCKET_CLOSED_PAYLOAD).decode()
        )

        assert isinstance(event, events.WebsocketClosedEvent)


class TestHandleWSMessage:
    @pytest.mark.asyncio
    async def test_text(self, ongaku_session: Session):
        payload: typing.Final[typing.Mapping[str, typing.Any]] = {
            "op": "ready",
            "resumed": False,
            "sessionId": "session_id",
        }

        message = aiohttp.WSMessage(
            aiohttp.WSMsgType.TEXT, orjson.dumps(payload).decode(), None
        )

        with (
            mock.patch.object(
                ongaku_session.app,
                "event_manager",
                new_callable=mock.Mock,
                return_value=mock.Mock(),
            ),
            mock.patch.object(
                ongaku_session.app.event_manager,
                "dispatch",
                new_callable=mock.AsyncMock,
                return_value=None,
            ) as event_dispatched,
        ):
            await ongaku_session._handle_ws_message(message)

            assert len(event_dispatched.call_args_list) == 2

            first_event_args = event_dispatched.call_args_list[0].args

            assert len(first_event_args) == 1

            assert isinstance(first_event_args[0], events.PayloadEvent)

            first_event_args = event_dispatched.call_args_list[1].args

            assert len(first_event_args) == 1

            assert isinstance(first_event_args[0], events.ReadyEvent)

    @pytest.mark.asyncio
    async def test_error(self, ongaku_session: Session):
        message = aiohttp.WSMessage(aiohttp.WSMsgType.ERROR, "", None)

        with mock.patch.object(ongaku_session, "transfer") as patched_transfer:
            assert ongaku_session.status == SessionStatus.NOT_CONNECTED

            await ongaku_session._handle_ws_message(message)

            assert ongaku_session.status == SessionStatus.FAILURE

            args = patched_transfer.call_args.args

            assert len(args) == 1

            assert isinstance(args[0], SessionHandler)

            assert args[0] == ongaku_session.client.session_handler

    @pytest.mark.asyncio
    async def test_closed(self, ongaku_session: Session):
        message = aiohttp.WSMessage(
            aiohttp.WSMsgType.CLOSED, aiohttp.WSCloseCode.GOING_AWAY, "extra"
        )

        with mock.patch.object(ongaku_session, "transfer") as patched_transfer:
            assert ongaku_session.status == SessionStatus.NOT_CONNECTED

            await ongaku_session._handle_ws_message(message)

            assert ongaku_session.status == SessionStatus.FAILURE

            args = patched_transfer.call_args.args

            assert len(args) == 1

            assert isinstance(args[0], SessionHandler)

            assert args[0] == ongaku_session.client.session_handler
