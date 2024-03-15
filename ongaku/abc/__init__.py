"""
Abstract classes.

All of the abstract classes for Ongaku.
"""

from .bases import OngakuEvent
from .events import PlayerBase
from .events import PlayerUpdateEvent
from .events import QueueEmptyEvent
from .events import QueueNextEvent
from .events import ReadyEvent
from .events import StatisticsEvent
from .events import TrackBase
from .events import TrackEndEvent
from .events import TrackExceptionEvent
from .events import TrackStartEvent
from .events import TrackStuckEvent
from .events import WebsocketClosedEvent
from .filters import Filter
from .lavalink import ExceptionError
from .lavalink import Info
from .lavalink import InfoGit
from .lavalink import InfoPlugin
from .lavalink import InfoVersion
from .lavalink import RestError
from .player import Player
from .player import PlayerState
from .player import PlayerVoice
from .playlist import Playlist
from .playlist import PlaylistInfo
from .route_planner import FailingAddress
from .route_planner import RoutePlannerDetails
from .route_planner import RoutePlannerStatus
from .session import Session
from .statistics import StatsCpu
from .statistics import StatsFrameStatistics
from .statistics import StatsMemory
from .track import Track
from .track import TrackInfo

__all__ = (
    # .events
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
    # .filters
    "Filter",
    # .lavalink
    "InfoVersion",
    "InfoGit",
    "InfoPlugin",
    "Info",
    "RestError",
    "ExceptionError",
    # .player
    "PlayerState",
    "PlayerVoice",
    "Player",
    # .route_planner
    "FailingAddress",
    "RoutePlannerDetails",
    "RoutePlannerStatus",
    # .session
    "Session",
    # .track
    "TrackInfo",
    "Track",
    "PlaylistInfo",
    "Playlist",
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
