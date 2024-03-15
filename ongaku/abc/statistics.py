"""
Statistics ABC's.

The statistic abstract classes.
"""

from __future__ import annotations

import typing as t

from pydantic import Field

from .bases import PayloadBase

__all__ = ("StatsMemory", "StatsCpu", "StatsFrameStatistics", "Statistics")


class StatsMemory(PayloadBase):
    """
    Statistics Memory.

    All of the Statistics Memory information.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/websocket.html#memory)
    """

    free: int
    """The amount of free memory in bytes."""
    used: int
    """The amount of used memory in bytes."""
    allocated: int
    """The amount of allocated memory in bytes."""
    reservable: int
    """The amount of reservable memory in bytes."""


class StatsCpu(PayloadBase):
    """
    Statistics CPU.

    All of the Statistics CPU information.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/websocket.html#cpu)
    """

    cores: int
    """The amount of cores the server has."""
    system_load: t.Annotated[float | int, Field(alias="systemLoad")]
    """The system load of the server."""
    lavalink_load: t.Annotated[float | int, Field(alias="lavalinkLoad")]
    """The load of Lavalink on the server."""


class StatsFrameStatistics(PayloadBase):
    """
    Statistics Frame Statistics.

    All of the Statistics frame statistics information.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/websocket.html#frame-stats)
    """

    sent: int
    """The amount of frames sent to Discord."""
    nulled: int
    """The amount of frames that were nulled."""
    deficit: int
    """The difference between sent frames and the expected amount of frames."""


class Statistics(PayloadBase):
    """
    Statistics.

    All of the Statistics information.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/websocket.html#stats-object)
    """

    players: int
    """The amount of players connected to the session."""
    playing_players: t.Annotated[int, Field(alias="playingPlayers")]
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
