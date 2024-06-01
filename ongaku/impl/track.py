"""
Track Impl's.

The track implemented classes.
"""

from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    import hikari

from ongaku.abc import track as track_

__all__ = ("Track", "TrackInfo")


class Track(track_.Track):
    def __init__(
        self,
        encoded: str,
        info: track_.TrackInfo,
        plugin_info: typing.Mapping[str, typing.Any],
        user_data: typing.Mapping[str, typing.Any],
        requestor: hikari.Snowflake | None,
    ) -> None:
        self._encoded = encoded
        self._info = info
        self._plugin_info = plugin_info
        self._user_data = user_data
        self._requestor = requestor

    @property
    def encoded(self) -> str:
        return self._encoded

    @property
    def info(self) -> track_.TrackInfo:
        return self._info

    @property
    def plugin_info(self) -> typing.Mapping[str, typing.Any]:
        return self._plugin_info

    @property
    def user_data(self) -> typing.Mapping[str, typing.Any]:
        return self._user_data

    @property
    def requestor(self) -> hikari.Snowflake | None:
        return self._requestor

    @requestor.setter
    def _set_requestor(self, value: hikari.Snowflake) -> None:
        self._requestor = value


class TrackInfo(track_.TrackInfo):
    def __init__(
        self,
        identifier: str,
        is_seekable: bool,
        author: str,
        length: int,
        is_stream: bool,
        position: int,
        title: str,
        source_name: str,
        uri: str | None,
        artwork_url: str | None,
        isrc: str | None,
    ) -> None:
        self._identifier = identifier
        self._is_seekable = is_seekable
        self._author = author
        self._length = length
        self._is_stream = is_stream
        self._position = position
        self._title = title
        self._source_name = source_name
        self._uri = uri
        self._artwork_url = artwork_url
        self._isrc = isrc

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def is_seekable(self) -> bool:
        return self._is_seekable

    @property
    def author(self) -> str:
        return self._author

    @property
    def length(self) -> int:
        return self._length

    @property
    def is_stream(self) -> bool:
        return self._is_stream

    @property
    def position(self) -> int:
        return self._position

    @property
    def title(self) -> str:
        return self._title

    @property
    def source_name(self) -> str:
        return self._source_name

    @property
    def uri(self) -> str | None:
        return self._uri

    @property
    def artwork_url(self) -> str | None:
        return self._artwork_url

    @property
    def isrc(self) -> str | None:
        return self._isrc


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
