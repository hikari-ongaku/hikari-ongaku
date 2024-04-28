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


from ongaku.abc.playlist import Playlist
from ongaku.abc.track import Track
from ongaku.client import Client
from ongaku.enums import BandType
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
from ongaku.events import OngakuEvent
from ongaku.events import PayloadEvent
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
    # .player
    "Player",
    # .session
    "Session",
    # .enums
    "BandType",
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
    # .abc.events
    "OngakuEvent",
    "PayloadEvent",
    "ReadyEvent",
    "PlayerUpdateEvent",
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
    # .abc.playlist
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
