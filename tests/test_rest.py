# ruff: noqa: D100, D101, D102
import typing as t
import unittest
from unittest.mock import AsyncMock
from unittest.mock import patch

import hikari

from ongaku import Playlist
from ongaku.abc.lavalink import ExceptionError
from ongaku.abc.lavalink import Info
from ongaku.abc.player import Player
from ongaku.abc.session import Session
from ongaku.abc.track import SearchResult
from ongaku.abc.track import Track
from ongaku.rest import RESTClient
from ongaku.rest import RESTPlayer
from ongaku.rest import RESTSession
from ongaku.rest import RESTTrack
from ongaku.rest import _HttpMethod
from test_abc import InfoTest
from test_abc import PlayerTest
from test_abc import SessionTest
from test_abc import PlaylistTest
from test_abc import TrackTest


class RestTest(unittest.IsolatedAsyncioTestCase):
    async def test_rest_info(self):
        mock_client = AsyncMock()

        rest_client = RESTClient(mock_client)

        assert rest_client.session == rest_client._rest_session
        assert rest_client.player == rest_client._rest_player
        assert rest_client.track == rest_client._rest_track

        with patch("ongaku.rest.RESTClient._rest_handler") as mock_rest_handler:
            mock_response = InfoTest.info_payload
            mock_rest_handler.return_value = mock_response

            with patch("aiohttp.ClientSession") as mock_session:
                mock_session.return_value.request.return_value.__aenter__.return_value.json.return_value = AsyncMock(
                    return_value=mock_response
                )

                result = await rest_client.fetch_info()

        mock_rest_handler.assert_called_once_with(
            "/info", mock_client._internal.headers, _HttpMethod.GET
        )
        self.assertEqual(result, Info._from_payload(InfoTest.info_payload))


class RestSessionTest(unittest.IsolatedAsyncioTestCase):
    async def test_session_update(self):
        with patch("ongaku.rest.RESTClient._rest_handler") as mock_rest_handler:
            mock_response = SessionTest.payload
            mock_rest_handler.return_value = mock_response

            mock_client = AsyncMock()

            rest_client = RESTClient(mock_client)

            rest_session = RESTSession(rest_client)

            result = await rest_session.update("session_id")

        mock_rest_handler.assert_called_once_with(
            "/sessions/session_id", mock_client._internal.headers, _HttpMethod.PATCH
        )
        self.assertEqual(result, Session._from_payload(SessionTest.payload))


class RestPlayerTest(unittest.IsolatedAsyncioTestCase):
    async def test_player_fetch_all(self):
        with patch("ongaku.rest.RESTClient._rest_handler") as mock_rest_handler:
            mock_response = [PlayerTest.player_payload]
            mock_rest_handler.return_value = mock_response

            mock_client = AsyncMock()

            rest_client = RESTClient(mock_client)

            rest_player = RESTPlayer(rest_client)

            result = await rest_player.fetch_all("session_id")

        mock_rest_handler.assert_called_once_with(
            "/sessions/session_id/players",
            mock_client._internal.headers,
            _HttpMethod.GET,
        )

        self.assertEqual(result, [Player._from_payload(PlayerTest.player_payload)])

    async def test_player_fetch(self):
        with patch("ongaku.rest.RESTClient._rest_handler") as mock_rest_handler:
            mock_response = PlayerTest.player_payload
            mock_rest_handler.return_value = mock_response

            mock_client = AsyncMock()

            rest_client = RESTClient(mock_client)

            rest_player = RESTPlayer(rest_client)

            result = await rest_player.fetch("session_id", hikari.Snowflake(1))

        mock_rest_handler.assert_called_once_with(
            "/sessions/session_id/players/1",
            mock_client._internal.headers,
            _HttpMethod.GET,
        )
        self.assertEqual(result, Player._from_payload(PlayerTest.player_payload))

    async def test_player_update(self):
        with patch("ongaku.rest.RESTClient._rest_handler") as mock_rest_handler:
            mock_response = PlayerTest.player_payload
            mock_rest_handler.return_value = mock_response

            mock_client = AsyncMock()

            mock_client._internal.headers = dict[str, t.Any]()

            rest_client = RESTClient(mock_client)

            rest_player = RESTPlayer(rest_client)

            result = await rest_player.update(hikari.Snowflake(1), "session_id")

        mock_rest_handler.assert_called_once_with(
            "/sessions/session_id/players/1",
            mock_client._internal.headers,
            _HttpMethod.PATCH,
            json={},
            params={"noReplace": "true"},
        )
        self.assertEqual(result, Player._from_payload(PlayerTest.player_payload))

    async def test_player_delete(self):
        with patch("ongaku.rest.RESTClient._rest_handler") as mock_rest_handler:
            mock_rest_handler.return_value = None

            mock_client = AsyncMock()

            rest_client = RESTClient(mock_client)

            rest_player = RESTPlayer(rest_client)

            result = await rest_player.delete("session_id", hikari.Snowflake(1))

        mock_rest_handler.assert_called_once_with(
            "/sessions/session_id/players/1",
            mock_client._internal.headers,
            _HttpMethod.DELETE,
        )
        self.assertEqual(result, None)


