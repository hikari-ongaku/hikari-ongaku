"""
Sessions.

The base hikari session.
"""

from __future__ import annotations

import abc
import asyncio
import typing as t

import aiohttp
import hikari

from .about import __version__
from .enums import ConnectionType
from .enums import VersionType
from .exceptions import PlayerMissingException
from .exceptions import SessionConnectionException
from .handlers import _WSHandler
from .internal import Trace
from .internal import logger
from .player import Player

if t.TYPE_CHECKING:
    from .client import Client

__all__ = ("Session",)

_logger = logger.getChild("session")


class Session:
    """
    Session.

    The session object, for a specific lavalink server session, or connection.
    """

    ssl: t.Final[bool]
    host: t.Final[str]
    port: t.Final[int]
    password: t.Final[str] | None
    version: t.Final[VersionType]
    remaining_attempts: int
    total_attempts: int

    base_uri: t.Final[str]
    base_headers: dict[str, t.Any]
    status: ConnectionType = ConnectionType.NOT_CONNECTED
    session_id: str | None = None
    players: t.MutableSequence[Player] = []
    _connection: asyncio.Task[None] | None = None

    def __init__(
        self,
        client: Client,
        ssl: bool,
        host: str,
        port: int,
        password: str | None,
        version: VersionType,
        attempts: int,
    ) -> None:
        self._client = client
        self.ssl = ssl
        self.host = host
        self.port = port
        self.password = password
        self.version = version
        self.remaining_attempts = attempts
        self.total_attempts = attempts
        self.base_uri = f"http{'s' if ssl else ''}://{host}:{port}"
        self.base_headers = {"Authorization": password} if password else {}
        self._handler = _WSHandler(self)

    @property
    def client(self) -> Client:
        """The Ongaku client."""
        return self._client

    def _get_session_id(self) -> str:
        """
        Get session id.
        
        Returns the session ID, or raises a SessionConnectionException
        """
        if self.session_id:
            return self.session_id

        raise SessionConnectionException(None)

    def _strike_server(self, reason: str) -> None:
        self.remaining_attempts -= 1

        _logger.warning(
            f"server: {self.host}:{self.port} has failed to load properly. Remaining attempts: {self.remaining_attempts}. Reason: {reason}."
        )

        if self.remaining_attempts == 0:
            _logger.critical(
                f"server: {self.host}:{self.port} has completely failed. Reason: {reason}."
            )

            self.status = ConnectionType.FAILURE

            asyncio.Task(self.client._session_handler.switch_session())

    async def _create_connection(self) -> None:
        session = await self.client._get_session()

        try:
            async with session.ws_connect(
                self.base_uri + self.version.value + "/websocket",
                headers=self.base_headers,
                timeout=5,
            ) as ws:
                self.status = ConnectionType.CONNECTED
                _logger.log(
                    Trace.LEVEL,
                    f"Websocket connection on session {self.host}:{self.port} successful.",
                )
                async for msg in ws:
                    await self._handler.handle_message(msg)
        except aiohttp.ClientConnectionError:
            self._strike_server("Client Timeout")

        except Exception as e:
            self._strike_server(str(e))

    def start(self) -> None:
        """
        Start up the session.

        Starts up a new session, and attempts a connection to the lavalink server.
        """
        try:
            bot = self._client.bot.get_me()
        except Exception:
            reason = f"Session: {self.host}:{self.port} could not start, due to the bot ID not being found."
            _logger.warning(reason)
            raise SessionConnectionException(None, reason)

        if bot is None:
            reason = f"Session: {self.host}:{self.port} could not start, due to the bot ID not being found."
            _logger.warning(reason)
            raise SessionConnectionException(None, reason)

        new_headers = {
            "User-Id": str(bot.id),
            "Client-Name": f"{bot.username.replace(' ', '_').strip()}::{__version__}",
        }

        self.base_headers.update(new_headers)

        _logger.log(Trace.LEVEL, "Starting websocket connection...")

        self._connection = asyncio.create_task(self._create_connection())

    def stop(self) -> None:
        """
        Stop the session.
        
        Stops and shuts down the sessions' connection, if it existed.
        """
        if self._connection:
            self._connection.cancel()
            self._connection = None


