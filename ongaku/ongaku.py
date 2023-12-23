from . import models, events, player, error
from . import rest
import typing as t
import enum as e
import aiohttp
import hikari
import logging

from hikari.api import VoiceConnection


class Ongaku:
    def __init__(
        self,
        bot: hikari.GatewayBot,
        *,
        host: str = "localhost",
        port: int = 2333,
        password: str | None = None,
        version: models.VersionType = models.VersionType.V4,
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
        version: models.VersionType
            The version of lavalink you are running. Currently only supports V3, or V4. (default is V4)
        """
        self._bot = bot

        self._players: dict[hikari.Snowflake, player.Player] = {}

        self._default_uri = f"http://{host}:{port}/{version.value}"

        self._headers: dict[str, t.Any] = {}

        if password:
            self._headers.update({"Authorization": password})

        self._rest = rest.RestApi(self)

        self._connected = False
        self._session_id: t.Optional[str] = None

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
        return self._connected

    async def connect(self, user_id: hikari.Snowflake) -> None:
        async with aiohttp.ClientSession() as session:
            new_header = {
                "User-Id": str(user_id),
                "Client-Name": f"{str(user_id)}::Unknown",
            }

            new_header.update(self._headers)
            try:
                async with session.ws_connect(
                    self._default_uri + "/websocket", headers=new_header
                ) as ws:
                    async for msg in ws:
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            try:
                                json_data = msg.json()
                            except:
                                logging.info("Failed to decode json data.")
                            else:
                                op_code = json_data["op"]
                                logging.info("received op code: " + op_code)
                                if op_code == "ready":
                                    self._connected = True
                                    try:
                                        ready = models.Ready(json_data)
                                    except Exception as e:
                                        logging.error(
                                            "Failed to convert a ready statement. Error:"
                                            + str(e)
                                        )
                                    else:
                                        ready_event = events.ReadyEvent(
                                            self._bot, ready
                                        )

                                        await self._bot.dispatch(ready_event)

                                        self._session_id = ready.session_id
                                elif op_code == "stats":
                                    try:
                                        stats = models.Statistics(json_data)
                                    except Exception as e:
                                        logging.error(
                                            "Failed to convert a statistics statement. Error:"
                                            + str(e)
                                        )
                                    else:
                                        ready_event = events.StatisticsEvent(
                                            self._bot, stats
                                        )

                                        await self._bot.dispatch(ready_event)
                                elif op_code == "event":
                                    event_type = json_data["type"]

                                    if event_type == "TrackStartEvent":
                                        try:
                                            track_start = models.TrackStart(json_data)
                                        except Exception as e:
                                            logging.error(
                                                "Failed to convert a event track start. Error:"
                                                + str(e)
                                            )
                                        else:
                                            track_start_event = events.TrackStartEvent(
                                                self._bot,
                                                track_start,
                                                json_data["guildId"],
                                            )

                                            await self._bot.dispatch(track_start_event)

                                    if event_type == "TrackEndEvent":
                                        try:
                                            track_end = models.TrackEnd(json_data)
                                        except Exception as e:
                                            logging.error(
                                                "Failed to convert a event track start. Error:"
                                                + str(e)
                                            )
                                        else:
                                            track_end_event = events.TrackEndEvent(
                                                self._bot,
                                                track_end,
                                                json_data["guildId"],
                                            )

                                            await self._bot.dispatch(track_end_event)

                                    if event_type == "TrackExceptionEvent":
                                        try:
                                            track_exception = models.TrackException(
                                                json_data
                                            )
                                        except Exception as e:
                                            logging.error(
                                                "Failed to convert a event track start. Error:"
                                                + str(e)
                                            )
                                        else:
                                            track_exception_event = (
                                                events.TrackExceptionEvent(
                                                    self._bot,
                                                    track_exception,
                                                    json_data["guildId"],
                                                )
                                            )

                                            await self._bot.dispatch(
                                                track_exception_event
                                            )

                                    if event_type == "TrackStuckEvent":
                                        try:
                                            track_stuck = models.TrackStuck(json_data)
                                        except Exception as e:
                                            logging.error(
                                                "Failed to convert a event track start. Error:"
                                                + str(e)
                                            )
                                        else:
                                            track_stuck_event = events.TrackStuckEvent(
                                                self._bot,
                                                track_stuck,
                                                json_data["guildId"],
                                            )

                                            await self._bot.dispatch(track_stuck_event)

                                    if event_type == "WebSocketClosedEvent":
                                        try:
                                            websocket_closed = models.WebsocketClosed(
                                                json_data
                                            )
                                        except Exception as e:
                                            logging.error(
                                                "Failed to convert a event track start. Error:"
                                                + str(e)
                                            )
                                        else:
                                            websocket_closed_event = (
                                                events.WebsocketClosedEvent(
                                                    self._bot,
                                                    websocket_closed,
                                                    json_data["guildId"],
                                                )
                                            )
                                            await self.delete_player(
                                                int(json_data["guildId"])
                                            )
                                            await self._bot.dispatch(
                                                websocket_closed_event
                                            )

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
