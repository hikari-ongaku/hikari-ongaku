# ruff: noqa: D100, D101, D102

import unittest

import hikari

from ongaku.abc import Player
from ongaku.abc import PlayerState
from ongaku.abc import PlayerVoice
from ongaku.abc import Track
from tests import payload


class TestPlayerState(unittest.TestCase):
    def test_base(self):
        player_state = PlayerState(time=1, position=2, connected=False, ping=3)

        assert player_state.time == 1
        assert player_state.position == 2
        assert player_state.connected == False
        assert player_state.ping == 3

    def test_from_payload(self):
        player_state = PlayerState._from_payload(payload.convert(payload.PLAYER_STATE))

        assert player_state.time == 1
        assert player_state.position == 2
        assert player_state.connected == False
        assert player_state.ping == 3

    def test_to_payload(self):
        player_state = PlayerState._from_payload(payload.convert(payload.PLAYER_STATE))

        assert player_state._to_payload == payload.PLAYER_STATE


class TestPlayerVoice(unittest.TestCase):
    def test_base(self):
        player_voice = PlayerVoice(
            token="test_token", endpoint="test_endpoint", session_id="test_session_id"
        )

        assert player_voice.token == "test_token"
        assert player_voice.endpoint == "test_endpoint"
        assert player_voice.session_id == "test_session_id"

    def test_from_payload(self):
        player_voice = PlayerVoice._from_payload(payload.convert(payload.PLAYER_VOICE))

        assert player_voice.token == "test_token"
        assert player_voice.endpoint == "test_endpoint"
        assert player_voice.session_id == "test_session_id"

    def test_to_payload(self):
        player_voice = PlayerVoice._from_payload(payload.convert(payload.PLAYER_VOICE))

        assert player_voice._to_payload == payload.PLAYER_VOICE


class TestPlayer(unittest.TestCase):
    def test_base(self):
        track = Track._from_payload(payload.convert(payload.TRACK))
        state = PlayerState._from_payload(payload.convert(payload.PLAYER_STATE))
        voice = PlayerVoice._from_payload(payload.convert(payload.PLAYER_VOICE))
        player = Player(
            guild_id=hikari.Snowflake(1234567890),
            track=track,
            volume=1,
            is_paused=False,
            state=state,
            voice=voice,
            filters={},
        )

        assert player.guild_id == hikari.Snowflake(1234567890)
        assert player.track == track
        assert player.volume == 1
        assert player.is_paused == False
        assert player.state == state
        assert player.voice == voice
        assert player.filters == {}

    def test_from_payload(self):
        track = Track._from_payload(payload.convert(payload.TRACK))
        state = PlayerState._from_payload(payload.convert(payload.PLAYER_STATE))
        voice = PlayerVoice._from_payload(payload.convert(payload.PLAYER_VOICE))
        player = Player._from_payload(payload.convert(payload.PLAYER))

        assert player.guild_id == hikari.Snowflake(1234567890)
        assert player.track == track
        assert player.volume == 1
        assert player.is_paused == False
        assert player.state == state
        assert player.voice == voice
        assert player.filters == {}

    def test_to_payload(self):
        player = Player._from_payload(payload.convert(payload.PLAYER))

        assert player._to_payload == payload.PLAYER
