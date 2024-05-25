# ruff: noqa: D101, D102

from __future__ import annotations

from ongaku.abc import statistics as statistics_


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
