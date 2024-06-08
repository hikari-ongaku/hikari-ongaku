# ruff: noqa: D100, D101, D102, D103

import typing

import mock
import pytest
from hikari.snowflakes import Snowflake

from ongaku import Playlist
from ongaku import errors
from ongaku.abc.track import Track
from ongaku.client import Client
from ongaku.impl import player as player
from ongaku.rest import RESTClient
from ongaku.session import Session
from tests import payloads


class TestRest:
    def test_properties(self, ongaku_client: Client):
        rest = RESTClient(ongaku_client)

        assert rest._client == ongaku_client

    @pytest.mark.asyncio
    async def test_load_track(self, ongaku_client: Client, ongaku_session: Session):
        rest = RESTClient(ongaku_client)

        track_payload = {"loadType": "track", "data": payloads.TRACK_PAYLOAD}

        playlist_payload = {"loadType": "playlist", "data": payloads.PLAYLIST_PAYLOAD}

        search_payload = {"loadType": "search", "data": [payloads.TRACK_PAYLOAD]}

        no_payload: typing.MutableMapping[str, typing.Any] = {
            "loadType": "empty",
            "data": {},
        }

        error_payload = {"loadType": "error", "data": payloads.EXCEPTION_ERROR_PAYLOAD}

        return_values = [
            track_payload,
            playlist_payload,
            search_payload,
            no_payload,
            error_payload,
        ]

        track_payload.update()

        # Test track return types.
        with (
            mock.patch.object(
                rest._client.session_handler,
                "fetch_session",
                return_value=ongaku_session,
            ),
            mock.patch.object(
                ongaku_session, "request", side_effect=return_values
            ) as patched_request,
        ):
            # Test singular track

            new_track = await rest.load_track("https://youtube.com/watch?v=video")

            patched_request.assert_called_with(
                "GET",
                "/loadtracks",
                dict,
                params={"identifier": "https://youtube.com/watch?v=video"},
            )

            assert isinstance(new_track, Track)

            assert new_track.encoded == "encoded"

            # Test playlist

            playlist = await rest.load_track(
                "https://www.youtube.com/watch?v=video&list=playlist"
            )

            patched_request.assert_called_with(
                "GET",
                "/loadtracks",
                dict,
                params={
                    "identifier": "https://www.youtube.com/watch?v=video&list=playlist"
                },
            )

            assert isinstance(playlist, Playlist)

            assert playlist.info.name == "name"

            # Test search

            search = await rest.load_track("ytsearch:a-track")

            patched_request.assert_called_with(
                "GET", "/loadtracks", dict, params={"identifier": "ytsearch:a-track"}
            )

            assert isinstance(search, typing.Sequence)

            assert len(search) >= 1

            # Test no results

            no_result = await rest.load_track("ytsearch:not-a-track")

            patched_request.assert_called_with(
                "GET",
                "/loadtracks",
                dict,
                params={"identifier": "ytsearch:not-a-track"},
            )

            assert no_result is None

            # Test error track

            with pytest.raises(errors.RestExceptionError) as rest_exception_error:
                await rest.load_track("https://youtube.com/watch?v=a-broken-video")

            patched_request.assert_called_with(
                "GET",
                "/loadtracks",
                dict,
                params={"identifier": "https://youtube.com/watch?v=a-broken-video"},
            )

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

        with (
            mock.patch.object(
                rest._client.session_handler,
                "fetch_session",
                return_value=ongaku_session,
            ),
            mock.patch.object(
                ongaku_session, "request", return_value=payloads.TRACK_PAYLOAD
            ) as patched_request,
        ):
            new_track = await rest.decode_track("encoded")

            patched_request.assert_called_once_with(
                "GET", "/decodetrack", dict, params={"encodedTrack": "encoded"}
            )

        assert isinstance(new_track, Track)

        assert new_track.encoded == "encoded"

        await ongaku_client._stop_event(mock.Mock())

    @pytest.mark.asyncio
    async def test_decode_tracks(self, ongaku_client: Client, ongaku_session: Session):
        rest = RESTClient(ongaku_client)

        with (
            mock.patch.object(
                rest._client.session_handler,
                "fetch_session",
                return_value=ongaku_session,
            ),
            mock.patch.object(
                ongaku_session, "request", return_value=[payloads.TRACK_PAYLOAD]
            ) as patched_request,
        ):
            tracks = await rest.decode_tracks(["encoded"])

            patched_request.assert_called_once_with(
                "POST",
                "/decodetracks",
                list,
                headers={"Content-Type": "application/json"},
                json=["encoded"],
            )

        assert isinstance(tracks, typing.Sequence)
        assert isinstance(tracks[0], Track)

        assert tracks[0].encoded == "encoded"

        await ongaku_client._stop_event(mock.Mock())

    @pytest.mark.asyncio
    async def test_fetch_players(
        self,
        ongaku_client: Client,
        ongaku_session: Session,
    ):
        rest = RESTClient(ongaku_client)

        with (
            mock.patch.object(
                rest._client.session_handler,
                "fetch_session",
                return_value=ongaku_session,
            ),
            mock.patch.object(
                ongaku_session, "request", return_value=[payloads.PLAYER_PAYLOAD]
            ) as patched_request,
        ):
            await rest.fetch_players("session_id")

            patched_request.assert_called_once_with(
                "GET", "/sessions/session_id/players", list
            )

    @pytest.mark.asyncio
    async def test_fetch_player(
        self,
        ongaku_client: Client,
        ongaku_session: Session,
    ):
        rest = RESTClient(ongaku_client)

        with (
            mock.patch.object(
                rest._client.session_handler,
                "fetch_session",
                return_value=ongaku_session,
            ),
            mock.patch.object(
                ongaku_session, "request", return_value=payloads.PLAYER_PAYLOAD
            ) as patched_request,
        ):
            await rest.fetch_player("session_id", Snowflake(1234567890))

            patched_request.assert_called_once_with(
                "GET", "/sessions/session_id/players/1234567890", dict
            )

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
                ongaku_session, "request", return_value=payloads.PLAYER_PAYLOAD
            ) as patched_request,
        ):
            await rest.update_player(
                "session_id",
                Snowflake(1234567890),
                track=mock.Mock(encoded="encoded"),
                position=1,
                end_time=2,
                volume=3,
                paused=False,
                voice=player.Voice("token", "endpoint", "session_id"),
                no_replace=False,
            )

            patched_request.assert_called_once_with(
                "PATCH",
                "/sessions/session_id/players/1234567890",
                dict,
                headers={"Content-Type": "application/json"},
                json={
                    "track": {"encoded": "encoded"},
                    "position": 1,
                    "endTime": 2,
                    "volume": 3,
                    "paused": False,
                    "voice": {
                        "token": "token",
                        "endpoint": "endpoint",
                        "sessionId": "session_id",
                    },
                },
                params={"noReplace": "false"},
            )

    @pytest.mark.asyncio
    async def test_delete_player(
        self,
        ongaku_client: Client,
        ongaku_session: Session,
    ):
        rest = RESTClient(ongaku_client)

        with (
            mock.patch.object(
                rest._client.session_handler,
                "fetch_session",
                return_value=ongaku_session,
            ),
            mock.patch.object(
                ongaku_session, "request", return_value=None
            ) as patched_request,
        ):
            await rest.delete_player("session_id", Snowflake(1234567890))

            patched_request.assert_called_once_with(
                "DELETE", "/sessions/session_id/players/1234567890", None
            )

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
                ongaku_session, "request", return_value=payloads.SESSION_PAYLOAD
            ) as patched_request,
        ):
            await rest.update_session("session_id", resuming=False, timeout=230)

            patched_request.assert_called_once_with(
                "PATCH",
                "/sessions/session_id",
                dict,
                headers={"Content-Type": "application/json"},
                json={"resuming": False, "timeout": 230},
            )

    @pytest.mark.asyncio
    async def test_fetch_info(self, ongaku_client: Client, ongaku_session: Session):
        rest = RESTClient(ongaku_client)

        with (
            mock.patch.object(
                rest._client.session_handler,
                "fetch_session",
                return_value=ongaku_session,
            ),
            mock.patch.object(
                ongaku_session, "request", return_value=payloads.INFO_PAYLOAD
            ) as patched_request,
        ):
            await rest.fetch_info()

            patched_request.assert_called_once_with(
                "GET",
                "/info",
                dict,
            )

    @pytest.mark.asyncio
    async def test_fetch_version(self, ongaku_client: Client, ongaku_session: Session):
        rest = RESTClient(ongaku_client)

        with (
            mock.patch.object(
                rest._client.session_handler,
                "fetch_session",
                return_value=ongaku_session,
            ),
            mock.patch.object(
                ongaku_session, "request", return_value=payloads.INFO_PAYLOAD
            ) as patched_request,
        ):
            await rest.fetch_version()

            patched_request.assert_called_once_with(
                "GET", "/version", str, version=False
            )

    @pytest.mark.asyncio
    async def test_fetch_stats(self, ongaku_client: Client, ongaku_session: Session):
        rest = RESTClient(ongaku_client)

        with (
            mock.patch.object(
                rest._client.session_handler,
                "fetch_session",
                return_value=ongaku_session,
            ),
            mock.patch.object(
                ongaku_session, "request", return_value=payloads.STATISTICS_PAYLOAD
            ) as patched_request,
        ):
            await rest.fetch_stats()

            patched_request.assert_called_once_with(
                "GET",
                "/stats",
                dict,
            )

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
                return_value=payloads.ROUTEPLANNER_STATUS_PAYLOAD,
            ) as patched_request,
        ):
            assert await rest.fetch_routeplanner_status() is not None

            patched_request.assert_called_once_with(
                "GET",
                "/routeplanner/status",
                dict,
            )

        with (
            mock.patch.object(
                rest._client.session_handler,
                "fetch_session",
                return_value=ongaku_session,
            ),
            mock.patch.object(
                ongaku_session, "request", side_effect=errors.RestEmptyError
            ) as patched_request,
        ):
            assert await rest.fetch_routeplanner_status() is None

            patched_request.assert_called_once_with(
                "GET",
                "/routeplanner/status",
                dict,
            )

    @pytest.mark.asyncio
    async def test_update_routeplanner_address(
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
                return_value=payloads.ROUTEPLANNER_STATUS_PAYLOAD,
            ) as patched_request,
        ):
            await rest.update_routeplanner_address("1.0.0.1")

            patched_request.assert_called_once_with(
                "POST", "/routeplanner/free/address", None, json={"address": "1.0.0.1"}
            )

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
