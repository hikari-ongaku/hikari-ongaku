import unittest
import hikari
from ongaku.abc.player import Player, PlayerState, PlayerVoice
from ongaku.abc.track import Track, TrackInfo

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


class PlayerTest(unittest.TestCase):
    def test_player(self):
        test_player_state = PlayerState(12, 24, True, 48)
        test_player_voice = PlayerVoice(
            "test_token", "test_endpoint", "test_session_id"
        )
        test_player = Player(
            hikari.Snowflake(19216868440),
            _test_track,
            100,
            False,
            test_player_state,
            test_player_voice,
        )

        assert test_player.guild_id == hikari.Snowflake(19216868440)
        assert test_player.track == _test_track
        assert test_player.volume == 100
        assert test_player.paused is False
        assert test_player.state.time == 12
        assert test_player.state.position == 24
        assert test_player.state.connected is True
        assert test_player.state.ping == 48
        assert test_player.voice.token == "test_token"
        assert test_player.voice.endpoint == "test_endpoint"
        assert test_player.voice.session_id == "test_session_id"

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
            if test_player.track.user_data is not None:
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
        assert test_player.paused is False
        assert test_player.state.time == 12
        assert test_player.state.position == 24
        assert test_player.state.connected is True
        assert test_player.state.ping == 48
        assert test_player.voice.token == "test_token"
        assert test_player.voice.endpoint == "test_endpoint"
        assert test_player.voice.session_id == "test_session_id"

        assert test_player.to_payload == payload

    def test_player_state(self):
        test_player_state = PlayerState(12, 24, True, 48)

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

        assert test_player_state.to_payload == payload

    def test_player_voice(self):
        test_player_voice = PlayerVoice(
            "test_token", "test_endpoint", "test_session_id"
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

        assert test_player_voice.to_payload == payload
