# ruff: noqa: D100, D101, D102, D103

import typing

import mock
import pytest
from hikari.snowflakes import Snowflake

from ongaku import errors
from ongaku.abc.session import SessionStatus
from ongaku.client import Client
from ongaku.impl.handlers import BasicSessionHandler
from ongaku.player import Player
from ongaku.session import Session


class TestBasicSessionHandler:
    @pytest.mark.asyncio
    async def test_properties(self, ongaku_client: Client):
        handler = BasicSessionHandler(client=ongaku_client)

        assert isinstance(handler.players, typing.Sequence)
        assert handler.players == ()

        assert isinstance(handler.sessions, typing.Sequence)
        assert handler.sessions == ()

        assert handler.is_alive is False

    @pytest.mark.asyncio
    async def test_start(self, ongaku_client: Client):
        handler = BasicSessionHandler(client=ongaku_client)

        assert handler.is_alive is False

        session_1 = Session(
            ongaku_client,
            name="session_1",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
            attempts=3,
        )
        session_2 = Session(
            ongaku_client,
            name="session_2",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
            attempts=3,
        )

        handler.add_session(session=session_1)
        handler.add_session(session=session_2)

        assert len(handler.sessions) == 2

        with mock.patch(
            "ongaku.session.Session.start", return_value=None
        ) as patched_session_start:
            await handler.start()

            assert patched_session_start.call_count == 2

            assert handler.is_alive is True

    @pytest.mark.asyncio
    async def test_stop(self, ongaku_client: Client):
        handler = BasicSessionHandler(client=ongaku_client)

        assert handler.is_alive is False

        session_1 = Session(
            ongaku_client,
            name="session_1",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
            attempts=3,
        )
        handler.add_session(session=session_1)

        session_2 = Session(
            ongaku_client,
            name="session_2",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
            attempts=3,
        )
        handler.add_session(session=session_2)

        # Start the session up.

        with mock.patch(
            "ongaku.session.Session.start", return_value=None
        ) as patched_session_start:
            await handler.start()

            assert patched_session_start.call_count == 2

            assert handler.is_alive is True

        with mock.patch(
            "ongaku.session.Session.stop", return_value=None
        ) as patched_session_stop:
            await handler.stop()

            assert patched_session_stop.call_count == 2

            assert handler.is_alive is False

    @pytest.mark.asyncio
    async def test_fetch_session(self, ongaku_client: Client, ongaku_session: Session):
        handler = BasicSessionHandler(client=ongaku_client)

        with mock.patch.object(handler, "_current_session", ongaku_session):
            # Test with current session

            session = handler.fetch_session()

            assert session == ongaku_session

        session_1 = Session(
            ongaku_client,
            name="session_1",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
            attempts=3,
        )
        handler.add_session(session=session_1)

        session_2 = Session(
            ongaku_client,
            name="session_2",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
            attempts=3,
        )
        handler.add_session(session=session_2)

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

        # Test with name set

        session = handler.fetch_session(name="session_1")

        assert session == session_1

        # Test session is not found.

        handler._sessions.clear()

        with pytest.raises(errors.SessionMissingError):
            handler.fetch_session(name="session_1")

    @pytest.mark.asyncio
    async def test_delete_session(self, ongaku_client: Client, ongaku_session: Session):
        handler = BasicSessionHandler(client=ongaku_client)

        handler._sessions = {"test_session": ongaku_session}

        with mock.patch.object(
            ongaku_session, "stop", new_callable=mock.AsyncMock, return_value=None
        ) as patched_stop:
            await handler.delete_session(name="test_session")

            patched_stop.assert_called_once()

        # Delete an existing session

        with pytest.raises(errors.SessionMissingError):
            await handler.delete_session(name="test_session")

            patched_stop.assert_called_once()

    @pytest.mark.asyncio
    async def test_add_session(self, ongaku_client: Client):
        handler = BasicSessionHandler(client=ongaku_client)

        assert len(handler.sessions) == 0

        session_1 = Session(
            ongaku_client,
            name="session_1",
            ssl=False,
            host="127.0.0.1",
            port=2333,
            password="youshallnotpass",
            attempts=3,
        )
        handler.add_session(session=session_1)

        assert len(handler.sessions) == 1

    @pytest.mark.asyncio
    async def test_add_player(self, ongaku_client: Client, ongaku_player: Player):
        handler = BasicSessionHandler(client=ongaku_client)

        assert len(handler.players) == 0

        handler.add_player(player=ongaku_player)

        assert len(handler.players) == 1

        with pytest.raises(errors.UniqueError):
            handler.add_player(player=ongaku_player)

    @pytest.mark.asyncio
    async def test_fetch_player(self, ongaku_client: Client, ongaku_session: Session):
        handler = BasicSessionHandler(client=ongaku_client)

        # Create a player

        assert len(handler.players) == 0

        with mock.patch.object(
            handler, "_current_session", return_value=ongaku_session
        ):
            original_player = handler.add_player(
                player=Player(ongaku_session, Snowflake(1234567890))
            )

            assert len(handler.players) == 1

            assert isinstance(original_player, Player)

            assert original_player.guild_id == Snowflake(1234567890)
            assert original_player.session == ongaku_session

        new_player = handler.fetch_player(guild=Snowflake(1234567890))

        assert len(handler.players) == 1

        assert isinstance(new_player, Player)

        assert new_player == original_player

        assert new_player.guild_id == Snowflake(1234567890)
        assert new_player.session == ongaku_session

    @pytest.mark.asyncio
    async def test_delete_player(self, ongaku_client: Client, ongaku_session: Session):
        handler = BasicSessionHandler(client=ongaku_client)

        # Create a player

        assert len(handler.players) == 0

        with mock.patch.object(
            handler, "_current_session", return_value=ongaku_session
        ):
            original_player = handler.add_player(
                player=Player(ongaku_session, Snowflake(1234567890))
            )

            assert len(handler.players) == 1

            assert isinstance(original_player, Player)

            assert original_player.guild_id == Snowflake(1234567890)
            assert original_player.session == ongaku_session

        # Delete the player.

        with mock.patch(
            "ongaku.player.Player.disconnect", return_value=None
        ) as patched_player:
            await handler.delete_player(guild=Snowflake(1234567890))

            assert len(handler.players) == 0

            patched_player.assert_called_once()
