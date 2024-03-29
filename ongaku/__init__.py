"""
A voice handling library for hikari.

GitHub:
https://github.com/MPlatypus/hikari-ongaku
Docs:
https://ongaku.mplaty.com/
"""

from __future__ import annotations

import logging

from . import internal

logging.addLevelName(internal.TRACE_LEVEL, internal.TRACE_NAME)


from .abc.bases import OngakuEvent
from .abc.events import PlayerBase
from .abc.events import PlayerUpdateEvent
from .abc.events import QueueEmptyEvent
from .abc.events import QueueNextEvent
from .abc.events import ReadyEvent
from .abc.events import StatisticsEvent
from .abc.events import TrackBase
from .abc.events import TrackEndEvent
from .abc.events import TrackExceptionEvent
from .abc.events import TrackStartEvent
from .abc.events import TrackStuckEvent
from .abc.events import WebsocketClosedEvent
from .abc.filters import Filters
from .abc.playlist import Playlist
from .abc.statistics import StatsCpu
from .abc.statistics import StatsFrameStatistics
from .abc.statistics import StatsMemory
from .abc.track import Track
from .client import Client
from .enums import BandType
from .enums import ConnectionType
from .enums import IPBlockType
from .enums import RoutePlannerType
from .enums import SeverityType
from .enums import TrackEndReasonType
from .enums import VersionType
from .errors import BuildException
from .errors import LavalinkException
from .errors import OngakuException
from .errors import PlayerConnectException
from .errors import PlayerException
from .errors import PlayerMissingException
from .errors import PlayerQueueException
from .errors import SessionConnectionException
from .errors import SessionException
from .errors import SessionHandlerException
from .errors import WebsocketClosureException
from .errors import WebsocketException
from .errors import WebsocketTypeException
from .internal.about import __author__
from .internal.about import __author_email__
from .internal.about import __license__
from .internal.about import __maintainer__
from .internal.about import __url__
from .internal.about import __version__
from .player import Player
from .session import Session

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
    "RoutePlannerType",
    "IPBlockType",
    # .exceptions
    "OngakuException",
    "WebsocketException",
    "WebsocketClosureException",
    "WebsocketTypeException",
    "SessionException",
    "SessionConnectionException",
    "PlayerException",
    "PlayerConnectException",
    "PlayerQueueException",
    "PlayerMissingException",
    "BuildException",
    "LavalinkException",
    "SessionHandlerException",
    # .player
    "Player",
    # .session
    "Session",
    # .abc.events
    "OngakuEvent",
    "ReadyEvent",
    "PlayerUpdateEvent",
    "StatsMemory",
    "StatsCpu",
    "StatsFrameStatistics",
    "StatisticsEvent",
    "WebsocketClosedEvent",
    "TrackBase",
    "TrackStartEvent",
    "TrackEndEvent",
    "TrackExceptionEvent",
    "TrackStuckEvent",
    "PlayerBase",
    "QueueEmptyEvent",
    "QueueNextEvent",
    # .abc.track
    "Track",
    "Playlist",
    # .abc.filter
    "Filters",
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
