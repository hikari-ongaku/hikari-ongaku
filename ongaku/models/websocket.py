import typing as t
import enum as e
import hikari

# Ready related.


class Ready:
    """
    The data sent when the bot is ready.
    """

    def __init__(self, data: dict) -> None:
        self._resumed = data["resumed"]
        self._session_id = data["sessionId"]

    @property
    def resumed(self) -> bool:
        return self._resumed

    @property
    def session_id(self) -> str:
        return self._session_id


# Statistics related:


class Memory:
    def __init__(self, data: dict) -> None:
        self._free = data["free"]
        self._used = data["used"]
        self._allocated = data["allocated"]
        self._reservable = data["reservable"]

    @property
    def free(self) -> int:
        return self._free

    @property
    def used(self) -> int:
        return self._used

    @property
    def allocated(self) -> int:
        return self._allocated

    @property
    def reservable(self) -> int:
        return self._reservable


class Cpu:
    def __init__(self, data: dict) -> None:
        self._cores = data["cores"]
        self._system_load = data["systemLoad"]
        self._lavalink_load = data["lavalinkLoad"]

    @property
    def cores(self) -> int:
        return self._cores

    @property
    def system_load(self) -> float:
        return self._system_load

    @property
    def lavalink_load(self) -> float:
        return self._lavalink_load


class FrameStatistics:
    def __init__(self, data: dict) -> None:
        self._sent = data["sent"]
        self._nulled = data["nulled"]
        self._deficit = data["deficit"]

    @property
    def sent(self) -> int:
        return self._sent

    @property
    def nulled(self) -> int:
        return self._nulled

    @property
    def deficit(self) -> int:
        return self._deficit


class Statistics:
    """
    The data sent when the statistics is called.
    """

    def __init__(self, data: dict) -> None:
        self._players = data["players"]
        self._playing_players = data["playingPlayers"]
        self._uptime = data["uptime"]

        try:
            self._memory = Memory(data["memory"])
        except:
            self._memory = None

        try:
            self._cpu = Cpu(data["cpu"])
        except:
            self._cpu = None

        try:
            self._frame_statistics = FrameStatistics(data["frameStats"])
        except:
            self._frame_statistics = None

    @property
    def players(self) -> int:
        return self._players

    @property
    def playing_players(self) -> int:
        return self._playing_players

    @property
    def uptime(self) -> int:
        return self._uptime

    @property
    def memory(self) -> t.Optional[Memory]:
        return self._memory

    @property
    def cpu(self) -> t.Optional[Cpu]:
        return self._cpu

    @property
    def frame_statistics(self) -> t.Optional[FrameStatistics]:
        return self._frame_statistics


class WebsocketClosed:
    def __init__(self, data: dict) -> None:
        self._code = data["code"]
        self._reason = data["reason"]
        self._by_remote = data["byRemote"]

    @property
    def code(self) -> int:
        return self._code

    @property
    def reason(self) -> str:
        return self._reason

    @property
    def by_remote(self) -> bool:
        return self._by_remote
