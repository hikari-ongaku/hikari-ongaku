# ruff: noqa
import unittest

import hikari

from ongaku.abc.player import Player
from ongaku.abc.player import PlayerState
from ongaku.abc.player import PlayerVoice
from ongaku.abc.track import Track
from ongaku.abc.track import TrackInfo

_test_info = TrackInfo(
    identifier="test_identifier",
    is_seekable=False,
    author="test_author",
    length=246,
    is_stream=True,
    position=200,
    title="test_title",
    source_name="test_source_name",
    uri=None,
    artwork_url=None,
    isrc=None
)
_test_track = Track(encoded="test_encoded", info=_test_info, plugin_info={}, user_data={}, requestor=None)



class PlayerTest(unittest.TestCase):
    def test_player(self):
        test_player_state = PlayerState(time=12, position=24, connected=True, ping=48)
        test_player_voice = PlayerVoice(
            token="test_token", endpoint="test_endpoint", session_id="test_session_id"
        )
        test_player = Player(
            guild_id=hikari.Snowflake(19216868440),
            track=_test_track,
            volume=100,
            is_paused=False,
            state=test_player_state,
            voice=test_player_voice,
            filters={},
        )

        assert test_player.guild_id == hikari.Snowflake(19216868440)
        assert test_player.track == _test_track
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

    def test_player_payload(self):
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
            },
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

        test_player = Player._from_payload(payload)

        assert test_player.guild_id == hikari.Snowflake(19216868440)
        if test_player.track is not None:
            assert test_player.track.encoded == "test_encoded"
            assert test_player.track.plugin_info == {}
            assert test_player.track.user_data == {}

            assert test_player.track.info.identifier == "test_identifier"
            assert test_player.track.info.is_seekable is True
            assert test_player.track.info.author == "test_author"
            assert test_player.track.info.length == 212000
            assert test_player.track.info.is_stream is False
            assert test_player.track.info.position == 0
            assert test_player.track.info.title == "test_title"
            assert test_player.track.info.uri == "test_uri"
            assert test_player.track.info.artwork_url == "test_artwork"
            assert test_player.track.info.isrc is None
            assert test_player.track.info.source_name == "test_source_name"

        assert test_player.volume == 100
        assert test_player.is_paused is False
        assert test_player.state.time == 12
        assert test_player.state.position == 24
        assert test_player.state.connected is True
        assert test_player.state.ping == 48
        assert test_player.voice.token == "test_token"
        assert test_player.voice.endpoint == "test_endpoint"
        assert test_player.voice.session_id == "test_session_id"
        assert test_player._to_payload == payload

    def test_player_state(self):
        test_player_state = PlayerState(time=12, position=24, connected=True, ping=48)

        assert test_player_state.time == 12
        assert test_player_state.position == 24
        assert test_player_state.connected is True
        assert test_player_state.ping == 48

    def test_player_state_payload(self):
        payload = {"time": 12, "position": 24, "connected": True, "ping": 48}

        test_player_state = PlayerState._from_payload(payload)

        assert test_player_state.time == 12
        assert test_player_state.position == 24
        assert test_player_state.connected is True
        assert test_player_state.ping == 48

        assert test_player_state._to_payload == payload

    def test_player_voice(self):
        test_player_voice = PlayerVoice(
            token="test_token", endpoint="test_endpoint", session_id="test_session_id"
        )

        assert test_player_voice.token == "test_token"
        assert test_player_voice.endpoint == "test_endpoint"
        assert test_player_voice.session_id == "test_session_id"

    def test_player_voice_payload(self):
        payload = {
            "token": "test_token",
            "endpoint": "test_endpoint",
            "sessionId": "test_session_id",
        }

        test_player_voice = PlayerVoice._from_payload(payload)

        assert test_player_voice.token == "test_token"
        assert test_player_voice.endpoint == "test_endpoint"
        assert test_player_voice.session_id == "test_session_id"

        assert test_player_voice._to_payload == payload
