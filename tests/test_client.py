from __future__ import annotations

from unittest import mock

import arc
import hikari
import pytest

from ongaku import errors
from ongaku.abc.extensions import Extension
from ongaku.api import builders
from ongaku.api import rest
from ongaku.client import Client
from ongaku.player import ControllablePlayer


@pytest.fixture
def client(hikari_app: hikari.GatewayBotAware) -> Client:
    return Client(hikari_app)


class MockExtension(Extension):
    pass


class TestClient:
    def test_properties(self):
        app = mock.Mock()
        handler = mock.Mock
        logs = "WARNING"
        injector = mock.Mock()

        client = Client(
            app,
            handler=handler,
            logs=logs,
            injector=injector,
        )

        assert client.app == app
        assert isinstance(client.rest, rest.RESTClient)
        assert client.is_alive is False
        assert isinstance(client.builder, builders.EntityBuilder)
        assert isinstance(client.handler, handler)
        assert client.injector == injector

    def test_from_arc_properties(self):
        arc_client = mock.Mock()
        handler = mock.Mock
        logs = "WARNING"

        client = Client.from_arc(
            arc_client,
            handler=handler,
            logs=logs,
        )

        assert client.app == arc_client.app
        assert isinstance(client.rest, rest.RESTClient)
        assert client.is_alive is False
        assert isinstance(client.builder, builders.EntityBuilder)
        assert isinstance(client.handler, handler)
        assert client.injector == arc_client.injector

    def test_from_tanjun_properties(self):
        tanjun_client = mock.Mock()
        handler = mock.Mock
        logs = "WARNING"

        with mock.patch.object(
            tanjun_client,
            "get_type_dependency",
        ) as patched_get_type_dependency:
            client = Client.from_tanjun(
                tanjun_client,
                handler=handler,
                logs=logs,
            )

        patched_get_type_dependency.assert_called_once_with(hikari.GatewayBotAware)

        assert client.app == patched_get_type_dependency.return_value
        assert isinstance(client.rest, rest.RESTClient)
        assert client.is_alive is False
        assert isinstance(client.builder, builders.EntityBuilder)
        assert isinstance(client.handler, handler)
        assert client.injector == tanjun_client.injector

    @pytest.mark.asyncio
    async def test__start_event(self, client: Client):
        assert client._client_session is None
        assert client.is_alive is False

        with (
            mock.patch.object(client, "_handler") as patched__handler,
            mock.patch.object(
                patched__handler,
                "start",
                new_callable=mock.AsyncMock,
            ) as patched_start,
        ):
            await client._start_event(mock.Mock())

        patched_start.assert_called_once_with(client._client_session)

        assert client._client_session is not None
        assert client.is_alive is True

        await client._client_session.close()  # type: ignore[reportGeneralTypeIssues]  # This shows as never, which is in fact completely incorrect.

    @pytest.mark.asyncio
    async def test__stop_event(self, client: Client):
        client._client_session = mock.AsyncMock()
        client._is_alive = True

        with (
            mock.patch.object(client, "_handler") as patched__handler,
            mock.patch.object(
                patched__handler,
                "stop",
                new_callable=mock.AsyncMock,
            ) as patched_start,
        ):
            await client._stop_event(mock.Mock())

        patched_start.assert_called_once_with()

        assert client._client_session is not None
        assert client.is_alive is True

    @pytest.mark.asyncio
    async def test__arc_player_injector(  # FIXME: Remake this test.  # noqa: FIX001, TD001, TD003
        self,
        client: Client,
        ongaku_player: ControllablePlayer,
    ):
        context: arc.GatewayContext = mock.Mock()

        inj_context: arc.InjectorOverridingContext = mock.Mock()

        with (
            mock.patch(
                "ongaku.client.Client.get_player",
                return_value=ongaku_player,
            ) as patched_get_player,
            mock.patch.object(
                inj_context,
                "set_type_dependency",
            ) as patched_set_type_dependency,
        ):
            await client._arc_player_injector(context, inj_context)

            patched_get_player.assert_called_once_with(context.guild_id)

            patched_set_type_dependency.assert_called_once_with(
                ControllablePlayer,
                ongaku_player,
            )

    @pytest.mark.asyncio
    async def test__arc_player_with_missing_guild_id(  # FIXME: Remake this test.  # noqa: FIX001, TD001, TD003
        self,
        hikari_app: hikari.GatewayBotAware,
        client: Client,
    ):
        arc_client = arc.GatewayClient(hikari_app)

        context: arc.GatewayContext = mock.Mock(guild_id=None)

        inj_context: arc.InjectorOverridingContext = arc.InjectorOverridingContext(
            arc_client.injector.make_context(),
        )

        with (
            mock.patch(
                "ongaku.client.Client.get_player",
                return_value=None,
            ) as patched_get_player,
            mock.patch.object(
                inj_context,
                "set_type_dependency",
            ) as patched_set_type_dependency,
        ):
            await client._arc_player_injector(context, inj_context)

        assert patched_get_player.assert_not_called()

        assert patched_set_type_dependency.assert_not_called()

        assert inj_context.get_type_dependency(ControllablePlayer) is None

    @pytest.mark.asyncio
    async def test__arc_player_with_missing_player(  # FIXME: Remake this test.  # noqa: FIX001, TD001, TD003
        self,
        client: Client,
    ):
        context: arc.GatewayContext = mock.Mock()

        inj_context: arc.InjectorOverridingContext = mock.Mock()

        with (
            mock.patch(
                "ongaku.client.Client.get_player",
                side_effect=errors.PlayerMissingError,
            ) as patched_get_player,
            mock.patch.object(
                inj_context,
                "set_type_dependency",
            ) as patched_set_type_dependency,
        ):
            await client._arc_player_injector(context, inj_context)

        patched_get_player.assert_called_once_with(context.guild_id)

        patched_set_type_dependency.assert_not_called()

    def test_create_session(self, client: Client):
        with (
            mock.patch.object(client, "_handler") as patched__handler,
            mock.patch.object(patched__handler, "add_session") as patched_add_session,
        ):
            client.create_session(
                name="session",
                ssl=False,
                host="1.2.3.4",
                port=1234,
                password="session_password",
            )

        patched_add_session.assert_called_once()  # FIXME: This should check the session correctly.  # noqa: TD001, TD002, TD003

    def test_get_session(self, client: Client):
        with (
            mock.patch.object(client, "_handler") as patched__handler,
            mock.patch.object(patched__handler, "get_session") as patched_get_session,
        ):
            client.get_session("test_session")

        patched_get_session.assert_called_once_with(name="test_session")

    @pytest.mark.asyncio
    async def test_delete_session(self, client: Client):
        with (
            mock.patch.object(client, "_handler") as patched__handler,
            mock.patch.object(
                patched__handler,
                "delete_session",
                new_callable=mock.AsyncMock,
            ) as patched_delete_session,
        ):
            await client.delete_session("test_session")

        patched_delete_session.assert_called_once_with(name="test_session")

    def test_create_player(self, client: Client):
        with (
            mock.patch.object(client, "_handler") as patched__handler,
            mock.patch.object(
                patched__handler,
                "get_player",
                side_effect=errors.PlayerMissingError,
            ) as patched_get_player,
        ):
            client.create_player(123)

        patched_get_player.assert_called_once_with(guild=hikari.Snowflake(123))

    def test_create_player_with_existing(self, client: Client):
        with (
            mock.patch.object(client, "_handler") as patched__handler,
            mock.patch.object(
                patched__handler,
                "get_player",
            ) as patched_get_player,
        ):
            assert client.create_player(123) == patched_get_player.return_value

        patched_get_player.assert_called_once_with(guild=hikari.Snowflake(123))

    def test_get_player(self, client: Client):
        with (
            mock.patch.object(client, "_handler") as patched__handler,
            mock.patch.object(patched__handler, "get_player") as patched_get_player,
        ):
            assert client.get_player(123) == patched_get_player.return_value

        patched_get_player.assert_called_once_with(name="test_session")

    @pytest.mark.asyncio
    async def test_delete_player(self, client: Client):
        with (
            mock.patch.object(client, "_handler") as patched__handler,
            mock.patch.object(
                patched__handler,
                "delete_player",
                new_callable=mock.AsyncMock,
            ) as patched_delete_player,
        ):
            await client.delete_session("test_player")

        patched_delete_player.assert_called_once_with(name="test_player")

    def test_create_extension(self, client: Client):
        mock_extension = mock.Mock()

        assert client._extensions == set()

        with (
            mock.patch.object(client, "_injector") as patched__injector,
            mock.patch.object(
                patched__injector,
                "set_type_dependency",
            ) as patched_set_type_dependency,
        ):
            client.create_extension(mock_extension)

        assert client._extensions == {type(mock_extension)}

        patched_set_type_dependency.assert_called_once_with(
            type(mock_extension),
            mock_extension,
        )

    def test_create_extension_with_type(self, client: Client):
        mock_extension = mock.Mock

        assert client._extensions == set()

        with (
            mock.patch.object(client, "_injector") as patched__injector,
            mock.patch.object(
                patched__injector,
                "set_type_dependency",
            ) as patched_set_type_dependency,
        ):
            client.create_extension(mock_extension)

        assert client._extensions == {mock_extension}

        patched_set_type_dependency.assert_called_once()  # FIXME: Not sure if I can even test this properly.  # noqa: TD001, TD002, TD003

    def test_get_extension(self, client: Client):
        mock_extension = mock.Mock

        with (
            mock.patch.object(client, "_injector") as patched__injector,
            mock.patch.object(
                patched__injector,
                "get_type_dependency",
            ) as patched_get_type_dependency,
        ):
            client.get_extension(mock_extension)

        patched_get_type_dependency.assert_called_once_with(mock_extension)

    def test_delete_extension(self, client: Client):
        mock_extension = mock.Mock

        client._extensions.add(mock_extension)

        with (
            mock.patch.object(client, "_injector") as patched__injector,
            mock.patch.object(
                patched__injector,
                "remove_type_dependency",
            ) as patched_get_type_dependency,
        ):
            client.delete_extension(mock_extension)

        patched_get_type_dependency.assert_called_once_with(mock_extension)

        assert client._extensions == set()
