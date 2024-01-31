"""Track ABC's.

The player's abstract classes.
"""

from __future__ import annotations

import typing as t

import attrs
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
    """Track information.

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
    def _from_payload(cls, payload: t.Mapping[str, t.Any]) -> TrackInfo:
        identifier = payload.get("identifier")
        if identifier is None:
            raise ValueError("identifier cannot be none.")
        if not isinstance(identifier, str):
            raise TypeError("identifier must be a string.")
        
        is_seekable = payload.get("isSeekable")
        if is_seekable is None:
            raise ValueError("isSeekable cannot be none.")
        if not isinstance(is_seekable, bool):
            raise TypeError("isSeekable must be a boolean.")
        
        author = payload.get("author")
        if author is None:
            raise ValueError("author cannot be none.")
        if not isinstance(author, str):
            raise TypeError("author must be a string.")
        
        length = payload.get("length")
        if length is None:
            raise ValueError("length cannot be none.")
        if not isinstance(length, int):
            raise TypeError("length must be a integer.")
        
        is_stream = payload.get("isStream")
        if is_stream is None:
            raise ValueError("isStream cannot be none.")
        if not isinstance(is_stream, bool):
            raise TypeError("isStream must be a boolean.")
        
        position = payload.get("position")
        if position is None:
            raise ValueError("position cannot be none.")
        if not isinstance(position, int):
            raise TypeError("position must be a integer.")
        
        title = payload.get("title")
        if title is None:
            raise ValueError("title cannot be none.")
        if not isinstance(title, str):
            raise TypeError("title must be a string.")
        
        uri = payload.get("uri")
        if uri is not None:
            if not isinstance(uri, str):
                raise TypeError("artworkUrl must be a string, or none.")
        
        artwork_url = payload.get("artworkUrl")
        if artwork_url is not None:
            if not isinstance(artwork_url, str):
                raise TypeError("artworkUrl must be a string, or none.")
        
        isrc = payload.get("isrc")
        if isrc is not None:
            if not isinstance(isrc, str):
                raise TypeError("isrc must be a string, or none.")

        source_name = payload.get("sourceName")
        if source_name is None:
            raise ValueError("sourceName cannot be none.")
        if not isinstance(source_name, str):
            raise TypeError("sourceName must be a string.")

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
    """Base track.

    The base track data.

    Find out more [here](https://lavalink.dev/api/rest.html#track).
    """

    encoded: str
    """The base64 encoded track data."""
    info: TrackInfo
    """Information about the track"""
    plugin_info: t.Mapping[t.Any, t.Any]
    """Additional track info provided by plugins"""
    user_data: t.Mapping[t.Any, t.Any]
    """Additional track data."""
    requestor: Snowflake | None = None
    """
    The person who requested this track.

    !!! INFO
        This is an internal feature, not something from lavalink. If this track is apart of a lavalink event, then it will most likely be empty.
    """

    @classmethod
    def _from_payload(cls, payload: t.Mapping[str, t.Any]) -> Track:
        
        encoded = payload.get("encoded")
        if encoded is None:
            raise ValueError("encoded cannot be none.")
        if not isinstance(encoded, str):
            raise TypeError("encoded must be a string.")
        
        track_info = payload.get("info")
        if track_info is None:
            raise ValueError("info cannot be none.")
        try:
            info = TrackInfo._from_payload(track_info)
        except TypeError:
            raise
        except ValueError:
            raise
        
        #TODO: These might need checks, however, I am unsure.
        plugin_info = payload.get("pluginInfo", {})
        user_data = payload.get("userData", {})

        return cls(
            encoded, 
            info, 
            plugin_info, 
            user_data,
            None,
        )


@attrs.define
class PlaylistInfo(PayloadBase[t.Mapping[str, t.Any]]):
    """Playlist information.

    The playlist info object.

    Find out more [here](https://lavalink.dev/api/rest#playlist-info).
    """

    name: str
    """The name of the playlist."""
    selected_track: int
    """The selected track of the playlist (`-1` if no track is selected)"""

    @classmethod
    def _from_payload(cls, payload: t.Mapping[str, t.Any]) -> PlaylistInfo:
        name = payload.get("name")
        if name is None:
            raise ValueError("name cannot be none.")
        if not isinstance(name, str):
            raise TypeError("name must be a string.")
        
        selected_track = payload.get("selectedTrack")
        if selected_track is None:
            raise ValueError("selectedTrack cannot be none.")
        if not isinstance(selected_track, int):
            raise TypeError("selectedTrack must be a integer.")

        return cls(
            name, 
            selected_track,
        )


@attrs.define
class Playlist(PayloadBase[t.Mapping[str, t.Any]]):
    """Playlist.

    The playlist object.

    Find out more [here](https://lavalink.dev/api/rest.html#playlist-result-data).
    """

    info: PlaylistInfo
    """The info of the playlist."""
    plugin_info: t.Mapping[str, t.Any]
    """Addition playlist info provided by plugins"""
    tracks: t.Sequence[Track]
    """The tracks in this playlist."""

    @classmethod
    def _from_payload(cls, payload: t.Mapping[str, t.Any]) -> Playlist:
        info = payload.get("info")
        print(info)
        if info is None:
            raise ValueError("info cannot be none.")
        try:
            info = PlaylistInfo._from_payload(info)
        except TypeError:
            raise
        except ValueError:
            raise

        #TODO: These might need checks, however, I am unsure.
        plugin_info = payload.get("pluginInfo", {})

        tracks: list[Track] = []
        for track in payload["tracks"]:
            try:
                new_track = Track._from_payload(track)
            except TypeError:
                raise
            except ValueError:
                raise

            tracks.append(new_track)

        return cls(
            info, 
            plugin_info, 
            tuple(tracks),
        )


@attrs.define
class SearchResult(PayloadBase[t.Sequence[t.Mapping[str, t.Any]]]):
    """Search result.

    A search result, that has a list of tracks, from the search result.

    Find out more [here](https://lavalink.dev/api/rest.html#search-result-data).
    """

    tracks: t.Sequence[Track]
    """The tracks from the search result."""

    @classmethod
    def _from_payload(cls, payload: t.Sequence[t.Mapping[str, t.Any]]) -> SearchResult:
        tracks: list[Track] = []
        for track in payload:
            try:
                new_track = Track._from_payload(track)
            except TypeError:
                raise
            except ValueError:
                raise

            tracks.append(new_track)

        return cls(tracks)


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
