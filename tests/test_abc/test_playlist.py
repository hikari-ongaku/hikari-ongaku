# ruff: noqa: D100, D101, D102

import unittest

from ongaku.abc import Track
from ongaku.abc.playlist import Playlist
from ongaku.abc.playlist import PlaylistInfo
from tests import payload


class TestPlaylist(unittest.TestCase):
    def test_base(self):
        playlist_info = PlaylistInfo._from_payload(
            payload.convert(payload.PLAYLIST_INFO)
        )
        track = Track._from_payload(payload.convert(payload.TRACK))
        playlist = Playlist(info=playlist_info, plugin_info={}, tracks=[track])

        assert playlist.info == playlist_info
        assert playlist.plugin_info == {}
        assert playlist.tracks == [track]

    def test_from_payload(self):
        playlist_info = PlaylistInfo._from_payload(
            payload.convert(payload.PLAYLIST_INFO)
        )
        track = Track._from_payload(payload.convert(payload.TRACK))
        playlist = Playlist._from_payload(payload.convert(payload.PLAYLIST))

        assert playlist.info == playlist_info
        assert playlist.plugin_info == {}
        assert playlist.tracks == [track]

    def test_to_payload(self):
        playlist = Playlist._from_payload(payload.convert(payload.PLAYLIST))

        assert playlist._to_payload == payload.PLAYLIST


class TestPlaylistInfo(unittest.TestCase):
    def test_base(self):
        playlist_info = PlaylistInfo(name="test_name", selected_track=1)

        assert playlist_info.name == "test_name"
        assert playlist_info.selected_track == 1

    def test_from_payload(self):
        playlist_info = PlaylistInfo._from_payload(
            payload.convert(payload.PLAYLIST_INFO)
        )

        assert playlist_info.name == "test_name"
        assert playlist_info.selected_track == 1

    def test_to_payload(self):
        playlist_info = PlaylistInfo._from_payload(
            payload.convert(payload.PLAYLIST_INFO)
        )

        assert playlist_info._to_payload == payload.PLAYLIST_INFO
