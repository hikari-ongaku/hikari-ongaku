from __future__ import annotations

import asyncio
import logging
import typing as t

import aiohttp
import hikari

from .abc.lavalink import RestError
from .enums import ConnectionType, VersionType
from .errors import (
    PlayerMissingException,
    RequiredException,
    SessionError,
)
from .events import EventHandler, WebsocketClosedEvent
from .player import Player
from .rest import RestApi

_logger = logging.getLogger("ongaku")

__all__ = ("Ongaku",)


class _OngakuInternal:
    def __init__(self, uri: str, max_retries: int = 3) -> None:
        """
        asdf
        """
        self._headers: dict[t.Any, t.Any] = {}
        self._session_id: t.Optional[str] = None
        self._uri: str = uri
        self._total_retries = max_retries
        self._remaining_retries = max_retries
        self._connected = ConnectionType.LOADING
        self._failure_reason = None

    @property
    def headers(self) -> dict[t.Any, t.Any]:
        return self._headers

    @property
    def uri(self) -> str:
        return self._uri

    @property
    def session_id(self) -> t.Optional[str]:
        return self._session_id

    @property
    def total_retries(self) -> int:
        return self._total_retries

    @property
    def remaining_retries(self) -> int:
        return self._remaining_retries

    @property
    def connected(self) -> ConnectionType:
        return self._connected

    @property
    def connection_failure(self) -> t.Optional[str]:
        return self._failure_reason

    def set_connection(
        self, connected: ConnectionType, *, reason: t.Optional[str] = None
    ) -> None:
        self._connected = connected
        if reason is not None:
            self._failure_reason = reason

    def set_session_id(self, session_id: str) -> None:
        self._session_id = session_id

    def add_headers(self, headers: dict[t.Any, t.Any]) -> None:
        self._headers.update(headers)

    def remove_headers(self, headers: t.Any) -> None:
        try:
            self._headers.pop(headers)
        except Exception as e:
            raise e

    def clear_headers(self) -> None:
        self._headers.clear()

    def remove_retry(self, set: int = 1) -> int:
        if set == -1:
            self._remaining_retries = 0
            _logger.warning("All lavalink attempts used!")
            return self._remaining_retries
        if self._remaining_retries == 0 or self._remaining_retries < set:
            raise ValueError("Already Zero.")
        self._remaining_retries -= set
        _logger.warning(
            f"Lavalink connection attempts used: {set} remaining: {self._remaining_retries}"
        )
        return self._remaining_retries

    async def check_error(self, payload: dict[str, t.Any]) -> t.Optional[RestError]:
        try:
            error = RestError._from_payload(payload)
        except Exception:
            raise

        return error


