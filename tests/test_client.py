# ruff: noqa: D100, D101, D102, D103

import arc
import mock
import pytest
from aiohttp import ClientSession
from arc.client import GatewayClient as ArcGatewayClient
from hikari.events.base_events import Event as Event
from hikari.impl import gateway_bot as gateway_bot_
from hikari.snowflakes import Snowflake
from tanjun.clients import Client as TanjunClient

from ongaku import errors
from ongaku.abc.handler import SessionHandler
from ongaku.builders import EntityBuilder
from ongaku.client import Client
from ongaku.player import Player
from ongaku.rest import RESTClient
from ongaku.session import Session
from tests.conftest import OngakuExtension


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

    def test_properties(self, gateway_bot: gateway_bot_.GatewayBot):
        client = Client(gateway_bot)

        assert client.app == gateway_bot

        assert isinstance(client.rest, RESTClient)

        assert client.is_alive is False

        assert isinstance(client.entity_builder, EntityBuilder)

        assert isinstance(client.session_handler, SessionHandler)

    @pytest.mark.asyncio
    async def test_get_client_session(self, gateway_bot: gateway_bot_.GatewayBot):
        client = Client(gateway_bot)

        with (
            mock.patch(
                "ongaku.impl.handlers.BasicSessionHandler.start"
            ) as patched_start,
            mock.patch(
                "ongaku.impl.handlers.BasicSessionHandler._is_alive", return_value=True
            ),
        ):
            await client._start_event(mock.Mock())

            assert client.is_alive is True

            patched_start.assert_called_once()

            assert isinstance(client._get_client_session(), ClientSession)

    @pytest.mark.asyncio
    async def test_start_event(
        self,
        gateway_bot: gateway_bot_.GatewayBot,
    ):
        client = Client(gateway_bot)

        with mock.patch(
            "ongaku.impl.handlers.BasicSessionHandler.start"
        ) as patched_start:
            await client._start_event(mock.Mock())

            patched_start.assert_called_once()

    @pytest.mark.asyncio
    async def test_stop_event(
        self,
        gateway_bot: gateway_bot_.GatewayBot,
    ):
        client = Client(gateway_bot)

        with (
            mock.patch("ongaku.impl.handlers.BasicSessionHandler.stop") as patched_stop,
            mock.patch("ongaku.client.Client._client_session", mock.AsyncMock()),
            mock.patch.object(client._client_session, "close") as patched_close,
        ):
            await client._stop_event(mock.Mock())

            patched_stop.assert_called_once()
            patched_close.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_session(
        self, gateway_bot: gateway_bot_.GatewayBot, ongaku_session: Session
    ):
        client = Client(gateway_bot)

        with (
            mock.patch.object(client, "_session_handler"),
            mock.patch.object(
                client.session_handler,
                "add_session",
                return_value=ongaku_session,
            ) as patched_add_session,
        ):
            client.create_session("test_session", ssl=False, host="127.0.0.1")

            patched_add_session.assert_called_once()

    @pytest.mark.asyncio
    async def test_player_create(
        self,
        gateway_bot: gateway_bot_.GatewayBot,
        ongaku_session: Session,
        ongaku_player: Player,
    ):
        client = Client(gateway_bot)

        # Create a new player.

        with (
            mock.patch.object(client, "_session_handler"),
            mock.patch.object(
                client.session_handler, "fetch_session", return_value=ongaku_session
            ),
            mock.patch.object(
                client.session_handler,
                "fetch_player",
                side_effect=errors.PlayerMissingError,
            ),
            mock.patch.object(
                client.session_handler,
                "add_player",
                return_value=mock.Mock(guild_id=Snowflake(1234567890)),
            ) as patched_add_player,
        ):
            player = client.create_player(1234567890)

            patched_add_player.assert_called_once()

            assert player.guild_id == Snowflake(1234567890)

        # Create an existing player.

        with (
            mock.patch.object(client, "_session_handler"),
            mock.patch.object(
                client.session_handler, "fetch_session", return_value=ongaku_session
            ),
            mock.patch.object(
                client.session_handler, "fetch_player", return_value=ongaku_player
            ),
            mock.patch.object(
                client.session_handler,
                "add_player",
                return_value=mock.Mock(guild_id=Snowflake(1234567890)),
            ) as patched_add_player,
        ):
            player = client.create_player(1234567890)

            assert player == ongaku_player

            patched_add_player.assert_not_called()

    @pytest.mark.asyncio
    async def test_player_fetch(
        self,
        gateway_bot: gateway_bot_.GatewayBot,
        ongaku_player: Player,
    ):
        client = Client(gateway_bot)

        client.session_handler.add_player(player=ongaku_player)

        player = client.fetch_player(1234567890)

        assert player.guild_id == Snowflake(1234567890)

        with mock.patch.object(
            ongaku_player, "disconnect", new_callable=mock.AsyncMock, return_value=None
        ):
            await client.session_handler.delete_player(guild=Snowflake(1234567890))

        with pytest.raises(errors.PlayerMissingError):
            client.fetch_player(1234567890)

    @pytest.mark.asyncio
    async def test_player_delete(
        self, gateway_bot: gateway_bot_.GatewayBot, ongaku_session: Session
    ):
        client = Client(gateway_bot)

        with (
            mock.patch.object(client, "_session_handler", return_value=ongaku_session),
            mock.patch.object(
                client.session_handler,
                "delete_player",
                new_callable=mock.AsyncMock,
                return_value=None,
            ) as patched_delete_player,
        ):
            await client.delete_player(Snowflake(1234567890))

            patched_delete_player.assert_called_once_with(guild=Snowflake(1234567890))

    def test_add_extension(self, gateway_bot: gateway_bot_.GatewayBot, ongaku_extension: OngakuExtension):
        client = Client(gateway_bot)

        assert client._extensions == {}

        client.add_extension(OngakuExtension, ongaku_extension)

        assert client._extensions == {OngakuExtension: ongaku_extension}

    def test_get_extension(self, gateway_bot: gateway_bot_.GatewayBot, ongaku_extension: OngakuExtension):
        client = Client(gateway_bot)

        client._extensions = {OngakuExtension: ongaku_extension}

        assert client.get_extension(OngakuExtension) == ongaku_extension

    def test_delete_extension(self, gateway_bot: gateway_bot_.GatewayBot, ongaku_extension: OngakuExtension):
        client = Client(gateway_bot)

        client._extensions = {OngakuExtension: ongaku_extension}

        client.delete_extension(OngakuExtension)

        assert client._extensions == {}


