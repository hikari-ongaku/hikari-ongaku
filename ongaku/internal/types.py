"""
Types.

All types for ongaku.
"""

from __future__ import annotations

import typing

import hikari
import pydantic

from ongaku.abc.bases import _snowflake_to_string
from ongaku.abc.bases import _string_to_snowflake
from ongaku.abc.info import Info
from ongaku.abc.player import Player
from ongaku.abc.player import PlayerVoice
from ongaku.abc.playlist import Playlist
from ongaku.abc.route_planner import RoutePlannerStatus
from ongaku.abc.session import Session
from ongaku.abc.statistics import Statistics
from ongaku.abc.track import Track

__all__ = (
    "RESTClientT",
    "GuildIdT",
)

# Type Variables.

RESTClientT = typing.TypeVar(
    "RESTClientT",
    Info,
    Player,
    PlayerVoice,
    Session,
    Playlist,
    Track,
    RoutePlannerStatus,
    Statistics,
    str,
    dict[str, typing.Any],
)

# Type Aliases
GuildIdT: typing.TypeAlias = "typing.Annotated[hikari.Snowflake, pydantic.WrapValidator(_string_to_snowflake), pydantic.WrapSerializer(_snowflake_to_string), pydantic.Field(alias='guildId')]"
