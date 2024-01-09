import unittest
import typing as t
from ongaku.abc.track import Track, TrackInfo, Playlist, PlaylistInfo, SearchResult

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
            "sourceName": "test_source_name"
        },
        "pluginInfo": {},
        "userData": {}
    }

    track_info_payload: dict[str, t.Any] = track_payload["info"]
    
    def test_track(self):
        test_info = TrackInfo(
            "test_identifier",
            False,
            "test_author",
            246,
            True,
            200,
            "test_title",
            "test_source_name",
            "test_uri",
            "test_artwork_url",
            "test_isrc",
        )
        test_track = Track("test_encoded", test_info, {}, {})

        assert test_track.encoded == "test_encoded"
        assert test_track.plugin_info == {}
        if test_track.user_data is not None:
            assert test_track.user_data == {}

        assert test_track.info == test_info


    def test_track_payload(self):

        test_track_info = TrackInfo.from_payload(self.track_info_payload)
        test_track = Track.from_payload(self.track_payload)

        assert test_track.encoded == "test_encoded"
        assert test_track.plugin_info == {}
        if test_track.user_data is not None:
            assert test_track.user_data == {}

        assert test_track.info == test_track_info

        assert test_track.to_payload == self.track_payload

    
    def test_track_info(self):
        test_info = TrackInfo(
            "test_identifier",
            False,
            "test_author",
            246,
            True,
            0,
            "test_title",
            "test_source_name",
            "test_uri",
            "test_artwork",
            "test_isrc",
        )

        assert test_info.identifier == "test_identifier"
        assert test_info.is_seekable is False
        assert test_info.author == "test_author"
        assert test_info.length == 246
        assert test_info.is_stream is True
        assert test_info.position == 0
        assert test_info.title == "test_title"
        assert test_info.uri == "test_uri"
        assert test_info.artwork_url == "test_artwork"
        assert test_info.isrc == "test_isrc"
        assert test_info.source_name == "test_source_name"
        
        assert test_info.to_payload == self.track_info_payload


    def test_track_info_payload(self): 
        test_info = TrackInfo.from_payload(self.track_info_payload)

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

        assert test_info.to_payload == self.track_info_payload


class PlaylistTest(unittest.TestCase):    
    playlist_payload: dict[str, t.Any] = {
        "loadType": "playlist",
        "data": {
            "info":{
                "name":"test_playlist_name",
                "selectedTrack":-1
            },
            "pluginInfo": {},
            "tracks": [TrackTest.track_payload]
        }
    }

    playlist_info_payload: dict[str, t.Any] = playlist_payload["data"]["info"]


    def test_playlist(self):
        test_info = TrackInfo(
            "test_identifier",
            False,
            "test_author",
            246,
            True,
            200,
            "test_title",
            "test_source_name",
            "test_uri",
            "test_artwork_url",
            "test_isrc",
        )
        test_track = Track("test_encoded", test_info, {}, {})
        test_playlist_info = PlaylistInfo("beans", 0)
        test_playlist = Playlist(test_playlist_info, {}, (test_track,))

        assert test_playlist.info == test_playlist_info
        assert test_playlist.plugin_info == {}
        assert test_playlist.tracks == (test_track,)

        assert test_playlist.to_payload == self.playlist_payload

    def test_playlist_payload(self):
        test_info = TrackInfo(
            "test_identifier",
            False,
            "test_author",
            246,
            True,
            200,
            "test_title",
            "test_source_name",
            "test_uri",
            "test_artwork_url",
            "test_isrc",
        )
        test_track = Track("test_encoded", test_info, {}, {})
        test_playlist_info = PlaylistInfo("beans", 0)
        test_playlist = Playlist.from_payload(self.playlist_payload)

        assert test_playlist.info == test_playlist_info
        assert test_playlist.plugin_info == {}
        assert test_playlist.tracks == (test_track,)

        assert test_playlist.to_payload == self.playlist_payload

    def test_playlist_info(self):
        test_playlist_info = PlaylistInfo("beans", 0)

        assert test_playlist_info.name == "beans"
        assert test_playlist_info.selected_track == 0

        assert test_playlist_info.to_payload == self.playlist_info_payload

    def test_playlist_info_payload(self):
        test_playlist_info = PlaylistInfo.from_payload(self.playlist_info_payload)

        assert test_playlist_info.name == "beans"
        assert test_playlist_info.selected_track == 0

        assert test_playlist_info.to_payload == self.playlist_info_payload

class SearchResultTest(unittest.TestCase):
    search_result_payload: dict[str, t.Any] = {
        "data":[TrackTest.track_payload]
    }

    def test_search_result(self):
        test_info = TrackInfo(
            "test_identifier",
            False,
            "test_author",
            246,
            True,
            200,
            "test_title",
            "test_source_name",
            "test_uri",
            "test_artwork_url",
            "test_isrc",
        )
        test_track = Track("test_encoded", test_info, {}, {})
        test_search_result = SearchResult((test_track,))

        assert test_search_result.tracks == (test_track,)

        assert test_search_result.to_payload == self.search_result_payload

    def test_search_result_payload(self):
        test_info = TrackInfo(
            "test_identifier",
            False,
            "test_author",
            246,
            True,
            0,
            "test_title",
            "test_source_name",
            "test_uri",
            "test_artwork",
            None,
        )
        test_track = Track("test_encoded", test_info, {}, {})
        test_search_result = SearchResult.from_payload(self.search_result_payload)

        assert test_search_result.tracks == (test_track,)

        assert test_search_result.to_payload == self.search_result_payload

