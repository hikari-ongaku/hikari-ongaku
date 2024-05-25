# ruff: noqa: D101, D102

from __future__ import annotations

import datetime

from ongaku.abc import errors as errors_

__all__ = (
    "RestError",
    "ExceptionError",
)


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
    def __init__(
        self, message: str, severity: errors_.SeverityType, cause: str
    ) -> None:
        self._message = message
        self._severity = severity
        self._cause = cause

    @property
    def message(self) -> str:
        return self._message

    @property
    def severity(self) -> errors_.SeverityType:
        return self._severity

    @property
    def cause(self) -> str:
        return self._cause


# MIT License

# Copyright (c) 2023 MPlatypus

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
