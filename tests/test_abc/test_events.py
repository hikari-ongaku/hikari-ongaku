# ruff: noqa: D100, D101, D102

import unittest

import hikari

from ongaku.abc.events import PlayerUpdate
from ongaku.abc.events import Ready
from ongaku.abc.events import WebsocketClosed
from ongaku.abc.player import PlayerState
from tests import payload


class TestReadyEvent(unittest.TestCase):
    def test_base(self):
        ready_event = Ready(resumed=False, session_id="test_session_id")

        assert ready_event.resumed == False
        assert ready_event.session_id == "test_session_id"

    def test_from_payload(self):
        ready_event = Ready._from_payload(payload.convert(payload.READY_OP))

        assert ready_event.resumed == False
        assert ready_event.session_id == "test_session_id"

    def test_to_payload(self):
        ready_event = Ready._from_payload(payload.convert(payload.READY_OP))

        assert ready_event._to_payload == payload.READY_OP


class TestPlayerUpdateEvent(unittest.TestCase):
    def test_base(self):
        player_state = PlayerState._from_payload(payload.convert(payload.PLAYER_STATE))
        player_update_event = PlayerUpdate(
            guild_id=hikari.Snowflake(1234567890),
            state=player_state,
        )

        assert player_update_event.guild_id == hikari.Snowflake(1234567890)
        assert player_update_event.state == player_state

    def test_from_payload(self):
        player_state = PlayerState._from_payload(payload.convert(payload.PLAYER_STATE))
        player_update_event = PlayerUpdate._from_payload(
            payload.convert(payload.PLAYER_UPDATE_OP)
        )

        assert player_update_event.guild_id == hikari.Snowflake(1234567890)
        assert player_update_event.state == player_state

    def test_to_payload(self):
        player_update_event = PlayerUpdate._from_payload(
            payload.convert(payload.PLAYER_UPDATE_OP)
        )

        assert player_update_event._to_payload == payload.PLAYER_UPDATE_OP


class TestWebsocketCloseEvent(unittest.TestCase):
    def test_base(self):
        websocket_closed_event = WebsocketClosed(
            hikari.Snowflake(1234567890), 1000, "test_reason", True
        )

        assert websocket_closed_event.guild_id == hikari.Snowflake(1234567890)
        assert websocket_closed_event.code == 1000
        assert websocket_closed_event.reason == "test_reason"
        assert websocket_closed_event.by_remote == True

    def test_from_payload(self):
        websocket_closed_event = WebsocketClosed._from_payload(
            payload.convert(payload.WEBSOCKET_CLOSED_EVENT_OP)
        )

        assert websocket_closed_event.guild_id == hikari.Snowflake(1234567890)
        assert websocket_closed_event.code == 1000
        assert websocket_closed_event.reason == "test_reason"
        assert websocket_closed_event.by_remote == True
