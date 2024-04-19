"""
A voice handling library for hikari.

GitHub:
https://github.com/MPlatypus/hikari-ongaku
Docs:
https://ongaku.mplaty.com/
"""

from __future__ import annotations

import logging

from ongaku.internal.logger import TRACE_LEVEL
from ongaku.internal.logger import TRACE_NAME

logging.addLevelName(TRACE_LEVEL, TRACE_NAME)


from ongaku.abc.bases import OngakuEvent
from ongaku.abc.filters import Filters
from ongaku.abc.playlist import Playlist
from ongaku.abc.statistics import StatsCpu
from ongaku.abc.statistics import StatsFrameStatistics
from ongaku.abc.statistics import StatsMemory
from ongaku.abc.track import Track
from ongaku.client import Client
from ongaku.enums import BandType
from ongaku.enums import ConnectionType
from ongaku.enums import IPBlockType
from ongaku.enums import RoutePlannerType
from ongaku.enums import SeverityType
from ongaku.enums import TrackEndReasonType
from ongaku.enums import VersionType
from ongaku.errors import BuildException
from ongaku.errors import LavalinkException
from ongaku.errors import OngakuException
from ongaku.errors import PlayerConnectException
from ongaku.errors import PlayerException
from ongaku.errors import PlayerMissingException
from ongaku.errors import PlayerQueueException
from ongaku.errors import SessionConnectionException
from ongaku.errors import SessionException
from ongaku.errors import SessionHandlerException
from ongaku.errors import WebsocketClosureException
from ongaku.errors import WebsocketException
from ongaku.errors import WebsocketTypeException
from ongaku.events import PlayerUpdateEvent
from ongaku.events import QueueEmptyEvent
from ongaku.events import QueueNextEvent
from ongaku.events import ReadyEvent
from ongaku.events import StatisticsEvent
from ongaku.events import TrackEndEvent
from ongaku.events import TrackExceptionEvent
from ongaku.events import TrackStartEvent
from ongaku.events import TrackStuckEvent
from ongaku.events import WebsocketClosedEvent
from ongaku.internal.about import __author__
from ongaku.internal.about import __author_email__
from ongaku.internal.about import __license__
from ongaku.internal.about import __maintainer__
from ongaku.internal.about import __url__
from ongaku.internal.about import __version__
from ongaku.player import Player
from ongaku.session import Session

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
    "TrackStartEvent",
    "TrackEndEvent",
    "TrackExceptionEvent",
    "TrackStuckEvent",
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
