"""
Track ABC's.

The tracks abstract classes.
"""

from __future__ import annotations

import typing

import hikari
import msgspec

from ongaku.abc.bases import PayloadBase

__all__ = (
    "TrackInfo",
    "Track",
)


class TrackInfo(PayloadBase):
    """
    Track information.

    All of the information about the track.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest.html#track-info)
    """

    identifier: str
    """The track identifier."""
    is_seekable: bool = msgspec.field(name="isSeekable")
    """Whether the track is seekable."""
    author: str
    """The track author."""
    length: int
    """The track length in milliseconds."""
    is_stream: bool = msgspec.field(name="isStream")
    """Whether the track is a stream."""
    position: int
    """The track position in milliseconds."""
    title: str
    """The track title."""
    source_name: str = msgspec.field(name="sourceName")
    """The tracks source name."""
    uri: str | None = msgspec.field(default=None)
    """The track uri."""
    artwork_url: str | None = msgspec.field(default=None, name="artworkUrl")
    """The track artwork url"""
    isrc: str | None = msgspec.field(default=None)
    """The track ISRC"""


class Track(PayloadBase):
    """Base track.

    The base track data.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest.html#track)
    """

    encoded: str
    """The base64 encoded track data."""
    info: TrackInfo
    """Information about the track."""
    plugin_info: typing.Mapping[typing.Any, typing.Any] | None = msgspec.field(
        default=None, name="pluginInfo"
    )
    """Additional track info provided by plugins."""
    user_data: typing.Mapping[typing.Any, typing.Any] | None = msgspec.field(
        default=None, name="userData"
    )
    """Additional track data."""
    requestor: hikari.Snowflake | None = msgspec.field(default=None)
    """
    The user who requested this track.

    !!! INFO
        This is an internal feature, not something from lavalink. If this track is apart of a lavalink event, then it will most likely be empty.
    """


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