class Ongaku:
    def __init__(
        self,
        bot: hikari.GatewayBot,
        *,
        host: str = "localhost",
        port: int = 2333,
        password: str | None = None,
        version: VersionType = VersionType.V4,
        max_retries: int = 3,
    ) -> None:
        """
        Base Ongaku class

        The base Ongaku class, where everything starts from.

        Parameters
        ----------
        bot : hikari.GatewayBot
            The bot that ongaku will attach to.
        host : str
            The host, or IP that your lavalink server is running on.
        port : int
            The port your lavalink server runs on.
        password : str | None
            The password for your lavalink server.
        version : models.VersionType
            The version of lavalink you are running. Currently only supports V3, or V4.
        max_retries : int
            The maximum amount of retries for the Websocket.
        """
        self._bot = bot

        self._players: dict[hikari.Snowflake, Player] = {}

        self._internal = _OngakuInternal(
            f"http://{host}:{port}/{version.value}", max_retries
        )

        if password:
            self._internal.add_headers({"Authorization": password})

        self._rest = RestApi(self)

        self._event_handler = EventHandler(self)

        bot.subscribe(hikari.StartedEvent, self._handle_connect)
        bot.subscribe(WebsocketClosedEvent, self._handle_disconnect)

    @property
    def players(self) -> t.Sequence[Player]:
        """
        players

        All the currently active players.

        Returns
        -------
        list[Player]
            A list of players
        """
        return list(self._players.values())

    @property
    def rest(self) -> RestApi:
        """
        Rest

        The REST API for the Lavalink server.

        Returns
        -------
        rest.RestApi
            The rest api for lavalink
        """
        return self._rest

    @property
    def bot(self) -> hikari.GatewayBot:
        """
        Gateway bot.

        The gateway bot the server is attached to.

        Returns:
        hikari.RESTAware
            A Rest aware hikari bot.
        """
        return self._bot

    @property
    def connection_type(self) -> ConnectionType:
        """
        Connected to lavalink.

        Whether or not it is connected to lavalink's websocket.

        Returns
        -------
        enums.ConnectionStatus.LOADING
            Ongaku has not yet attempted to connect to the lavalink server.
        enums.ConnectionStatus.CONNECTED
            Ongaku has successfully connected to the lavalink server.
        enums.ConnectionStatus.FAILURE
            Ongaku has failed to connect to the lavalink server. Check connection_failure_reason for more information.


        """
        return self._internal.connected

    @property
    def connection_failure_reason(self) -> t.Optional[str]:
        return self._internal.connection_failure

    @property
    def internal(self) -> _OngakuInternal:
        """
        For internal information about the bot.

        Returns
        -------
        OngakuInternal
            An internal class for ongaku.
        """
        return self._internal

    async def create_player(
        self,
        guild_id: hikari.Snowflake,
        channel_id: hikari.Snowflake,
    ) -> Player:
        """
        Create a new player

        Creates a new player for the specified guild, and places it in the specified channel.

        Parameters
        ----------
        guild_id : hikari.Snowflake
            The guild id that the bot is in
        channel_id : hikari.Snowflake
            The channel id that the bot will join too.

        Raises
        ------
        PlayerCreateException
            Raised when the player failed to be created.

        Returns
        -------
        Player
            The player that is now in the channel you have specified.
        """
        # FIXME: Fix the issue where, if the bot is invited to the channel via this, then kicked by a user, allow the bot to join back without a "already in guild" error

        bot = self.bot.get_me()

        if bot is None:
            raise RequiredException("The bot is required to be able to connect.")

        bot_state = self.bot.cache.get_voice_state(guild_id, bot.id)

        if bot_state is not None and bot_state.channel_id is not None:
            await self.bot.voice.disconnect(guild_id)
            try:
                self._players.pop(guild_id)
            except Exception:
                pass

        new_player = Player(self.bot, self, guild_id)

        try:
            await new_player.connect(channel_id)
        except Exception:
            raise

        self._players.update({guild_id: new_player})
        return new_player

    async def fetch_player(self, guild_id: hikari.Snowflake) -> Player:
        """
        Fetch a player

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
        fetched_player = self._players.get(guild_id)

        if fetched_player is None:
            raise PlayerMissingException(guild_id)

        return fetched_player

    async def delete_player(self, guild_id: hikari.Snowflake) -> None:
        """
        delete a player

        Deletes a player from the specified guild, and disconnect it if it has not been disconnected already.

        Parameters
        ----------
        guild_id : hikari.Snowflake
            The guild id that the player belongs to.

        Raises
        ------
        PlayerMissingException
            The player was not found for the guild specified.
        """

        try:
            player = self._players.pop(guild_id)
        except Exception as e:
            raise PlayerMissingException(e)

        await player.disconnect()

    async def _handle_connect(self, event: hikari.StartedEvent):
        """
        This is an internal function, that handles the connection, and starting of the websocket.
        """

        if (
            self._internal.connected == ConnectionType.CONNECTED
            or self._internal.connected == ConnectionType.FAILURE
        ):
            return

        try:
            bot = self.bot.get_me()
        except Exception:
            self._internal.remove_retry(-1)
            self._internal.set_connection(
                ConnectionType.FAILURE, reason="Bot ID could not be found."
            )
            _logger.error("Ongaku could not start, due to the bot ID not being found.")
            return

        if bot is None:
            self._internal.remove_retry(-1)
            self._internal.set_connection(
                ConnectionType.FAILURE, reason="Bot ID could not be found."
            )
            _logger.error("Ongaku could not start, due to the bot ID not being found.")
            return

        new_header = {
            "User-Id": str(bot.id),
            "Client-Name": f"{str(bot.id)}::Unknown",
        }

        new_header.update(self._internal.headers)

        while self._internal.remaining_retries > 1:
            await asyncio.sleep(3)
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.ws_connect(
                        self._internal.uri + "/websocket", headers=new_header
                    ) as ws:
                        async for msg in ws:
                            if msg.type == aiohttp.WSMsgType.ERROR:
                                self._internal.set_connection(
                                    ConnectionType.FAILURE,
                                    reason=msg.data,
                                )
                                raise SessionError(_logger.error(msg.json()))

                            if msg.type == aiohttp.WSMsgType.CLOSED:
                                pass
                            if msg.type == aiohttp.WSMsgType.TEXT:
                                try:
                                    json_data = msg.json()
                                except Exception:
                                    _logger.info("Failed to decode json data.")
                                else:
                                    self._internal.set_connection(
                                        ConnectionType.CONNECTED
                                    )
                                    await self._event_handler.handle_payload(json_data)

                except Exception as e:
                    self._internal.set_connection(
                        ConnectionType.FAILURE, reason=f"Exception Raised: {e}"
                    )
                    self._internal.remove_retry(1)
        else:
            _logger.error(
                f"Maximum connection attempts reached. Reason: {self._internal.connection_failure}"
            )

    async def _handle_disconnect(self, event: WebsocketClosedEvent):
        """
        This is an internal function, that handles the disconnection of a websocket (Discord)
        """
        player = self._players[hikari.Snowflake(event.guild_id)]

        if event.code == 4014:
            await player.disconnect()

        if event.code == 4006:
            if player.channel_id is None:
                return
            await player.disconnect()
            self._players.pop(hikari.Snowflake(event.guild_id))
            await self.create_player(
                hikari.Snowflake(player.guild_id), hikari.Snowflake(player.channel_id)
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
