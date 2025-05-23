from __future__ import annotations

import datetime
from unittest import mock

import hikari

from ongaku.player import Player
from ongaku.player import State
from ongaku.player import Voice


def test_player():
    mock_track = mock.Mock()
    mock_state = mock.Mock()
    mock_voice = mock.Mock()
    mock_filters = mock.Mock()

    player = Player(
        guild_id=hikari.Snowflake(123),
        track=mock_track,
        volume=1,
        is_paused=False,
        state=mock_state,
        voice=mock_voice,
        filters=mock_filters,
    )

    assert player.guild_id == hikari.Snowflake(123)
    assert player.track == mock_track
    assert player.volume == 1
    assert player.is_paused is False
    assert player.state == mock_state
    assert player.voice == mock_voice
    assert player.filters == mock_filters


class TestState:
    def test_properties(self):
        mock_time = mock.Mock()

        state = State(
            time=mock_time,
            position=1,
            connected=True,
            ping=2,
        )

        assert state.time == mock_time
        assert state.position == 1
        assert state.connected is True
        assert state.ping == 2

    def test_empty(self):
        state = State.empty()

        assert state.time == datetime.datetime.fromtimestamp(
            0,
            tz=datetime.timezone.utc,
        )
        assert state.position == 0
        assert state.connected is False
        assert state.ping == -1


class TestVoice:
    def test_properties(self):
        voice = Voice(
            token="token",
            endpoint="endpoint",
            session_id="session_id",
        )

        assert voice.token == "token"
        assert voice.endpoint == "endpoint"
        assert voice.session_id == "session_id"

    def test_empty(self):
        voice = Voice.empty()

        assert voice.token == ""
        assert voice.endpoint == ""
        assert voice.session_id == ""


class TestControllablePlayer:
    def test_properties(self):
        raise NotImplementedError

    def test_connect(self):
        raise NotImplementedError

    def test_connect_with_missing_session_id(self):
        raise NotImplementedError

    def test_connect_with_missing_events(self):
        raise NotImplementedError

    def test_disconnect(self):
        raise NotImplementedError

    def test_disconnect_with_missing_session_id(self):
        raise NotImplementedError

    def test_play(self):
        raise NotImplementedError

    def test_play_with_missing_session_id(self):
        raise NotImplementedError

    def test_play_with_missing_channel_id(self):
        raise NotImplementedError

    def test_play_with_missing_queue(self):
        raise NotImplementedError

    def test_disconnect_with_missing_session_id(self):
        raise NotImplementedError

    def test_add(self):
        raise NotImplementedError

    def test_pause(self):
        raise NotImplementedError

    def test_pause_with_missing_session_id(self):
        raise NotImplementedError

    def test_stop(self):
        raise NotImplementedError

    def test_stop_with_missing_session_id(self):
        raise NotImplementedError

    def test_shuffle(self):
        raise NotImplementedError

    def test_skip(self):
        raise NotImplementedError

    def test_skip_with_missing_session_id(self):
        raise NotImplementedError

    def test_skip_with_empty_queue(self):
        raise NotImplementedError

    def test_skip_with_multiple(self):
        raise NotImplementedError

    def test_remove(self):
        raise NotImplementedError

    def test_remove_with_empty_queue(self):
        raise NotImplementedError

    def test_remove_with_invalid_index(self):
        raise NotImplementedError

    def test_clear(self):
        raise NotImplementedError

    def test_clear_with_missing_session_id(self):
        raise NotImplementedError

    def test_set_autoplay(self):
        raise NotImplementedError

    def test_set_volume(self):
        raise NotImplementedError

    def test_set_volume_with_missing_session_id(self):
        raise NotImplementedError

    def test_set_volume_with_invalid_volume(self):
        raise NotImplementedError

    def test_set_position(self):
        raise NotImplementedError

    def test_set_position_with_missing_session_id(self):
        raise NotImplementedError

    def test_set_position_with_invalid_position(self):
        raise NotImplementedError

    def test_set_position_with_missing_queue(self):
        raise NotImplementedError

    def test_set_filters(self):
        raise NotImplementedError

    def test_set_filters_with_missing_session_id(self):
        raise NotImplementedError

    def test_set_loop(self):
        raise NotImplementedError

    def test_transfer(self):
        raise NotImplementedError

    def test_transfer_with_no_connection(self):
        raise NotImplementedError

    def test_pause(self):
        raise NotImplementedError

    def test__update(self):
        raise NotImplementedError

    def test__track_end_event(self):
        raise NotImplementedError  # FIXME: Add more tests for track end event.  # noqa: TD001, TD002, TD003

    def test__track_end_event_with_missing_session_id(self):
        raise NotImplementedError  # FIXME: Add more tests for track end event.  # noqa: TD001, TD002, TD003

    def test__player_update_event(self):
        raise NotImplementedError  # FIXME: Add more tests for track end event.  # noqa: TD001, TD002, TD003
