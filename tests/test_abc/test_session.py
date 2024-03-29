# ruff: noqa: D100, D101, D102

import unittest

from ongaku.abc.session import Session
from tests import payload


class TestSession(unittest.TestCase):
    def test_base(self):
        session = Session(resuming=False, timeout=1)

        assert session.resuming == False
        assert session.timeout == 1

    def test_from_payload(self):
        session = Session._from_payload(payload.convert(payload.REST_SESSION_UPDATE))

        assert session.resuming == False
        assert session.timeout == 1

    def test_to_payload(self):
        session = Session._from_payload(payload.convert(payload.REST_SESSION_UPDATE))

        assert session._to_payload == payload.REST_SESSION_UPDATE
