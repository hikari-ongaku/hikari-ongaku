"""
Statistics ABC's.

The statistic abstract classes.
"""

from __future__ import annotations

import abc
import typing

__all__ = ("Memory", "Cpu", "FrameStatistics", "Statistics")


class Statistics(abc.ABC):
    """
    Statistics.

    All of the Statistics information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#stats-object)
    """

    __slots__: typing.Sequence[str] = (
        "_players",
        "_playing_players",
        "_uptime",
        "_memory",
        "_cpu",
        "_frame_statistics"
    )

    @property
    def players(self) -> int:
        """The amount of players connected to the session."""
        ...

    @property
    def playing_players(self) -> int:
        """The amount of players playing a track."""
        ...

    @property
    def uptime(self) -> int:
        """The uptime of the session in milliseconds."""
        ...

    @property
    def memory(self) -> Memory:
        """The memory stats of the session."""
        ...

    @property
    def cpu(self) -> Cpu:
        """The CPU stats of the session."""
        ...

    @property
    def frame_stats(self) -> FrameStatistics | None:
        """The frame statistics of the session."""
        ...

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Statistics):
            return False

        if self.players != other.players:
            return False

        if self.playing_players != other.playing_players:
            return False

        if self.uptime != other.uptime:
            return False

        if self.memory != other.memory:
            return False

        if self.cpu != other.cpu:
            return False

        return self.frame_stats == other.frame_stats


class Memory(abc.ABC):
    """
    Statistics Memory.

    All of the Statistics Memory information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#memory)
    """

    __slots__: typing.Sequence[str] = (
        "_free",
        "_used",
        "_allocated",
        "_reservable",
    )

    @property
    def free(self) -> int:
        """The amount of free memory in bytes."""
        return self._free

    @property
    def used(self) -> int:
        """The amount of used memory in bytes."""
        return self._used

    @property
    def allocated(self) -> int:
        """The amount of allocated memory in bytes."""
        return self._allocated

    @property
    def reservable(self) -> int:
        """The amount of reservable memory in bytes."""
        return self._reservable

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Memory):
            return False

        if self.free != other.free:
            return False

        if self.used != other.used:
            return False

        if self.allocated != other.allocated:
            return False

        return self.reservable == other.reservable


class Cpu(abc.ABC):
    """
    Statistics CPU.

    All of the Statistics CPU information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#cpu)
    """

    __slots__: typing.Sequence[str] = (
        "_cores",
        "_system_load",
        "_lavalink_load",
    )

    @property
    def cores(self) -> int:
        """The amount of cores the server has."""
        return self._cores

    @property
    def system_load(self) -> float:
        """The system load of the server."""
        return self._system_load

    @property
    def lavalink_load(self) -> float:
        """The load of Lavalink on the server."""
        return self._lavalink_load

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cpu):
            return False

        if self.cores != other.cores:
            return False

        if self.system_load != other.system_load:
            return False

        return self.lavalink_load == other.lavalink_load


class FrameStatistics(abc.ABC):
    """
    Statistics Frame Statistics.

    All of the Statistics frame statistics information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#frame-stats)
    """

    __slots__: typing.Sequence[str] = ("_sent", "_nulled", "_deficit")

    @property
    def sent(self) -> int:
        """The amount of frames sent to Discord."""
        return self._sent

    @property
    def nulled(self) -> int:
        """The amount of frames that were nulled."""
        return self._nulled

    @property
    def deficit(self) -> int:
        """The difference between sent frames and the expected amount of frames."""
        return self._deficit

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FrameStatistics):
            return False

        if self.sent != other.sent:
            return False

        if self.nulled != other.nulled:
            return False

        return self.deficit == other.deficit


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
