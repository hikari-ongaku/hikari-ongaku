"""
Playlist ABC's.

The playlist abstract classes.
"""

from __future__ import annotations

import abc
import typing

from ongaku.abc.track import Track

__all__ = ("PlaylistInfo", "Playlist")


class Playlist(abc.ABC):
    """
    Playlist.

    The playlist object.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#playlist-result-data)
    """

    @property
    @abc.abstractmethod
    def info(self) -> PlaylistInfo:
        """Addition playlist info provided by plugins."""
        ...

    @property
    @abc.abstractmethod
    def tracks(self) -> typing.Sequence[Track]:
        """The tracks in this playlist."""
        ...

    @property
    @abc.abstractmethod
    def plugin_info(self) -> typing.Mapping[str, typing.Any]:
        """Addition playlist info provided by plugins."""
        ...


class PlaylistInfo(abc.ABC):
    """
    Playlist information.

    The playlist info object.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#playlist-info)
    """

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """The name of the playlist."""
        ...

    @property
    @abc.abstractmethod
    def selected_track(self) -> int:
        """The selected track of the playlist (`-1` if no track is selected)."""
        ...


# MIT License

# Copyright (c) 2023 MPlatypus

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
