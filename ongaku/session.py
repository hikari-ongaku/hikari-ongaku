"""Sessions.

The base hikari session.
"""

from __future__ import annotations

import abc
import asyncio
import typing as t

import aiohttp
import attrs
import hikari

from . import internal
from .enums import ConnectionType
from .errors import PlayerMissingException
from .errors import RequiredException
from .errors import SessionException
from .events import EventHandler
from .player import Player

if t.TYPE_CHECKING:
    from .client import Client

__all__ = ("Session",)

_logger = internal.logger.getChild("session")


@attrs.define
class _SessionInternal:
    attempts: int
    remaining_attempts: int
    base_uri: str
    headers: dict[str, t.Any]
    session_id: str | None = None
    connection_status: ConnectionType = ConnectionType.LOADING
    connection_failure_reason: str = ""

    @classmethod
    def build(
        cls, uri: str, headers: dict[str, t.Any], attempts: int
    ) -> _SessionInternal:
        return cls(attempts, attempts, uri, headers)


class Session(abc.ABC):
    """Session.

    A base session item, for sharding the sets of players.

    Parameters
    ----------
    client : Client
        The Ongaku client that it will be connected too.
    name : str
        The name of the session. This can be anything.
    """

    def __init__(self, client: Client, name: str) -> None:
        self._client = client
        self._name = name

        self._players: dict[hikari.Snowflake, Player] = {}

        self._internal = _SessionInternal.build(
            self.client._internal.base_uri,
            self.client._internal.headers,
            self.client._internal.attempts,
        )

        self._event_handler = EventHandler(self)

        self._connection: asyncio.Task[t.Any] | None = None

        self._player_session = PlayerSession(self)

    @property
    def name(self) -> str:
        """The name of the session."""
        return self._name

    @property
    def client(self) -> Client:
        """The [client][ongaku.Client] object that this session has attached to."""
        return self._client

    @property
    def players(self) -> t.Sequence[Player]:
        """The players, that are attached to this session."""
        return list(self._players.values())

    @property
    def player(self) -> PlayerSession:
        """The player functions."""
        return self._player_session

    async def _websocket(self, new_headers: dict[str, t.Any]):
        while self._internal.remaining_attempts > 1:
            if self._internal.remaining_attempts < self._internal.attempts:
                await asyncio.sleep(3)
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.ws_connect(
                        self._internal.base_uri + "/websocket", headers=new_headers
                    ) as ws:
                        _logger.log(
                            internal.Trace.LEVEL, "Websocket connection successful!"
                        )
                        async for msg in ws:
                            _logger.log(
                                internal.Trace.LEVEL,
                                f"Received message, with data: {msg.data}",
                            )
                            if msg.type == aiohttp.WSMsgType.ERROR:
                                _logger.warning(
                                    f"An error has occurred with the websocket connection. Reason: {msg.data}"
                                )
                                self._internal.connection_status = (
                                    ConnectionType.FAILURE
                                )
                                self._internal.connection_failure_reason = msg.data
                                raise SessionException(
                                    "An internal error has happened to this lavalink connection: "
                                    + msg.data
                                )

                            if msg.type == aiohttp.WSMsgType.CLOSED:
                                raise SessionException(
                                    "Session has received a closure message."
                                )

                            if msg.type == aiohttp.WSMsgType.TEXT:
                                _logger.log(
                                    internal.Trace.LEVEL, f"Decoding payload..."
                                )
                                try:
                                    json_data = msg.json()
                                except Exception as e:
                                    _logger.warning(
                                        f"Failed to decode payload. Error {e}, payload: {msg.data}"
                                    )
                                    raise SessionException(
                                        "Failed to decode payload: " + msg.data
                                    )
                                else:
                                    self._internal.connection_status = (
                                        ConnectionType.CONNECTED
                                    )
                                    self._internal.connection_failure_reason = ""

                                    await self._event_handler.handle_payload(json_data)

                except Exception as e:
                    self._internal.remaining_attempts -= 1
                    self._internal.connection_status = ConnectionType.FAILURE
                    self._internal.connection_failure_reason = f"Exception Raised: {e}"
                    raise

        raise SessionException(
            f"Maximum connection attempts reached. Reason: {self._internal.connection_failure_reason}"
        )

    async def _connect(self):
        """Connect to the lavalink websocket."""
        if (
            self._internal.connection_status == ConnectionType.CONNECTED
            or self._internal.connection_status == ConnectionType.FAILURE
        ):
            raise SessionException(
                "This session has failed its connection attempts. Please check your lavalink connection."
            )

        try:
            bot = self._client.bot.get_me()
        except Exception:
            self._internal.remaining_attempts = -1
            self._internal.connection_status = ConnectionType.FAILURE
            self._internal.connection_failure_reason = "Bot ID could not be found."
            _logger.warning("Bot ID cannot be None.")
            raise SessionException(
                "Ongaku could not start, due to the bot ID not being found."
            )

        if bot is None:
            self._internal.remaining_attempts = -1
            self._internal.connection_status = ConnectionType.FAILURE
            self._internal.connection_failure_reason = "Bot ID could not be found."
            _logger.warning("Bot ID cannot be None.")
            raise SessionException(
                "Ongaku could not start, due to the bot ID not being found."
            )

        new_header = {
            "User-Id": str(bot.id),
            "Client-Name": f"{str(bot.id)}::Unknown",
        }

        new_header.update(self._internal.headers)
        _logger.log(internal.Trace.LEVEL, "Starting websocket connection...")
        task = asyncio.create_task(self._websocket(new_header))

        self._connection = task

    async def _disconnect(self) -> None:
        _logger.log(internal.Trace.LEVEL, "Destroying connection...")
        if self._connection:
            self._connection.cancel()

        _logger.log(internal.Trace.LEVEL, f"successfully destroyed connection.")


