"""
Playlist Impl's.

The playlist implemented classes.
"""

from __future__ import annotations

import typing

from ongaku.abc import playlist as playlist_
from ongaku.abc import track as track_

__all__ = ("Playlist", "PlaylistInfo")


class Playlist(playlist_.Playlist):
    def __init__(
        self,
        *,
        info: playlist_.PlaylistInfo,
        tracks: typing.Sequence[track_.Track],
        plugin_info: typing.Mapping[str, typing.Any],
    ) -> None:
        self._info = info
        self._tracks = tracks
        self._plugin_info = plugin_info


class PlaylistInfo(playlist_.PlaylistInfo):
    def __init__(self, *, name: str, selected_track: int) -> None:
        self._name = name
        self._selected_track = selected_track


# MIT License

# Copyright (c) 2023-present MPlatypus

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
