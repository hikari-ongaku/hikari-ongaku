import hikari
import typing as t
from .. import abc


class ReadyEvent(abc.Ready, abc.OngakuEvent):
    def __init__(self, app: hikari.RESTAware, payload: dict[t.Any, t.Any]) -> None:
        self._app = app
        self._resumed = payload["resumed"]
        self._session_id = payload["sessionId"]

    @property
    def app(self):
        return self._app

    @property
    def resumed(self):
        return self._resumed

    @property
    def session_id(self):
        return self._session_id

class StatisticsEvent(abc.Statistics, abc.OngakuEvent):
    def __init__(self, app: hikari.RESTAware, payload: dict[t.Any, t.Any]) -> None:
        self._app = app
        self.players = payload["players"]
        self.playing_players = payload["playingPlayers"]
        self.uptime = payload["uptime"]
        self.memory = abc.Memory.as_payload(payload["memory"])
        self.cpu = abc.Cpu.as_payload(payload["cpu"])
        self.frame_statistics = abc.FrameStatistics.as_payload(payload["FrameStatistics"])

    @property
    def app(self) -> hikari.RESTAware:
        return self._app


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
