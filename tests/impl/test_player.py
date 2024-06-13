# ruff: noqa: D100, D101, D102, D103

import datetime

from hikari.snowflakes import Snowflake

from ongaku.impl.filters import Filters
from ongaku.impl.player import Player
from ongaku.impl.player import State
from ongaku.impl.player import Voice
from ongaku.impl.track import Track


def test_player(track: Track, filters: Filters):
    state = State(datetime.datetime.now(), 2, True, 3)
    voice = Voice("token", "endpoint", "session_id")
    player = Player(Snowflake(1234567890), track, 1, True, state, voice, filters)

    assert isinstance(player.guild_id, Snowflake)
    assert player.guild_id == Snowflake(1234567890)
    assert player.track == track
    assert player.volume == 1
    assert player.is_paused is True
    assert player.state == state
    assert player.voice == voice
    assert player.filters == filters


def test_player_state():
    time = datetime.datetime.now()
    player_state = State(time, 2, True, 3)

    assert player_state.time == time
    assert player_state.position == 2
    assert player_state.connected is True
    assert player_state.ping == 3


def test_player_voice():
    player_voice = Voice("token", "endpoint", "session_id")

    assert player_voice.token == "token"
    assert player_voice.endpoint == "endpoint"
    assert player_voice.session_id == "session_id"
