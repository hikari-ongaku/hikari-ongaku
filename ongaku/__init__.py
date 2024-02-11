"""A voice handling library for hikari.

GitHub: 
https://github.com/MPlatypus/hikari-ongaku
Docs:
https://ongaku.mplaty.com/
"""

from __future__ import annotations
import logging
from . import internal
logging.addLevelName(internal.Trace.LEVEL, internal.Trace.NAME)

from . import abc
from . import enums
from . import errors
from . import ext
from .abc import events
from .abc import lavalink
from .abc import player
from .abc import session
from .abc import track
from .abc.events import QueueEmptyEvent
from .abc.events import QueueNextEvent
from .abc.events import ReadyEvent
from .abc.events import StatisticsEvent
from .abc.events import TrackEndEvent
from .abc.events import TrackExceptionEvent
from .abc.events import TrackStartEvent
from .abc.events import TrackStuckEvent
from .abc.events import WebsocketClosedEvent
from .abc.filters import Filter
from .abc.lavalink import ExceptionError
from .abc.lavalink import RestError
from .abc.player import Player
from .abc.player import PlayerState
from .abc.player import PlayerVoice
from .abc.session import Session
from .abc.track import Playlist
from .abc.track import SearchResult
from .abc.track import Track
from .about import __author__
from .about import __author_email__
from .about import __license__
from .about import __maintainer__
from .about import __url__
from .about import __version__
from .client import Client
from .enums import BandType
from .enums import ConnectionType
from .enums import SeverityType
from .enums import TrackEndReasonType
from .enums import VersionType
from .errors import BuildException
from .errors import GatewayRequiredException
from .errors import LavalinkConnectionException
from .errors import LavalinkException
from .errors import OngakuBaseException
from .errors import PlayerException
from .errors import PlayerMissingException
from .errors import PlayerQueueException
from .errors import RequiredException
from .errors import SessionStartException
from .errors import TimeoutException

__all__ = (
    # .about
    "__author__",
    "__author_email__",
    "__maintainer__",
    "__license__",
    "__url__",
    "__version__",
    # .client
    "Client",
    # .enums
    "SeverityType",
    "TrackEndReasonType",
    "VersionType",
    "ConnectionType",
    "BandType",
    # .errors
    "OngakuBaseException",
    "BuildException",
    "LavalinkException",
    "LavalinkConnectionException",
    "SessionStartException",
    "PlayerException",
    "PlayerMissingException",
    "PlayerQueueException",
    "GatewayRequiredException",
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
    "QueueEmptyEvent",
    "QueueNextEvent",
    # .abc.lavalink
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
    # .abc.filters
    "Filter",
    # Other
    "errors",
    "enums",
    "abc",
    "ext",
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
