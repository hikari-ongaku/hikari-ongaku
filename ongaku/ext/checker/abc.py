# noqa: D100
from __future__ import annotations

import enum

import attrs


@attrs.define
class Checked:
    """
    Checked value.

    The checked, and confirmed value, with its specific type attached.
    """

    value: str
    """The value.
    
    This is the value, based on the [type][ongaku.ext.checker.abc.CheckedType] it is.
    """
    type: CheckedType
    """The type of the checked value."""


class CheckedType(enum.IntEnum):
    """
    Checked type.

    The type of result you have received.
    """

    QUERY = 0
    """The result was a query."""
    TRACK = 1
    """The result was a track."""
    PLAYLIST = 2
    """The result was a playlist."""
