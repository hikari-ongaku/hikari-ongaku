from __future__ import annotations
import abc
import attrs
import asyncio
import logging
import aiohttp
import hikari
import typing as t
from .enums import ConnectionType
from .errors import SessionException, NodeException
from .events import EventHandler
from .player import Player

if t.TYPE_CHECKING:
    from .client import Client

__all__ = ("Node",)

INTERNAL_LOGGER = logging.getLogger(__name__)


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
    client : Client
        The Ongaku client that it will be connected too.
    name : str
        The name of the node. This can be anything.
    """

    def __init__(self, client: Client, name: str) -> None:
        self._client = client
        self._name = name

        self._players: dict[hikari.Snowflake, Player] = {}

        self._internal = _NodeInternal.build(
            self.client._internal.base_uri,
            self.client._internal.headers,
            self.client._internal.attempts,
        )

        self._event_handler = EventHandler(self)

    @property
    def name(self) -> str:
        """The name of the node."""
        return self._name

    @property
    def client(self) -> Client:
        """The [client][client.client] object that this node has attached to."""
        return self._client

    @property
    def players(self) -> t.Sequence[Player]:
        """The players, that are attached to this node."""
        return list(self._players.values())

    async def delete_player(self, guild_id: hikari.Snowflake) -> None:
        """
        Delete player

        Delete a specific player, via it's guild ID.

        Parameters
        ----------
        guild_id : hikari.Snowflake
            The guild ID that the player is for.

        Raises
        ------
        KeyError
            If the guild does not exist.
        """
        try:
            self._players.pop(guild_id)
        except KeyError:
            raise KeyError("The guild id's player was not found.")

    async def _connect(self):
        """
        This is an internal function, that handles the connection, and starting of the websocket.
        """

        if (
            self._internal.connection_status == ConnectionType.CONNECTED
            or self._internal.connection_status == ConnectionType.FAILURE
        ):
            raise NodeException(
                "This node has failed its connection attempts. Please check your lavalink connection."
            )

        try:
            bot = self._client.bot.get_me()
        except Exception:
            self._internal.remaining_attempts = -1
            self._internal.connection_status = ConnectionType.FAILURE
            self._internal.connection_failure_reason = "Bot ID could not be found."
            raise NodeException(
                "Ongaku could not start, due to the bot ID not being found."
            )

        if bot is None:
            self._internal.remaining_attempts = -1
            self._internal.connection_status = ConnectionType.FAILURE
            self._internal.connection_failure_reason = "Bot ID could not be found."
            raise NodeException(
                "Ongaku could not start, due to the bot ID not being found."
            )

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
                                raise SessionException(
                                    "An internal error has happened to this lavalink connection: "
                                    + msg.data
                                )

                            if msg.type == aiohttp.WSMsgType.CLOSED:
                                pass

                            if msg.type == aiohttp.WSMsgType.TEXT:
                                try:
                                    json_data = msg.json()
                                except Exception:
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
        else:
            raise NodeException(
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
