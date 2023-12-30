# This file deals with events, from payloads.
from __future__ import annotations

import typing as t
import logging
from . import errors
from .abc import (
    ReadyEvent,
    StatisticsEvent,
    TrackStartEvent,
    TrackEndEvent,
    TrackExceptionEvent,
    TrackStuckEvent,
    WebsocketClosedEvent,
)

if t.TYPE_CHECKING:
    from ..ongaku import Ongaku

_logger = logging.getLogger("ongaku.events")

class EventHandler:
    def __init__(self, ongaku: Ongaku) -> None:
        self._ongaku = ongaku

    async def handle_payload(self, payload: dict[t.Any, t.Any]) -> None:
        try:
            op_code = payload["op"]
        except Exception as e:
            raise e

        if op_code == "ready":
            await self._ready_payload(payload)

        elif op_code == "stats":
            await self._stats_payload(payload)

        elif op_code == "event":
            await self._event_payload(payload)

        elif op_code == "playerUpdate":
            pass

        else:
            logging.warning(f"OP code not recognized: {op_code}")

    async def _ready_payload(self, payload: dict[t.Any, t.Any]) -> None:
        try:
            session_id = payload["sessionId"]
        except:
            raise errors.SessionNotStartedException("Missing session id.")

        if session_id == None:
            raise errors.SessionNotStartedException("Missing session id.")

        self._ongaku.internal.set_session_id(session_id)

        try:
            event = ReadyEvent.as_payload(self._ongaku.bot, payload)
        except Exception as e:
            raise e

        logging.getLogger("ongaku.info").info("Successfully connected to the server.")
        await self._ongaku.bot.dispatch(event)

    async def _stats_payload(self, payload: dict[t.Any, t.Any]) -> None:
        try:
            event = StatisticsEvent.as_payload(self._ongaku.bot, payload)
        except Exception as e:
            raise e

        await self._ongaku.bot.dispatch(event)

    async def _event_payload(self, payload: dict[t.Any, t.Any]) -> None:
        try:
            event_type = payload["type"]
        except Exception as e:
            raise e

        if event_type == "TrackStartEvent":
            try:
                event = TrackStartEvent.as_payload(self._ongaku.bot, payload)
            except Exception as e:
                raise e

        elif event_type == "TrackEndEvent":
            try:
                event = TrackEndEvent.as_payload(self._ongaku.bot, payload)
            except Exception as e:
                raise e

        elif event_type == "TrackExceptionEvent":
            try:
                event = TrackExceptionEvent.as_payload(self._ongaku.bot, payload)
            except Exception as e:
                raise e

        elif event_type == "TrackStuckEvent":
            try:
                event = TrackStuckEvent.as_payload(self._ongaku.bot, payload)
            except Exception as e:
                raise e

        elif event_type == "WebSocketClosedEvent":
            try:
                event = WebsocketClosedEvent.as_payload(self._ongaku.bot, payload)
            except Exception as e:
                raise e

        else:
            return

        await self._ongaku.bot.dispatch(event)
