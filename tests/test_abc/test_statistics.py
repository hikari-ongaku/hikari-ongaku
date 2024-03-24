# ruff: noqa: D100, D101, D102

import unittest

from ongaku.abc.statistics import Statistics
from ongaku.abc.statistics import StatsCpu
from ongaku.abc.statistics import StatsFrameStatistics
from ongaku.abc.statistics import StatsMemory
from tests import payload


class TestStatsMemory(unittest.TestCase):
    def test_base(self):
        stats_memory = StatsMemory(free=1, used=2, allocated=3, reservable=4)

        assert stats_memory.free == 1
        assert stats_memory.used == 2
        assert stats_memory.allocated == 3
        assert stats_memory.reservable == 4

    def test_from_payload(self):
        stats_memory = StatsMemory._from_payload(payload.convert(payload.STATS_MEMORY))

        assert stats_memory.free == 1
        assert stats_memory.used == 2
        assert stats_memory.allocated == 3
        assert stats_memory.reservable == 4

    def test_to_payload(self):
        stats_memory = StatsMemory._from_payload(payload.convert(payload.STATS_MEMORY))
        assert stats_memory._to_payload == payload.STATS_MEMORY


class TestStatsCpu(unittest.TestCase):
    def test_base(self):
        stats_cpu = StatsCpu(cores=1, system_load=2.2, lavalink_load=3.3)

        assert stats_cpu.cores == 1
        assert stats_cpu.system_load == 2.2
        assert stats_cpu.lavalink_load == 3.3

    def test_from_payload(self):
        stats_cpu = StatsCpu._from_payload(payload.convert(payload.STATS_CPU))

        assert stats_cpu.cores == 1
        assert stats_cpu.system_load == 2.2
        assert stats_cpu.lavalink_load == 3.3

    def test_to_payload(self):
        stats_cpu = StatsCpu._from_payload(payload.convert(payload.STATS_CPU))

        assert stats_cpu._to_payload == payload.STATS_CPU


class TestStatsFrameStatistics(unittest.TestCase):
    def test_base(self):
        stats_frame_statistics = StatsFrameStatistics(sent=1, nulled=2, deficit=3)

        assert stats_frame_statistics.sent == 1
        assert stats_frame_statistics.nulled == 2
        assert stats_frame_statistics.deficit == 3

    def test_from_payload(self):
        stats_frame_statistics = StatsFrameStatistics._from_payload(
            payload.convert(payload.STATS_FRAME_STATS)
        )

        assert stats_frame_statistics.sent == 1
        assert stats_frame_statistics.nulled == 2
        assert stats_frame_statistics.deficit == 3

    def test_to_payload(self):
        stats_frame_statistics = StatsFrameStatistics._from_payload(
            payload.convert(payload.STATS_FRAME_STATS)
        )
        assert stats_frame_statistics._to_payload == payload.STATS_FRAME_STATS


class TestStatistics(unittest.TestCase):
    def test_base(self):
        memory = StatsMemory._from_payload(payload.convert(payload.STATS_MEMORY))
        cpu = StatsCpu._from_payload(payload.convert(payload.STATS_CPU))
        frame_statistics = StatsFrameStatistics._from_payload(
            payload.convert(payload.STATS_FRAME_STATS)
        )
        statistics = Statistics(
            players=1,
            playing_players=2,
            uptime=3,
            memory=memory,
            cpu=cpu,
            frame_statistics=frame_statistics,
        )

        assert statistics.players == 1
        assert statistics.playing_players == 2
        assert statistics.uptime == 3
        assert statistics.memory == memory
        assert statistics.cpu == cpu
        assert statistics.frame_statistics == frame_statistics

    def test_from_payload(self):
        memory = StatsMemory._from_payload(payload.convert(payload.STATS_MEMORY))
        cpu = StatsCpu._from_payload(payload.convert(payload.STATS_CPU))
        frame_statistics = StatsFrameStatistics._from_payload(
            payload.convert(payload.STATS_FRAME_STATS)
        )
        statistics = Statistics._from_payload(payload.convert(payload.STATS_OP))

        assert statistics.players == 1
        assert statistics.playing_players == 2
        assert statistics.uptime == 3
        assert statistics.memory == memory
        assert statistics.cpu == cpu
        assert statistics.frame_statistics == frame_statistics

    def test_to_payload(self):
        statistics = Statistics._from_payload(payload.convert(payload.STATS_OP))

        assert statistics._to_payload == payload.STATS_OP
