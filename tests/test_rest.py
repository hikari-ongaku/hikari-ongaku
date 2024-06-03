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
from ongaku.abc.routeplanner import RoutePlannerType
from ongaku.abc.statistics import Statistics
from ongaku.abc.track import Track
from ongaku.client import Client
from ongaku.impl import player as player
from ongaku.impl.player import Voice
from ongaku.rest import RESTClient
from ongaku.session import Session
from tests import payloads


class TestRest:
    def test_properties(self, ongaku_client: Client):
        rest = RESTClient(ongaku_client)

        assert rest._client == ongaku_client

    @pytest.mark.asyncio
    async def test_load_track(
        self, ongaku_client: Client, ongaku_session: Session, track: Track
    ):
        rest = RESTClient(ongaku_client)

        # Test track return types.
        with mock.patch.object(
            rest._client.session_handler, "fetch_session", return_value=ongaku_session
        ):
            # Test singular track

            new_track = await rest.load_track("https://youtube.com/watch?v=d3BQ-UZh0a8")

            assert isinstance(new_track, Track)

            assert new_track.encoded == track.encoded

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
    async def test_decode_track(
        self, ongaku_client: Client, ongaku_session: Session, track: Track
    ):
        rest = RESTClient(ongaku_client)

        with mock.patch.object(
            rest._client.session_handler, "fetch_session", return_value=ongaku_session
        ):
            new_track = await rest.decode_track(track.encoded)

        assert isinstance(track, Track)

        assert new_track.encoded == track.encoded

        await ongaku_client._stop_event(mock.Mock())

    @pytest.mark.asyncio
    async def test_decode_tracks(
        self, ongaku_client: Client, ongaku_session: Session, track: Track
    ):
        rest = RESTClient(ongaku_client)

        with mock.patch.object(
            rest._client.session_handler, "fetch_session", return_value=ongaku_session
        ):
            tracks = await rest.decode_tracks([track.encoded])

        assert isinstance(tracks, typing.Sequence)
        assert isinstance(tracks[0], Track)

        assert tracks[0].encoded == track.encoded

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

            wait_time = 0
            while not patched_dispatch.called:
                sleep_for = 0.05
                await asyncio.sleep(sleep_for)
                wait_time += sleep_for

                if wait_time >= 5:
                    raise Exception("Could not connect to lavalink.")

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

            wait_time = 0
            while not patched_dispatch.called:
                sleep_for = 0.05
                await asyncio.sleep(sleep_for)
                wait_time += sleep_for

                if wait_time >= 5:
                    raise Exception("Could not connect to lavalink.")

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
                "track": {"encoded": track.encoded},
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

            wait_time = 0
            while not patched_dispatch.called:
                sleep_for = 0.05
                await asyncio.sleep(sleep_for)
                wait_time += sleep_for

                if wait_time >= 5:
                    raise Exception("Could not connect to lavalink.")

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

        # Test with payload

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
                return_value=payloads.ROUTEPLANNER_STATUS_PAYLOAD,
            ) as patched_request,
        ):
            routeplanner_status = await rest.fetch_routeplanner_status()

            assert routeplanner_status is not None

            assert routeplanner_status.cls == RoutePlannerType.ROTATING_ROUTE_PLANNER

            patched_request.assert_called_once_with(
                "GET",
                "/routeplanner/status",
                dict,
            )

        # Test without raise empty payload

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
                side_effect=errors.RestEmptyError,
            ) as patched_request,
        ):
            routeplanner_status = await rest.fetch_routeplanner_status()

            assert routeplanner_status is None

            patched_request.assert_called_once_with(
                "GET",
                "/routeplanner/status",
                dict,
            )

        await ongaku_client._stop_event(mock.Mock())

    @pytest.mark.asyncio
    async def test_update_routeplanner_address(
        self, ongaku_client: Client, ongaku_session: Session
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
                return_value=None,
            ) as patched_request,
        ):
            await rest.update_routeplanner_address("1.0.0.1")

            patched_request.assert_called_once_with(
                "POST", "/routeplanner/free/address", None, json={"address": "1.0.0.1"}
            )

        await ongaku_client._stop_event(mock.Mock())

    @pytest.mark.asyncio
    async def test_update_all_routeplanner_address(
        self, ongaku_client: Client, ongaku_session: Session
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
                return_value=None,
            ) as patched_request,
        ):
            await rest.update_all_routeplanner_addresses()

            patched_request.assert_called_once_with(
                "POST",
                "/routeplanner/free/all",
                None,
            )

        await ongaku_client._stop_event(mock.Mock())
