"""
Abstract classes.

All of the abstract classes for Ongaku.
"""

from __future__ import annotations

from ongaku.abc.errors import ExceptionError
from ongaku.abc.errors import SeverityType
from ongaku.abc.events import OngakuEvent
from ongaku.abc.events import TrackEndReasonType
from ongaku.abc.extension import Extension
from ongaku.abc.filters import BandType
from ongaku.abc.filters import ChannelMix
from ongaku.abc.filters import Distortion
from ongaku.abc.filters import Equalizer
from ongaku.abc.filters import Filters
from ongaku.abc.filters import Karaoke
from ongaku.abc.filters import LowPass
from ongaku.abc.filters import Rotation
from ongaku.abc.filters import Timescale
from ongaku.abc.filters import Tremolo
from ongaku.abc.filters import Vibrato
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
    "BandType",
    "ChannelMix",
    "Cpu",
    "Distortion",
    "Equalizer",
    "ExceptionError",
    "Extension",
    "FailingAddress",
    "Filters",
    "FrameStatistics",
    "Git",
    "IPBlock",
    "IPBlockType",
    "Info",
    "Karaoke",
    "LowPass",
    "Memory",
    "OngakuEvent",
    "Player",
    "Playlist",
    "PlaylistInfo",
    "Plugin",
    "Rotation",
    "RoutePlannerDetails",
    "RoutePlannerStatus",
    "RoutePlannerType",
    "Session",
    "SessionHandler",
    "SessionStatus",
    "SeverityType",
    "State",
    "Statistics",
    "Timescale",
    "Track",
    "TrackEndReasonType",
    "TrackInfo",
    "Tremolo",
    "Version",
    "Vibrato",
    "Voice",
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
