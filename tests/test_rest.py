# ruff: noqa: D100, D101, D102, D103

import asyncio
import typing

import mock
import pytest
from hikari import OwnUser
from hikari.impl import gateway_bot as gateway_bot_
from hikari.snowflakes import Snowflake

from ongaku import Playlist
from ongaku import errors
from ongaku.abc.info import Info
from ongaku.abc.player import Player
from ongaku.abc.routeplanner import RoutePlannerStatus
from ongaku.abc.statistics import Statistics
from ongaku.abc.track import Track
from ongaku.client import Client
from ongaku.impl import player as player
from ongaku.impl import track as track_
from ongaku.impl.player import Voice
from ongaku.rest import RESTClient
from ongaku.session import Session
from tests import payloads

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


@pytest.fixture
def track() -> Track:
    track_info = track_.TrackInfo(
        "identifier",
        False,
        "author",
        1,
        True,
        2,
        "title",
        "source_name",
        "uri",
        "artwork_url",
        "isrc",
    )
    return track_.Track(ENCODED_TRACK, track_info, {}, {}, None)


class TestRest:
    @pytest.mark.asyncio
    async def test_load_track(self, ongaku_client: Client, ongaku_session: Session):
        rest = RESTClient(ongaku_client)

        # Test track return types.
        with mock.patch.object(
            rest._client.session_handler, "fetch_session", return_value=ongaku_session
        ):
            # Test singular track

            track = await rest.load_track("https://youtube.com/watch?v=d3BQ-UZh0a8")

            assert isinstance(track, Track)

            assert track.encoded == ENCODED_TRACK

            # Test playlist

            playlist = await rest.load_track(
                "https://www.youtube.com/watch?v=vvANy49Kqhw&list=PLVVOXbE6Ls1hIR1dz7HS7pqs4mDLN4JSR"
            )

            assert isinstance(playlist, Playlist)

            assert playlist.info.name == "STUPENDOUSLY SINISTER SONGS"

            # Test search

            search = await rest.load_track("ytsearch:DEAD AHEAD")

            assert isinstance(search, typing.Sequence)

            assert len(search) >= 1

            # Test no results

            no_result = await rest.load_track(
                "ytsearch:shjdfhjskdhgjksdhfgkjshdfjhsdgkjhsdkjfhsdjkfhskjhasjkdhgfasdkjfhsjkfh"
            )

            assert no_result is None

            # Test error track

            with pytest.raises(errors.RestExceptionError) as rest_exception_error:
                await rest.load_track("https://youtube.com/watch?v=not-a-valid-video")

            assert isinstance(rest_exception_error.value, errors.RestExceptionError)

        # Test malformed search result.
        with (
            mock.patch.object(
                rest._client.session_handler,
                "fetch_session",
                return_value=ongaku_session,
            ),
            mock.patch.object(
                ongaku_session,
                "request",
                return_value={"loadType": "search", "data": [{}, {}, {}]},
            ) as patched_request,
            pytest.raises(errors.BuildError) as build_error,
        ):
            await rest.load_track("ytsearch:malformed-search")

        patched_request.assert_called_once_with(
            "GET",
            "/loadtracks",
            dict,
            params={"identifier": "ytsearch:malformed-search"},
        )

        assert isinstance(build_error.value, errors.BuildError)

        # Test malformed track result.
        with (
            mock.patch.object(
                rest._client.session_handler,
                "fetch_session",
                return_value=ongaku_session,
            ),
            mock.patch.object(
                ongaku_session,
                "request",
                return_value={"loadType": "track", "data": {}},
            ) as patched_request,
            pytest.raises(errors.BuildError) as build_error,
        ):
            await rest.load_track("ytsearch:malformed-track")

        patched_request.assert_called_once_with(
            "GET",
            "/loadtracks",
            dict,
            params={"identifier": "ytsearch:malformed-track"},
        )

        assert isinstance(build_error.value, errors.BuildError)

        # Test malformed playlist result.
        with (
            mock.patch.object(
                rest._client.session_handler,
                "fetch_session",
                return_value=ongaku_session,
            ),
            mock.patch.object(
                ongaku_session,
                "request",
                return_value={"loadType": "playlist", "data": {}},
            ) as patched_request,
            pytest.raises(errors.BuildError) as build_error,
        ):
            await rest.load_track("ytsearch:malformed-playlist")

        patched_request.assert_called_once_with(
            "GET",
            "/loadtracks",
            dict,
            params={"identifier": "ytsearch:malformed-playlist"},
        )

        assert isinstance(build_error.value, errors.BuildError)

        await ongaku_client._stop_event(mock.Mock())

    @pytest.mark.asyncio
    async def test_decode_track(self, ongaku_client: Client, ongaku_session: Session):
        rest = RESTClient(ongaku_client)

        with mock.patch.object(
            rest._client.session_handler, "fetch_session", return_value=ongaku_session
        ):
            track = await rest.decode_track(ENCODED_TRACK)

        assert isinstance(track, Track)

        assert track.encoded == ENCODED_TRACK

        await ongaku_client._stop_event(mock.Mock())

    @pytest.mark.asyncio
    async def test_decode_tracks(self, ongaku_client: Client, ongaku_session: Session):
        rest = RESTClient(ongaku_client)

        with mock.patch.object(
            rest._client.session_handler, "fetch_session", return_value=ongaku_session
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

        with (
            mock.patch.object(gateway_bot, "get_me", return_value=bot_user),
            mock.patch.object(
                gateway_bot.event_manager,
                "dispatch",
                new_callable=mock.AsyncMock,
                return_value=None,
            ) as patched_dispatch,
        ):
            session = Session(
                Client(gateway_bot),
                "test_name",
                False,
                "127.0.0.1",
                2333,
                "youshallnotpass",
                3,
            )
            session._authorization_headers = {"Authorization": session.password}

            await session.start()

            while not patched_dispatch.called:
                await asyncio.sleep(0.05)

            assert session.session_id is not None

        with mock.patch.object(
            rest._client.session_handler, "fetch_session", return_value=session
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

        with (
            mock.patch.object(gateway_bot, "get_me", return_value=bot_user),
            mock.patch.object(
                gateway_bot.event_manager,
                "dispatch",
                new_callable=mock.AsyncMock,
                return_value=None,
            ) as patched_dispatch,
        ):
            session = Session(
                Client(gateway_bot),
                "test_name",
                False,
                "127.0.0.1",
                2333,
                "youshallnotpass",
                3,
            )
            session._authorization_headers = {"Authorization": session.password}

            await session.start()

            while not patched_dispatch.called:
                await asyncio.sleep(0.05)

            assert session.session_id is not None

        with mock.patch.object(
            rest._client.session_handler, "fetch_session", return_value=session
        ):
            session_id = session._get_session_id()

            await rest.update_player(session_id, 1234567890, volume=3)

            new_player = await rest.fetch_player(session_id, 1234567890)

            assert isinstance(new_player, Player)

            assert new_player.guild_id == Snowflake(1234567890)

        await session.stop()

        await ongaku_client._stop_event(mock.Mock())

    @pytest.mark.asyncio
    async def test_update_player(
        self,
        ongaku_client: Client,
        ongaku_session: Session,
        track: Track,
    ):
        rest = RESTClient(ongaku_client)

        with (
            mock.patch.object(
                rest._client.session_handler,
                "fetch_session",
                return_value=ongaku_session,
            ),
            mock.patch.object(
                ongaku_session,
                "request",
                new_callable=mock.AsyncMock,
                return_value=payloads.PLAYER_PAYLOAD,
            ) as patched_request,
        ):
            await rest.update_player(
                "session_id",
                1234567890,
                track=track,
                position=1,
                end_time=2,
                volume=3,
                paused=False,
                voice=Voice("token", "endpoint", "session_id"),
                no_replace=False,
            )

            headers = {"Content-Type": "application/json"}

            json = {
                "track": {"encoded": ENCODED_TRACK},
                "position": 1,
                "endTime": 2,
                "volume": 3,
                "paused": False,
                "voice": {
                    "token": "token",
                    "endpoint": "endpoint",
                    "sessionId": "session_id",
                },
            }

            params = {"noReplace": "false"}

            patched_request.assert_called_once_with(
                "PATCH",
                "/sessions/session_id/players/1234567890",
                dict,
                headers=headers,
                json=json,
                params=params,
            )

        await ongaku_client._stop_event(mock.Mock())

    @pytest.mark.asyncio
    async def test_delete_player(
        self,
        gateway_bot: gateway_bot_.GatewayBot,
        ongaku_client: Client,
        bot_user: OwnUser,
    ):
        rest = RESTClient(ongaku_client)

        with (
            mock.patch.object(gateway_bot, "get_me", return_value=bot_user),
            mock.patch.object(
                gateway_bot.event_manager,
                "dispatch",
                new_callable=mock.AsyncMock,
                return_value=None,
            ) as patched_dispatch,
        ):
            session = Session(
                Client(gateway_bot),
                "test_name",
                False,
                "127.0.0.1",
                2333,
                "youshallnotpass",
                3,
            )
            session._authorization_headers = {"Authorization": session.password}

            await session.start()

            while not patched_dispatch.called:
                await asyncio.sleep(0.05)

            assert session.session_id is not None

        with mock.patch.object(
            rest._client.session_handler, "fetch_session", return_value=session
        ):
            session_id = session._get_session_id()

            await rest.update_player(session_id, 1234567890, volume=3)

            new_player = await rest.fetch_player(session_id, 1234567890)

            assert isinstance(new_player, Player)

            assert new_player.guild_id == Snowflake(1234567890)

            await rest.delete_player(session_id, 1234567890)

            with pytest.raises(errors.RestRequestError):
                await rest.fetch_player(session_id, 1234567890)

        await session.stop()

        await ongaku_client._stop_event(mock.Mock())

    @pytest.mark.asyncio
    async def test_update_session(self, ongaku_client: Client, ongaku_session: Session):
        rest = RESTClient(ongaku_client)

        with (
            mock.patch.object(
                rest._client.session_handler,
                "fetch_session",
                return_value=ongaku_session,
            ),
            mock.patch.object(
                ongaku_session,
                "request",
                return_value={"resuming": False, "timeout": 300},
            ) as patched_request,
        ):
            await rest.update_session("session_id", resuming=False, timeout=300)

            patched_request.assert_called_once_with(
                "PATCH",
                "/sessions/session_id",
                dict,
                headers={"Content-Type": "application/json"},
                json={"resuming": False, "timeout": 300},
            )

        # await ongaku_client._stop_event(mock.Mock())

    @pytest.mark.asyncio
    async def test_fetch_info(self, ongaku_client: Client, ongaku_session: Session):
        rest = RESTClient(ongaku_client)

        with mock.patch.object(
            rest._client.session_handler, "fetch_session", return_value=ongaku_session
        ):
            info = await rest.fetch_info()

        assert isinstance(info, Info)

        assert info.version.major == 4

        await ongaku_client._stop_event(mock.Mock())

    @pytest.mark.asyncio
    async def test_fetch_version(self, ongaku_client: Client, ongaku_session: Session):
        rest = RESTClient(ongaku_client)

        with mock.patch.object(
            rest._client.session_handler, "fetch_session", return_value=ongaku_session
        ):
            version = await rest.fetch_version()

        assert isinstance(version, str)

        assert version.startswith("4")

        await ongaku_client._stop_event(mock.Mock())

    @pytest.mark.asyncio
    async def test_fetch_stats(self, ongaku_client: Client, ongaku_session: Session):
        rest = RESTClient(ongaku_client)

        with mock.patch.object(
            rest._client.session_handler, "fetch_session", return_value=ongaku_session
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
            rest._client.session_handler, "fetch_session", return_value=ongaku_session
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
            rest._client.session_handler, "fetch_session", return_value=ongaku_session
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
            rest._client.session_handler, "fetch_session", return_value=ongaku_session
        ):
            if await rest.fetch_routeplanner_status():
                await rest.update_all_routeplanner_addresses()

        await ongaku_client._stop_event(mock.Mock())
