"""
Playlist.

All of the playlist related classes.
"""

from .bases import PayloadBase

import typing as t

from pydantic import Field

from .track import Track

__all__ = (
    "PlaylistInfo",
    "Playlist"
)


class PlaylistInfo(PayloadBase):
    """Playlist information.

    The playlist info object.

    Find out more [here](https://lavalink.dev/api/rest#playlist-info).
    """

    name: str
    """The name of the playlist."""
    selected_track: t.Annotated[
        int | None, Field(default=-1, alias="selectedTrack")
    ] = None
    """The selected track of the playlist (`-1` if no track is selected)"""


class Playlist(PayloadBase):
    """Playlist.

    The playlist object.

    Find out more [here](https://lavalink.dev/api/rest.html#playlist-result-data).
    """

    info: PlaylistInfo
    """The info of the playlist."""
    plugin_info: t.Annotated[t.Mapping[t.Any, t.Any] | None, Field(alias="pluginInfo")]
    """Addition playlist info provided by plugins"""
    tracks: t.Sequence[Track]
    """The tracks in this playlist."""