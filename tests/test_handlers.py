# ruff: noqa: D100, D101, D102, D103

import typing

import mock
import pytest
from hikari.impl import gateway_bot as gateway_bot_
from hikari.snowflakes import Snowflake
from hikari.users import OwnUser

from ongaku.abc.session import SessionStatus
from ongaku.client import Client
from ongaku.impl.handlers import BasicSessionHandler
from ongaku.player import Player
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


@pytest.fixture
def bot_user() -> OwnUser:
    return mock.Mock(global_name="test_username", username="test_username")


class TestBasicSessionHandler:
    @pytest.mark.asyncio
    async def test_properties(self, ongaku_client: Client):
        handler = BasicSessionHandler(ongaku_client)

        assert handler.is_alive is False

        assert isinstance(handler.players, typing.Sequence)
        assert handler.players == ()

        assert isinstance(handler.sessions, typing.Sequence)
        assert handler.sessions == ()

    @pytest.mark.asyncio
    async def test_start(self, ongaku_client: Client):
        handler = BasicSessionHandler(ongaku_client)

        assert handler.is_alive is False

        session_1 = handler.add_session(False, "127.0.0.1", 2333, "youshallnotpass", 3)

        session_2 = handler.add_session(False, "127.0.0.1", 2333, "youshallnotpass", 3)

        with (
            mock.patch.object(
                session_1, "start", return_value=None
            ) as patched_session_1,
            mock.patch.object(
                session_2, "start", return_value=None
            ) as patched_session_2,
        ):
            await handler.start()

            patched_session_1.assert_called_once()
            patched_session_2.assert_called_once()

            assert handler.is_alive is True

    @pytest.mark.asyncio
    async def test_stop(
        self, ongaku_client: Client, ongaku_session: Session, bot_user: OwnUser
    ):
        handler = BasicSessionHandler(ongaku_client)

        assert handler.is_alive is False

        session_1 = handler.add_session(False, "127.0.0.1", 2333, "youshallnotpass", 3)

        session_2 = handler.add_session(False, "127.0.0.1", 2333, "youshallnotpass", 3)

        # Start the session up.

        with (
            mock.patch.object(
                session_1, "start", return_value=None
            ) as patched_session_1,
            mock.patch.object(
                session_2, "start", return_value=None
            ) as patched_session_2,
        ):
            await handler.start()

            patched_session_1.assert_called_once()
            patched_session_2.assert_called_once()

            assert handler.is_alive is True

        with (
            mock.patch.object(
                session_1, "stop", return_value=None
            ) as patched_session_1,
            mock.patch.object(
                session_2, "stop", return_value=None
            ) as patched_session_2,
        ):
            await handler.stop()

            patched_session_1.assert_called_once()
            patched_session_2.assert_called_once()

            assert handler.is_alive is False

    @pytest.mark.asyncio
    async def test_fetch_session(self, ongaku_client: Client, ongaku_session: Session):
        handler = BasicSessionHandler(ongaku_client)

        with mock.patch.object(handler, "_current_session", ongaku_session):
            # Test with current session

            session = handler.fetch_session()

            assert session == ongaku_session

        session_1 = handler.add_session(False, "127.0.0.1", 2333, "youshallnotpass", 3)
        session_2 = handler.add_session(False, "127.0.0.1", 2333, "youshallnotpass", 3)

        assert len(handler.sessions) == 2

        with (
            mock.patch.object(
                session_1,
                "_status",
                new_callable=mock.PropertyMock(return_value=SessionStatus.FAILURE),
            ),
            mock.patch.object(
                session_2,
                "_status",
                new_callable=mock.PropertyMock(return_value=SessionStatus.CONNECTED),
            ),
        ):
            # Test without current session, first session failed.

            session = handler.fetch_session()

            assert session == session_2

            assert handler._current_session == session_2

    @pytest.mark.asyncio
    async def test_add_session(self, ongaku_client: Client, ongaku_session: Session):
        handler = BasicSessionHandler(ongaku_client)

        assert len(handler.sessions) == 0

        handler.add_session(
            ongaku_session.ssl,
            ongaku_session.host,
            ongaku_session.port,
            ongaku_session.password,
            ongaku_session._attempts,
        )

        assert len(handler.sessions) == 1

    @pytest.mark.asyncio
    async def test_add_player(self, ongaku_client: Client, ongaku_session: Session):
        handler = BasicSessionHandler(ongaku_client)

        assert len(handler.players) == 0

        handler.add_player(Player(ongaku_session, Snowflake(1234567890)))

        assert len(handler.players) == 1

    @pytest.mark.asyncio
    async def test_create_player(self, ongaku_client: Client, ongaku_session: Session):
        handler = BasicSessionHandler(ongaku_client)

        # Create a player

        assert len(handler.players) == 0

        with mock.patch.object(handler, "fetch_session", return_value=ongaku_session):
            original_player = await handler.create_player(Snowflake(1234567890))

            assert len(handler.players) == 1

            assert isinstance(original_player, Player)

            assert original_player.guild_id == Snowflake(1234567890)
            assert original_player.session == ongaku_session

        # Create a player but one exists.

        new_player = await handler.create_player(Snowflake(1234567890))

        assert len(handler.players) == 1

        assert isinstance(new_player, Player)

        assert new_player == original_player

        assert new_player.guild_id == Snowflake(1234567890)
        assert new_player.session == ongaku_session

    @pytest.mark.asyncio
    async def test_fetch_player(self, ongaku_client: Client, ongaku_session: Session):
        handler = BasicSessionHandler(ongaku_client)

        # Create a player

        assert len(handler.players) == 0

        with mock.patch.object(handler, "fetch_session", return_value=ongaku_session):
            original_player = await handler.create_player(Snowflake(1234567890))

            assert len(handler.players) == 1

            assert isinstance(original_player, Player)

            assert original_player.guild_id == Snowflake(1234567890)
            assert original_player.session == ongaku_session

        new_player = handler.fetch_player(Snowflake(1234567890))

        assert len(handler.players) == 1

        assert isinstance(new_player, Player)

        assert new_player == original_player

        assert new_player.guild_id == Snowflake(1234567890)
        assert new_player.session == ongaku_session

    @pytest.mark.asyncio
    async def test_delete_player(
        self, ongaku_client: Client, ongaku_session: Session, bot_user: OwnUser
    ):
        handler = BasicSessionHandler(ongaku_client)

        # Create a player

        assert len(handler.players) == 0

        with mock.patch.object(handler, "fetch_session", return_value=ongaku_session):
            original_player = await handler.create_player(Snowflake(1234567890))

            assert len(handler.players) == 1

            assert isinstance(original_player, Player)

            assert original_player.guild_id == Snowflake(1234567890)
            assert original_player.session == ongaku_session

        # Delete the player.

        with mock.patch.object(
            original_player, "disconnect", return_value=None
        ) as patched_player:
            await handler.delete_player(Snowflake(1234567890))

            assert len(handler.players) == 0

            patched_player.assert_called_once()