class BaseSessionHandler(abc.ABC):
    """
    Base Session handler.

    The base class for creating a new session handler.

    Raises
    ------
    SessionConnectionException
        You should raise this, when it cannot find an available session.
    """

    def __init__(self, client: Client) -> None: ...

    @abc.abstractproperty
    def sessions(self) -> t.Sequence[Session]:
        """All available sessions."""
        ...

    @abc.abstractproperty
    def players(self) -> t.Sequence[Player]:
        """All players, across all sessions."""
        ...

    @abc.abstractmethod
    def add_server(
        self,
        *,
        ssl: bool = False,
        host: str = "localhost",
        port: int = 2333,
        password: str | None = "youshallnotpass",
        version: VersionType = VersionType.V4,
    ) -> None:
        """Add a server to the handler."""
        ...

    @abc.abstractmethod
    async def start(self) -> None:
        """Start all of the servers up."""
        ...

    @abc.abstractmethod
    async def stop(self) -> None:
        """Stop all of the servers."""
        ...

    @abc.abstractmethod
    async def fetch_session(self) -> Session:
        """Fetch the current session."""
        ...

    @abc.abstractmethod
    async def switch_session(self) -> Session:
        """
        Switch session.
        
        called when a session fails.
        """
        ...

    @abc.abstractmethod
    async def create_player(self, guild_id: hikari.Snowflake) -> Player:
        """
        Create a player.

        Creates a player for the specified session.
        """
        ...

    @abc.abstractmethod
    async def fetch_player(self, guild_id: hikari.Snowflake) -> Player:
        """
        Fetch a player.

        Fetches a player from the current session that its in.
        """
        ...

    @abc.abstractmethod
    async def delete_player(self, guild_id: hikari.Snowflake) -> None:
        """
        Delete a player.

        Deletes a player from the current session that its in.
        """
        ...


class GeneralSessionHandler(BaseSessionHandler):
    """
    General session handler.

    This simply just returns the next available, and working server.
    """

    def __init__(self, client: Client) -> None:
        self._client = client

        self._sessions: list[Session] = []

        self._started = False

        self._current_session: Session | None = None

    @property
    def sessions(self) -> t.Sequence[Session]:
        """All available sessions."""
        return self._sessions

    @property
    def players(self) -> t.Sequence[Player]:
        players_sequence: t.MutableSequence[Player] = []

        for session in self.sessions:
            players_sequence.extend(session.players)

        return players_sequence

    def add_server(
        self,
        *,
        ssl: bool = False,
        host: str = "localhost",
        port: int = 2333,
        password: str | None = "youshallnotpass",
        version: VersionType = VersionType.V4,
    ) -> None:
        new_server = Session(
            self._client, ssl, host, port, password, version, self._client._attempts
        )

        self._sessions.append(new_server)

        if self._started:
            new_server.start()

    async def start(self) -> None:
        self._started = True

        sessions = self.sessions

        pos = 0

        started_servers = 0
        while started_servers != len(sessions):
            await asyncio.sleep(1)
            
            if pos >= len(sessions):
                pos = 0
            else:
                pos += 1
            
            session = sessions[pos - 1]

            if session.status == ConnectionType.CONNECTED:
                started_servers += 1
                continue
            
            if session.status == ConnectionType.NOT_CONNECTED:
                if session.remaining_attempts >= 1:
                    session.remaining_attempts -= 1
                    session.start()
                else:
                    continue

    async def stop(self) -> None:
        for server in self.sessions:
            server.stop()

    async def fetch_session(self) -> Session:
        if (
            self._current_session
            and self._current_session.status == ConnectionType.CONNECTED
        ):
            return self._current_session

        for session in self.sessions:
            if session.status == ConnectionType.CONNECTED:
                self._current_session = session
                return self._current_session

        raise SessionConnectionException(None)

    async def switch_session(self) -> Session:
        current_session = self._current_session

        new_session = await self.fetch_session()

        if current_session is None:
            return new_session

        current_session.stop()

        for player in current_session.players:
            new_player = await player._transfer_player(new_session)
            new_session.players.append(new_player)

        self._current_session = new_session

        return new_session

    async def create_player(self, guild_id: hikari.Snowflake) -> Player:
        for player in self.players:
            if player.guild_id == guild_id:
                return player

        session = await self.fetch_session()

        new_player = Player(session, guild_id)

        session.players.append(new_player)

        return new_player

    async def fetch_player(self, guild_id: hikari.Snowflake) -> Player:
        for player in self.players:
            if player.guild_id == guild_id:
                return player

        raise PlayerMissingException(guild_id)

    async def delete_player(self, guild_id: hikari.Snowflake) -> None:
        player = await self.fetch_player(guild_id)

        await player.disconnect()
        
        player.session.players.remove(player)


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
