import attrs
import typing as t
from .base import PayloadBase

@attrs.define
class TrackInfo(PayloadBase):
    """
    Track information

    All of the track information.

    Find out more [here](https://lavalink.dev/api/rest.html#track-info).

    Parameters
    ----------
    identifier : str
        The track identifier
    is_seekable : bool
        Whether the track is seekable
    author : str
        The track author
    length : int
        The track length in milliseconds
    is_stream : bool
        Whether the track is a stream
    title : str
        The track position in milliseconds
    source_name : str
        The track source name
    uri : str | None
        The track uri
    artwork_url : str | None
        The track artwork url
    isrc : str | None
        The track ISRC
    """

    identifier: str
    is_seekable: bool
    author: str
    length: int
    is_stream: bool
    position: int
    title: str
    source_name: str
    uri: t.Optional[str] = None
    artwork_url: t.Optional[str] = None
    isrc: t.Optional[str] = None

    @classmethod
    def from_payload(cls, payload: dict[str, t.Any]):
        """
        Track info parser

        parse a payload of information, to receive a `TrackInfo` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        TrackInfo
            The Track Info you parsed.
        """
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
class Track(PayloadBase):
    """
    Track

    The base track object.

    Find out more [here](https://lavalink.dev/api/rest.html#track).

    Parameters
    ----------
    encoded : str
        The base64 encoded track data
    info : TrackInfo
        Information about the track
    plugin_info : dict[Any, Any]
        Additional track info provided by plugins
    user_data : dict[Any, Any]
        Additional track data.
    """

    encoded: str
    info: TrackInfo
    plugin_info: dict[t.Any, t.Any]
    user_data: dict[t.Any, t.Any] | None = None

    @classmethod
    def from_payload(cls, payload: dict[str, t.Any]):
        """
        Track parser

        parse a payload of information, to receive a `Track` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        Track
            The Track you parsed.
        """
        encoded = payload["encoded"]
        info = TrackInfo.from_payload(payload["info"])
        plugin_info = payload["pluginInfo"]
        try:
            user_data = payload["userData"]
        except Exception:
            user_data = None

        return cls(encoded, info, plugin_info, user_data)


@attrs.define
class PlaylistInfo(PayloadBase):
    """
    Playlist info

    The playlist info object.

    Find out more [here](https://lavalink.dev/api/rest.html#track-info).

    Parameters
    ----------
    name : str
        The name of the playlist
    selected_track : int
        The selected track of the playlist (`-1` if no track is selected)
    """

    name: str
    selected_track: int

    @classmethod
    def from_payload(cls, payload: dict[str, t.Any]):
        """
        Playlist Info parser

        parse a payload of information, to receive a `PlaylistInfo` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        PlaylistInfo
            The Playlist Info you parsed.
        """
        name = payload["name"]
        selected_track = payload["selectedTrack"]

        return cls(name, selected_track)


@attrs.define
class Playlist(PayloadBase):
    """
    Playlist

    The playlist object.

    Find out more [here](https://lavalink.dev/api/rest.html#track-info).

    Parameters
    ----------
    info : PlaylistInfo
        The info of the playlist
    plugin_info : pluginInfo
        Addition playlist info provided by plugins
    tracks : tuple[Track]
    """

    info: PlaylistInfo
    plugin_info: dict[t.Any, t.Any]
    tracks: tuple[Track, ...]

    @classmethod
    def from_payload(cls, payload: dict[str, t.Any]):
        """
        Playlist Info parser

        parse a payload of information, to receive a `PlaylistInfo` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        PlaylistInfo
            The Playlist Info you parsed.
        """
        info = payload["info"]
        plugin_info = payload["pluginInfo"]

        tracks: list[Track] | tuple[Track, ...] = []
        for track in payload["tracks"]:
            try:
                new_track = Track.from_payload(track)
            except Exception as e:
                raise e

            tracks.append(new_track)

        return cls(info, plugin_info, tuple(tracks))


@attrs.define
class SearchResult(PayloadBase):
    tracks: tuple[Track, ...]

    @classmethod
    def from_payload(cls, payload: dict[str, t.Any]):
        """
        Playlist Info parser

        parse a payload of information, to receive a `PlaylistInfo` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        PlaylistInfo
            The Playlist Info you parsed.
        """
        tracks: list[Track] | tuple[Track, ...] = []
        print(payload)
        for track in payload:
            try:
                new_track = Track.from_payload(track)
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
