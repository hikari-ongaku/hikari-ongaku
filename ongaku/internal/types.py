"""
Types.

All types for ongaku.
"""
from __future__ import annotations

import typing as t

from ongaku.abc.info import Info
from ongaku.abc.player import Player
from ongaku.abc.player import PlayerVoice
from ongaku.abc.session import Session
from ongaku.abc.playlist import Playlist
from ongaku.abc.track import Track
from ongaku.abc.route_planner import RoutePlannerStatus
from ongaku.abc.statistics import Statistics

__all__ = (
    "RESTClientT",
)

RESTClientT = t.TypeVar(
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
    dict[str, t.Any],
)