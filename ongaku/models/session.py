class Session:
    def __init__(self, data: dict) -> None:
        self._resuming = data["resuming"]
        self._timeout = data["timeout"]

    @property
    def resuming(self) -> bool:
        return self._resuming

    @property
    def timeout(self) -> bool:
        return self._timeout
