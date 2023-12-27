from . import errors, player, enums, events, abc
from . import rest
import typing as t
import aiohttp
import hikari
import logging
import asyncio

_logger = logging.getLogger("ongaku") # Internal logger.

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
        self._connected = enums.ConnectionStatus.LOADING
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
    def connected(self) -> enums.ConnectionStatus:
        return self._connected
    
    @property
    def connection_failure(self) -> t.Optional[str]:
        return self._failure_reason

    def set_connection(self, connected: enums.ConnectionStatus, *, reason: t.Optional[str] = None) -> None:
        self._connected = connected
        if reason != None:
            print(reason)
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
        _logger.warning(f"Lavalink connection attempts used: {set} remaining: {self._remaining_retries}")
        return self._remaining_retries
        
    async def check_error(self, payload: dict[t.Any, t.Any]) -> t.Optional[abc.Error]:
        try:
            error = abc.Error.as_payload(payload)
        except:
            return
        
        return error

class Ongaku:
    def __init__(
        self,
        bot: hikari.GatewayBot,
        *,
        host: str = "localhost",
        port: int = 2333,
        password: str | None = None,
        version: enums.VersionType = enums.VersionType.V4,
        max_retries: int = 3,
    ) -> None:
        """
        Base Ongaku class

        The base Ongaku class, where everything starts from.

        Parameters
        ----------
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

        self._players: dict[hikari.Snowflake, player.Player] = {}

        self._internal = _OngakuInternal(
            f"http://{host}:{port}/{version.value}", max_retries
        )

        if password:
            self._internal.add_headers({"Authorization": password})

        self._rest = rest.RestApi(self)

        self._event_handler = events.EventHandler(self)

        bot.subscribe(hikari.StartedEvent, self._handle_connect)

    @property
    def players(self) -> list[player.Player]:
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
    def rest(self) -> rest.RestApi:
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
    def connection_status(self) -> enums.ConnectionStatus:
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
    ) -> player.Player:
        """
        Creates a new node.

        Creates a new node for players to attach to.

        Parameters
        ----------
        bot : hikari.GatewayBot
            The bot that you are currently running.
        shard_id : int
            The current shard id.
        user_id : hikari.Snowflake
            The bots user id.
        """

        connection = self.bot.voice.connections.get(guild_id)

        if isinstance(connection, player.Player):
            await self.bot.voice.disconnect(guild_id)

        new_player = await self.bot.voice.connect_to(
            guild_id, channel_id, player.Player, bot=self.bot, ongaku=self
        )

        self._players.update({guild_id: new_player})
        print(self._players)
        return new_player

    async def fetch_player(self, guild_id: hikari.Snowflake) -> player.Player:
        fetched_player = self._players.get(guild_id)

        if fetched_player == None:
            raise errors.PlayerMissingException(guild_id)

        return fetched_player

    async def delete_player(self, guild_id: hikari.Snowflake) -> None:
        print(self._players, guild_id)
        try:
            self._players.pop(guild_id)
        except Exception as e:
            print(e)
            raise e
        
    async def _handle_connect(self, event: hikari.StartedEvent):
        if self._internal.connected == enums.ConnectionStatus.CONNECTED or self._internal.connected == enums.ConnectionStatus.FAILURE:
            return
        
        try:
            bot = self.bot.get_me()
        except:
            self._internal.remove_retry(-1)
            self._internal.set_connection(enums.ConnectionStatus.FAILURE, reason="Bot ID could not be found.")
            _logger.error("Ongaku could not start, due to the bot ID not being found.")
            return
        
        if bot == None:
            self._internal.remove_retry(-1)
            self._internal.set_connection(enums.ConnectionStatus.FAILURE, reason="Bot ID could not be found.")
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
                    async with session.ws_connect( #type: ignore
                        self._internal.uri + "/websocket", headers=new_header
                    ) as ws:
                        async for msg in ws:
                            if msg.type == aiohttp.WSMsgType.ERROR: #type: ignore
                                _logger.error(msg.json())

                            if msg.type == aiohttp.WSMsgType.CLOSED: #type: ignore
                                print("ws closed.")
                            if msg.type == aiohttp.WSMsgType.TEXT: #type: ignore
                                try:
                                    json_data = msg.json()
                                except:
                                    _logger.info("Failed to decode json data.")
                                else:
                                    #error = await self._internal.check_error(json_data)

                                    #if error:
                                    #    self._internal.remove_retry()
                                    #    self._internal.set_connection(enums.ConnectionStatus.FAILURE, reason=error.message)
                                    #    return 
                                    
                                    self._internal.set_connection(enums.ConnectionStatus.CONNECTED)
                                    await self._event_handler.handle_payload(json_data)

                            elif msg.type == aiohttp.WSMsgType.ERROR: #type: ignore
                                self._internal.set_connection(enums.ConnectionStatus.FAILURE, reason=msg.data)
                except Exception as e:
                    self._internal.set_connection(enums.ConnectionStatus.FAILURE, reason=f"Exception Raised: {e}")
                    self._internal.remove_retry(1)
        else:
            _logger.error(f"Maximum connection attempts reached. Reason: {self._internal.connection_failure}")
