"""Statistics.

The statistics payload.
"""

from __future__ import annotations

from .bases import PayloadBase
import typing as t

from pydantic import Field

__all__ = (
    "StatsMemory",
    "StatsCpu",
    "StatsFrameStatistics",
    "Statistics"
)

class StatsMemory(PayloadBase):
    """
    All of the Statistics Memory information.

    Find out more [here](https://lavalink.dev/api/websocket.html#memory).
    """

    free: int
    """The amount of free memory in bytes"""
    used: int
    """The amount of used memory in bytes"""
    allocated: int
    """The amount of allocated memory in bytes"""
    reservable: int
    """The amount of reservable memory in bytes"""


class StatsCpu(PayloadBase):
    """
    All of the Statistics CPU information.

    Find out more [here](https://lavalink.dev/api/websocket.html#cpu).
    """

    cores: int
    """The amount of cores the server has."""
    system_load: t.Annotated[float | int, Field(alias="systemLoad")]
    """The system load of the server."""
    lavalink_load: t.Annotated[float | int, Field(alias="lavalinkLoad")]
    """The load of Lavalink on the server."""


class StatsFrameStatistics(PayloadBase):
    """
    All of the Statistics frame statistics information.

    Find out more [here](https://lavalink.dev/api/websocket.html#frame-stats).
    """

    sent: int
    """The amount of frames sent to Discord."""
    nulled: int
    """The amount of frames that were nulled."""
    deficit: int
    """The difference between sent frames and the expected amount of frames."""


class Statistics(PayloadBase):
    """
    All of the Statistics information.

    Find out more [here](https://lavalink.dev/api/websocket.html#stats-object).
    """

    players: int
    """The amount of players connected to the session."""
    playing_players: int
    """The amount of players playing a track."""
    uptime: int
    """The uptime of the session in milliseconds."""
    memory: StatsMemory
    """The memory stats of the session."""
    cpu: StatsCpu
    """The cpu stats of the session."""
    frame_statistics: t.Annotated[
        StatsFrameStatistics | None, Field(default=None, alias="frameStats")
    ] = None
    """The frame stats of the session."""