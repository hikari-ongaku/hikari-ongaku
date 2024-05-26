# ruff: noqa: D100, D101, D102, D103

from ongaku.impl.session import Session


def test_session():
    session = Session(True, 1)

    assert session.resuming is True
    assert session.timeout == 1