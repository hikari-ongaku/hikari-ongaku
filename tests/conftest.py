import os
import typing

import mock
import pytest
from hikari import OwnUser
from hikari.impl import gateway_bot as gateway_bot_
from hikari.impl.event_manager import EventManagerImpl
from hikari.intents import Intents
from hikari.snowflakes import Snowflake

from ongaku.client import Client
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
def ongaku_session(ongaku_client: Client) -> Session:
    ssl = os.getenv("LL_SSL", "false").lower() != "false"

    return Session(
        ongaku_client, "test_session", ssl, os.getenv("LL_HOST", "127.0.0.1"), int(os.getenv("LL_PORT", "2333")), os.getenv("LL_PASSWORD", "youshallnotpass"), 3
    )


@pytest.fixture
def ongaku_player(ongaku_session: Session) -> Player:
    return Player(ongaku_session, Snowflake(1234567890))


@pytest.fixture
def track_info() -> TrackInfo:
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
def track(track_info: TrackInfo) -> Track:
    return Track(ENCODED_TRACK, track_info, {}, {}, None)


@pytest.fixture
def bot_user() -> OwnUser:
    return mock.Mock(
        global_name="test_username", username="test_username", id=Snowflake(1234567890)
    )


@pytest.fixture
def event_manager() -> EventManagerImpl:
    return EventManagerImpl(mock.AsyncMock(), mock.AsyncMock(), Intents.ALL)
