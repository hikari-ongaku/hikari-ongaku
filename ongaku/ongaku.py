from . import player, error, enums, events
from . import rest
import typing as t
import aiohttp
import hikari
import logging


class OngakuInternal:
    def __init__(self, uri: str, max_retries: int = 3) -> None:
        self._headers: dict[t.Any, t.Any] = {}
        self._session_id: t.Optional[str] = None
        self._uri: str = uri
        self._total_retries = max_retries
        self._remaining_retries = max_retries
        self._connected = False

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
    def connected(self) -> bool:
        return self._connected

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

    def remove_attempt(self) -> int:
        return self._remaining_retries - 1


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
            The host, or IP that your lavalink server is running on. (default is 'localhost')
        port : int
            The port your lavalink server runs on. (default is 2333)
        password : str | None
            The password for your lavalink server. (default is None)
        version : models.VersionType
            The version of lavalink you are running. Currently only supports V3, or V4. (default is V4)
        max_retries : int
            The maximum amount of retries for the Websocket. (default is 3)
        """
        self._bot = bot

        self._players: dict[hikari.Snowflake, player.Player] = {}

        if password:
            self._internal.add_headers({"Authorization": password})

        self._rest = rest.RestApi(self)

        self._event_handler = events.EventHandler(self)

        self._internal = OngakuInternal(
            f"http://{host}:{port}/{version.value}", max_retries
        )

    @property
    def players(self) -> list[player.Player]:
        """
        players

        All the currently active players.
        """
        return list(self._players.values())

    @property
    def rest(self) -> rest.RestApi:
        return self._rest

    @property
    def bot(self) -> hikari.GatewayBot:
        """
        Gateway bot.

        The gateway bot the server is attached to.
        """
        return self._bot

    @property
    def connected(self) -> bool:
        """
        Connected to lavalink.

        Whether or not it is connected to lavalink's websocket.

        Returns
        -------
        A boolean. If true, it is connected to the server, if false, it is not.
        """
        return self._internal.connected

    @property
    def internal(self) -> OngakuInternal:
        """
        This is for internal related stuff. Do not touch this area.
        """
        return self._internal

    async def connect(self, user_id: hikari.Snowflake) -> None:
        async with aiohttp.ClientSession() as session:
            new_header = {
                "User-Id": str(user_id),
                "Client-Name": f"{str(user_id)}::Unknown",
            }

            new_header.update(self._internal.headers)
            try:
                async with session.ws_connect(
                    self._internal.uri + "/websocket", headers=new_header
                ) as ws:
                    async for msg in ws:
                        if msg.type == aiohttp.WSMsgType.ERROR:
                            logging.error(msg.json())

                        if msg.type == aiohttp.WSMsgType.CLOSED:
                            print("ws closed.")
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            try:
                                json_data = msg.json()
                            except:
                                logging.info("Failed to decode json data.")
                            else:
                                await self._event_handler.handle_payload(json_data)

                        elif msg.type == aiohttp.WSMsgType.ERROR:
                            break
            except Exception as e:
                raise error.LavalinkConnectionException(e)

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

        print("connections:", self.bot.voice.connections)
        connection = self.bot.voice.connections.get(guild_id)

        print("connection:", connection, type(connection))

        if isinstance(connection, player.Player):
            print("disconnecting...")
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
            raise error.PlayerMissingException(guild_id)

        return fetched_player

    async def delete_player(self, guild_id: hikari.Snowflake) -> None:
        print(self._players, guild_id)
        try:
            self._players.pop(guild_id)
        except Exception as e:
            print(e)
            raise e
