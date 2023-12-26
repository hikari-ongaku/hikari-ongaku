import abc
import typing as t


class Session(abc.ABC):
    def __init__(self, payload: dict[t.Any, t.Any]) -> None:
        self._resuming = payload["resuming"]
        self._timeout = payload["timeout"]

    _resuming: bool
    _timeout: bool

    @property
    def resuming(self) -> bool:
        return self._resuming

    @property
    def timeout(self) -> bool:
        return self._timeout
