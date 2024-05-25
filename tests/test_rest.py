# ruff: noqa: D100, D101, D102, D103

import typing

import mock
import pytest
from hikari.impl import gateway_bot as gateway_bot_

from ongaku.abc.info import Info
from ongaku.abc.routeplanner import RoutePlannerStatus
from ongaku.abc.statistics import Statistics
from ongaku.abc.track import Track
from ongaku.client import Client
from ongaku.rest import RESTClient
from ongaku.session import Session

ENCODED_TRACK: typing.Final[str] = (
    "QAAAuQMAGURFQUQgQUhFQUQgfCBEcmVkZ2UgU29uZyEADlRoZSBTdHVwZW5kaXVtAAAAAAAExqgAC2QzQlEtVVpoMGE4AAEAK2h0dHBzOi8vd3d3LnlvdXR1YmUuY29tL3dhdGNoP3Y9ZDNCUS1VWmgwYTgBADRodHRwczovL2kueXRpbWcuY29tL3ZpL2QzQlEtVVpoMGE4L21heHJlc2RlZmF1bHQuanBnAAAHeW91dHViZQAAAAAAAAAA"
)


@pytest.fixture
def gateway_bot() -> gateway_bot_.GatewayBot:
    return gateway_bot_.GatewayBot("", banner=None, suppress_optimization_warning=True)


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

    @pytest.mark.asyncio
    async def test_decode_track(self, ongaku_client: Client, ongaku_session: Session):
        rest = RESTClient(ongaku_client)

        with mock.patch.object(
            rest._client._session_handler, "fetch_session", return_value=ongaku_session
        ):
            track = await rest.decode_track(ENCODED_TRACK)

        assert isinstance(track, Track)

        assert track.encoded == ENCODED_TRACK

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

    @pytest.mark.asyncio
    async def test_fetch_players(self, ongaku_client: Client, ongaku_session: Session):
        rest = RESTClient(ongaku_client)

        # TODO: Startup a session, and also create a fake player.

        with mock.patch.object(
            rest._client._session_handler, "fetch_session", return_value=ongaku_session
        ):
            # players = await rest.fetch_players()
            pass

        raise Exception()

    @pytest.mark.asyncio
    async def test_fetch_player(self, ongaku_client: Client, ongaku_session: Session):
        rest = RESTClient(ongaku_client)

        # TODO: Startup a session, and also create a fake player.

        with mock.patch.object(
            rest._client._session_handler, "fetch_session", return_value=ongaku_session
        ):
            # players = await rest.fetch_player()
            pass

        raise Exception()

    @pytest.mark.asyncio
    async def test_update_player(self, ongaku_client: Client, ongaku_session: Session):
        rest = RESTClient(ongaku_client)

        # TODO: Startup a session, and also create a fake player.

        with mock.patch.object(
            rest._client._session_handler, "fetch_session", return_value=ongaku_session
        ):
            # players = await rest.update_player()
            pass

        raise Exception()

    @pytest.mark.asyncio
    async def test_delete_player(self, ongaku_client: Client, ongaku_session: Session):
        rest = RESTClient(ongaku_client)

        # TODO: Startup a session, and also create a fake player.

        with mock.patch.object(
            rest._client._session_handler, "fetch_session", return_value=ongaku_session
        ):
            # players = await rest.delete_player()
            pass

        raise Exception()

    @pytest.mark.asyncio
    async def test_update_session(self, ongaku_client: Client, ongaku_session: Session):
        rest = RESTClient(ongaku_client)

        # TODO: Startup a session, and also create a fake player.

        with mock.patch.object(
            rest._client._session_handler, "fetch_session", return_value=ongaku_session
        ):
            # players = await rest.update_session()
            pass

        raise Exception()

    @pytest.mark.asyncio
    async def test_fetch_info(self, ongaku_client: Client, ongaku_session: Session):
        rest = RESTClient(ongaku_client)

        with mock.patch.object(
            rest._client._session_handler, "fetch_session", return_value=ongaku_session
        ):
            info = await rest.fetch_info()

        assert isinstance(info, Info)

        assert info.version.major == 4

    @pytest.mark.asyncio
    async def test_fetch_version(self, ongaku_client: Client, ongaku_session: Session):
        rest = RESTClient(ongaku_client)

        with mock.patch.object(
            rest._client._session_handler, "fetch_session", return_value=ongaku_session
        ):
            version = await rest.fetch_version()

        assert isinstance(version, str)

        assert version.startswith("4")

    @pytest.mark.asyncio
    async def test_fetch_stats(self, ongaku_client: Client, ongaku_session: Session):
        rest = RESTClient(ongaku_client)

        with mock.patch.object(
            rest._client._session_handler, "fetch_session", return_value=ongaku_session
        ):
            stats = await rest.fetch_stats()

        assert isinstance(stats, Statistics)

        assert stats.players == 0

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
