# ruff: noqa: D101, D102

from __future__ import annotations

import datetime

from ongaku.abc import errors as errors_
from ongaku.enums import SeverityType


class RestError(errors_.RestError):
    def __init__(
        self,
        timestamp: datetime.datetime,
        status: int,
        error: str,
        message: str,
        path: str,
        trace: str | None,
    ) -> None:
        self._timestamp = timestamp
        self._status = status
        self._error = error
        self._message = message
        self._path = path
        self._trace = trace

    @property
    def timestamp(self) -> datetime.datetime:
        return self._timestamp

    @property
    def status(self) -> int:
        return self._status

    @property
    def error(self) -> str:
        return self._error

    @property
    def message(self) -> str:
        return self._message

    @property
    def path(self) -> str:
        return self._path

    @property
    def trace(self) -> str | None:
        return self._trace


class ExceptionError(errors_.ExceptionError):
    def __init__(self, message: str, severity: SeverityType, cause: str) -> None:
        self._message = message
        self._severity = severity
        self._cause = cause

    @property
    def message(self) -> str:
        return self._message

    @property
    def severity(self) -> SeverityType:
        return self._severity

    @property
    def cause(self) -> str:
        return self._cause
