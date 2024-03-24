# ruff: noqa: D100, D101, D102

import unittest


from ongaku.abc.error import RestError, ExceptionError
from ongaku.enums import SeverityType
from tests import payload


class TestRestError(unittest.TestCase):
    def test_base(self):
        error = RestError(
            timestamp=1, 
            status=404, 
            error="test_error", 
            trace="...", 
            message="test_message", 
            path="test_path"
        )

        assert error.timestamp == 1
        assert error.status == 404
        assert error.trace == "..."
        assert error.message == "test_message"
        assert error.path == "test_path"

    def test_from_payload(self):
        error = RestError._from_payload(payload.convert(payload.REST_ERROR))

        assert error.timestamp == 1
        assert error.status == 404
        assert error.trace == "..."
        assert error.message == "test_message"
        assert error.path == "/v4/sessions/test_session"

    def test_to_payload(self):
        error = RestError._from_payload(payload.convert(payload.REST_ERROR))

        assert error._to_payload == payload.REST_ERROR

class TestExceptionError(unittest.TestCase):
    def test_base(self):
        error = ExceptionError(message="test_message", severity=SeverityType.COMMON, cause="test_cause")

        assert error.message == "test_message"
        assert error.severity == SeverityType.COMMON
        assert error.cause == "test_cause"

    def test_from_payload(self):
        error = ExceptionError._from_payload(payload.convert(payload.EXCEPTION))

        assert error.message == "test_message"
        assert error.severity == SeverityType.COMMON
        assert error.cause == "test_cause"

    def test_to_payload(self):
        error = ExceptionError._from_payload(payload.convert(payload.EXCEPTION))

        assert error._to_payload == payload.EXCEPTION