class TestArcPlayerInjector:
    @pytest.mark.asyncio
    async def test_working(
        self, gateway_bot: gateway_bot_.GatewayBot, ongaku_player: Player
    ):
        client = Client(gateway_bot)

        context: arc.GatewayContext = mock.Mock()

        inj_context: arc.InjectorOverridingContext = mock.Mock()

        with (
            mock.patch(
                "ongaku.client.Client.fetch_player", return_value=ongaku_player
            ) as patched_fetch_player,
            mock.patch.object(
                inj_context, "set_type_dependency"
            ) as patched_set_type_dependency,
        ):
            await client._arc_player_injector(context, inj_context)

            patched_fetch_player.assert_called_once_with(context.guild_id)

            patched_set_type_dependency.assert_called_once_with(Player, ongaku_player)

    @pytest.mark.asyncio
    async def test_missing_guild_id(self, gateway_bot: gateway_bot_.GatewayBot):
        client = Client(gateway_bot)

        arc_client = ArcGatewayClient(gateway_bot)

        context: arc.GatewayContext = mock.Mock(guild_id=None)

        inj_context: arc.InjectorOverridingContext = arc.InjectorOverridingContext(
            arc_client.injector.make_context()
        )

        with pytest.raises(KeyError):
            await client._arc_player_injector(context, inj_context)

            inj_context.get_type_dependency(Player)

    @pytest.mark.asyncio
    async def test_missing_player(
        self, gateway_bot: gateway_bot_.GatewayBot, ongaku_player: Player
    ):
        client = Client(gateway_bot)

        context: arc.GatewayContext = mock.Mock()

        inj_context: arc.InjectorOverridingContext = mock.Mock()

        with (
            mock.patch(
                "ongaku.client.Client.fetch_player",
                side_effect=errors.PlayerMissingError,
            ) as patched_fetch_player,
            mock.patch.object(
                inj_context, "set_type_dependency"
            ) as patched_set_type_dependency,
        ):
            await client._arc_player_injector(context, inj_context)

            patched_fetch_player.assert_called_once_with(context.guild_id)

            patched_set_type_dependency.assert_not_called()
