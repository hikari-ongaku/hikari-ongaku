"""A voice handling library for hikari

GitHub: 
https://github.com/MPlatypus/hikari-ongaku
Docs:
https://ongaku.mplaty.com/
"""

from __future__ import annotations

from . import abc, enums, errors
from .abc import events, lavalink, player, session, track
from .abc.events import (
    ReadyEvent,
    StatisticsEvent,
    TrackEndEvent,
    TrackExceptionEvent,
    TrackStartEvent,
    TrackStuckEvent,
    WebsocketClosedEvent,
)
from .abc.lavalink import ExceptionError, Info, RestError
from .abc.player import Player, PlayerState, PlayerVoice
from .abc.session import Session
from .abc.track import Playlist, SearchResult, Track
from .enums import (
    ConnectionType,
    PlatformType,
    SeverityType,
    TrackEndReasonType,
    VersionType,
)
from .errors import (
    BuildException,
    GatewayOnlyException,
    LavalinkConnectionException,
    LavalinkException,
    OngakuBaseException,
    PlayerException,
    PlayerMissingException,
    PlayerQueueException,
    PlayerSettingException,
    RequiredException,
    SessionNotStartedException,
    TimeoutException,
)
from .ongaku import Ongaku

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
    "RequiredException",
    "TimeoutException",
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


# MIT License

# Copyright (c) 2023 MPlatypus

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
