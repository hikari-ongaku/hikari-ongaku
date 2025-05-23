from __future__ import annotations

import typing
from unittest import mock

import pytest

from ongaku.client import Client
from ongaku.player import ControllablePlayer
from ongaku.session import ControllableSession

if typing.TYPE_CHECKING:
    import hikari


@pytest.fixture
def hikari_app() -> hikari.GatewayBotAware:
    return mock.Mock()


@pytest.fixture
def ongaku_client(hikari_app: hikari.GatewayBotAware) -> Client:
    return Client(hikari_app)


@pytest.fixture
def ongaku_session(ongaku_client: Client) -> ControllableSession:
    return ControllableSession(
        ongaku_client,
        name="name",
        ssl=False,
        host="host",
        port=1,
        password="password",
    )


@pytest.fixture
def ongaku_player(ongaku_session: ControllableSession) -> ControllablePlayer:
    return ControllablePlayer(
        ongaku_session,
        123,
    )
