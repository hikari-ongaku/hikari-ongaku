"""
Track ABC's.

The tracks abstract classes.
"""

from __future__ import annotations

import typing
import hikari
import attrs

__all__ = (
    "TrackInfo",
    "Track",
)


@attrs.define
class TrackInfo:
    """
    Track information.

    All of the information about the track.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#track-info)
    """

    _identifier: str = attrs.field(alias="identifier")
    _is_seekable: bool = attrs.field(alias="is_seekable")
    _author: str = attrs.field(alias="author")
    _length: int = attrs.field(alias="length")
    _is_stream: bool = attrs.field(alias="is_stream")
    _position: int = attrs.field(alias="position")
    _title: str = attrs.field(alias="title")
    _source_name: str = attrs.field(alias="source_name")
    _uri: str | None = attrs.field(alias="uri")
    _artwork_url: str | None = attrs.field(alias="artwork_url")
    _isrc: str | None = attrs.field(alias="isrc")

    @property
    def identifier(self) -> str:
        """The track identifier."""
        return self._identifier

    @property
    def is_seekable(self) -> bool:
        """Whether the track is seekable."""
        return self._is_seekable

    @property
    def author(self) -> str:
        """The track author."""
        return self._author
    
    @property
    def length(self) -> int:
        """The track length in milliseconds."""
        return self._length

    @property
    def is_stream(self) -> bool:
        """Whether the track is a stream."""
        return self._is_stream
    
    @property
    def position(self) -> int:
        """The track position in milliseconds."""
        return self._position

    @property
    def title(self) -> str:
        """The track title."""
        return self._title
    
    @property
    def source_name(self) -> str:
        """The tracks source name."""
        return self._source_name
    
    @property
    def uri(self) -> str | None:
        """The track URI."""
        return self._uri
    
    @property
    def artwork_url(self) -> str | None:
        """The track artwork URL."""
        return self._artwork_url

    @property
    def isrc(self) -> str | None:
        """The track ISRC."""
        return self._isrc

@attrs.define
class Track:
    """Base track.

    The base track data.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#track)
    """

    _encoded: str = attrs.field(alias="encoded")
    _info: TrackInfo = attrs.field(alias="info")
    _plugin_info: typing.Mapping[str, typing.Any] = attrs.field(alias="plugin_info")
    _user_data: typing.Mapping[str, typing.Any] = attrs.field(alias="user_data")
    _requestor: hikari.Snowflake | None = attrs.field(default=None, alias="requestor")

    @property
    def encoded(self) -> str:
        """The base64 encoded track data."""
        return self._encoded

    @property
    def info(self) -> TrackInfo:
        """Information about the track."""
        return self._info
    
    @property
    def plugin_info(self) -> typing.Mapping[str, typing.Any]:
        """Additional track info provided by plugins."""
        return self._plugin_info
    
    @property
    def user_data(self) -> typing.Mapping[str, typing.Any]:
        """Additional track data."""
        return self._user_data
    
    @property
    def requestor(self) -> hikari.Snowflake | None:
        """The person who requested this track."""
        return self._requestor
    
    @requestor.setter
    def _set_requestor(self, value: hikari.Snowflake) -> hikari.Snowflake | None:
        self._requestor = value

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
