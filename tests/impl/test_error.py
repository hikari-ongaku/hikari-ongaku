# ruff: noqa: D100, D101, D102, D103

import datetime

from ongaku.abc.errors import SeverityType
from ongaku.impl.errors import ExceptionError
from ongaku.impl.errors import RestError


def test_rest_error():
    time = datetime.datetime.now()
    rest_error = RestError(time, 2, "error", "message", "path", "trace")

    assert rest_error.timestamp == time
    assert rest_error.status == 2
    assert rest_error.error == "error"
    assert rest_error.message == "message"
    assert rest_error.path == "path"
    assert rest_error.trace == "trace"


def test_exception_error():
    exception_error = ExceptionError("message", SeverityType.COMMON, "cause")

    assert exception_error.message == "message"
    assert exception_error.severity == SeverityType.COMMON
    assert exception_error.cause == "cause"