class RestTrackTest(unittest.IsolatedAsyncioTestCase):
    async def test_track_load_empty(self):
        with patch("ongaku.rest.RESTClient._rest_handler") as mock_rest_handler:
            mock_response: dict[str, t.Any] = {}
            mock_response.update({"loadType": "empty"})
            mock_response.update({"data": {}})
            mock_rest_handler.return_value = mock_response

            mock_client = AsyncMock()

            rest_client = RESTClient(mock_client)

            rest_player = RESTTrack(rest_client)

            result = await rest_player.load("test")

        mock_rest_handler.assert_called_once_with(
            "/loadtracks",
            mock_client._internal.headers,
            _HttpMethod.GET,
            params={"identifier": "test"},
        )

        self.assertEqual(result, None)

    async def test_track_load_error(self):
        error_payload = {
            "data": {
                "message": "test_message",
                "severity": "common",
                "cause": "test_cause",
            }
        }
        with patch("ongaku.rest.RESTClient._rest_handler") as mock_rest_handler:
            mock_response: dict[str, t.Any] = {}
            mock_response.update({"loadType": "error"})
            mock_response.update({"data": error_payload})
            mock_rest_handler.return_value = mock_response

            mock_client = AsyncMock()

            rest_client = RESTClient(mock_client)

            rest_player = RESTTrack(rest_client)

            result = await rest_player.load("test")

        mock_rest_handler.assert_called_once_with(
            "/loadtracks",
            mock_client._internal.headers,
            _HttpMethod.GET,
            params={"identifier": "test"},
        )

        self.assertEqual(result, ExceptionError._from_payload(error_payload["data"]))

        # FIXME: I need this to check that it returns the error object properly, somehow. Don't ask me how.

    async def test_track_load_search(self):
        with patch("ongaku.rest.RESTClient._rest_handler") as mock_rest_handler:
            mock_response: dict[str, t.Any] = {}
            mock_response.update({"loadType": "search"})
            mock_response.update({"data": [TrackTest.track_payload]})
            mock_rest_handler.return_value = mock_response

            mock_client = AsyncMock()

            rest_client = RESTClient(mock_client)

            rest_player = RESTTrack(rest_client)

            result = await rest_player.load("test")

        mock_rest_handler.assert_called_once_with(
            "/loadtracks",
            mock_client._internal.headers,
            _HttpMethod.GET,
            params={"identifier": "test"},
        )

        self.assertEqual(result, SearchResult._from_payload([TrackTest.track_payload]))

    async def test_track_load_track(self):
        with patch("ongaku.rest.RESTClient._rest_handler") as mock_rest_handler:
            mock_response: dict[str, t.Any] = {}
            mock_response.update({"loadType": "track"})
            mock_response.update({"data": TrackTest.track_payload})
            mock_rest_handler.return_value = mock_response

            mock_client = AsyncMock()

            rest_client = RESTClient(mock_client)

            rest_player = RESTTrack(rest_client)

            result = await rest_player.load("test")

        mock_rest_handler.assert_called_once_with(
            "/loadtracks",
            mock_client._internal.headers,
            _HttpMethod.GET,
            params={"identifier": "test"},
        )

        self.assertEqual(result, Track._from_payload(TrackTest.track_payload))

    async def test_track_load_playlist(self):
        with patch("ongaku.rest.RESTClient._rest_handler") as mock_rest_handler:
            mock_response: dict[str, t.Any] = {}
            mock_response.update({"loadType": "playlist"})
            mock_response.update({"data": PlaylistTest.playlist_payload})
            mock_rest_handler.return_value = mock_response

            mock_client = AsyncMock()

            rest_client = RESTClient(mock_client)

            rest_player = RESTTrack(rest_client)

            result = await rest_player.load("test")

        mock_rest_handler.assert_called_once_with(
            "/loadtracks",
            mock_client._internal.headers,
            _HttpMethod.GET,
            params={"identifier": "test"},
        )

        self.assertEqual(result, Playlist._from_payload(PlaylistTest.playlist_payload))

    async def test_decode(self):
        with patch("ongaku.rest.RESTClient._rest_handler") as mock_rest_handler:
            mock_response: dict[str, t.Any] = TrackTest.track_payload
            mock_rest_handler.return_value = mock_response

            mock_client = AsyncMock()

            rest_client = RESTClient(mock_client)

            rest_player = RESTTrack(rest_client)

            result = await rest_player.decode("test_track")

        mock_rest_handler.assert_called_once_with(
            "/decodetrack",
            mock_client._internal.headers,
            _HttpMethod.GET,
            params={"encodedTrack": "test_track"},
        )

        self.assertEqual(result, Track._from_payload(TrackTest.track_payload))

    async def test_decode_many(self):
        with patch("ongaku.rest.RESTClient._rest_handler") as mock_rest_handler:
            mock_response: list[dict[str, t.Any]] = [TrackTest.track_payload]
            mock_rest_handler.return_value = mock_response

            mock_client = AsyncMock()

            rest_client = RESTClient(mock_client)

            rest_player = RESTTrack(rest_client)

            result = await rest_player.decode_many(["test_track"])

        mock_rest_handler.assert_called_once_with(
            "/decodetracks",
            mock_client._internal.headers,
            _HttpMethod.GET,
            json=["test_track"],
        )

        self.assertEqual(result, Track._from_payload(TrackTest.track_payload))
