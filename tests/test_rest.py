# ruff: noqa: D100, D101, D102, D103

import asyncio
import typing

import mock
import pytest
from hikari import OwnUser
from hikari.impl import gateway_bot as gateway_bot_
from hikari.snowflakes import Snowflake

from ongaku.abc.info import Info
from ongaku.abc.player import Player
from ongaku.abc.routeplanner import RoutePlannerStatus
from ongaku.abc.statistics import Statistics
from ongaku.abc.track import Track
from ongaku.client import Client
from ongaku.errors import RestErrorException
from ongaku.rest import RESTClient
from ongaku.session import Session

ENCODED_TRACK: typing.Final[str] = (
    "QAAAuQMAGURFQUQgQUhFQUQgfCBEcmVkZ2UgU29uZyEADlRoZSBTdHVwZW5kaXVtAAAAAAAExqgAC2QzQlEtVVpoMGE4AAEAK2h0dHBzOi8vd3d3LnlvdXR1YmUuY29tL3dhdGNoP3Y9ZDNCUS1VWmgwYTgBADRodHRwczovL2kueXRpbWcuY29tL3ZpL2QzQlEtVVpoMGE4L21heHJlc2RlZmF1bHQuanBnAAAHeW91dHViZQAAAAAAAAAA"
)


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


