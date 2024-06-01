"""
Statistics Impl's.

The statistics implemented classes.
"""

from __future__ import annotations

from ongaku.abc import statistics as statistics_

__all__ = ("Statistics", "Memory", "Cpu", "FrameStatistics")


class Statistics(statistics_.Statistics):
    def __init__(
        self,
        players: int,
        playing_players: int,
        uptime: int,
        memory: statistics_.Memory,
        cpu: statistics_.Cpu,
        frame_statistics: statistics_.FrameStatistics | None,
    ) -> None:
        self._players = players
        self._playing_players = playing_players
        self._uptime = uptime
        self._memory = memory
        self._cpu = cpu
        self._frame_statistics = frame_statistics

    @property
    def players(self) -> int:
        return self._players

    @property
    def playing_players(self) -> int:
        return self._playing_players

    @property
    def uptime(self) -> int:
        return self._uptime

    @property
    def memory(self) -> statistics_.Memory:
        return self._memory

    @property
    def cpu(self) -> statistics_.Cpu:
        return self._cpu

    @property
    def frame_stats(self) -> statistics_.FrameStatistics | None:
        return self._frame_statistics


class Memory(statistics_.Memory):
    def __init__(self, free: int, used: int, allocated: int, reservable: int) -> None:
        self._free = free
        self._used = used
        self._allocated = allocated
        self._reservable = reservable

    @property
    def free(self) -> int:
        return self._free

    @property
    def used(self) -> int:
        return self._used

    @property
    def allocated(self) -> int:
        return self._allocated

    @property
    def reservable(self) -> int:
        return self._reservable


class Cpu(statistics_.Cpu):
    def __init__(self, cores: int, system_load: float, lavalink_load: float) -> None:
        self._cores = cores
        self._system_load = system_load
        self._lavalink_load = lavalink_load

    @property
    def cores(self) -> int:
        return self._cores

    @property
    def system_load(self) -> float:
        return self._system_load

    @property
    def lavalink_load(self) -> float:
        return self._lavalink_load


class FrameStatistics(statistics_.FrameStatistics):
    def __init__(self, sent: int, nulled: int, deficit: int) -> None:
        self._sent = sent
        self._nulled = nulled
        self._deficit = deficit

    @property
    def sent(self) -> int:
        return self._sent

    @property
    def nulled(self) -> int:
        return self._nulled

    @property
    def deficit(self) -> int:
        return self._deficit


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
