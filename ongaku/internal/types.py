"""
Types.

All types for ongaku.
"""

from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from ongaku.abc.info import Info
    from ongaku.abc.player import Player
    from ongaku.abc.player import PlayerVoice
    from ongaku.abc.playlist import Playlist
    from ongaku.abc.route_planner import RoutePlannerStatus
    from ongaku.abc.session import Session
    from ongaku.abc.statistics import Statistics
    from ongaku.abc.track import Track

__all__ = ("RESTClientT",)

# Type Variables.

RESTClientT = typing.TypeVar(
    "RESTClientT",
    bound="Info | Player | PlayerVoice | Session | Playlist | Track | RoutePlannerStatus | Statistics | str | dict[str, typing.Any]",
)


# Type Aliases
