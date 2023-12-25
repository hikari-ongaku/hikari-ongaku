import abc

class Session(abc.ABC):
    @property
    def resuming(self) -> bool:
        ...

    @property
    def timeout(self) -> bool:
        ...