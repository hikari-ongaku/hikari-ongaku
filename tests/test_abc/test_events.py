# ruff: noqa: D100, D101, D102
import json
import typing as t
import unittest

import hikari

from ongaku.abc.events import ReadyEvent
from ongaku.abc.events import StatisticsEvent
from ongaku.abc.events import StatsCpu
from ongaku.abc.events import StatsFrameStatistics
from ongaku.abc.events import StatsMemory
from ongaku.abc.events import TrackBase
from ongaku.abc.events import TrackEndEvent
from ongaku.abc.events import TrackExceptionEvent
from ongaku.abc.events import TrackStartEvent
from ongaku.abc.events import TrackStuckEvent
from ongaku.abc.events import WebsocketClosedEvent
from ongaku.abc.lavalink import ExceptionError
from ongaku.enums import SeverityType
from ongaku.enums import TrackEndReasonType

from .test_track import TrackTest

_test_bot = hikari.GatewayBot("", banner=None)


class ReadyEventTest(unittest.TestCase):
    ready_payload = {"resumed": True, "sessionId": "test_session_id"}

    def test_base(self):
        test_ready_event = ReadyEvent(
            bot_app=_test_bot, resumed=True, session_id="test_session_id"
        )

        assert test_ready_event.app == _test_bot
        assert test_ready_event.resumed is True
        assert test_ready_event.session_id == "test_session_id"

    def test_base_payload(self):
        test_ready_event = ReadyEvent._from_payload(self.ready_payload, app=_test_bot)

        assert test_ready_event.app == _test_bot
        assert test_ready_event.resumed is True
        assert test_ready_event.session_id == "test_session_id"


class StatsEventTest(unittest.TestCase):
    stats_payload: dict[str, t.Any] = {
        "players": 1,
        "playingPlayers": 1,
        "uptime": 123456789,
        "memory": {
            "free": 123456789,
            "used": 123456789,
            "allocated": 123456789,
            "reservable": 123456789,
        },
        "cpu": {"cores": 4, "systemLoad": 0.5, "lavalinkLoad": 0.5},
        "frameStats": {"sent": 6000, "nulled": 10, "deficit": -3010},
    }

    memory_payload = stats_payload["memory"]

    cpu_payload = stats_payload["cpu"]

    frame_stats_payload = stats_payload["frameStats"]

    def test_base(self):
        test_memory = StatsMemory(
            free=123456789, used=123456789, allocated=123456789, reservable=123456789
        )
        test_cpu = StatsCpu(cores=4, system_load=0.5, lavalink_load=0.5)
        test_frame_stats = StatsFrameStatistics(sent=6000, nulled=10, deficit=-3010)

        test_stats_event = StatisticsEvent(
            bot_app=_test_bot,
            players=1,
            playing_players=1,
            uptime=123456789,
            memory=test_memory,
            cpu=test_cpu,
            frame_statistics=test_frame_stats,
        )

        assert test_stats_event.app == _test_bot
        assert test_stats_event.players == 1
        assert test_stats_event.playing_players == 1
        assert test_stats_event.uptime == 123456789
        assert test_stats_event.memory == test_memory
        assert test_stats_event.cpu == test_cpu
        if test_stats_event.frame_statistics is not None:
            assert test_stats_event.frame_statistics == test_frame_stats

        print(json.dumps(test_stats_event._to_payload, indent=4))

        assert test_stats_event._to_payload == self.stats_payload

    def test_base_payload(self):
        test_stats_event = StatisticsEvent._from_payload(
            self.stats_payload, app=_test_bot
        )

        assert test_stats_event.app == _test_bot
        assert test_stats_event.players == 1
        assert test_stats_event.playing_players == 1
        assert test_stats_event.uptime == 123456789
        assert test_stats_event.memory.free == 123456789
        assert test_stats_event.memory.used == 123456789
        assert test_stats_event.memory.allocated == 123456789
        assert test_stats_event.memory.reservable == 123456789
        assert test_stats_event.cpu.cores == 4
        assert test_stats_event.cpu.system_load == 0.5
        assert test_stats_event.cpu.lavalink_load == 0.5
        if test_stats_event.frame_statistics is not None:
            assert test_stats_event.frame_statistics.sent == 6000
            assert test_stats_event.frame_statistics.nulled == 10
            assert test_stats_event.frame_statistics.deficit == -3010

        assert test_stats_event._to_payload == self.stats_payload

    def test_memory(self):
        test_memory = StatsMemory(
            free=123456789, used=123456789, allocated=123456789, reservable=123456789
        )

        assert test_memory.free == 123456789
        assert test_memory.used == 123456789
        assert test_memory.allocated == 123456789
        assert test_memory.reservable == 123456789

        assert test_memory._to_payload == self.memory_payload

    def test_memory_payload(self):
        test_memory = StatsMemory._from_payload(self.memory_payload)

        assert test_memory.free == 123456789
        assert test_memory.used == 123456789
        assert test_memory.allocated == 123456789
        assert test_memory.reservable == 123456789

        assert test_memory._to_payload == self.memory_payload

    def test_cpu(self):
        test_cpu = StatsCpu(cores=4, system_load=0.5, lavalink_load=0.5)

        assert test_cpu.cores == 4
        assert test_cpu.system_load == 0.5
        assert test_cpu.lavalink_load == 0.5
        print(test_cpu._to_payload)
        assert test_cpu._to_payload == self.cpu_payload

    def test_cpu_payload(self):
        test_cpu = StatsCpu._from_payload(self.cpu_payload)

        assert test_cpu.cores == 4
        assert test_cpu.system_load == 0.5
        assert test_cpu.lavalink_load == 0.5

        assert test_cpu._to_payload == self.cpu_payload

    def test_frame_stats(self):
        test_frame_stats = StatsFrameStatistics(sent=6000, nulled=10, deficit=-3010)

        assert test_frame_stats.sent == 6000
        assert test_frame_stats.nulled == 10
        assert test_frame_stats.deficit == -3010

        assert test_frame_stats._to_payload == self.frame_stats_payload

    def test_frame_stats_payload(self):
        test_frame_stats = StatsFrameStatistics._from_payload(self.frame_stats_payload)

        assert test_frame_stats.sent == 6000
        assert test_frame_stats.nulled == 10
        assert test_frame_stats.deficit == -3010

        assert test_frame_stats._to_payload == self.frame_stats_payload


