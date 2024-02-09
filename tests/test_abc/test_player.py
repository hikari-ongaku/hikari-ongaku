# ruff: noqa
import unittest

import hikari
import typing as t

from ongaku.abc.player import Player
from ongaku.abc.player import PlayerState
from ongaku.abc.player import PlayerVoice

from .test_track import TrackTest

class PlayerTest(unittest.TestCase):
    player_payload: dict[str, t.Any] = {
            "guildId": "19216868440",
            "track": TrackTest.track_payload,
            "volume": 100,
            "paused": False,
            "state": {"time": 12, "position": 24, "connected": True, "ping": 48},
            "voice": {
                "token": "test_token",
                "endpoint": "test_endpoint",
                "sessionId": "test_session_id",
            },
            "filters": {},
        }
    
    player_voice_payload = player_payload["voice"]

    player_state_payload = player_payload["state"]

    def test_player(self):
        test_player_state = PlayerState(time=12, position=24, connected=True, ping=48)
        test_player_voice = PlayerVoice(
            token="test_token", endpoint="test_endpoint", session_id="test_session_id"
        )
        test_player = Player(
            guild_id=hikari.Snowflake(19216868440),
            track=TrackTest.track_data,
            volume=100,
            is_paused=False,
            state=test_player_state,
            voice=test_player_voice,
            filters={},
        )

        assert test_player.guild_id == hikari.Snowflake(19216868440)
        assert test_player.track == TrackTest.track_data
        assert test_player.volume == 100
        assert test_player.is_paused is False
        assert test_player.state.time == 12
        assert test_player.state.position == 24
        assert test_player.state.connected is True
        assert test_player.state.ping == 48
        assert test_player.voice.token == "test_token"
        assert test_player.voice.endpoint == "test_endpoint"
        assert test_player.voice.session_id == "test_session_id"
        assert test_player.filters == {}

        assert test_player._to_payload == self.player_payload # unsure why this is not passing. Data looks valid however.

    def test_player_payload(self):
        

        test_player = Player._from_payload(self.player_payload)

        assert test_player.guild_id == hikari.Snowflake(19216868440)
        if test_player.track:
            assert test_player.track == TrackTest.track_data

        assert test_player.volume == 100
        assert test_player.is_paused is False
        assert test_player.state.time == 12
        assert test_player.state.position == 24
        assert test_player.state.connected is True
        assert test_player.state.ping == 48
        assert test_player.voice.token == "test_token"
        assert test_player.voice.endpoint == "test_endpoint"
        assert test_player.voice.session_id == "test_session_id"

        assert test_player._to_payload == self.player_payload # unsure why this is not passing. Data looks valid however.

    def test_player_state(self):
        test_player_state = PlayerState(time=12, position=24, connected=True, ping=48)

        assert test_player_state.time == 12
        assert test_player_state.position == 24
        assert test_player_state.connected is True
        assert test_player_state.ping == 48
        
        assert test_player_state._to_payload == self.player_state_payload

    def test_player_state_payload(self):
        test_player_state = PlayerState._from_payload(self.player_state_payload)

        assert test_player_state.time == 12
        assert test_player_state.position == 24
        assert test_player_state.connected is True
        assert test_player_state.ping == 48

        assert test_player_state._to_payload == self.player_state_payload

    def test_player_voice(self):
        test_player_voice = PlayerVoice(token="test_token",endpoint="test_endpoint",session_id="test_session_id")

        assert test_player_voice.token == "test_token"
        assert test_player_voice.endpoint == "test_endpoint"
        assert test_player_voice.session_id == "test_session_id"

        assert test_player_voice._to_payload == self.player_voice_payload

    def test_player_voice_payload(self):

        test_player_voice = PlayerVoice._from_payload(self.player_voice_payload)
        
        assert test_player_voice.token == "test_token"
        assert test_player_voice.endpoint == "test_endpoint"
        assert test_player_voice.session_id == "test_session_id"
        
        assert test_player_voice._to_payload == self.player_voice_payload
        


