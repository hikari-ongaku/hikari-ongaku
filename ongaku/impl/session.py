# ruff: noqa: D101, D102

from __future__ import annotations

from ongaku.abc import session as session_


class Session(session_.Session):
    def __init__(self, resuming: bool, timeout: int) -> None:
        self._resuming = resuming
        self._timeout = timeout

    @property
    def resuming(self) -> bool:
        return self._resuming

    @property
    def timeout(self) -> int:
        return self._timeout
