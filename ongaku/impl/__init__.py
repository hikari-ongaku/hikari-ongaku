"""Implementation.

All implementations of abstract classes.
"""

from __future__ import annotations

from ongaku.impl.filters import ChannelMix
from ongaku.impl.filters import Distortion
from ongaku.impl.filters import Equalizer
from ongaku.impl.filters import Filters
from ongaku.impl.filters import Karaoke
from ongaku.impl.filters import LowPass
from ongaku.impl.filters import Rotation
from ongaku.impl.filters import Timescale
from ongaku.impl.filters import Tremolo
from ongaku.impl.filters import Vibrato
from ongaku.impl.handlers import BasicSessionHandler
from ongaku.impl.info import Git
from ongaku.impl.info import Info
from ongaku.impl.info import Plugin
from ongaku.impl.info import Version
from ongaku.impl.player import Player
from ongaku.impl.player import State
from ongaku.impl.player import Voice
from ongaku.impl.playlist import Playlist
from ongaku.impl.playlist import PlaylistInfo
from ongaku.impl.routeplanner import FailingAddress
from ongaku.impl.routeplanner import IPBlock
from ongaku.impl.routeplanner import RoutePlannerDetails
from ongaku.impl.routeplanner import RoutePlannerStatus
from ongaku.impl.session import Session
from ongaku.impl.statistics import Cpu
from ongaku.impl.statistics import FrameStatistics
from ongaku.impl.statistics import Memory
from ongaku.impl.statistics import Statistics
from ongaku.impl.track import Track
from ongaku.impl.track import TrackInfo

__all__ = ( # noqa: RUF022
    # .filters
    "Filters",
    "Equalizer",
    "Karaoke",
    "Timescale",
    "Tremolo",
    "Vibrato",
    "Rotation",
    "Distortion",
    "ChannelMix",
    "LowPass",
    # .handlers
    "BasicSessionHandler",
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
    "Playlist",
    "PlaylistInfo",
    # .routeplanner
    "RoutePlannerStatus",
    "RoutePlannerDetails",
    "IPBlock",
    "FailingAddress",
    # .session
    "Session",
    # .statistics
    "Statistics",
    "Memory",
    "Cpu",
    "FrameStatistics",
    # .track
    "Track",
    "TrackInfo",
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