class TrackBaseTest(unittest.TestCase):
    payload = {
        "guildId": "19216868440",
        "track": TrackTest.track_payload,
    }

    def test_track_base(self):
        test_track_base = TrackBase(
            bot_app=_test_bot,
            guild_id=hikari.Snowflake(19216868440),
            track=TrackTest.track_data,
        )

        assert test_track_base.app == _test_bot
        assert test_track_base.track == TrackTest.track_data
        assert test_track_base.guild_id == hikari.Snowflake(19216868440)

        assert test_track_base._to_payload == self.payload

    def test_track_base_payload(self):
        test_track_base = TrackBase._from_payload(self.payload, app=_test_bot)

        assert test_track_base.app == _test_bot
        assert test_track_base.guild_id == hikari.Snowflake(19216868440)
        assert test_track_base.track == TrackTest.track_data

        assert test_track_base._to_payload == self.payload


class TrackStartTest(unittest.TestCase):
    payload = {
        "guildId": "19216868440",
        "track": TrackTest.track_payload,
    }

    def test_base(self):
        test_start_event = TrackStartEvent(
            bot_app=_test_bot,
            guild_id=hikari.Snowflake(19216868440),
            track=TrackTest.track_data,
        )

        assert test_start_event.app == _test_bot
        assert test_start_event.track == TrackTest.track_data
        assert test_start_event.guild_id == hikari.Snowflake(19216868440)

        assert test_start_event._to_payload == self.payload

    def test_base_payload(self):
        test_start_event = TrackStartEvent._from_payload(self.payload, app=_test_bot)

        assert test_start_event.app == _test_bot
        assert test_start_event.guild_id == hikari.Snowflake(19216868440)
        assert test_start_event.track == TrackTest.track_data

        assert test_start_event._to_payload == self.payload


