from __future__ import annotations

import typing as t
import hikari
import asyncio
import aiohttp
import logging

_logger = logging.getLogger("ongaku.node")

from .abc import WebsocketClosedEvent, RestError
from .enums import ConnectionType
from .events import EventHandler

if t.TYPE_CHECKING:
    from .ongaku import Ongaku

    OngakuT = t.TypeVar("OngakuT", bound="Ongaku")

class _NodeInternal:
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
        _logger.warning(
            f"Lavalink connection attempts used: {set} remaining: {self._remaining_retries}"
        )
        return self._remaining_retries

    async def check_error(self, payload: dict[t.Any, t.Any]) -> t.Optional[RestError]:
        try:
            error = RestError.as_payload(payload)
        except:
            return

        return error


class Node:
    def __init__(self, ongaku: Ongaku, name: str, retries: int = 3) -> None:
        """
        Base Node class.

        This is a node, that will attach itself to players, and a shard.

        Parameters
        ----------
        ongaku : Ongaku
            The base Ongaku object you have created.
        name : str
            The name you wish to assign to the node.
        retries : int
            The amount of retries the node can attempt, before raising an error.
        """

        self._ongaku = ongaku
        self._name = name
        self._session_id: str | None = None
        self._internal = _NodeInternal(self._ongaku.internal.uri, retries)

        self._event_handler = EventHandler(self)

        self._ongaku.bot.subscribe(WebsocketClosedEvent, self._handle_disconnect)

    async def build(self):
        """
        Build the node

        Build the node you just created.


        """
        if (
            self._internal.connected == ConnectionType.CONNECTED
            or self._internal.connected == ConnectionType.FAILURE
        ):
            return

        try:
            bot = self._ongaku.bot.get_me()
        except:
            self._internal.remove_retry(-1)
            self._internal.set_connection(
                ConnectionType.FAILURE, reason="Bot ID could not be found."
            )
            _logger.error("Ongaku could not start, due to the bot ID not being found.")
            return

        if bot == None:
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
                    async with session.ws_connect(  # type: ignore
                        self._internal.uri + "/websocket", headers=new_header
                    ) as ws:
                        async for msg in ws:
                            if msg.type == aiohttp.WSMsgType.ERROR:  # type: ignore
                                _logger.error(msg.json())

                            if msg.type == aiohttp.WSMsgType.CLOSED:  # type: ignore
                                print("ws closed.")
                            if msg.type == aiohttp.WSMsgType.TEXT:  # type: ignore
                                try:
                                    json_data = msg.json()
                                except:
                                    _logger.info("Failed to decode json data.")
                                else:
                                    # error = await self._internal.check_error(json_data)

                                    # if error:
                                    #    self._internal.remove_retry()
                                    #    self._internal.set_connection(enums.ConnectionStatus.FAILURE, reason=error.message)
                                    #    return

                                    self._internal.set_connection(
                                        ConnectionType.CONNECTED
                                    )
                                    await self._event_handler.handle_payload(json_data)

                            elif msg.type == aiohttp.WSMsgType.ERROR:  # type: ignore
                                self._internal.set_connection(
                                    ConnectionType.FAILURE, reason=msg.data
                                )
                except Exception as e:
                    self._internal.set_connection(
                        ConnectionType.FAILURE, reason=f"Exception Raised: {e}"
                    )
                    self._internal.remove_retry(1)
        else:
            _logger.error(
                f"Maximum connection attempts reached for node {self._name}. Reason: {self._internal.connection_failure}"
            )

    

    async def _handle_disconnect(self, event: WebsocketClosedEvent):
        player = self._ongaku.players[hikari.Snowflake(event.guild_id)]

        if event.code == 4014:
            await player.disconnect()

        if event.code == 4006:
            await player.disconnect()
            await self._ongaku.create_player(player.guild_id, player.channel_id)
