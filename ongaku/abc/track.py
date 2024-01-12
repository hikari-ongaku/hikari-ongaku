from __future__ import annotations

import attrs
import typing as t
from hikari import Snowflake
from .base import PayloadBase

__all__ = (
    "TrackInfo",
    "Track",
    "PlaylistInfo",
    "SearchResult",
)


@attrs.define
class TrackInfo(PayloadBase[dict[str, t.Any]]):
    """
    Track information

    All of the track information.

    Find out more [here](https://lavalink.dev/api/rest.html#track-info).
    """

    identifier: str
    """The track identifier."""
    is_seekable: bool
    """Whether the track is seekable."""
    author: str
    """The track author."""
    length: int
    """The track length in milliseconds."""
    is_stream: bool
    """Whether the track is a stream."""
    position: int
    """The track position in milliseconds."""
    title: str
    """The track title."""
    source_name: str
    """The tracks source name."""
    uri: t.Optional[str] = None
    """The track uri."""
    artwork_url: t.Optional[str] = None
    """The track artwork url"""
    isrc: t.Optional[str] = None
    """The track ISRC"""

    @classmethod
    def _from_payload(cls, payload: dict[str, t.Any]) -> TrackInfo:
        identifier = payload["identifier"]
        is_seekable = payload["isSeekable"]
        author = payload["author"]
        length = payload["length"]
        is_stream = payload["isStream"]
        position = payload["position"]
        title = payload["title"]
        try:  # TODO: This needs to be switched to actually check if it exists first, and if it doesn't set it as none.
            uri = payload["uri"]
        except Exception:
            uri = None
        try:
            artwork_url = payload["artworkUrl"]
        except Exception:
            artwork_url = None
        try:
            isrc = payload["isrc"]
        except Exception:
            isrc = None
        source_name = payload["sourceName"]

        return cls(
            identifier,
            is_seekable,
            author,
            length,
            is_stream,
            position,
            title,
            source_name,
            uri,
            artwork_url,
            isrc,
        )


@attrs.define
class Track(PayloadBase[dict[str, t.Any]]):
    """
    Track

    The base track object.

    Find out more [here](https://lavalink.dev/api/rest.html#track).
    """

    encoded: str
    """The base64 encoded track data."""
    info: TrackInfo
    """Information about the track"""
    plugin_info: t.Mapping[str, t.Any]
    """Additional track info provided by plugins"""
    user_data: t.Mapping[str, t.Any] | None = None
    """Additional track data."""
    requestor: Snowflake | None = None
    """
    The person who requested this track.

    !!! NOTE
        This is an internal feature, not something from lavalink. If this track is apart of a lavalink event, then it will most likely be empty.
    """
    

    @classmethod
    def _from_payload(cls, payload: dict[str, t.Any]) -> Track:
        encoded = payload["encoded"]
        info = TrackInfo._from_payload(payload["info"])
        plugin_info = payload["pluginInfo"]
        try:
            user_data = payload["userData"]
        except Exception:
            user_data = None

        return cls(encoded, info, plugin_info, user_data, None)


@attrs.define
class PlaylistInfo(PayloadBase[dict[str, t.Any]]):
    """
    Playlist info

    The playlist info object.

    Find out more [here](https://lavalink.dev/api/rest.html#track-info).
    """

    name: str
    """The name of the playlist."""
    selected_track: int
    """The selected track of the playlist (`-1` if no track is selected)"""

    @classmethod
    def _from_payload(cls, payload: dict[str, t.Any]) -> PlaylistInfo:
        name = payload["name"]
        selected_track = payload["selectedTrack"]

        return cls(name, selected_track)


@attrs.define
class Playlist(PayloadBase[dict[str, t.Any]]):
    """
    Playlist

    The playlist object.

    Find out more [here](https://lavalink.dev/api/rest.html#track-info).
    """

    info: PlaylistInfo
    """The info of the playlist."""
    plugin_info: t.Mapping[str, t.Any]
    """Addition playlist info provided by plugins"""
    tracks: t.Sequence[Track]
    """The tracks in this playlist."""

    @classmethod
    def _from_payload(cls, payload: dict[str, t.Any]) -> Playlist:
        info = payload["info"]
        plugin_info = payload["pluginInfo"]

        tracks: list[Track] | tuple[Track, ...] = []
        for track in payload["tracks"]:
            try:
                new_track = Track._from_payload(track)
            except Exception as e:
                raise e

            tracks.append(new_track)

        return cls(info, plugin_info, tuple(tracks))


@attrs.define
class SearchResult(PayloadBase[list[dict[str, t.Any]]]):
    """
    Search Result

    A search result, that has a list of tracks, from the search result.
    """
    tracks: t.Sequence[Track]
    """The tracks from the search result."""

    @classmethod
    def _from_payload(cls, payload: list[dict[str, t.Any]]) -> SearchResult:
        tracks: list[Track] | tuple[Track, ...] = []

        for track in payload:
            try:
                new_track = Track._from_payload(track)
            except Exception as e:
                raise e

            tracks.append(new_track)

        return cls(tuple(tracks))


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
