import unittest
import ongaku
import hikari


class OngakuTest(unittest.TestCase):
    def test_base(self):
        test_bot = hikari.GatewayBot("", banner=None)
        test_ongaku = ongaku.Ongaku(
            test_bot,
            host="test_host",
            port=1234,
            password="test_password",
            version=ongaku.VersionType.V3,
        )

        assert test_ongaku.bot == test_bot

    def test_internal(self):
        pass
