import typing

import mock
import pytest
from hikari import OwnUser
from hikari.impl import gateway_bot as gateway_bot_
from hikari.impl.event_manager import EventManagerImpl
from hikari.intents import Intents
from hikari.snowflakes import Snowflake

from ongaku.abc.filters import BandType
from ongaku.client import Client
from ongaku.impl import filters as filters_
from ongaku.impl.track import Track
from ongaku.impl.track import TrackInfo
from ongaku.player import Player
from ongaku.session import Session

ENCODED_TRACK: typing.Final[str] = (
    "QAAAuQMAGURFQUQgQUhFQUQgfCBEcmVkZ2UgU29uZyEADlRoZSBTdHVwZW5kaXVtAAAAAAAExqgAC2QzQlEtVVpoMGE4AAEAK2h0dHBzOi8vd3d3LnlvdXR1YmUuY29tL3dhdGNoP3Y9ZDNCUS1VWmgwYTgBADRodHRwczovL2kueXRpbWcuY29tL3ZpL2QzQlEtVVpoMGE4L21heHJlc2RlZmF1bHQuanBnAAAHeW91dHViZQAAAAAAAAAA"
)


@pytest.fixture
def gateway_bot() -> gateway_bot_.GatewayBot:
    return mock.Mock()


@pytest.fixture
def ongaku_client(gateway_bot: gateway_bot_.GatewayBot) -> Client:
    return Client(gateway_bot)


@pytest.fixture
def ongaku_session(
    gateway_bot: gateway_bot_.GatewayBot, ongaku_client: Client
) -> Session:
    return mock.Mock(
        app=gateway_bot,
        client=ongaku_client,
        name="test_session",
        ssl=False,
        host="host",
        port=1234,
        password="password",
        attempts=3,
    )


@pytest.fixture
def ongaku_player(ongaku_session: Session) -> Player:
    return mock.Mock(session=ongaku_session, guild_id=Snowflake(1234567890))


@pytest.fixture
def ongaku_track_info() -> TrackInfo:
    return TrackInfo(
        "identifier",
        False,
        "author",
        100,
        True,
        2,
        "title",
        "source_name",
        "uri",
        "artwork_url",
        "isrc",
    )


@pytest.fixture
def ongaku_track(ongaku_track_info: TrackInfo) -> Track:
    return Track(ENCODED_TRACK, ongaku_track_info, {}, {}, None)


@pytest.fixture
def ongaku_filters() -> filters_.Filters:
    return filters_.Filters(
        volume=1.2,
        equalizer=[filters_.Equalizer(BandType.HZ100, 0.95)],
        karaoke=filters_.Karaoke(1, 0.5, 4.5, 6),
        timescale=filters_.Timescale(1.2, 2.3, 4),
        tremolo=filters_.Tremolo(1.2, 1),
        vibrato=filters_.Vibrato(3, 0.5),
        rotation=filters_.Rotation(6),
        distortion=filters_.Distortion(2.1, 3, 6.9, 7.2, 9.4, 2, 4.1, 8),
        channel_mix=filters_.ChannelMix(0, 1, 0.5, 0.63),
        low_pass=filters_.LowPass(3.8),
    )


@pytest.fixture
def bot_user() -> OwnUser:
    return mock.Mock(
        global_name="test_username", username="test_username", id=Snowflake(1234567890)
    )


@pytest.fixture
def event_manager() -> EventManagerImpl:
    return EventManagerImpl(mock.AsyncMock(), mock.AsyncMock(), Intents.ALL)
