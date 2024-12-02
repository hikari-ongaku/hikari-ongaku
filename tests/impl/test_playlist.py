# ruff: noqa: D100, D101, D102, D103

import typing

from ongaku.impl.playlist import Playlist
from ongaku.impl.playlist import PlaylistInfo
from ongaku.impl.track import Track


def test_playlist_info():
    playlist_info = PlaylistInfo(name="name", selected_track=1)

    assert playlist_info.name == "name"
    assert playlist_info.selected_track == 1


def test_playlist(ongaku_track: Track):
    info = PlaylistInfo(name="name", selected_track=1)
    playlist = Playlist(info=info, tracks=[ongaku_track], plugin_info={})

    assert playlist.info == info
    assert playlist.plugin_info == {}
    assert isinstance(playlist.tracks, typing.Sequence)
    assert len(playlist.tracks) == 1
    assert playlist.tracks[0] == ongaku_track
