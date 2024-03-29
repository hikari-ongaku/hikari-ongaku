# ruff: noqa: D100, D101, D102
import unittest

import hikari

import ongaku
from ongaku.rest import RESTClient


class ClientTest(unittest.TestCase):
    def test_base(self):
        test_bot = hikari.GatewayBot("", banner=None)
        test_client = ongaku.Client(
            test_bot,
        )

        assert test_client.bot == test_bot
        assert len(test_client.sessions) == 0
        assert isinstance(test_client.rest, RESTClient)
