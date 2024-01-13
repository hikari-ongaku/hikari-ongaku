from __future__ import annotations
import abc
import attrs
import asyncio
import logging
import aiohttp
import hikari
import typing as t
from .enums import ConnectionType
from .errors import SessionError
from .events import EventHandler
from .player import Player

if t.TYPE_CHECKING:
    from .ongaku import Ongaku

__all__ = ("Node",)

_logger = logging.getLogger("ongaku.node")


@attrs.define
class _NodeInternal:
    attempts: int
    remaining_attempts: int
    base_uri: str
    headers: dict[str, t.Any]
    session_id: str | None = None
    connection_status: ConnectionType = ConnectionType.LOADING
    connection_failure_reason: str = ""

    @classmethod
    def build(cls, uri: str, headers: dict[str, t.Any], attempts: int) -> _NodeInternal:
        return cls(attempts, attempts, uri, headers)


class Node(abc.ABC):
    """
    Node

    A base node item, for sharding the sets of players.

    Parameters
    ----------
    ongaku : Ongaku
        The ongaku object that it will always connect to.
    name : str
        The name of the node.
    """

    def __init__(self, ongaku: Ongaku, name: str) -> None:
        self._ongaku = ongaku
        self._name = name

        self._players: dict[hikari.Snowflake, Player] = {}

        self._internal = _NodeInternal.build(
            self.ongaku.internal.base_uri,
            self.ongaku.internal.headers,
            self.ongaku.internal.attempts,
        )

        self._event_handler = EventHandler(self)

    @property
    def ongaku(self) -> Ongaku:
        return self._ongaku

    @property
    def players(self) -> t.Sequence[Player]:
        return list(self._players.values())

    async def delete_player(self, guild_id: hikari.Snowflake) -> None:
        try:
            self._players.pop(guild_id)
        except Exception:
            raise

    async def connect(self):
        """
        This is an internal function, that handles the connection, and starting of the websocket.
        """

        if (
            self._internal.connection_status == ConnectionType.CONNECTED
            or self._internal.connection_status == ConnectionType.FAILURE
        ):
            return

        try:
            bot = self._ongaku.bot.get_me()
        except Exception:
            self._internal.remaining_attempts = -1
            self._internal.connection_status = ConnectionType.FAILURE
            self._internal.connection_failure_reason = "Bot ID could not be found."
            _logger.error("Ongaku could not start, due to the bot ID not being found.")
            return

        if bot is None:
            self._internal.remaining_attempts = -1
            self._internal.connection_status = ConnectionType.FAILURE
            self._internal.connection_failure_reason = "Bot ID could not be found."
            _logger.error("Ongaku could not start, due to the bot ID not being found.")
            return

        new_header = {
            "User-Id": str(bot.id),
            "Client-Name": f"{str(bot.id)}::Unknown",
        }

        new_header.update(self._internal.headers)

        while self._internal.remaining_attempts > 1:
            await asyncio.sleep(3)
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.ws_connect(
                        self._internal.base_uri + "/websocket", headers=new_header
                    ) as ws:
                        async for msg in ws:
                            if msg.type == aiohttp.WSMsgType.ERROR:
                                self._internal.connection_status = (
                                    ConnectionType.FAILURE
                                )
                                self._internal.connection_failure_reason = msg.data
                                raise SessionError(_logger.error(msg.json()))

                            if msg.type == aiohttp.WSMsgType.CLOSED:
                                pass
                            if msg.type == aiohttp.WSMsgType.TEXT:
                                try:
                                    json_data = msg.json()
                                except Exception:
                                    _logger.info("Failed to decode json data.")
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
        else:
            _logger.error(
                f"Maximum connection attempts reached. Reason: {self._internal.connection_failure_reason}"
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