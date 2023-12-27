# This file deals with events, from payloads.
from __future__ import annotations

import typing as t
import logging
from . import track, other
from .. import errors

if t.TYPE_CHECKING:
    from ..ongaku import Ongaku

    OngakuT = t.TypeVar("OngakuT", bound="Ongaku")


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
        print("payload: ", payload)

        try:
            session_id = payload["sessionId"]
        except:
            raise errors.InvalidSessionId()

        if session_id == None:
            raise errors.InvalidSessionId()

        self._ongaku.internal.set_session_id(session_id)

        try:
            event = other.ReadyEvent(self._ongaku.bot, payload)
        except Exception as e:
            print(e, e.args)
            raise e

        await self._ongaku.bot.dispatch(event)

    async def _stats_payload(self, payload: dict[t.Any, t.Any]) -> None:
        try:
            event = other.StatisticsEvent(self._ongaku.bot, payload)
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
                event = track.TrackStartEvent(self._ongaku.bot, payload)
            except Exception as e:
                raise e

        elif event_type == "TrackEndEvent":
            try:
                event = track.TrackEndEvent(self._ongaku.bot, payload)
            except Exception as e:
                raise e

        elif event_type == "TrackExceptionEvent":
            try:
                event = track.TrackExceptionEvent(self._ongaku.bot, payload)
            except Exception as e:
                raise e

        elif event_type == "TrackStuckEvent":
            try:
                event = track.TrackStuckEvent(self._ongaku.bot, payload)
            except Exception as e:
                raise e

        elif event_type == "WebSocketClosedEvent":
            try:
                event = other.WebsocketClosedEvent(self._ongaku.bot, payload)
            except Exception as e:
                raise e

        else:
            return

        await self._ongaku.bot.dispatch(event)
