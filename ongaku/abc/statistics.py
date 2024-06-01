"""
Statistics ABC's.

The statistic abstract classes.
"""

from __future__ import annotations

import abc

__all__ = ("Memory", "Cpu", "FrameStatistics", "Statistics")


class Statistics(abc.ABC):
    """
    Statistics.

    All of the Statistics information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#stats-object)
    """

    @property
    @abc.abstractmethod
    def players(self) -> int:
        """The amount of players connected to the session."""
        ...

    @property
    @abc.abstractmethod
    def playing_players(self) -> int:
        """The amount of players playing a track."""
        ...

    @property
    @abc.abstractmethod
    def uptime(self) -> int:
        """The uptime of the session in milliseconds."""
        ...

    @property
    @abc.abstractmethod
    def memory(self) -> Memory:
        """The memory stats of the session."""
        ...

    @property
    @abc.abstractmethod
    def cpu(self) -> Cpu:
        """The CPU stats of the session."""
        ...

    @property
    @abc.abstractmethod
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

        if self.frame_stats != other.frame_stats:
            return False

        return True


class Memory(abc.ABC):
    """
    Statistics Memory.

    All of the Statistics Memory information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#memory)
    """

    @property
    @abc.abstractmethod
    def free(self) -> int:
        """The amount of free memory in bytes."""
        ...

    @property
    @abc.abstractmethod
    def used(self) -> int:
        """The amount of used memory in bytes."""
        ...

    @property
    @abc.abstractmethod
    def allocated(self) -> int:
        """The amount of allocated memory in bytes."""
        ...

    @property
    @abc.abstractmethod
    def reservable(self) -> int:
        """The amount of reservable memory in bytes."""
        ...

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Memory):
            return False

        if self.free != other.free:
            return False

        if self.used != other.used:
            return False

        if self.allocated != other.allocated:
            return False

        if self.reservable != other.reservable:
            return False

        return True


class Cpu(abc.ABC):
    """
    Statistics CPU.

    All of the Statistics CPU information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#cpu)
    """

    @property
    @abc.abstractmethod
    def cores(self) -> int:
        """The amount of cores the server has."""
        ...

    @property
    @abc.abstractmethod
    def system_load(self) -> float:
        """The system load of the server."""
        ...

    @property
    @abc.abstractmethod
    def lavalink_load(self) -> float:
        """The load of Lavalink on the server."""
        ...

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cpu):
            return False

        if self.cores != other.cores:
            return False

        if self.system_load != other.system_load:
            return False

        if self.lavalink_load != other.lavalink_load:
            return False

        return True


class FrameStatistics(abc.ABC):
    """
    Statistics Frame Statistics.

    All of the Statistics frame statistics information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#frame-stats)
    """

    @property
    @abc.abstractmethod
    def sent(self) -> int:
        """The amount of frames sent to Discord."""
        ...

    @property
    @abc.abstractmethod
    def nulled(self) -> int:
        """The amount of frames that were nulled."""
        ...

    @property
    @abc.abstractmethod
    def deficit(self) -> int:
        """The difference between sent frames and the expected amount of frames."""
        ...

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FrameStatistics):
            return False

        if self.sent != other.sent:
            return False

        if self.nulled != other.nulled:
            return False

        if self.deficit != other.deficit:
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
