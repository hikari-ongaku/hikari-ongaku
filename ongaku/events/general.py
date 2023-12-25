import hikari
import typing as t
from .. import abc


class ReadyEvent(abc.Ready, abc.OngakuEvent):
    def __init__(
        self, app: hikari.RESTAware, payload: dict[t.Any, t.Any]
    ) -> None:
        self._app = app
        self._resumed = payload["resumed"]
        self._session_id = payload["sessionId"]
        super().__init__()

    @property
    def app(self):
        return self._app

    @property
    def resumed(self):
        return self._resumed

    @property
    def session_id(self):
        return self._session_id

class Memory(abc.Memory):
    def __init__(self, payload: dict[t.Any, t.Any]) -> None:
        self._free = payload["free"]
        self._used = payload["used"]
        self._allocated = payload["allocated"]
        self._reservable = payload["reservable"]

    @property
    def free(self):
        return self._free

    @property
    def used(self):
        return self._used

    @property
    def allocated(self):
        return self._allocated

    @property
    def reservable(self):
        return self._reservable

class Cpu(abc.Cpu):
    def __init__(self, payload: dict[t.Any, t.Any]) -> None:
        self._cores = payload["cores"]
        self._system_load = payload["systemLoad"]
        self._lavalink_load = payload["lavalinkLoad"]

    @property
    def cores(self):
        return self._cores

    @property
    def system_load(self):
        return self._system_load

    @property
    def lavalink_load(self):
        return self._lavalink_load

class FrameStatistics(abc.FrameStatistics):
    def __init__(self, payload: dict[t.Any, t.Any]) -> None:
        self._sent = payload["sent"]
        self._nulled = payload["nulled"]
        self._deficit = payload["deficit"]

    @property
    def sent(self):
        return self._sent

    @property
    def nulled(self):
        return self._nulled

    @property
    def deficit(self):
        return self._deficit

class StatisticsEvent(abc.Statistics, abc.OngakuEvent):
    def __init__(
        self,
        app: hikari.RESTAware,
        payload: dict[t.Any, t.Any]
    ) -> None:
                
        self._app = app
        self._players = payload["players"]
        self._playing_players = payload["playingPlayers"]
        self._uptime = payload["uptime"]
        self._memory = Memory(payload["memory"])
        self._cpu = Cpu(payload["cpu"])
        self._frame_statistics = FrameStatistics(payload["FrameStatistics"])

    @property
    def app(self) -> hikari.RESTAware:
        return self._app

    @property
    def players(self):
        return self._players

    @property
    def playing_players(self):
        return self._playing_players

    @property
    def uptime(self):
        return self._uptime

    @property
    def memory(self):
        return self._memory

    @property
    def cpu(self):
        return self._cpu

    @property
    def frame_statistics(self):
        return self._frame_statistics


class PlayerQueueEmptyEvent(abc.PlayerQueueEmpty, abc.OngakuEvent):
    """
    Called when a players queue is zero.
    """

    def __init__(self, app: hikari.RESTAware, guild_id: hikari.Snowflake) -> None:
        self._app = app
        self._guild_id = guild_id
        super().__init__()

    @property
    def app(self):
        return self._app

    @property
    def guild_id(self):
        return self._guild_id


class WebsocketClosedEvent(abc.WebsocketClosed, abc.OngakuEvent):
    """
    Called when a track starts!
    """

    def __init__(self, app: hikari.RESTAware, payload: dict[t.Any, t.Any]) -> None:
        self._app = app
        self._guild_id = payload["guildId"]
        self._code = payload["code"]
        self._reason = payload["reason"]
        self._by_remote = payload["byRemote"]

    @property
    def app(self):
        return self._app

    @property
    def guild_id(self):
        return self._guild_id

    @property
    def code(self):
        return self._code

    @property
    def reason(self):
        return self._reason

    @property
    def by_remote(self):
        return self._by_remote
