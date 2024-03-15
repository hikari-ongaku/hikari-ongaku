"""
Playlist ABC's.

The playlist abstract classes.
"""

import typing as t

from pydantic import Field

from .bases import PayloadBase
from .track import Track

__all__ = ("PlaylistInfo", "Playlist")


class PlaylistInfo(PayloadBase):
    """
    Playlist information.

    The playlist info object.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#playlist-info)
    """

    name: str
    """The name of the playlist."""
    selected_track: t.Annotated[
        int | None, Field(default=-1, alias="selectedTrack")
    ] = None
    """The selected track of the playlist (`-1` if no track is selected)."""


class Playlist(PayloadBase):
    """
    Playlist.

    The playlist object.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest.html#playlist-result-data)
    """

    info: PlaylistInfo
    """The info of the playlist."""
    plugin_info: t.Annotated[t.Mapping[t.Any, t.Any] | None, Field(alias="pluginInfo")]
    """Addition playlist info provided by plugins."""
    tracks: t.Sequence[Track]
    """The tracks in this playlist."""


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
