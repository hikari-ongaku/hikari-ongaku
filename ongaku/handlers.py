"""
Handler.

Handles all payload related events.
"""

from __future__ import annotations

import typing as t

import ujson
from aiohttp import WSMessage
from aiohttp import WSMsgType

from .abc import OngakuEvent
from .abc import PlayerUpdateEvent
from .abc import ReadyEvent
from .abc import StatisticsEvent
from .abc import TrackEndEvent
from .abc import TrackExceptionEvent
from .abc import TrackStartEvent
from .abc import TrackStuckEvent
from .abc import WebsocketClosedEvent
from .enums import WebsocketEventType
from .enums import WebsocketOPCodeType
from .errors import WebsocketTypeException
from .internal import TRACE_LEVEL
from .internal import logger

if t.TYPE_CHECKING:
    from .session import Session

__all__ = (
    "_EventHandler",
    "_WSHandler",
)

_logger = logger.getChild("handlers")


class _EventHandler:
    def __init__(self, session: Session) -> None:
        self._client = session.client
        self._session = session

    async def _handle_event(
        self, payload: str, event_payload: dict[str, t.Any]
    ) -> OngakuEvent:
        event_type: WebsocketEventType | str | None = event_payload.get("type")

        if event_type is None:
            raise WebsocketTypeException(None, "OP code not found.")

        try:
            event_type = WebsocketEventType(event_type)
        except Exception:
            raise WebsocketTypeException(None, f"OP code: {event_type} is not known.")

        match event_type:
            case WebsocketEventType.TRACK_START_EVENT:
                event = TrackStartEvent._build(payload, self._session, self._client.bot)

            case WebsocketEventType.TRACK_END_EVENT:
                event = TrackEndEvent._build(payload, self._session, self._client.bot)

            case WebsocketEventType.TRACK_EXCEPTION_EVENT:
                event = TrackExceptionEvent._build(
                    payload, self._session, self._client.bot
                )

            case WebsocketEventType.TRACK_STUCK_EVENT:
                event = TrackStuckEvent._build(payload, self._session, self._client.bot)

            case WebsocketEventType.WEBSOCKET_CLOSED_EVENT:
                event = WebsocketClosedEvent._build(
                    payload, self._session, self._client.bot
                )

        return event

    async def handle_event(self, payload: str) -> None:
        event_payload: dict[str, t.Any] = ujson.loads(payload)

        op_code: WebsocketOPCodeType | str | None = event_payload.get("op")

        if op_code is None:
            raise WebsocketTypeException(None, "OP code not found.")

        try:
            op_code = WebsocketOPCodeType(op_code)
        except Exception:
            raise WebsocketTypeException(None, f"OP code: {op_code} is not known.")

        match op_code:
            case WebsocketOPCodeType.READY:
                event = ReadyEvent._build(payload, self._session, self._client.bot)

                self._session.session_id = event.session_id

            case WebsocketOPCodeType.PLAYER_UPDATE:
                event = PlayerUpdateEvent._build(
                    payload, self._session, self._client.bot
                )

            case WebsocketOPCodeType.STATS:
                event = StatisticsEvent._build(payload, self._session, self._client.bot)

            case WebsocketOPCodeType.EVENT:
                event = await self._handle_event(payload, event_payload)

        self._client.bot.dispatch(event)


class _WSHandler:
    def __init__(
        self, session: Session, event_handler: _EventHandler | None = None
    ) -> None:
        self._client = session.client
        self._session = session

        if event_handler:
            self._event_handler = event_handler
        else:
            self._event_handler = _EventHandler(session)

    async def handle_message(self, message: WSMessage) -> None:
        match message.type:
            case WSMsgType.TEXT:
                # Handle a text response.
                if not isinstance(message.data, str):
                    raise WebsocketTypeException(
                        None,
                        "Unable to handle event due to data not being of type str.",
                    )

                await self._event_handler.handle_event(message.data)

            case WSMsgType.ERROR:
                # handle error for the websocket.
                _logger.warning(
                    f"An error has occurred on websocket: {self._session.host}:{self._session.port} Reason: {message.data}"
                )

                self._session._strike_server(message.data)

            case WSMsgType.CLOSE:
                # handle close event for websocket.
                _logger.warning(
                    f"Websocket has closed for: {self._session.host}:{self._session.port}. Closure code: {message.data}"
                )
                # self._session._strike_server(f"Websocket Closure. Reason: {message.data}")
                await self._session.client._session_handler.switch_session()

            case _:
                _logger.log(TRACE_LEVEL, f"Received a {message.type}. Ignoring.")


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