class TestRest:
    @pytest.mark.asyncio
    async def test_load_track(self, ongaku_client: Client, ongaku_session: Session):
        rest = RESTClient(ongaku_client)

        with mock.patch.object(
            rest._client._session_handler, "fetch_session", return_value=ongaku_session
        ):
            track = await rest.load_track("https://youtube.com/watch?v=d3BQ-UZh0a8")

        assert isinstance(track, Track)

        assert track.encoded == ENCODED_TRACK

        await ongaku_client._stop_event(mock.Mock())

    @pytest.mark.asyncio
    async def test_decode_track(self, ongaku_client: Client, ongaku_session: Session):
        rest = RESTClient(ongaku_client)

        with mock.patch.object(
            rest._client._session_handler, "fetch_session", return_value=ongaku_session
        ):
            track = await rest.decode_track(ENCODED_TRACK)

        assert isinstance(track, Track)

        assert track.encoded == ENCODED_TRACK

        await ongaku_client._stop_event(mock.Mock())

    @pytest.mark.asyncio
    async def test_decode_tracks(self, ongaku_client: Client, ongaku_session: Session):
        rest = RESTClient(ongaku_client)

        with mock.patch.object(
            rest._client._session_handler, "fetch_session", return_value=ongaku_session
        ):
            tracks = await rest.decode_tracks([ENCODED_TRACK])

        assert isinstance(tracks, typing.Sequence)
        assert isinstance(tracks[0], Track)

        assert tracks[0].encoded == ENCODED_TRACK

        await ongaku_client._stop_event(mock.Mock())

    @pytest.mark.asyncio
    async def test_fetch_players(
        self,
        gateway_bot: gateway_bot_.GatewayBot,
        ongaku_client: Client,
        bot_user: OwnUser,
    ):
        rest = RESTClient(ongaku_client)

        with mock.patch.object(gateway_bot, "get_me", return_value=bot_user):
            session = Session(
                Client(gateway_bot),
                "test_name",
                False,
                "127.0.0.1",
                2333,
                "youshallnotpass",
                3,
            )
            session._base_headers = {"Authorization": session.password}

            await session.start()
            await asyncio.sleep(2)

        with mock.patch.object(
            rest._client._session_handler, "fetch_session", return_value=session
        ):
            session_id = session._get_session_id()

            await rest.update_player(session_id, 1234567890, volume=3)

            players = await rest.fetch_players(session_id)

            assert isinstance(players, typing.Sequence)

            assert len(players) == 1

            assert players[0].guild_id == Snowflake(1234567890)

        await session.stop()

        await ongaku_client._stop_event(mock.Mock())

    @pytest.mark.asyncio
    async def test_fetch_player(
        self,
        gateway_bot: gateway_bot_.GatewayBot,
        ongaku_client: Client,
        bot_user: OwnUser,
    ):
        rest = RESTClient(ongaku_client)

        with mock.patch.object(gateway_bot, "get_me", return_value=bot_user):
            session = Session(
                Client(gateway_bot),
                "test_name",
                False,
                "127.0.0.1",
                2333,
                "youshallnotpass",
                3,
            )
            session._base_headers = {"Authorization": session.password}

            await session.start()
            await asyncio.sleep(2)

        with mock.patch.object(
            rest._client._session_handler, "fetch_session", return_value=session
        ):
            session_id = session._get_session_id()

            await rest.update_player(session_id, 1234567890, volume=3)

            player = await rest.fetch_player(session_id, 1234567890)

            assert isinstance(player, Player)

            assert player.guild_id == Snowflake(1234567890)

        await session.stop()

        await ongaku_client._stop_event(mock.Mock())

    @pytest.mark.asyncio
    async def test_update_player(
        self,
        gateway_bot: gateway_bot_.GatewayBot,
        ongaku_client: Client,
        bot_user: OwnUser,
    ):
        rest = RESTClient(ongaku_client)

        with mock.patch.object(gateway_bot, "get_me", return_value=bot_user):
            session = Session(
                Client(gateway_bot),
                "test_name",
                False,
                "127.0.0.1",
                2333,
                "youshallnotpass",
                3,
            )
            session._base_headers = {"Authorization": session.password}

            await session.start()
            await asyncio.sleep(2)

        with mock.patch.object(
            rest._client._session_handler, "fetch_session", return_value=session
        ):
            session_id = session._get_session_id()

            await rest.update_player(session_id, 1234567890, volume=3)

            player = await rest.fetch_player(session_id, 1234567890)

            assert player.guild_id == Snowflake(1234567890)

            assert player.volume == 3

            await rest.update_player(session_id, 1234567890, volume=5)

            player = await rest.fetch_player(session_id, 1234567890)

            assert player.guild_id == Snowflake(1234567890)

            assert player.volume == 5

        await session.stop()

        await ongaku_client._stop_event(mock.Mock())

    @pytest.mark.asyncio
    async def test_delete_player(
        self,
        gateway_bot: gateway_bot_.GatewayBot,
        ongaku_client: Client,
        bot_user: OwnUser,
    ):
        rest = RESTClient(ongaku_client)

        with mock.patch.object(gateway_bot, "get_me", return_value=bot_user):
            session = Session(
                Client(gateway_bot),
                "test_name",
                False,
                "127.0.0.1",
                2333,
                "youshallnotpass",
                3,
            )
            session._base_headers = {"Authorization": session.password}

            await session.start()
            await asyncio.sleep(2)

        with mock.patch.object(
            rest._client._session_handler, "fetch_session", return_value=session
        ):
            session_id = session._get_session_id()

            await rest.update_player(session_id, 1234567890, volume=3)

            player = await rest.fetch_player(session_id, 1234567890)

            assert isinstance(player, Player)

            assert player.guild_id == Snowflake(1234567890)

            await rest.delete_player(session_id, 1234567890)

            with pytest.raises(RestErrorException):
                await rest.fetch_player(session_id, 1234567890)

        await session.stop()

        await ongaku_client._stop_event(mock.Mock())

    @pytest.mark.asyncio
    async def test_update_session(
        self,
        gateway_bot: gateway_bot_.GatewayBot,
        ongaku_client: Client,
        bot_user: OwnUser,
    ):
        rest = RESTClient(ongaku_client)

        with mock.patch.object(gateway_bot, "get_me", return_value=bot_user):
            session = Session(
                Client(gateway_bot),
                "test_name",
                False,
                "127.0.0.1",
                2333,
                "youshallnotpass",
                3,
            )
            session._base_headers = {"Authorization": session.password}

            await session.start()
            await asyncio.sleep(2)

        with mock.patch.object(
            rest._client._session_handler, "fetch_session", return_value=session
        ):
            session_id = session._get_session_id()

            await rest.update_session(session_id, resuming=False, timeout=300)

            # FIXME: I need to see if this actually updated? Not even sure this is something I can test?

        await session.stop()

        await ongaku_client._stop_event(mock.Mock())

    @pytest.mark.asyncio
    async def test_fetch_info(self, ongaku_client: Client, ongaku_session: Session):
        rest = RESTClient(ongaku_client)

        with mock.patch.object(
            rest._client._session_handler, "fetch_session", return_value=ongaku_session
        ):
            info = await rest.fetch_info()

        assert isinstance(info, Info)

        assert info.version.major == 4

        await ongaku_client._stop_event(mock.Mock())

    @pytest.mark.asyncio
    async def test_fetch_version(self, ongaku_client: Client, ongaku_session: Session):
        rest = RESTClient(ongaku_client)

        with mock.patch.object(
            rest._client._session_handler, "fetch_session", return_value=ongaku_session
        ):
            version = await rest.fetch_version()

        assert isinstance(version, str)

        assert version.startswith("4")

        await ongaku_client._stop_event(mock.Mock())

    @pytest.mark.asyncio
    async def test_fetch_stats(self, ongaku_client: Client, ongaku_session: Session):
        rest = RESTClient(ongaku_client)

        with mock.patch.object(
            rest._client._session_handler, "fetch_session", return_value=ongaku_session
        ):
            stats = await rest.fetch_stats()

        assert isinstance(stats, Statistics)

        assert stats.playing_players == 0

        await ongaku_client._stop_event(mock.Mock())

    @pytest.mark.asyncio
    async def test_fetch_routeplanner_status(
        self, ongaku_client: Client, ongaku_session: Session
    ):
        rest = RESTClient(ongaku_client)

        with mock.patch.object(
            rest._client._session_handler, "fetch_session", return_value=ongaku_session
        ):
            routeplanner_status = await rest.fetch_routeplanner_status()

        if routeplanner_status:
            assert isinstance(routeplanner_status, RoutePlannerStatus)

            assert routeplanner_status.cls is None

        await ongaku_client._stop_event(mock.Mock())

    @pytest.mark.asyncio
    async def test_update_routeplanner_address(
        self, ongaku_client: Client, ongaku_session: Session
    ):
        rest = RESTClient(ongaku_client)

        # TODO: Make sure these methods work with, and without routeplanner enabled.

        with mock.patch.object(
            rest._client._session_handler, "fetch_session", return_value=ongaku_session
        ):
            if await rest.fetch_routeplanner_status():
                await rest.update_routeplanner_address("111.222.333.444")

        await ongaku_client._stop_event(mock.Mock())

    @pytest.mark.asyncio
    async def test_update_all_routeplanner_address(
        self, ongaku_client: Client, ongaku_session: Session
    ):
        rest = RESTClient(ongaku_client)

        # TODO: Make sure these methods work with, and without routeplanner enabled.

        with mock.patch.object(
            rest._client._session_handler, "fetch_session", return_value=ongaku_session
        ):
            if await rest.fetch_routeplanner_status():
                await rest.update_all_routeplanner_addresses()

        await ongaku_client._stop_event(mock.Mock())
