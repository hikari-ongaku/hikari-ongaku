# ruff: noqa: D100, D101, D102

import unittest

import hikari

from ongaku.abc.events import PlayerUpdateEvent
from ongaku.abc.events import ReadyEvent
from ongaku.abc.events import StatisticsEvent
from ongaku.abc.player import PlayerState
from ongaku.abc.statistics import StatsCpu
from ongaku.abc.statistics import StatsFrameStatistics
from ongaku.abc.statistics import StatsMemory
from tests import objects
from tests import payload


class TestReadyEvent(unittest.TestCase):
    def test_base(self):
        ready_event = ReadyEvent(
            _client=objects.test_ongaku_client,
            _session=objects.test_session,
            _app=objects.test_gateway_bot,
            resumed=False,
            session_id="test_session_id",
        )

        assert ready_event.client == objects.test_ongaku_client
        assert ready_event.session == objects.test_session
        assert ready_event.app == objects.test_gateway_bot
        assert ready_event.resumed == False
        assert ready_event.session_id == "test_session_id"

    def test_from_payload(self):
        ready_event = ReadyEvent._build(
            payload.convert(payload.READY_OP),
            objects.test_session,
            objects.test_gateway_bot,
        )

        assert ready_event.client == objects.test_ongaku_client
        assert ready_event.session == objects.test_session
        assert ready_event.app == objects.test_gateway_bot
        assert ready_event.resumed == False
        assert ready_event.session_id == "test_session_id"

    def test_to_payload(self):
        ready_event = ReadyEvent._build(
            payload.convert(payload.READY_OP),
            objects.test_session,
            objects.test_gateway_bot,
        )

        assert ready_event._to_payload == payload.READY_OP


class TestPlayerUpdateEvent(unittest.TestCase):
    def test_base(self):
        player_state = PlayerState._from_payload(payload.convert(payload.PLAYER_STATE))
        player_update_event = PlayerUpdateEvent(
            _client=objects.test_ongaku_client,
            _session=objects.test_session,
            _app=objects.test_gateway_bot,
            guild_id=hikari.Snowflake(1234567890),
            state=player_state,
        )

        assert player_update_event.client == objects.test_ongaku_client
        assert player_update_event.session == objects.test_session
        assert player_update_event.app == objects.test_gateway_bot
        assert player_update_event.guild_id == hikari.Snowflake(1234567890)
        assert player_update_event.state == player_state

    def test_from_payload(self):
        player_state = PlayerState._from_payload(payload.convert(payload.PLAYER_STATE))
        player_update_event = PlayerUpdateEvent._build(
            payload.convert(payload.PLAYER_UPDATE_OP),
            objects.test_session,
            objects.test_gateway_bot,
        )

        assert player_update_event.client == objects.test_ongaku_client
        assert player_update_event.session == objects.test_session
        assert player_update_event.app == objects.test_gateway_bot
        assert player_update_event.guild_id == hikari.Snowflake(1234567890)
        assert player_update_event.state == player_state

    def test_to_payload(self):
        player_update_event = PlayerUpdateEvent._build(
            payload.convert(payload.PLAYER_UPDATE_OP),
            objects.test_session,
            objects.test_gateway_bot,
        )

        assert player_update_event._to_payload == payload.PLAYER_UPDATE_OP


class TestStatisticsEvent(unittest.TestCase):
    def test_base(self):
        statistics_memory = StatsMemory._from_payload(
            payload.convert(payload.STATS_MEMORY)
        )
        statistics_cpu = StatsCpu._from_payload(payload.convert(payload.STATS_CPU))
        statistics_frame_statistics = StatsFrameStatistics._from_payload(
            payload.convert(payload.STATS_FRAME_STATS)
        )
        statistics_event = StatisticsEvent(
            players=1,
            playing_players=2,
            uptime=3,
            memory=statistics_memory,
            cpu=statistics_cpu,
            frame_statistics=statistics_frame_statistics,
            _client=objects.test_ongaku_client,
            _session=objects.test_session,
            _app=objects.test_gateway_bot,
        )

        assert statistics_event.client == objects.test_ongaku_client
        assert statistics_event.session == objects.test_session
        assert statistics_event.app == objects.test_gateway_bot
        assert statistics_event.players == 1
        assert statistics_event.playing_players == 2
        assert statistics_event.uptime == 3
        assert statistics_event.memory == statistics_memory
        assert statistics_event.cpu == statistics_cpu
        assert statistics_event.frame_statistics == statistics_frame_statistics

    def test_from_payload(self):
        statistics_memory = StatsMemory._from_payload(
            payload.convert(payload.STATS_MEMORY)
        )
        statistics_cpu = StatsCpu._from_payload(payload.convert(payload.STATS_CPU))
        statistics_frame_statistics = StatsFrameStatistics._from_payload(
            payload.convert(payload.STATS_FRAME_STATS)
        )
        statistics_event = StatisticsEvent._from_payload(
            payload.convert(payload.STATS_OP)
        )

        assert statistics_event.client == objects.test_ongaku_client
        assert statistics_event.session == objects.test_session
        assert statistics_event.app == objects.test_gateway_bot
        assert statistics_event.players == 1
        assert statistics_event.playing_players == 2
        assert statistics_event.uptime == 3
        assert statistics_event.memory == statistics_memory
        assert statistics_event.cpu == statistics_cpu
        assert statistics_event.frame_statistics == statistics_frame_statistics

    def test_to_payload(self):
        statistics_event = StatisticsEvent._from_payload(
            payload.convert(payload.STATS_OP)
        )

        assert statistics_event._to_payload == payload.STATS_OP


class TestWebsocketCloseEvent(unittest.TestCase):
    def test_base(self):
        pass
