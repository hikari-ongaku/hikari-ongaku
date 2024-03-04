"""Handler.

Handles all payload related events.
"""

from __future__ import annotations

import abc
import typing as t

import hikari
import ujson
from aiohttp import WSMessage
from aiohttp import WSMsgType

from . import session
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
from .exceptions import SessionHandlerException
from .exceptions import WebsocketClosureException
from .exceptions import WebsocketTypeException
from .player import Player

if t.TYPE_CHECKING:
    from .client import Client

__all__ = (
    "_EventHandler",
    "_WSHandler",
    "BaseSessionHandler",
    "ShardSessionHandler",
)


class _EventHandler:
    def __init__(self, session: session.Session) -> None:
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
                event = TrackStartEvent._from_payload(payload, self._client.bot)

            case WebsocketEventType.TRACK_END_EVENT:
                event = TrackEndEvent._from_payload(payload, self._client.bot)

            case WebsocketEventType.TRACK_EXCEPTION_EVENT:
                event = TrackExceptionEvent._from_payload(payload, self._client.bot)

            case WebsocketEventType.TRACK_STUCK_EVENT:
                event = TrackStuckEvent._from_payload(payload, self._client.bot)

            case WebsocketEventType.WEBSOCKET_CLOSED_EVENT:
                event = WebsocketClosedEvent._from_payload(payload, self._client.bot)

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
                event = ReadyEvent._from_payload(payload, self._client.bot)

                self._session._session_id = event.session_id

            case WebsocketOPCodeType.PLAYER_UPDATE:
                event = PlayerUpdateEvent._from_payload(payload, self._client.bot)

            case WebsocketOPCodeType.STATS:
                event = StatisticsEvent._from_payload(payload, self._client.bot)

            case WebsocketOPCodeType.EVENT:
                event = await self._handle_event(payload, event_payload)

        self._client.bot.dispatch(event)


class _WSHandler:
    def __init__(
        self, session: session.Session, event_handler: _EventHandler | None = None
    ) -> None:
        self._client = session.client
        self._session = session

        if event_handler:
            self._event_handler = event_handler
        else:
            self._event_handler = _EventHandler(session)

    async def _handle_error(self) -> None:
        pass

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
                await self._handle_error()

            case WSMsgType.CLOSE:
                # handle close event for websocket.
                raise WebsocketClosureException(message.data, message.extra)

            case _:
                pass


class BaseSessionHandler(abc.ABC):
    """Session Handler.

    The base class for all session handlers within ongaku.
    """

    @abc.abstractmethod
    def __init__(self, client: Client) -> None: ...

    @property
    @abc.abstractmethod
    def client(self) -> Client:
        """Ongaku Client."""
        ...

    @property
    @abc.abstractmethod
    def sessions(self) -> t.Sequence[session.Session]:
        """A sequence of sessions."""
        ...

    @property
    @abc.abstractmethod
    def players(self) -> t.Sequence[Player]:
        """A sequence of players."""
        ...

    @abc.abstractmethod
    async def start(self) -> None:
        """Start up the session handler."""
        ...

    @abc.abstractmethod
    async def stop(self) -> None:
        """Stop the session handler."""
        ...

    @abc.abstractmethod
    async def create_player(self, guild_id: hikari.Snowflake) -> Player:
        """Create a player on a session."""

    @abc.abstractmethod
    async def fetch_player(self, guild_id: hikari.Snowflake) -> Player:
        """Fetch a player from a session."""

    @abc.abstractmethod
    async def delete_player(self, guild_id: hikari.Snowflake) -> None:
        """Delete a player from a session."""


class ShardSessionHandler(BaseSessionHandler):
    """Shard based session handler.

    A shard based session handler, that creates, and handles all sessions via a shard related events.
    """

    def __init__(self, client: Client) -> None:
        self._client = client

        self.client.bot.subscribe(hikari.ShardEvent, self._shard_event)

        self._sessions: dict[str, session.Session] = {}
        self._players: dict[hikari.Snowflake, Player] = {}

    @property
    def client(self) -> Client:
        """Ongaku Client."""
        return self._client

    @property
    def sessions(self) -> t.Sequence[session.Session]:
        """All sessions on the session handler."""
        return tuple(self._sessions.values())

    @property
    def players(self) -> t.Sequence[Player]:
        """All players on the sessions in the session handler."""
        return tuple(self._players.values())

    async def _shard_event(self, event: hikari.ShardEvent) -> None:
        if isinstance(event, hikari.events.ShardReadyEvent):
            print("Creating session:", event.shard.id)

            new_session = session.Session(self.client, str(event.shard.id))

            try:
                await new_session.connect()
            except:
                raise

            self._sessions.update({str(event.shard.id): new_session})

            print("Session has been created, and added.")

    async def start(self) -> None: #noqa: D102
        pass

    async def stop(self) -> None: #noqa: D102
        self.client.bot.unsubscribe(hikari.ShardEvent, self._shard_event)

        for player in self.players:
            await player.disconnect()

        for session in self.sessions:
            await session.disconnect()

    async def create_player(self, guild_id: hikari.Snowflake) -> Player: #noqa: D102
        print("Creating a player")

        player = self._players.get(guild_id)

        if player:
            return player

        shard = hikari.snowflakes.calculate_shard_id(self.client.bot, guild_id)

        print(shard)

        session = self._sessions.get(str(shard))

        if session:
            new_player = await session.create_player(guild_id)

            self._players.update({guild_id: new_player})

            return new_player

        raise SessionHandlerException(
            f"Could not find a session, to create player for guild: {guild_id}"
        )

    async def fetch_player(self, guild_id: hikari.Snowflake) -> Player: #noqa: D102
        player = self._players.get(guild_id)

        if player:
            return player

        raise SessionHandlerException(f"Could not find a session for guild: {guild_id}")

    async def delete_player(self, guild_id: hikari.Snowflake) -> None: #noqa: D102
        player = await self.fetch_player(guild_id)

        await player.disconnect()


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
