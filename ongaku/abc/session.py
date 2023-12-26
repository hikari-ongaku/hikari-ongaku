import abc
import typing as t
import dataclasses

@dataclasses.dataclass
class Session(abc.ABC):
    resuming: bool
    timeout: bool

    @classmethod
    def as_payload(cls, payload: dict[t.Any, t.Any]):
        resuming = payload["resuming"]
        timeout = payload["timeout"]

        return cls(resuming, timeout)
    
    @property
    def raw(self) -> dict[str, t.Any]:
        return dataclasses.asdict(self)
