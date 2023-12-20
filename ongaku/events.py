import hikari, attr
import typing as t

from . import models

class OngakuEvent(hikari.Event):
    """
    The base Ongaku events.
    """

@attr.define()
class ReadyEvent(OngakuEvent):
    app: hikari.GatewayBot

    _event: models.Ready

    @property
    def resumed(self) -> bool:
        return self._event._resumed
    
    @property
    def session_id(self) -> str:
        return self._event._session_id
    
@attr.define()
class StatisticsEvent(OngakuEvent):
    app: hikari.GatewayBot

    _event: models.Statistics

    @property
    def players(self) -> int:
        return self._event._players
    
    @property
    def playing_players(self) -> int:
        return self._event._playing_players
    
    @property
    def uptime(self) -> int:
        return self._event._uptime
    
    @property
    def memory(self) -> t.Optional[models.Memory]:
        return self._event._memory
    
    @property
    def cpu(self) -> t.Optional[models.Cpu]:
        return self._event._cpu
    
    @property
    def frame_statistics(self) -> t.Optional[models.FrameStatistics]:
        return self._event._frame_statistics

@attr.define()
class TrackStartEvent(OngakuEvent):
    """
    Called when a track starts!
    """
    
    app: hikari.GatewayBot

    _event: models.TrackStart

    _guild_id: int

    @property
    def track(self) -> models.Track:
        return self._event.track
    
    @property
    def guild_id(self) -> int:
        return self._guild_id

@attr.define()
class TrackEndEvent(OngakuEvent):
    """
    Called when a track starts!
    """
    
    app: hikari.GatewayBot

    _event: models.TrackEnd

    _guild_id: int

    @property
    def track(self) -> models.Track:
        return self._event.track
    
    @property
    def reason(self) -> models.TrackEndReasonType:
        return self._event.reason
    
    @property
    def guild_id(self) -> int:
        return self._guild_id

@attr.define()
class TrackExceptionEvent(OngakuEvent):
    """
    Called when a track starts!
    """
    
    app: hikari.GatewayBot

    _event: models.TrackException

    _guild_id: int

    @property
    def track(self) -> models.Track:
        return self._event.track
    
    @property
    def exception(self) -> models.TrackExceptionException:
        return self._event.exception
    
    @property
    def guild_id(self) -> int:
        return self._guild_id

@attr.define()
class TrackStuckEvent(OngakuEvent):
    """
    Called when a track starts!
    """
    
    app: hikari.GatewayBot

    _event: models.TrackStuck

    _guild_id: int

    @property
    def track(self) -> models.Track:
        return self._event.track
    
    @property
    def threshold_ms(self) -> int:
        return self._event.threshold_ms
    
    @property
    def guild_id(self) -> int:
        return self._guild_id

@attr.define()
class WebsocketClosedEvent(OngakuEvent):
    """
    Called when a track starts!
    """
    
    app: hikari.GatewayBot

    _event: models.WebsocketClosed

    _guild_id: int

    @property
    def code(self) -> int:
        return self._event.code
    
    @property
    def reason(self) -> str:
        return self._event.reason
    
    @property
    def by_remote(self) -> bool:
        return self._event.by_remote

    @property
    def guild_id(self) -> int:
        return self._guild_id