class TrackEndTest(unittest.TestCase):
    payload = {
        "guildId": "19216868440",
        "track": TrackTest.track_payload,
        "reason": "finished",
    }

    def test_base(self):
        test_end_event = TrackEndEvent(
            bot_app=_test_bot,
            guild_id=hikari.Snowflake(19216868440),
            track=TrackTest.track_data,
            reason=TrackEndReasonType.FINISHED,
        )

        assert test_end_event.app == _test_bot
        assert test_end_event.track == TrackTest.track_data
        assert test_end_event.guild_id == hikari.Snowflake(19216868440)
        assert test_end_event.reason == TrackEndReasonType.FINISHED

        assert test_end_event._to_payload == self.payload

    def test_base_payload(self):
        test_end_event = TrackEndEvent._from_payload(self.payload, app=_test_bot)

        assert test_end_event.app == _test_bot
        assert test_end_event.guild_id == hikari.Snowflake(19216868440)
        assert test_end_event.track == TrackTest.track_data
        assert test_end_event.reason == TrackEndReasonType.FINISHED


class TrackExceptionTest(unittest.TestCase):
    payload = {
        "guildId": "19216868440",
        "track": TrackTest.track_payload,
        "exception": {
            "message": "test_message",
            "severity": "common",
            "cause": "test_cause",
        },
    }

    def test_base(self):
        test_exception_event = TrackExceptionEvent(
            bot_app=_test_bot,
            guild_id=hikari.Snowflake(19216868440),
            track=TrackTest.track_data,
            exception=ExceptionError(
                message="test_message", severity=SeverityType.COMMON, cause="test_cause"
            ),
        )

        assert test_exception_event.app == _test_bot
        assert test_exception_event.track == TrackTest.track_data
        assert test_exception_event.guild_id == hikari.Snowflake(19216868440)
        assert test_exception_event.exception.message == "test_message"
        assert test_exception_event.exception.severity == SeverityType.COMMON
        assert test_exception_event.exception.cause == "test_cause"

        assert test_exception_event._to_payload == self.payload

    def test_base_payload(self):
        test_exception_event = TrackExceptionEvent._from_payload(
            self.payload, app=_test_bot
        )

        assert test_exception_event.app == _test_bot
        assert test_exception_event.guild_id == hikari.Snowflake(19216868440)
        assert test_exception_event.track == TrackTest.track_data
        assert test_exception_event.exception.message == "test_message"
        assert test_exception_event.exception.severity == SeverityType.COMMON
        assert test_exception_event.exception.cause == "test_cause"

        assert test_exception_event._to_payload == self.payload


class TrackStuckTest(unittest.TestCase):
    payload = {
        "guildId": "19216868440",
        "track": TrackTest.track_payload,
        "thresholdMs": 123456789,
    }

    def test_base(self):
        test_stuck_event = TrackStuckEvent(
            bot_app=_test_bot,
            guild_id=hikari.Snowflake(19216868440),
            track=TrackTest.track_data,
            threshold_ms=123456789,
        )

        assert test_stuck_event.app == _test_bot
        assert test_stuck_event.track == TrackTest.track_data
        assert test_stuck_event.guild_id == hikari.Snowflake(19216868440)
        assert test_stuck_event.threshold_ms == 123456789

        assert test_stuck_event._to_payload == self.payload

    def test_base_payload(self):
        test_stuck_event = TrackStuckEvent._from_payload(self.payload, app=_test_bot)

        assert test_stuck_event.app == _test_bot
        assert test_stuck_event.guild_id == hikari.Snowflake(19216868440)
        assert test_stuck_event.track == TrackTest.track_data
        assert test_stuck_event.threshold_ms == 123456789

        assert test_stuck_event._to_payload == self.payload


class WebsocketClosedTest(unittest.TestCase):
    payload = {
        "guildId": "19216868440",
        "code": 4006,
        "reason": "test_reason",
        "byRemote": True,
    }

    def test_base(self):
        test_websocket_closed_event = WebsocketClosedEvent(
            bot_app=_test_bot,
            guild_id=hikari.Snowflake(19216868440),
            code=4006,
            reason="test_reason",
            by_remote=True,
        )

        assert test_websocket_closed_event.app == _test_bot
        assert test_websocket_closed_event.code == 4006
        assert test_websocket_closed_event.reason == "test_reason"
        assert test_websocket_closed_event.by_remote is True

        assert test_websocket_closed_event._to_payload == self.payload

    def test_base_payload(self):
        test_websocket_closed_event = WebsocketClosedEvent._from_payload(
            self.payload, app=_test_bot
        )

        assert test_websocket_closed_event.app == _test_bot
        assert test_websocket_closed_event.code == 4006
        assert test_websocket_closed_event.reason == "test_reason"
        assert test_websocket_closed_event.by_remote is True

        assert test_websocket_closed_event._to_payload == self.payload
