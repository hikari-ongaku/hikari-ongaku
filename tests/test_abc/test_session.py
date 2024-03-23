# ruff: noqa: D100, D101, D102

import unittest

from ongaku.abc.session import Session


class SessionTest(unittest.TestCase):
    payload = {"resuming": True, "timeout": 10}

    def test_session(self):
        test_session = Session(resuming=True, timeout=10)

        assert test_session.resuming is True
        assert test_session.timeout == 10

        assert test_session._to_payload == self.payload

    def test_session_payload(self):
        test_session = Session._from_payload(self.payload)

        assert test_session.resuming is True
        assert test_session.timeout == 10

        assert test_session._to_payload == self.payload
