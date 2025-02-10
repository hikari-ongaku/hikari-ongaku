import datetime
import typing

import aiohttp
import mock
import orjson
import pytest
from aiohttp import web
from hikari import OwnUser
from hikari.impl import gateway_bot as gateway_bot_
from hikari.snowflakes import Snowflake

import ongaku
from ongaku import errors
from ongaku import events
from ongaku.abc.session import SessionStatus
from ongaku.client import Client
from ongaku.player import Player
from ongaku.session import Session
from tests import payloads
from tests.conftest import FakeEvent
from tests.conftest import OngakuExtension


class TestSession:
    def test_properties(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_name",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
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

        assert session.auth_headers == {"Authorization": session.password}

        assert session.status == SessionStatus.NOT_CONNECTED

    @pytest.mark.asyncio
    async def test__get_session_id(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_name",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        with mock.patch(
            "ongaku.session.Session._session_id",
            new_callable=mock.PropertyMock,
            return_value="session_id",
        ):
            session_id = session._get_session_id()

            assert session_id == "session_id"

        with pytest.raises(errors.SessionStartError):
            session_id = session._get_session_id()

    @pytest.mark.asyncio
    async def test_transfer(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_name",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        handler = mock.Mock()

        player_1 = Player(session, Snowflake(1234567891))
        player_2 = Player(session, Snowflake(1234567890))

        new_session = Session(
            ongaku_client,
            name="test_session_1",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )
        session._players = {
            player_1.guild_id: player_1,
            player_2.guild_id: player_2,
        }

        handler.players = tuple(session._players.values())

        with (
            mock.patch.object(handler, "fetch_session", return_value=new_session) as patched_fetch_session,
            mock.patch(
                "ongaku.player.Player.transfer",
            ) as patched_player_transfer,
        ):
            await session.transfer(handler)

            patched_player_transfer.assert_called_with(session=handler.fetch_session())

            assert patched_player_transfer.call_count == 2

            assert len(handler.players) == 2

            assert handler.players[0].guild_id == player_1.guild_id
            assert handler.players[1].guild_id == player_2.guild_id

    @staticmethod
    async def handler(request: web.Request):
        assert request.url.path == "/v4/websocket"

        assert request.headers.get("User-Id", None) == "1234567890"
        assert (
            request.headers.get("Client-Name", None)
            == f"test_username/{ongaku.__version__}"
        )
        assert request.headers.get("Authorization", None) == "password"

        ws = web.WebSocketResponse()
        await ws.prepare(request)
        await ws.send_str(orjson.dumps(payloads.READY_PAYLOAD).decode())

        await ws.close()

        return ws

    @pytest.mark.asyncio
    async def test__websocket(
        self,
        gateway_bot: gateway_bot_.GatewayBot,
        bot_user: OwnUser,
        aiohttp_client: typing.Any,
    ):
        ongaku_client = Client(gateway_bot)

        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="password",
        )

        app = web.Application()
        app.router.add_route("GET", "/v4/websocket", self.handler)

        client = await aiohttp_client(app)

        with (
            mock.patch.object(gateway_bot, "get_me", return_value=bot_user) as patched_get_me,
            mock.patch("ongaku.client.Client._get_client_session", return_value=client) as patched_get_client_session,
            mock.patch.object(
                session,
                "_base_uri",
                new_callable=mock.PropertyMock(return_value=""),
            ),
            mock.patch.object(
                gateway_bot.event_manager,
                "dispatch",
                new_callable=mock.AsyncMock,
                return_value=None,
            ) as patched_dispatch,
            mock.patch("ongaku.session.Session.transfer") as patched_transfer,
        ):
            await session._websocket()

            assert patched_dispatch.call_count == 2

            first_event, second_event = patched_dispatch.call_args_list

            assert len(first_event.args) == 1

            assert isinstance(first_event.args[0], events.PayloadEvent)

            assert len(second_event.args) == 1

            assert isinstance(second_event.args[0], events.ReadyEvent)

            patched_transfer.assert_called_once_with(ongaku_client.session_handler)

    @pytest.mark.asyncio
    async def test_start(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        with mock.patch(
            "ongaku.session.Session._websocket", new_callable=mock.AsyncMock
        ) as patched_websocket:
            await session.start()

            patched_websocket.assert_called_once()

            assert session._session_task is not None

    @pytest.mark.asyncio
    async def test_stop(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        with mock.patch(
            "ongaku.session.Session._websocket", new_callable=mock.AsyncMock
        ) as patched_websocket:
            await session.start()

            patched_websocket.assert_called_once()

            assert session._session_task is not None

            await session.stop()

            assert session._session_task is None


class TestRequest:
    @pytest.mark.asyncio
    async def test_return_string(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        cs = aiohttp.ClientSession()

        with (
            mock.patch.object(session.client, "_client_session", cs),
            mock.patch.object(
                cs,
                "request",
                new_callable=mock.AsyncMock,
                return_value=mock.AsyncMock(
                    status=200, text=mock.AsyncMock(return_value="text")
                ),
            ) as patched_request,
        ):
            response = await session.request("GET", "/string", str)

            patched_request.assert_called_once_with(
                "GET",
                session.base_uri + "/v4/string",
                headers=session.auth_headers,
                json={},
                params={},
            )

            assert response == "text"

        await cs.close()

    @pytest.mark.asyncio
    async def test_return_integer(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        cs = aiohttp.ClientSession()

        with (
            mock.patch.object(session.client, "_client_session", cs),
            mock.patch.object(
                cs,
                "request",
                new_callable=mock.AsyncMock,
                return_value=mock.AsyncMock(
                    status=200, text=mock.AsyncMock(return_value=1234567890)
                ),
            ) as patched_request,
        ):
            response = await session.request("GET", "/integer", int)

            patched_request.assert_called_once_with(
                "GET",
                session.base_uri + "/v4/integer",
                headers=session.auth_headers,
                json={},
                params={},
            )

            assert isinstance(response, int)
            assert response == 1234567890

        await cs.close()

    @pytest.mark.asyncio
    async def test_return_float(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        cs = aiohttp.ClientSession()

        with (
            mock.patch.object(session.client, "_client_session", cs),
            mock.patch.object(
                cs,
                "request",
                new_callable=mock.AsyncMock,
                return_value=mock.AsyncMock(
                    status=200, text=mock.AsyncMock(return_value=4.2)
                ),
            ) as patched_request,
        ):
            response = await session.request("GET", "/float", float)

            patched_request.assert_called_once_with(
                "GET",
                session.base_uri + "/v4/float",
                headers=session.auth_headers,
                json={},
                params={},
            )

            assert isinstance(response, float)
            assert response == 4.2

        await cs.close()

    @pytest.mark.asyncio
    async def test_return_boolean(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        cs = aiohttp.ClientSession()

        with (
            mock.patch.object(session.client, "_client_session", cs),
            mock.patch.object(
                cs,
                "request",
                new_callable=mock.AsyncMock,
                return_value=mock.AsyncMock(
                    status=200, text=mock.AsyncMock(return_value=True)
                ),
            ) as patched_request,
        ):
            response = await session.request("GET", "/boolean", bool)

            patched_request.assert_called_once_with(
                "GET",
                session.base_uri + "/v4/boolean",
                headers=session.auth_headers,
                json={},
                params={},
            )

            assert isinstance(response, bool)
            assert response is True

        await cs.close()

    @pytest.mark.asyncio
    async def test_return_dict(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        cs = aiohttp.ClientSession()

        return_dict = {"beanos": "Very cool."}

        with (
            mock.patch.object(session.client, "_client_session", cs),
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
            response = await session.request("GET", "/dict", dict)

            patched_request.assert_called_once_with(
                "GET",
                session.base_uri + "/v4/dict",
                headers=session.auth_headers,
                json={},
                params={},
            )

            assert isinstance(response, dict)
            assert response == return_dict

        await cs.close()

    @pytest.mark.asyncio
    async def test_return_list(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        cs = aiohttp.ClientSession()

        return_list = ["beanos", "are", "very", "cool"]

        with (
            mock.patch.object(session.client, "_client_session", cs),
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
            response = await session.request("GET", "/list", list)

            patched_request.assert_called_once_with(
                "GET",
                session.base_uri + "/v4/list",
                headers=session.auth_headers,
                json={},
                params={},
            )

            assert isinstance(response, list)
            assert response == return_list

        await cs.close()

    @pytest.mark.asyncio
    async def test_return_tuple(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        cs = aiohttp.ClientSession()

        return_tuple = ("beanos", "are", "very", "cool")

        with (
            mock.patch.object(session.client, "_client_session", cs),
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
            response = await session.request("GET", "/tuple", tuple)

            patched_request.assert_called_once_with(
                "GET",
                session.base_uri + "/v4/tuple",
                headers=session.auth_headers,
                json={},
                params={},
            )

            assert isinstance(response, tuple)
            assert response == return_tuple

        await cs.close()

    @pytest.mark.asyncio
    async def test_return_none(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        cs = aiohttp.ClientSession()

        with (
            mock.patch.object(session.client, "_client_session", cs),
            mock.patch.object(
                cs,
                "request",
                new_callable=mock.AsyncMock,
                return_value=mock.AsyncMock(
                    status=204, text=mock.AsyncMock(return_value=None)
                ),
            ) as patched_request,
        ):
            response = await session.request("GET", "/none", None)

            patched_request.assert_called_once_with(
                "GET",
                session.base_uri + "/v4/none",
                headers=session.auth_headers,
                json={},
                params={},
            )

            assert response is None

        await cs.close()

    @pytest.mark.asyncio
    async def test_headers(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        cs = aiohttp.ClientSession()

        test_headers = {"fruit": "banana"}

        with (
            mock.patch.object(session.client, "_client_session", cs),
            mock.patch.object(
                cs,
                "request",
                new_callable=mock.AsyncMock,
                return_value=mock.AsyncMock(
                    status=204, text=mock.AsyncMock(return_value="")
                ),
            ) as patched_request,
        ):
            response = await session.request("GET", "/headers", None, headers=test_headers)

            headers = dict(test_headers)

            headers.update(session.auth_headers)

            patched_request.assert_called_with(
                "GET",
                session.base_uri + "/v4/headers",
                headers=headers,
                json={},
                params={},
            )

            assert response is None

        await cs.close()

    @pytest.mark.asyncio
    async def test_json(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        cs = aiohttp.ClientSession()

        test_json = {"fruit": "banana"}

        with (
            mock.patch.object(session.client, "_client_session", cs),
            mock.patch.object(
                cs,
                "request",
                new_callable=mock.AsyncMock,
                return_value=mock.AsyncMock(
                    status=204, text=mock.AsyncMock(return_value="")
                ),
            ) as patched_request,
        ):
            response = await session.request("GET", "/json", None, json=test_json)

            patched_request.assert_called_with(
                "GET",
                session.base_uri + "/v4/json",
                headers=session.auth_headers,
                json=test_json,
                params={},
            )

            assert response is None

        await cs.close()

    @pytest.mark.asyncio
    async def test_params(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        cs = aiohttp.ClientSession()

        test_params = {"fruit": "banana"}

        with (
            mock.patch.object(session.client, "_client_session", cs),
            mock.patch.object(
                cs,
                "request",
                new_callable=mock.AsyncMock,
                return_value=mock.AsyncMock(
                    status=204, text=mock.AsyncMock(return_value="")
                ),
            ) as patched_request,
        ):
            response = await session.request("GET", "/params", None, params=test_params)

            params = dict(test_params)

            params.update({})

            patched_request.assert_called_with(
                "GET",
                session.base_uri + "/v4/params",
                headers=session.auth_headers,
                json={},
                params=params,
            )

            assert response is None

        await cs.close()

    @pytest.mark.asyncio
    async def test_rest_status_error(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        cs = aiohttp.ClientSession()

        with (
            mock.patch.object(session.client, "_client_session", cs),
            mock.patch.object(
                cs,
                "request",
                new_callable=mock.AsyncMock,
                return_value=mock.AsyncMock(
                    status=400, reason="reason", text=mock.AsyncMock(return_value="")
                ),
            ) as patched_request,
            pytest.raises(errors.RestStatusError) as patched_rest_error,
        ):
            await session.request("GET", "/error", str)

        assert isinstance(patched_rest_error.value, errors.RestStatusError)

        assert patched_rest_error.value.status == 400
        assert patched_rest_error.value.reason == "reason"

        patched_request.assert_called_once_with(
            "GET",
            "http://127.0.0.1:2333/v4/error",
            headers={"Authorization": "youshallnotpass"},
            json={},
            params={}
        )

        await cs.close()

    @pytest.mark.asyncio
    async def test_rest_request_error(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        cs = aiohttp.ClientSession()

        with (
            mock.patch.object(session.client, "_client_session", cs),
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
            ) as patched_request,
            pytest.raises(errors.RestRequestError) as patched_rest_error,
        ):
            await session.request("GET", "/error", str)

        assert isinstance(patched_rest_error.value, errors.RestRequestError)

        patched_request.assert_called_once_with(
            "GET",
            "http://127.0.0.1:2333/v4/error",
            headers={"Authorization": "youshallnotpass"},
            json={},
            params={}
        )

        assert patched_rest_error.value.timestamp == datetime.datetime.fromtimestamp(
            1 / 1000, datetime.timezone.utc
        )
        assert patched_rest_error.value.status == 2
        assert patched_rest_error.value.error == "error"
        assert patched_rest_error.value.message == "message"
        assert patched_rest_error.value.path == "path"
        assert patched_rest_error.value.trace == "trace"

        await cs.close()

    @pytest.mark.asyncio
    async def test_build_error(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        cs = aiohttp.ClientSession()

        with (
            mock.patch.object(session.client, "_client_session", cs),
            mock.patch.object(
                cs,
                "request",
                new_callable=mock.AsyncMock,
                return_value=mock.AsyncMock(
                    status=200, text=mock.AsyncMock("I am malformed.")
                ),
            ) as patched_request,
            pytest.raises(errors.BuildError) as patched_build_error,
        ):
            await session.request("GET", "/error", dict)

        patched_request.assert_called_once_with(
            "GET",
            "http://127.0.0.1:2333/v4/error",
            headers={"Authorization": "youshallnotpass"},
            json={},
            params={}
        )

        assert isinstance(patched_build_error.value, errors.BuildError)

        await cs.close()

    @pytest.mark.asyncio
    async def test_optional_without_response_with_optional_with_type(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        cs = aiohttp.ClientSession()

        with (
            mock.patch.object(session.client, "_client_session", cs),
            mock.patch.object(
                cs,
                "request",
                new_callable=mock.AsyncMock,
                return_value=mock.AsyncMock(
                    status=204,
                    text=mock.AsyncMock(
                        return_value=None
                    ),
                ),
            ) as patched_request,
        ):
            response = await session.request(
                "GET",
                "/none",
                str,
                optional=True
            )

            assert response == None

            patched_request.assert_called_with(
                "GET",
                session.base_uri + "/v4/none",
                headers=session.auth_headers,
                json={},
                params={}
            )
        
        await cs.close()

    @pytest.mark.asyncio
    async def test_optional_without_response_without_optional_with_type(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        cs = aiohttp.ClientSession()

        with (
            mock.patch.object(session.client, "_client_session", cs),
            mock.patch.object(
                cs,
                "request",
                new_callable=mock.AsyncMock,
                return_value=mock.AsyncMock(
                    status=204,
                    text=mock.AsyncMock(
                        return_value=None
                    ),
                ),
            ) as patched_request,
        ):
            with pytest.raises(errors.RestEmptyError):
                await session.request(
                    "GET",
                    "/none",
                    str,
                    optional=False
                )            

            patched_request.assert_called_with(
                "GET",
                session.base_uri + "/v4/none",
                headers=session.auth_headers,
                json={},
                params={}
            )
        
        await cs.close()

    @pytest.mark.asyncio
    async def test_optional_without_response_without_optional_without_type(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        cs = aiohttp.ClientSession()
        
        with (
            mock.patch.object(session.client, "_client_session", cs),
            mock.patch.object(
                cs,
                "request",
                new_callable=mock.AsyncMock,
                return_value=mock.AsyncMock(
                    status=204,
                    text=mock.AsyncMock(
                        return_value=None
                    ),
                ),
            ) as patched_request,
        ):
            response = await session.request(
                "GET",
                "/none",
                None,
                optional=False
            )

            assert response == None

            patched_request.assert_called_with(
                "GET",
                session.base_uri + "/v4/none",
                headers=session.auth_headers,
                json={},
                params={}
            )
        
        await cs.close()

    @pytest.mark.asyncio
    async def test_optional_with_response_with_optional_with_type(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        cs = aiohttp.ClientSession()

        with (
            mock.patch.object(session.client, "_client_session", cs),
            mock.patch.object(
                cs,
                "request",
                new_callable=mock.AsyncMock,
                return_value=mock.AsyncMock(
                    status=200,
                    text=mock.AsyncMock(
                        return_value="cool string"
                    ),
                ),
            ) as patched_request,
        ):
            response = await session.request(
                "GET",
                "/none",
                str,
                optional=True
            )

            assert response == "cool string"

            patched_request.assert_called_with(
                "GET",
                session.base_uri + "/v4/none",
                headers=session.auth_headers,
                json={},
                params={}
            )
        
        await cs.close()

    @pytest.mark.asyncio
    async def test_optional_with_response_without_optional_with_type(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        cs = aiohttp.ClientSession()

        with (
            mock.patch.object(session.client, "_client_session", cs),
            mock.patch.object(
                cs,
                "request",
                new_callable=mock.AsyncMock,
                return_value=mock.AsyncMock(
                    status=200,
                    text=mock.AsyncMock(
                        return_value="cool string"
                    ),
                ),
            ) as patched_request,
        ):
            response = await session.request(
                "GET",
                "/none",
                str,
                optional=False
            )

            assert response == "cool string"

            patched_request.assert_called_with(
                "GET",
                session.base_uri + "/v4/none",
                headers=session.auth_headers,
                json={},
                params={}
            )
        
        await cs.close()

    @pytest.mark.asyncio
    async def test_optional_with_response_without_optional_without_type(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        cs = aiohttp.ClientSession()

        with (
            mock.patch.object(session.client, "_client_session", cs),
            mock.patch.object(
                cs,
                "request",
                new_callable=mock.AsyncMock,
                return_value=mock.AsyncMock(
                    status=200,
                    text=mock.AsyncMock(
                        return_value="cool string"
                    ),
                ),
            ) as patched_request,
        ):
            response = await session.request(
                "GET",
                "/none",
                None,
                optional=False
            )

            assert response == None

            patched_request.assert_called_with(
                "GET",
                session.base_uri + "/v4/none",
                headers=session.auth_headers,
                json={},
                params={}
            )
        
        await cs.close()


class TestHandleOPCode:
    @pytest.mark.asyncio
    async def test_ready_event(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        event = session._handle_op_code(orjson.dumps(payloads.READY_PAYLOAD).decode())

        assert isinstance(event, events.ReadyEvent)

    @pytest.mark.asyncio
    async def test_player_update_event(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        event = session._handle_op_code(
            orjson.dumps(payloads.PLAYER_UPDATE_PAYLOAD).decode()
        )

        assert isinstance(event, events.PlayerUpdateEvent)

    @pytest.mark.asyncio
    async def test_statistics_event(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        payload = dict(payloads.STATISTICS_PAYLOAD)

        payload.update({"op": "stats"})

        event = session._handle_op_code(orjson.dumps(payload).decode())

        assert isinstance(event, events.StatisticsEvent)

    @pytest.mark.asyncio
    async def test_track_start_event(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        event = session._handle_op_code(
            orjson.dumps(payloads.TRACK_START_PAYLOAD).decode()
        )

        assert isinstance(event, events.TrackStartEvent)

    @pytest.mark.asyncio
    async def test_track_end_event(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        event = session._handle_op_code(
            orjson.dumps(payloads.TRACK_END_PAYLOAD).decode()
        )

        assert isinstance(event, events.TrackEndEvent)

    @pytest.mark.asyncio
    async def test_track_exception_event(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        event = session._handle_op_code(
            orjson.dumps(payloads.TRACK_EXCEPTION_PAYLOAD).decode()
        )

        assert isinstance(event, events.TrackExceptionEvent)

    @pytest.mark.asyncio
    async def test_track_stuck_event(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        event = session._handle_op_code(
            orjson.dumps(payloads.TRACK_STUCK_PAYLOAD).decode()
        )

        assert isinstance(event, events.TrackStuckEvent)

    @pytest.mark.asyncio
    async def test_websocket_closed_event(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        event = session._handle_op_code(
            orjson.dumps(payloads.WEBSOCKET_CLOSED_PAYLOAD).decode()
        )

        assert isinstance(event, events.WebsocketClosedEvent)

    @pytest.mark.asyncio
    async def test_unknown_op(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        event = session._handle_op_code(
            orjson.dumps(
                {
                    "op": "banana",
                }
            ).decode()
        )

        assert event is None

    @pytest.mark.asyncio
    async def test_unknown_event(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        event = session._handle_op_code(
            orjson.dumps({"op": "event", "type": "banana"}).decode()
        )

        assert event is None

    @pytest.mark.asyncio
    async def test_extension_event(
        self, ongaku_client: Client, ongaku_extension: OngakuExtension
    ):
        ongaku_client._extensions = {OngakuExtension: ongaku_extension}

        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        event = session._handle_op_code(
            orjson.dumps({"op": "event", "type": "banana"}).decode()
        )

        assert isinstance(event, FakeEvent)


class TestHandleWSMessage:
    @pytest.mark.asyncio
    async def test_text(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        message = aiohttp.WSMessage(
            aiohttp.WSMsgType.TEXT, orjson.dumps(payloads.READY_PAYLOAD).decode(), None
        )

        with (
            mock.patch.object(
                session.app,
                "event_manager",
                new_callable=mock.Mock,
            ),
            mock.patch.object(
                session.app.event_manager,
                "dispatch",
                new_callable=mock.AsyncMock,
                return_value=None,
            ) as patched_event_dispatch,
        ):
            assert await session._handle_ws_message(message) is True

            assert patched_event_dispatch.call_count == 2

            
            first_event, second_event = patched_event_dispatch.call_args_list

            assert len(first_event.args) == 1

            assert isinstance(first_event.args[0], events.PayloadEvent)

            assert len(second_event.args) == 1

            assert isinstance(second_event.args[0], events.ReadyEvent)

    @pytest.mark.asyncio
    async def test_error(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        message = aiohttp.WSMessage(aiohttp.WSMsgType.ERROR, "", None)

        assert await session._handle_ws_message(message) is False

    @pytest.mark.asyncio
    async def test_closed(self, ongaku_client: Client):
        session = Session(
            ongaku_client,
            name="test_session",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
        )

        message = aiohttp.WSMessage(
            aiohttp.WSMsgType.CLOSED, aiohttp.WSCloseCode.GOING_AWAY, "extra"
        )

        assert await session._handle_ws_message(message) is False
