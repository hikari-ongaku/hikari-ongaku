"""
A voice handling library for hikari.

GitHub:
https://github.com/hikari-ongaku/hikari-ongaku
Docs:
https://ongaku.mplaty.com
"""

from __future__ import annotations

import logging

from ongaku.abc import Playlist
from ongaku.abc import Track
from ongaku.abc.errors import SeverityType
from ongaku.abc.events import TrackEndReasonType
from ongaku.abc.filters import BandType
from ongaku.abc.routeplanner import IPBlockType
from ongaku.abc.routeplanner import RoutePlannerType
from ongaku.abc.session import SessionStatus
from ongaku.client import Client
from ongaku.errors import BuildError
from ongaku.errors import ClientAliveError
from ongaku.errors import ClientError
from ongaku.errors import NoSessionsError
from ongaku.errors import OngakuError
from ongaku.errors import PlayerConnectError
from ongaku.errors import PlayerError
from ongaku.errors import PlayerMissingError
from ongaku.errors import PlayerNotConnectedError
from ongaku.errors import PlayerQueueError
from ongaku.errors import RestEmptyError
from ongaku.errors import RestError
from ongaku.errors import RestExceptionError
from ongaku.errors import RestRequestError
from ongaku.errors import RestStatusError
from ongaku.errors import SessionError
from ongaku.errors import SessionHandlerError
from ongaku.errors import SessionMissingError
from ongaku.errors import SessionStartError
from ongaku.errors import TimeoutError
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
from ongaku.impl import BasicSessionHandler
from ongaku.impl.filters import Filters
from ongaku.internal import __author__
from ongaku.internal import __author_email__
from ongaku.internal import __license__
from ongaku.internal import __maintainer__
from ongaku.internal import __url__
from ongaku.internal import __version__
from ongaku.internal.logger import TRACE_LEVEL
from ongaku.internal.logger import TRACE_NAME
from ongaku.player import Player
from ongaku.session import Session

logging.addLevelName(TRACE_LEVEL, TRACE_NAME)

__all__ = (  # noqa: RUF022
    # .internal
    "__author__",
    "__author_email__",
    "__maintainer__",
    "__license__",
    "__url__",
    "__version__",
    # .client
    "Client",
    # .errors
    "OngakuError",
    "RestError",
    "RestStatusError",
    "RestRequestError",
    "RestEmptyError",
    "RestExceptionError",
    "ClientError",
    "ClientAliveError",
    "SessionError",
    "SessionStartError",
    "SessionMissingError",
    "SessionHandlerError",
    "NoSessionsError",
    "PlayerError",
    "PlayerConnectError",
    "PlayerNotConnectedError",
    "PlayerQueueError",
    "PlayerMissingError",
    "BuildError",
    "TimeoutError",
    # .events
    "PayloadEvent",
    "ReadyEvent",
    "PlayerUpdateEvent",
    "StatisticsEvent",
    "TrackStartEvent",
    "TrackEndEvent",
    "TrackExceptionEvent",
    "TrackStuckEvent",
    "WebsocketClosedEvent",
    "QueueEmptyEvent",
    "QueueNextEvent",
    # .player
    "Player",
    # .session
    "Session",
    # .abc
    "SeverityType",
    "TrackEndReasonType",
    "BandType",
    "Playlist",
    "RoutePlannerType",
    "IPBlockType",
    "SessionStatus",
    "Track",
    # .impl
    "Filters",
    "BasicSessionHandler",
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
