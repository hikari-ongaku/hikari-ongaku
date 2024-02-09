# ruff: noqa

import typing as t
import unittest

from ongaku.abc.track import Playlist
from ongaku.abc.track import PlaylistInfo
from ongaku.abc.track import SearchResult
from ongaku.abc.track import Track
from ongaku.abc.track import TrackInfo


class TrackTest(unittest.TestCase):
    track_payload: dict[str, t.Any] = {
        "encoded": "test_encoded",
        "info": {
            "identifier": "test_identifier",
            "isSeekable": False,
            "author": "test_author",
            "length": 246,
            "isStream": True,
            "position": 0,
            "title": "test_title",
            "uri": "test_uri",
            "artworkUrl": "test_artwork",
            "isrc": None,
            "sourceName": "test_source_name",
        },
        "pluginInfo": {},
        "userData": {},
    }

    track_info_payload: dict[str, t.Any] = track_payload["info"]

    def test_track(self):
        test_info = TrackInfo(
            identifier="test_identifier",
            is_seekable=False,
            author="test_author",
            length=246,
            is_stream=True,
            position=200,
            title="test_title",
            source_name="test_source_name",
            uri=None,
            artwork_url=None,
            isrc=None,
        )
        test_track = Track(
            encoded="test_encoded",
            info=test_info,
            plugin_info={},
            user_data={},
            requestor=None,
        )

        assert test_track.encoded == "test_encoded"
        assert test_track.plugin_info == {}
        assert test_track.user_data == {}

        assert test_track.info == test_info

    def test_track_payload(self):
        test_track_info = TrackInfo._from_payload(self.track_info_payload)
        test_track = Track._from_payload(self.track_payload)

        assert test_track.encoded == "test_encoded"
        assert test_track.plugin_info == {}
        assert test_track.user_data == {}

        assert test_track.info == test_track_info

        assert test_track._to_payload == self.track_payload

    def test_track_info(self):
        test_info = TrackInfo(
            identifier="test_identifier",
            is_seekable=False,
            author="test_author",
            length=246,
            is_stream=True,
            position=0,
            title="test_title",
            source_name="test_source_name",
            uri="test_uri",
            artwork_url="test_artwork",
            isrc=None,
        )

        assert test_info.identifier == "test_identifier"
        assert test_info.is_seekable is False
        assert test_info.author == "test_author"
        assert test_info.length == 246
        assert test_info.is_stream is True
        assert test_info.position == 0
        assert test_info.title == "test_title"
        assert test_info.uri == "test_uri"
        assert test_info.artwork_url is "test_artwork"
        assert test_info.isrc is None
        assert test_info.source_name == "test_source_name"

        assert test_info._to_payload == self.track_info_payload

    def test_track_info_payload(self):
        test_info = TrackInfo._from_payload(self.track_info_payload)

        assert test_info.identifier == "test_identifier"
        assert test_info.is_seekable is False
        assert test_info.author == "test_author"
        assert test_info.length == 246
        assert test_info.is_stream is True
        assert test_info.position == 0
        assert test_info.title == "test_title"
        assert test_info.uri == "test_uri"
        assert test_info.artwork_url == "test_artwork"
        assert test_info.isrc is None
        assert test_info.source_name == "test_source_name"

        assert test_info._to_payload == self.track_info_payload


class PlaylistTest(unittest.TestCase):
    playlist_payload: dict[str, t.Any] = {
        "info": {"name": "test_playlist_name", "selectedTrack": -1},
        "pluginInfo": {},
        "tracks": [TrackTest.track_payload,],
    }

    playlist_info_payload: dict[str, t.Any] = playlist_payload["info"]

    def test_playlist(self):
        test_info = TrackInfo(
            identifier="test_identifier",
            is_seekable=False,
            author="test_author",
            length=246,
            is_stream=True,
            position=0,
            title="test_title",
            source_name="test_source_name",
            uri="test_uri",
            artwork_url="test_artwork",
            isrc=None,
        )
        test_track = Track(
            encoded="test_encoded",
            info=test_info,
            plugin_info={},
            user_data={},
            requestor=None,
        )
        test_playlist_info = PlaylistInfo(name="test_playlist_name", selected_track=-1)
        test_playlist = Playlist(
            info=test_playlist_info, plugin_info={}, tracks=(test_track,)
        )

        assert test_playlist.info == test_playlist_info
        assert test_playlist.plugin_info == {}
        assert test_playlist.tracks == (test_track,)

        assert test_playlist._to_payload == self.playlist_payload #TODO: This seems to print out valid data, however, its not passing the check. More investigation required.

    def test_playlist_payload(self):
        test_info = TrackInfo(
            identifier="test_identifier",
            is_seekable=False,
            author="test_author",
            length=246,
            is_stream=True,
            position=0,
            title="test_title",
            source_name="test_source_name",
            uri="test_uri",
            artwork_url="test_artwork",
            isrc=None,
        )
        test_track = Track(
            encoded="test_encoded",
            info=test_info,
            plugin_info={},
            user_data={},
            requestor=None,
        )
        test_playlist_info = PlaylistInfo(name="test_playlist_name", selected_track=-1)
        test_playlist = Playlist._from_payload(self.playlist_payload)

        assert test_playlist.info == test_playlist_info
        assert test_playlist.plugin_info == {}
        assert tuple(test_playlist.tracks) == (test_track,)

        assert test_playlist._to_payload == self.playlist_payload

    def test_playlist_info(self):
        test_playlist_info = PlaylistInfo(name="test_playlist_name", selected_track=-1)

        assert test_playlist_info.name == "test_playlist_name"
        assert test_playlist_info.selected_track == -1

        assert test_playlist_info._to_payload == self.playlist_info_payload

    def test_playlist_info_payload(self):
        test_playlist_info = PlaylistInfo._from_payload(self.playlist_info_payload)

        assert test_playlist_info.name == "test_playlist_name"
        assert test_playlist_info.selected_track == -1

        assert test_playlist_info._to_payload == self.playlist_info_payload


class SearchResultTest(unittest.TestCase):
    search_result_payload: list[dict[str, t.Any]] = [TrackTest.track_payload]

    def test_search_result(self):
        test_info = TrackInfo(
            identifier="test_identifier",
            is_seekable=False,
            author="test_author",
            length=246,
            is_stream=True,
            position=200,
            title="test_title",
            source_name="test_source_name",
            uri=None,
            artwork_url=None,
            isrc=None,
        )
        test_track = Track(
            encoded="test_encoded",
            info=test_info,
            plugin_info={},
            user_data={},
            requestor=None,
        )
        test_search_result = SearchResult(tracks=(test_track,))

        assert test_search_result.tracks == (test_track,)

    def test_search_result_payload(self):
        test_info = TrackInfo(
            identifier="test_identifier",
            is_seekable=False,
            author="test_author",
            length=246,
            is_stream=True,
            position=0,
            title="test_title",
            source_name="test_source_name",
            uri="test_uri",
            artwork_url="test_artwork",
            isrc=None,
        )
        test_track = Track(
            encoded="test_encoded",
            info=test_info,
            plugin_info={},
            user_data={},
            requestor=None,
        )
        test_search_result = SearchResult._from_payload(self.search_result_payload)

        print(test_search_result.tracks)

        assert tuple(test_search_result.tracks) == (test_track,)
