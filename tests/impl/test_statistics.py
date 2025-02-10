from ongaku.impl.statistics import Cpu
from ongaku.impl.statistics import FrameStatistics
from ongaku.impl.statistics import Memory
from ongaku.impl.statistics import Statistics


def test_statistics():
    memory = Memory(free=1, used=2, allocated=3, reservable=4)
    cpu = Cpu(cores=1, system_load=2.3, lavalink_load=4.5)
    frame_statistics = FrameStatistics(sent=1, nulled=2, deficit=3)
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
    assert statistics.frame_stats == frame_statistics


def test_statistics_memory():
    stats_memory = Memory(free=1, used=2, allocated=3, reservable=4)

    assert stats_memory.free == 1
    assert stats_memory.used == 2
    assert stats_memory.allocated == 3
    assert stats_memory.reservable == 4


def test_statistics_cpu():
    stats_cpu = Cpu(cores=1, system_load=2.3, lavalink_load=4.5)

    assert stats_cpu.cores == 1
    assert stats_cpu.system_load == 2.3
    assert stats_cpu.lavalink_load == 4.5


def test_statistics_frame_stats():
    stats_frame_statistics = FrameStatistics(sent=1, nulled=2, deficit=3)

    assert stats_frame_statistics.sent == 1
    assert stats_frame_statistics.nulled == 2
    assert stats_frame_statistics.deficit == 3
