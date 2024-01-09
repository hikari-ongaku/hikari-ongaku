import unittest
from ongaku.abc.session import Session


class SessionTest(unittest.TestCase):
    def test_session(self):
        test_session = Session(False, 100)

        assert test_session.resuming is False
        assert test_session.timeout == 100

    def test_session_payload(self):
        payload = {
            "resuming": True,
            "timeout": 10
        }

        test_session = Session.from_payload(payload)

        assert test_session.resuming is True
        assert test_session.timeout == 10

        assert test_session.to_payload == payload
