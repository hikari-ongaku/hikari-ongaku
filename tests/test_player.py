# ruff: noqa: D100, D101, D102

import unittest

import hikari

from ongaku import Client
from ongaku import Player
from ongaku import Session
from ongaku import VersionType

fake_bot = hikari.GatewayBot("", banner=None)

fake_client = Client(fake_bot)

fake_session = Session(
    fake_client, False, "127.0.0.1", 2333, "youshallnotpass", VersionType.V4, attempts=3
)


class TestPlayer(unittest.IsolatedAsyncioTestCase):
    async def test_default(self):
        player = Player(fake_session, hikari.Snowflake(1234567890))

        assert player.audio_filter is None

        assert player.channel_id is None

        assert player.guild_id == hikari.Snowflake(1234567890)

        assert player.session == fake_session

        assert player.auto_play == True

    async def test_connect(self):
        player = Player(fake_session, hikari.Snowflake(1234567890))

        await player.connect(hikari.Snowflake(1234567890))