class PlayerSession:
    def __init__(self, session: Session) -> None:
        self._session = session

    async def create_player(self, guild_id: hikari.Snowflake) -> Player:
        """Create a new player.

        Creates a new player for the specified guild, and places it in the specified channel.

        Parameters
        ----------
        guild_id : hikari.Snowflake
            The Guild ID the player will be in.

        Raises
        ------
        PlayerException
            Raised when the player failed to be created.

        Returns
        -------
        Player
            The player that has been successfully created.
        """
        _logger.log(
            internal.Trace.LEVEL,
            f"bot player: {guild_id} in node: {self._session.name}",
        )
        bot = self._session.client.bot.get_me()

        if bot is None:
            raise RequiredException("The bot is required to be able to connect.")

        bot_state = self._session.client.bot.cache.get_voice_state(guild_id, bot.id)

        if bot_state is not None and bot_state.channel_id is not None:
            try:
                self._session._players.pop(guild_id)
            except KeyError:
                raise SessionException("This session has not yet been started.")

        new_player = Player(self._session, guild_id)

        self._session._players.update({guild_id: new_player})

        _logger.log(
            internal.Trace.LEVEL,
            f"successfully created player: {guild_id} in node: {self._session.name}",
        )

        return new_player

    async def fetch_player(self, guild_id: hikari.Snowflake) -> Player:
        """Fetch a player.

        Fetch a player for the specified guild.

        Parameters
        ----------
        guild_id : hikari.Snowflake
            The guild id that the player belongs to.

        Raises
        ------
        PlayerMissingException
            The player was not found for the guild specified.

        Returns
        -------
        Player
            The player that belongs to the specified guild.
        """
        _logger.log(
            internal.Trace.LEVEL,
            f"finding player: {guild_id} in node: {self._session.name}",
        )

        for player in self._session._players.values():
            if player.guild_id == guild_id:
                _logger.log(
                    internal.Trace.LEVEL,
                    f"successfully found player: {guild_id} in node: {self._session.name}",
                )
                return player

        raise PlayerMissingException(guild_id)

    async def delete_player(self, guild_id: hikari.Snowflake) -> None:
        """Delete a player.

        Deletes a player from the specified guild, and disconnects it, if it has not been disconnected already.

        Parameters
        ----------
        guild_id : hikari.Snowflake
            The guild id that the player belongs to.

        Raises
        ------
        PlayerMissingException
            The player was not found for the guild specified.

        """
        _logger.log(
            internal.Trace.LEVEL,
            f"deleting player: {guild_id} in node: {self._session.name}",
        )

        player = await self.fetch_player(guild_id)

        await player.disconnect()

        self._session._players.pop(guild_id)

        _logger.log(
            internal.Trace.LEVEL,
            f"successfully deleted player: {guild_id} in node: {self._session.name}",
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
