"""Events.

The event handler for ongaku's sessions.
"""

from __future__ import annotations

import logging
import typing as t

from ongaku import internal

from .abc import ReadyEvent
from .abc import StatisticsEvent
from .abc import TrackEndEvent
from .abc import TrackExceptionEvent
from .abc import TrackStartEvent
from .abc import TrackStuckEvent
from .abc import WebsocketClosedEvent
from .errors import SessionStartException

if t.TYPE_CHECKING:
    from .session import Session

_logger = internal.logger.getChild("events")


class EventHandler:
    """The base event handler.

    !!! warning
        Please do not build this on your own. This is built internally.
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    async def handle_payload(self, payload: t.Mapping[t.Any, t.Any]) -> None:
        """Handle all incoming payloads."""
        _logger.log(internal.Trace.LEVEL, f"Handling payload...")
        try:
            op_code = payload["op"]
        except Exception as e:
            raise e

        if op_code == "ready":
            _logger.log(internal.Trace.LEVEL, f"Decoding ready payload...")
            await self.ready_payload(payload)

        elif op_code == "stats":
            _logger.log(internal.Trace.LEVEL, f"Decoding stats payload...")
            await self.stats_payload(payload)

        elif op_code == "event":
            _logger.log(internal.Trace.LEVEL, f"Decoding event payload...")
            await self.event_payload(payload)

        elif op_code == "playerUpdate":
            _logger.log(internal.Trace.LEVEL, f"Decoding playerUpdate payload...")
            pass

        else:
            logging.warning(f"OP code not recognized: {op_code}")

    async def ready_payload(self, payload: t.Mapping[t.Any, t.Any]) -> None:
        """Handle ready payload."""
        try:
            session_id = str(payload["sessionId"])
        except Exception:
            raise SessionStartException("Session id does not exist in ready payload.")

        if session_id.strip() == "":
            raise SessionStartException("Session ID cannot be none.")

        self._session._internal.session_id = session_id

        try:
            event = ReadyEvent._from_payload(payload, self._session.client.bot)
        except Exception as e:
            raise e

        
        await self._session.client.bot.dispatch(event)
        _logger.log(internal.Trace.LEVEL, "Successful decode, and dispatch of ready payload.")

    async def stats_payload(self, payload: t.Mapping[t.Any, t.Any]) -> None:
        """Handle statistics payload."""
        try:
            event = StatisticsEvent._from_payload(payload, app=self._session.client.bot)
        except Exception as e:
            raise e

        await self._session.client.bot.dispatch(event)

        _logger.log(internal.Trace.LEVEL, "Successful decode, and dispatch of stats payload.")

    async def event_payload(self, payload: t.Mapping[t.Any, t.Any]) -> None:
        """Handle event payloads."""
        try:
            event_type = payload["type"]
        except Exception as e:
            raise e

        if event_type == "TrackStartEvent":
            try:
                event = TrackStartEvent._from_payload(
                    payload, app=self._session.client.bot
                )
            except Exception as e:
                raise e

        elif event_type == "TrackEndEvent":
            try:
                event = TrackEndEvent._from_payload(
                    payload, app=self._session.client.bot
                )
            except Exception as e:
                raise e

        elif event_type == "TrackExceptionEvent":
            try:
                event = TrackExceptionEvent._from_payload(
                    payload, app=self._session.client.bot
                )
            except Exception as e:
                raise e

        elif event_type == "TrackStuckEvent":
            try:
                event = TrackStuckEvent._from_payload(
                    payload, app=self._session.client.bot
                )
            except Exception as e:
                raise e

        elif event_type == "WebSocketClosedEvent":
            try:
                event = WebsocketClosedEvent._from_payload(
                    payload, app=self._session.client.bot
                )
            except Exception as e:
                raise e

        else:
            logging.warning(f"Event code not recognized: {event_type}")
            raise Exception(f"Unknown event code: {event_type}")
        
        _logger.log(internal.Trace.LEVEL, "Successful decode, and dispatch of event payload.")

        await self._session.client.bot.dispatch(event)


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
