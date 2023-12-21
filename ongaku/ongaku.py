from . import error, models, events, player
from . import rest_api
import typing as t
import enum as e
import aiohttp
import hikari
import logging


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
        self._standard_uri = f"http://{host}:{port}/{version.value}"

        self._headers: dict[str, t.Any] = {}

        if password:
            self._headers.update({"Authorization": password})

        self._bot = bot

        self._players: dict[int, player.Player] = {}

        self.rest = rest_api.Rest(self)

        self._session_id: str | None = None

    async def connect(self, user_id: int) -> None:
        """
        Connects up the websocket to the lavalink server.
        """
        self._user_id = user_id

        async with aiohttp.ClientSession() as session:
            new_header = {
                "User-Id": str(user_id),
                "Client-Name": f"{str(user_id)}::Unknown",
            }

            new_header.update(self._headers)

            async with session.ws_connect(
                self._standard_uri + "/websocket", headers=new_header
            ) as ws:
                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        try:
                            json_data: dict = msg.json()
                        except:
                            logging.info("Failed to decode json data.")
                        else:
                            try:
                                op_code = json_data["op"]
                            except:
                                raise error.LavalinkException(models.Error(json_data))

                            if op_code == "ready":
                                try:
                                    ready = models.Ready(json_data)
                                except Exception as e:
                                    logging.error(
                                        "Failed to convert a ready statement. Error:"
                                        + str(e)
                                    )
                                else:
                                    ready_event = events.ReadyEvent(self._bot, ready)

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
                                            json_data["guild_id"],
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
                                            self._bot, track_end, json_data["guild_id"]
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
                                                json_data["guild_id"],
                                            )
                                        )

                                        await self._bot.dispatch(track_exception_event)

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
                                            json_data["guild_id"],
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
                                        logging.info("Disconnected...")

                                        websocket_closed_event = (
                                            events.WebsocketClosedEvent(
                                                self._bot,
                                                websocket_closed,
                                                json_data["guild_id"],
                                            )
                                        )

                                        await self._bot.dispatch(websocket_closed_event)

                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        break

    async def create_player(self, guild_id: hikari.Snowflake, channel_id: hikari.Snowflake) -> player.Player:
        music = player.Player(self._bot, guild_id, channel_id)

        self._players.update({guild_id: music})

        return music

    async def fetch_player(self, guild_id: int) -> player.Player:
        return self._players[guild_id]

    async def delete_player(self, guild_id: int) -> None:
        self._players.pop(guild_id)

    async def connect_player(self, guild_id: int) -> None:
        """
        Connects a player, so it can play audio.
        """
        try:
            player = self._players[guild_id]
        except:
            pass
