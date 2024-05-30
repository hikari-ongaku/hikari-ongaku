# ruff: noqa: D100, D101, D102, D103

import mock
import pytest
from aiohttp import ClientSession
from arc.client import GatewayClient as ArcGatewayClient
from hikari.events import StartedEvent
from hikari.impl import gateway_bot as gateway_bot_
from hikari.snowflakes import Snowflake
from tanjun.clients import Client as TanjunClient

from ongaku import Player
from ongaku.client import Client
from ongaku.errors import PlayerMissingError
from ongaku.rest import RESTClient
from ongaku.session import Session


@pytest.fixture
def gateway_bot() -> gateway_bot_.GatewayBot:
    return gateway_bot_.GatewayBot("", banner=None, suppress_optimization_warning=True)


@pytest.fixture
def ongaku_client(gateway_bot: gateway_bot_.GatewayBot) -> Client:
    return Client(gateway_bot)


@pytest.fixture
def ongaku_session(ongaku_client: Client) -> Session:
    return Session(
        ongaku_client, "test_session", False, "127.0.0.1", 2333, "youshallnotpass", 3
    )


class TestClient:
    def test_from_arc(self, gateway_bot: gateway_bot_.GatewayBot):
        command_client = ArcGatewayClient(gateway_bot)

        client = Client.from_arc(command_client)

        assert client.app == gateway_bot

        assert client.is_alive is False

        assert isinstance(client.rest, RESTClient)

    def test_from_tanjun(self, gateway_bot: gateway_bot_.GatewayBot):
        command_client = TanjunClient.from_gateway_bot(gateway_bot)

        client = Client.from_tanjun(command_client)

        assert client.app == gateway_bot

        assert client.is_alive is False

        assert isinstance(client.rest, RESTClient)

    @pytest.mark.asyncio
    async def test_properties(self, gateway_bot: gateway_bot_.GatewayBot):
        client = Client(gateway_bot)

        assert client.app == gateway_bot

        assert isinstance(client.rest, RESTClient)

        assert isinstance(client.is_alive, bool)
        assert client.is_alive is False

    @pytest.mark.asyncio
    async def test_get_client_session(self, gateway_bot: gateway_bot_.GatewayBot):
        client = Client(gateway_bot)

        assert isinstance(client._get_client_session(), ClientSession)

    @pytest.mark.asyncio
    async def test_player_create(
        self, gateway_bot: gateway_bot_.GatewayBot, ongaku_session: Session
    ):
        client = Client(gateway_bot)

        await gateway_bot.dispatch(StartedEvent(app=gateway_bot))

        with mock.patch.object(
            client.session_handler, "fetch_session", return_value=ongaku_session
        ):
            player = await client.create_player(1234567890)

        assert isinstance(player, Player)

        assert player.guild_id == Snowflake(1234567890)

    @pytest.mark.asyncio
    async def test_player_fetch(
        self, gateway_bot: gateway_bot_.GatewayBot, ongaku_session: Session
    ):
        client = Client(gateway_bot)

        await gateway_bot.dispatch(StartedEvent(app=gateway_bot))

        with mock.patch.object(
            client.session_handler, "fetch_session", return_value=ongaku_session
        ):
            await client.create_player(1234567890)

        player = client.fetch_player(1234567890)

        assert isinstance(player, Player)

        assert player.guild_id == Snowflake(1234567890)

    @pytest.mark.asyncio
    async def test_player_delete(
        self, gateway_bot: gateway_bot_.GatewayBot, ongaku_session: Session
    ):
        client = Client(gateway_bot)

        await gateway_bot.dispatch(StartedEvent(app=gateway_bot))

        with mock.patch.object(
            client.session_handler, "fetch_session", return_value=ongaku_session
        ):
            await client.create_player(1234567890)

        player = client.fetch_player(1234567890)

        assert isinstance(player, Player)

        assert player.guild_id == Snowflake(1234567890)

        with mock.patch.object(player, "disconnect", return_value=None):
            await client.delete_player(1234567890)

        with pytest.raises(PlayerMissingError):
            client.fetch_player(1234567890)
