from __future__ import annotations

from unittest import mock

from ongaku.session import ControllableSession
from ongaku.session import Session
from ongaku.session import SessionStatus


def test_session():
    session = Session(resuming=True, timeout=1)

    assert session.resuming is True
    assert session.timeout == 1


class TestControllableSession:
    def test_properties(self):
        client = mock.Mock()

        controllable_session = ControllableSession(
            client=client,
            name="name",
            ssl=True,
            host="host",
            port=1234,
            password="password",
        )

        assert controllable_session.client == client
        assert controllable_session.app == client.app
        assert controllable_session.name == "name"
        assert controllable_session.ssl is True
        assert controllable_session.host == "host"
        assert controllable_session.port == 1234
        assert controllable_session.password == "password"
        assert controllable_session.base_uri == "https://host:1234"
        assert controllable_session.status == SessionStatus.NOT_CONNECTED
        assert controllable_session.session_id is None

    def test_start(self):
        raise NotImplementedError

    def test_start_with_missing_bot(self):
        raise NotImplementedError

    def test__websocket(self):
        raise NotImplementedError

    def test__websocket_with_failed_connection(self):
        raise NotImplementedError

    def test__handle_payload(self):
        raise NotImplementedError

    def test_request(self):
        raise NotImplementedError

    def test_request_with_optional(self):
        raise NotImplementedError

    def test_request_with_ignore_default_headers(self):
        raise NotImplementedError

    def test_transfer(self):
        raise NotImplementedError
