"""
Track ABC's.

The tracks abstract classes.
"""

from __future__ import annotations

import abc
import typing

if typing.TYPE_CHECKING:
    import hikari

__all__ = (
    "TrackInfo",
    "Track",
)


class Track(abc.ABC):
    """
    Track.

    The base track.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#track)
    """

    __slots__: typing.Sequence[str] = (
        "_encoded",
        "_info",
        "_plugin_info",
        "_user_data",
        "_requestor",
    )

    @property
    def encoded(self) -> str:
        """The BASE-64 encoded track data."""
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
        """Additional track data.

        !!! warning
            If you store a value of any type under the name `ongaku_requestor` it will be overridden.
        """
        return self._user_data

    @property
    def requestor(self) -> hikari.Snowflake | None:
        """The person who requested this track."""
        return self._requestor

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Track):
            return False

        if self.encoded != other.encoded:
            return False

        if self.info != other.info:
            return False

        if self.plugin_info != other.plugin_info:
            return False

        if self.user_data != other.user_data:
            return False

        if self.requestor != other.requestor:
            return False

        return True


class TrackInfo(abc.ABC):
    """
    Track information.

    All of the information about the track.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#track-info)
    """

    __slots__: typing.Sequence[str] = (
        "_identifier",
        "_is_seekable",
        "_author",
        "_length",
        "_is_stream",
        "_position",
        "_title",
        "_source_name",
        "_uri",
        "_artwork_url",
        "_isrc",
    )

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

    def __eq__(self, other: object) -> bool:  # noqa: C901
        if not isinstance(other, TrackInfo):
            return False

        if self.identifier != other.identifier:
            return False

        if self.is_seekable != other.is_seekable:
            return False

        if self.author != other.author:
            return False

        if self.length != other.length:
            return False

        if self.is_stream != other.is_stream:
            return False

        if self.position != other.position:
            return False

        if self.title != other.title:
            return False

        if self.source_name != other.source_name:
            return False

        if self.uri != other.uri:
            return False

        if self.artwork_url != other.artwork_url:
            return False

        if self.isrc != other.isrc:
            return False

        return True


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
