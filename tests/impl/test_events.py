# ruff: noqa: D100, D101, D102, D103

import datetime

import pytest
from hikari.snowflakes import Snowflake

from ongaku.abc.errors import SeverityType
from ongaku.abc.events import TrackEndReasonType
from ongaku.impl.errors import ExceptionError
from ongaku.impl.events import PlayerUpdate
from ongaku.impl.events import Ready
from ongaku.impl.events import TrackEnd
from ongaku.impl.events import TrackException
from ongaku.impl.events import TrackStart
from ongaku.impl.events import TrackStuck
from ongaku.impl.events import WebsocketClosed
from ongaku.impl.player import State
from ongaku.impl.track import Track
from ongaku.impl.track import TrackInfo


@pytest.fixture
def track() -> Track:
    track_info = TrackInfo(
        "identifier",
        False,
        "author",
        1,
        True,
        2,
        "title",
        "source_name",
        "uri",
        "artwork_url",
        "isrc",
    )
    return Track("encoded", track_info, {}, {}, None)


def test_ready():
    ready = Ready(False, "session_id")

    assert ready.resumed is False
    assert ready.session_id == "session_id"


def test_player_update():
    time = datetime.datetime.now()
    state = State(time, 2, False, 3)
    player_update = PlayerUpdate(Snowflake(1234567890), state)

    assert isinstance(player_update.guild_id, Snowflake)
    assert player_update.guild_id == Snowflake(1234567890)
    assert player_update.state == state


def test_websocket_closed():
    websocket_closed = WebsocketClosed(Snowflake(1234567890), 1, "reason", False)

    assert isinstance(websocket_closed.guild_id, Snowflake)
    assert websocket_closed.guild_id == Snowflake(1234567890)
    assert websocket_closed.code == 1
    assert websocket_closed.reason == "reason"
    assert websocket_closed.by_remote is False


def test_track_start(track: Track):
    track_start = TrackStart(Snowflake(1234567890), track)

    assert isinstance(track_start.guild_id, Snowflake)
    assert track_start.guild_id == Snowflake(1234567890)
    assert track_start.track == track


def test_track_end(track: Track):
    track_end = TrackEnd(Snowflake(1234567890), track, TrackEndReasonType.FINISHED)

    assert isinstance(track_end.guild_id, Snowflake)
    assert track_end.guild_id == Snowflake(1234567890)
    assert track_end.track == track
    assert track_end.reason == TrackEndReasonType.FINISHED


def test_track_exception(track: Track):
    exception = ExceptionError("message", SeverityType.COMMON, "cause")
    track_exception = TrackException(Snowflake(1234567890), track, exception)

    assert isinstance(track_exception.guild_id, Snowflake)
    assert track_exception.guild_id == Snowflake(1234567890)
    assert track_exception.track == track
    assert track_exception.exception == exception


def test_track_stuck(track: Track):
    track_stuck = TrackStuck(Snowflake(1234567890), track, 1)

    assert isinstance(track_stuck.guild_id, Snowflake)
    assert track_stuck.guild_id == Snowflake(1234567890)
    assert track_stuck.track == track
    assert track_stuck.threshold_ms == 1
