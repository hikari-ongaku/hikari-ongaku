from __future__ import annotations

from .ongaku import Ongaku
from .enums import (
    SeverityType,
    TrackEndReasonType,
    PlatformType,
    VersionType,
    ConnectionType,
)
from .errors import (
    OngakuBaseException,
    BuildException,
    LavalinkException,
    LavalinkConnectionException,
    SessionNotStartedException,
    PlayerException,
    PlayerSettingException,
    PlayerMissingException,
    PlayerQueueException,
    GatewayOnlyException,
)

from .abc import events, lavalink, player, session, track
from .abc.events import (
    ReadyEvent,
    StatisticsEvent,
    TrackStartEvent,
    TrackEndEvent,
    TrackExceptionEvent,
    TrackStuckEvent,
    WebsocketClosedEvent,
)
from .abc.lavalink import Info, RestError, ExceptionError
from .abc.player import Player, PlayerState, PlayerVoice
from .abc.session import Session
from .abc.track import Track, Playlist, SearchResult

from . import errors, enums, abc

__all__ = (
    # .ongaku
    "Ongaku",
    # .enums
    "SeverityType",
    "TrackEndReasonType",
    "PlatformType",
    "VersionType",
    "ConnectionType",
    # .errors
    "OngakuBaseException",
    "BuildException",
    "LavalinkException",
    "LavalinkConnectionException",
    "SessionNotStartedException",
    "PlayerException",
    "PlayerSettingException",
    "PlayerMissingException",
    "PlayerQueueException",
    "GatewayOnlyException",
    # .abc
    "events",
    "lavalink",
    "player",
    "session",
    "track",
    # .abc.events
    "ReadyEvent",
    "StatisticsEvent",
    "TrackStartEvent",
    "TrackEndEvent",
    "TrackExceptionEvent",
    "TrackStuckEvent",
    "WebsocketClosedEvent",
    # .abc.lavalink
    "Info",
    "RestError",
    "ExceptionError",
    # .abc.player
    "Player",
    "PlayerState",
    "PlayerVoice",
    # .abc.session
    "Session",
    # .abc.track
    "Track",
    "Playlist",
    "SearchResult",
    # Other
    "errors",
    "enums",
    "abc",
)
