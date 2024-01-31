# ruff: noqa
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
from ongaku.abc.track import Track
from ongaku.abc.track import TrackInfo
from ongaku.enums import SeverityType
from ongaku.enums import TrackEndReasonType

# TODO: make sure to fix, and add, _from_payload for all items.
# TODO: Fix user data error.

_test_bot = hikari.GatewayBot("", banner=None)
_test_info = TrackInfo(
    "test_identifier",
    False,
    "test_author",
    246,
    True,
    200,
    "test_title",
    "test_source_name",
)
_test_track = Track("test_encoded", _test_info, {}, {})


class ReadyEventTest(unittest.TestCase):  # noqa: D101
    def test_base(self):  # noqa: D102
        test_ready_event = ReadyEvent(_test_bot, False, "test_session_id")

        assert test_ready_event.app == _test_bot
        assert test_ready_event.resumed is False
        assert test_ready_event.session_id == "test_session_id"

    def test_base_payload(self):  # noqa: D102
        test_ready_event = ReadyEvent._from_payload(
            {"resumed": True, "sessionId": "test_session_id_payload"}, app=_test_bot
        )

        assert test_ready_event.app == _test_bot
        assert test_ready_event.resumed is True
        assert test_ready_event.session_id == "test_session_id_payload"


class StatsEventTest(unittest.TestCase):  # noqa: D101
    def test_base(self):  # noqa: D102
        test_memory = StatsMemory(1, 2, 3, 4)
        test_cpu = StatsCpu(1, 2.3, 4.5)
        test_frame_stats = StatsFrameStatistics(68, 12, -5)

        test_stats_event = StatisticsEvent(
            _test_bot, 2, 1, 32, test_memory, test_cpu, test_frame_stats
        )

        assert test_stats_event.app == _test_bot
        assert test_stats_event.players == 2
        assert test_stats_event.playing_players == 1
        assert test_stats_event.uptime == 32
        assert test_stats_event.memory.free == 1
        assert test_stats_event.memory.used == 2
        assert test_stats_event.memory.allocated == 3
        assert test_stats_event.memory.reservable == 4
        assert test_stats_event.cpu.cores == 1
        assert test_stats_event.cpu.system_load == 2.3
        assert test_stats_event.cpu.lavalink_load == 4.5
        if test_stats_event.frame_statistics is not None:
            assert test_stats_event.frame_statistics.sent == 68
            assert test_stats_event.frame_statistics.nulled == 12
            assert test_stats_event.frame_statistics.deficit == -5

    def test_base_payload(self):  # noqa: D102
        payload = {
            "op": "stats",
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

        test_stats_event = StatisticsEvent._from_payload(payload, app=_test_bot)

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

    def test_memory(self):  # noqa: D102
        test_memory = StatsMemory(1, 2, 3, 4)

        assert test_memory.free == 1
        assert test_memory.used == 2
        assert test_memory.allocated == 3
        assert test_memory.reservable == 4

    def test_memory_payload(self):  # noqa: D102
        payload = {
            "free": 123456789,
            "used": 123456789,
            "allocated": 123456789,
            "reservable": 123456789,
        }

        test_memory = StatsMemory._from_payload(payload)

        assert test_memory.free == 123456789
        assert test_memory.used == 123456789
        assert test_memory.allocated == 123456789
        assert test_memory.reservable == 123456789

    def test_cpu(self):  # noqa: D102
        test_cpu = StatsCpu(1, 2.3, 4)

        assert test_cpu.cores == 1
        assert test_cpu.system_load == 2.3
        assert test_cpu.lavalink_load == 4

    def test_cpu_payload(self):  # noqa: D102
        payload = {"cores": 4, "systemLoad": 0.5, "lavalinkLoad": 0.5}

        test_cpu = StatsCpu._from_payload(payload)

        assert test_cpu.cores == 4
        assert test_cpu.system_load == 0.5
        assert test_cpu.lavalink_load == 0.5

    def test_frame_stats(self):  # noqa: D102
        test_frame_stats = StatsFrameStatistics(1, 2, -3)

        assert test_frame_stats.sent == 1
        assert test_frame_stats.nulled == 2
        assert test_frame_stats.deficit == -3

    def test_frame_stats_payload(self):
        payload = {"sent": 6000, "nulled": 10, "deficit": -3010}

        test_frame_stats = StatsFrameStatistics._from_payload(payload)

        assert test_frame_stats.sent == 6000
        assert test_frame_stats.nulled == 10
        assert test_frame_stats.deficit == -3010


class TrackBaseTest(unittest.TestCase):
    def test_track_base(self):
        test_track_base = TrackBase(
            _test_bot,
            hikari.Snowflake(19216868440),
            _test_track,
        )

        assert test_track_base.app == _test_bot
        assert test_track_base.track == _test_track
        assert test_track_base.guild_id == hikari.Snowflake(19216868440)

    def test_track_base_payload(self):
        payload = {
            "guildId": "19216868440",
            "track": {
                "encoded": "test_encoded",
                "info": {
                    "identifier": "test_identifier",
                    "isSeekable": True,
                    "author": "test_author",
                    "length": 212000,
                    "isStream": False,
                    "position": 0,
                    "title": "test_title",
                    "uri": "test_uri",
                    "artworkUrl": "test_artwork",
                    "isrc": None,
                    "sourceName": "test_source_name",
                },
                "pluginInfo": {},
            },
        }
        test_track_base = TrackBase._from_payload(payload, app=_test_bot)

        assert test_track_base.app == _test_bot
        assert test_track_base.guild_id == hikari.Snowflake(19216868440)
        assert test_track_base.track.encoded == "test_encoded"
        assert test_track_base.track.plugin_info == {}
        assert test_track_base.track.user_data == {}

        assert test_track_base.track.info.identifier == "test_identifier"
        assert test_track_base.track.info.is_seekable is True
        assert test_track_base.track.info.author == "test_author"
        assert test_track_base.track.info.length == 212000
        assert test_track_base.track.info.is_stream is False
        assert test_track_base.track.info.position == 0
        assert test_track_base.track.info.title == "test_title"
        assert test_track_base.track.info.uri == "test_uri"
        assert test_track_base.track.info.artwork_url == "test_artwork"
        assert test_track_base.track.info.isrc is None
        assert test_track_base.track.info.source_name == "test_source_name"


class TrackStartTest(unittest.TestCase):
    def test_base(self):
        test_start_event = TrackStartEvent(
            _test_bot, hikari.Snowflake(19216868440), _test_track,
        )

        assert test_start_event.app == _test_bot
        assert test_start_event.track == _test_track
        assert test_start_event.guild_id == hikari.Snowflake(19216868440)

    def test_base_payload(self):
        payload = {
            "guildId": "19216868440",
            "track": {
                "encoded": "test_encoded",
                "info": {
                    "identifier": "test_identifier",
                    "isSeekable": True,
                    "author": "test_author",
                    "length": 212000,
                    "isStream": False,
                    "position": 0,
                    "title": "test_title",
                    "uri": "test_uri",
                    "artworkUrl": "test_artwork",
                    "isrc": None,
                    "sourceName": "test_source_name",
                },
                "pluginInfo": {},
            },
        }

        test_start_event = TrackStartEvent._from_payload(payload, app=_test_bot)

        assert test_start_event.app == _test_bot
        assert test_start_event.guild_id == hikari.Snowflake(19216868440)
        assert test_start_event.track.encoded == "test_encoded"
        assert test_start_event.track.plugin_info == {}
        assert test_start_event.track.user_data == {}

        assert test_start_event.track.info.identifier == "test_identifier"
        assert test_start_event.track.info.is_seekable is True
        assert test_start_event.track.info.author == "test_author"
        assert test_start_event.track.info.length == 212000
        assert test_start_event.track.info.is_stream is False
        assert test_start_event.track.info.position == 0
        assert test_start_event.track.info.title == "test_title"
        assert test_start_event.track.info.uri == "test_uri"
        assert test_start_event.track.info.artwork_url == "test_artwork"
        assert test_start_event.track.info.isrc is None
        assert test_start_event.track.info.source_name == "test_source_name"


class TrackEndTest(unittest.TestCase):
    def test_base(self):
        test_end_event = TrackEndEvent(
            _test_bot,
            hikari.Snowflake(19216868440),
            _test_track,
            TrackEndReasonType.FINISHED,
        )

        assert test_end_event.app == _test_bot
        assert test_end_event.track == _test_track
        assert test_end_event.guild_id == hikari.Snowflake(19216868440)
        assert test_end_event.reason == TrackEndReasonType.FINISHED

    def test_base_payload(self):
        payload = {
            "guildId": "19216868440",
            "track": {
                "encoded": "test_encoded",
                "info": {
                    "identifier": "test_identifier",
                    "isSeekable": True,
                    "author": "test_author",
                    "length": 212000,
                    "isStream": False,
                    "position": 0,
                    "title": "test_title",
                    "uri": "test_uri",
                    "artworkUrl": "test_artwork",
                    "isrc": None,
                    "sourceName": "test_source_name",
                },
                "pluginInfo": {},
            },
            "reason": "finished",
        }

        test_end_event = TrackEndEvent._from_payload(payload, app=_test_bot)

        assert test_end_event.app == _test_bot
        assert test_end_event.guild_id == hikari.Snowflake(19216868440)
        assert test_end_event.track.encoded == "test_encoded"
        assert test_end_event.track.plugin_info == {}
        assert test_end_event.track.user_data == {}

        assert test_end_event.track.info.identifier == "test_identifier"
        assert test_end_event.track.info.is_seekable is True
        assert test_end_event.track.info.author == "test_author"
        assert test_end_event.track.info.length == 212000
        assert test_end_event.track.info.is_stream is False
        assert test_end_event.track.info.position == 0
        assert test_end_event.track.info.title == "test_title"
        assert test_end_event.track.info.uri == "test_uri"
        assert test_end_event.track.info.artwork_url == "test_artwork"
        assert test_end_event.track.info.isrc is None
        assert test_end_event.track.info.source_name == "test_source_name"
        assert test_end_event.reason == TrackEndReasonType.FINISHED


class TrackExceptionTest(unittest.TestCase):
    def test_base(self):
        test_exception_event = TrackExceptionEvent(
            _test_bot,
            hikari.Snowflake(19216868440),
            _test_track,
            ExceptionError("test_message", SeverityType.COMMON, "test_cause"),
        )

        assert test_exception_event.app == _test_bot
        assert test_exception_event.track == _test_track
        assert test_exception_event.guild_id == hikari.Snowflake(19216868440)
        assert test_exception_event.exception.message == "test_message"
        assert test_exception_event.exception.severity == SeverityType.COMMON
        assert test_exception_event.exception.cause == "test_cause"

    def test_base_payload(self):
        payload = {
            "guildId": "19216868440",
            "track": {
                "encoded": "test_encoded",
                "info": {
                    "identifier": "test_identifier",
                    "isSeekable": True,
                    "author": "test_author",
                    "length": 212000,
                    "isStream": False,
                    "position": 0,
                    "title": "test_title",
                    "uri": "test_uri",
                    "artworkUrl": "test_artwork",
                    "isrc": None,
                    "sourceName": "test_source_name",
                },
                "pluginInfo": {},
            },
            "exception": {
                "message": "test_message",
                "severity": "common",
                "cause": "test_cause",
            },
        }

        test_exception_event = TrackExceptionEvent._from_payload(payload, app=_test_bot)

        assert test_exception_event.app == _test_bot
        assert test_exception_event.guild_id == hikari.Snowflake(19216868440)
        assert test_exception_event.track.encoded == "test_encoded"
        assert test_exception_event.track.plugin_info == {}
        assert test_exception_event.track.user_data == {}

        assert test_exception_event.track.info.identifier == "test_identifier"
        assert test_exception_event.track.info.is_seekable is True
        assert test_exception_event.track.info.author == "test_author"
        assert test_exception_event.track.info.length == 212000
        assert test_exception_event.track.info.is_stream is False
        assert test_exception_event.track.info.position == 0
        assert test_exception_event.track.info.title == "test_title"
        assert test_exception_event.track.info.uri == "test_uri"
        assert test_exception_event.track.info.artwork_url == "test_artwork"
        assert test_exception_event.track.info.isrc is None
        assert test_exception_event.track.info.source_name == "test_source_name"
        assert test_exception_event.exception.message == "test_message"
        assert test_exception_event.exception.severity == SeverityType.COMMON
        assert test_exception_event.exception.cause == "test_cause"


class TrackStuckTest(unittest.TestCase):
    def test_base(self):
        test_end_event = TrackStuckEvent(
            _test_bot,
            hikari.Snowflake(19216868440),
            _test_track,
            60,
        )

        assert test_end_event.app == _test_bot
        assert test_end_event.track == _test_track
        assert test_end_event.guild_id == hikari.Snowflake(19216868440)
        assert test_end_event.threshold_ms == 60

    def test_base_payload(self):
        payload = {
            "guildId": "19216868440",
            "track": {
                "encoded": "test_encoded",
                "info": {
                    "identifier": "test_identifier",
                    "isSeekable": True,
                    "author": "test_author",
                    "length": 212000,
                    "isStream": False,
                    "position": 0,
                    "title": "test_title",
                    "uri": "test_uri",
                    "artworkUrl": "test_artwork",
                    "isrc": None,
                    "sourceName": "test_source_name",
                },
                "pluginInfo": {},
            },
            "thresholdMs": 123456789,
        }

        test_end_event = TrackStuckEvent._from_payload(payload, app=_test_bot)

        assert test_end_event.app == _test_bot
        assert test_end_event.guild_id == hikari.Snowflake(19216868440)
        assert test_end_event.track.encoded == "test_encoded"
        assert test_end_event.track.plugin_info == {}
        assert test_end_event.track.user_data == {}

        assert test_end_event.track.info.identifier == "test_identifier"
        assert test_end_event.track.info.is_seekable is True
        assert test_end_event.track.info.author == "test_author"
        assert test_end_event.track.info.length == 212000
        assert test_end_event.track.info.is_stream is False
        assert test_end_event.track.info.position == 0
        assert test_end_event.track.info.title == "test_title"
        assert test_end_event.track.info.uri == "test_uri"
        assert test_end_event.track.info.artwork_url == "test_artwork"
        assert test_end_event.track.info.isrc is None
        assert test_end_event.track.info.source_name == "test_source_name"
        assert test_end_event.threshold_ms == 123456789


class WebsocketClosedTest(unittest.TestCase):
    def test_base(self):
        test_websocket_closed_event = WebsocketClosedEvent(
            _test_bot, hikari.Snowflake(19216868440), 4000, "test_reason", False
        )

        assert test_websocket_closed_event.app == _test_bot
        assert test_websocket_closed_event.code == 4000
        assert test_websocket_closed_event.reason == "test_reason"
        assert test_websocket_closed_event.by_remote is False

    def test_base_payload(self):
        payload = {
            "guildId": "19216868440",
            "code": 4006,
            "reason": "test_reason",
            "byRemote": True,
        }

        test_websocket_closed_event = WebsocketClosedEvent._from_payload(
            payload, app=_test_bot
        )

        assert test_websocket_closed_event.app == _test_bot
        assert test_websocket_closed_event.code == 4006
        assert test_websocket_closed_event.reason == "test_reason"
        assert test_websocket_closed_event.by_remote is True
