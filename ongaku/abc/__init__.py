"""
Abstract classes.

All of the abstract classes for Ongaku.
"""

from __future__ import annotations

from ongaku.abc.errors import ExceptionError
from ongaku.abc.errors import SeverityType
from ongaku.abc.events import OngakuEvent
from ongaku.abc.events import TrackEndReasonType
from ongaku.abc.handler import SessionHandler
from ongaku.abc.info import Git
from ongaku.abc.info import Info
from ongaku.abc.info import Plugin
from ongaku.abc.info import Version
from ongaku.abc.player import Player
from ongaku.abc.player import State
from ongaku.abc.player import Voice
from ongaku.abc.playlist import Playlist
from ongaku.abc.playlist import PlaylistInfo
from ongaku.abc.routeplanner import FailingAddress
from ongaku.abc.routeplanner import IPBlock
from ongaku.abc.routeplanner import IPBlockType
from ongaku.abc.routeplanner import RoutePlannerDetails
from ongaku.abc.routeplanner import RoutePlannerStatus
from ongaku.abc.routeplanner import RoutePlannerType
from ongaku.abc.session import Session
from ongaku.abc.session import SessionStatus
from ongaku.abc.statistics import Cpu
from ongaku.abc.statistics import FrameStatistics
from ongaku.abc.statistics import Memory
from ongaku.abc.statistics import Statistics
from ongaku.abc.track import Track
from ongaku.abc.track import TrackInfo

__all__ = (
    # .errors
    "ExceptionError",
    "SeverityType",
    # .events
    "OngakuEvent",
    "TrackEndReasonType",
    # .handler
    "SessionHandler",
    # .info
    "Info",
    "Version",
    "Git",
    "Plugin",
    # .player
    "Player",
    "State",
    "Voice",
    # .playlist
    "PlaylistInfo",
    "Playlist",
    # .routeplanner
    "RoutePlannerStatus",
    "RoutePlannerDetails",
    "IPBlock",
    "FailingAddress",
    "RoutePlannerType",
    "IPBlockType",
    # .session
    "Session",
    "SessionStatus",
    # .statistics
    "Statistics",
    "Memory",
    "Cpu",
    "FrameStatistics",
    # .track
    "TrackInfo",
    "Track",
)


# MIT License

# Copyright (c) 2023-present MPlatypus

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
