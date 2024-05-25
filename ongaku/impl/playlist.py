# ruff: noqa: D101, D102

from __future__ import annotations

import typing

from ongaku.abc import playlist as playlist_
from ongaku.abc import track as track_


class Playlist(playlist_.Playlist):
    def __init__(
        self,
        info: playlist_.PlaylistInfo,
        tracks: typing.Sequence[track_.Track],
        plugin_info: typing.Mapping[str, typing.Any],
    ) -> None:
        self._info = info
        self._tracks = tracks
        self._plugin_info = plugin_info

    @property
    def info(self) -> playlist_.PlaylistInfo:
        return self._info

    @property
    def tracks(self) -> typing.Sequence[track_.Track]:
        return self._tracks

    @property
    def plugin_info(self) -> typing.Mapping[str, typing.Any]:
        return self._plugin_info


class PlaylistInfo(playlist_.PlaylistInfo):
    def __init__(self, name: str, selected_track: int) -> None:
        self._name = name
        self._selected_track = selected_track

    @property
    def name(self) -> str:
        return self._name

    @property
    def selected_track(self) -> int:
        return self._selected_track
