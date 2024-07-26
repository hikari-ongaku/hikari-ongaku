import typing

import hikari
import mock
import orjson
import pytest
from hikari import OwnUser
from hikari.impl import gateway_bot as gateway_bot_
from hikari.impl.event_manager import EventManagerImpl
from hikari.intents import Intents
from hikari.snowflakes import Snowflake

from ongaku.abc.extension import Extension
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
        identifier="identifier",
        is_seekable=False,
        author="author",
        length=100,
        is_stream=True,
        position=2,
        title="title",
        source_name="source_name",
        uri="uri",
        artwork_url="artwork_url",
        isrc="isrc",
    )


@pytest.fixture
def ongaku_track(ongaku_track_info: TrackInfo) -> Track:
    return Track(
        encoded=ENCODED_TRACK,
        info=ongaku_track_info,
        plugin_info={},
        user_data={},
        requestor=None,
    )


@pytest.fixture
def ongaku_filters() -> filters_.Filters:
    return filters_.Filters(
        volume=1.2,
        equalizer=[filters_.Equalizer(band=BandType.HZ100, gain=0.95)],
        karaoke=filters_.Karaoke(
            level=1, mono_level=0.5, filter_band=4.5, filter_width=6
        ),
        timescale=filters_.Timescale(speed=1.2, pitch=2.3, rate=4),
        tremolo=filters_.Tremolo(frequency=1.2, depth=1),
        vibrato=filters_.Vibrato(frequency=3, depth=0.5),
        rotation=filters_.Rotation(rotation_hz=6),
        distortion=filters_.Distortion(
            sin_offset=2.1,
            sin_scale=3,
            cos_offset=6.9,
            cos_scale=7.2,
            tan_offset=9.4,
            tan_scale=2,
            offset=4.1,
            scale=8,
        ),
        channel_mix=filters_.ChannelMix(
            left_to_left=0, left_to_right=1, right_to_left=0.5, right_to_right=0.63
        ),
        low_pass=filters_.LowPass(smoothing=3.8),
    )


class FakeEvent(hikari.Event):
    def __init__(self, app: hikari.RESTAware) -> None:
        self._app = mock.Mock()

    @property
    def app(self) -> hikari.RESTAware:
        return self._app


class OngakuExtension(Extension):
    def event_handler(self, payload: str) -> hikari.Event | None:
        mapped_payload = orjson.loads(payload)

        assert isinstance(mapped_payload, typing.Mapping)

        if mapped_payload["op"] == "event" and mapped_payload["type"] == "banana":
            return FakeEvent(self.client.app)
        
@pytest.fixture
def ongaku_extension(ongaku_client: Client) -> OngakuExtension:
    return OngakuExtension(ongaku_client)


@pytest.fixture
def bot_user() -> OwnUser:
    return mock.Mock(
        global_name="test_username", username="test_username", id=Snowflake(1234567890)
    )


@pytest.fixture
def event_manager() -> EventManagerImpl:
    return EventManagerImpl(mock.AsyncMock(), mock.AsyncMock(), Intents.ALL)
