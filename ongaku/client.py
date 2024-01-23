"""Ongaku Client.

Ongaku base client where everything is started from.
"""

from __future__ import annotations

import logging
import typing as t

import attrs
import hikari

from .enums import VersionType
from .errors import NodeException
from .errors import PlayerMissingException
from .errors import RequiredException
from .node import Node
from .player import Player
from .rest import RESTClient

INTERNAL_LOGGER = logging.getLogger(__name__)

__all__ = ("Client",)


@attrs.define
class _ClientInternal:
    headers: dict[str, t.Any]
    base_uri: str
    attempts: int


class Client:
    """Base Ongaku class.

    The base Ongaku class, where everything starts from.

    !!! WARNING
        Do not change `max_retries` unless you know what you are doing. If your websocket does not stay connected/doesn't connect on the first try, do not use this as a fix.

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
    auto_nodes : bool
        Whether or not auto nodes are enabled.
    """

    def __init__(
        self,
        bot: hikari.GatewayBot,
        *,
        host: str = "localhost",
        port: int = 2333,
        password: str | None = None,
        version: VersionType = VersionType.V4,
        max_retries: int = 3,
        auto_nodes: bool = True,
    ) -> None:
        self._bot = bot

        self._players: dict[hikari.Snowflake, Player] = {}

        headers: dict[str, t.Any] = {}

        if password:
            headers.update({"Authorization": password})

        self._internal = _ClientInternal(
            headers, f"http://{host}:{port}/{version.value}", max_retries
        )

        self._rest = RESTClient(self)

        self._nodes: dict[int | str, Node] = {}

        if auto_nodes:
            bot.subscribe(hikari.ShardEvent, self._handle_nodes)
        bot.subscribe(hikari.StoppingEvent, self._handle_shutdown)

    @property
    def nodes(self) -> t.Sequence[Node]:
        """The nodes, that are attached to this lavalink server."""
        return list(self._nodes.values())

    @property
    def rest(self) -> RESTClient:
        """The REST access. For the lavalink server."""
        return self._rest

    @property
    def bot(self) -> hikari.GatewayBot:
        """The App or Bot that lavalink is connected too."""
        return self._bot

    async def create_player(self, guild_id: hikari.Snowflake) -> Player:
        """Create a new player.

        Creates a new player for the specified guild, and places it in the specified channel. It will attach itself to the correct node as well.

        Parameters
        ----------
        guild_id : hikari.Snowflake
            The Guild ID the player will be in.

        Raises
        ------
        PlayerException : Raised when the player failed to be created.
        NodeException : The node tht the bot needs to connect too, has not been created.

        Returns
        -------
        Player : The player that has been successfully created
        """
        shard_id = hikari.snowflakes.calculate_shard_id(self.bot, guild_id)

        bot = self.bot.get_me()

        if bot is None:
            raise RequiredException("The bot is required to be able to connect.")

        bot_state = self.bot.cache.get_voice_state(guild_id, bot.id)

        if bot_state is not None and bot_state.channel_id is not None:
            try:
                self._players.pop(guild_id)
            except KeyError:
                raise NodeException(
                    "The node this player needs to attach too, has not yet been created."
                )

        node = self._nodes.get(shard_id)

        if not node:
            raise NodeException("Node does not exist.")

        new_player = Player(node, guild_id)

        self._players.update({guild_id: new_player})
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
        for player in self.walk_players():
            if player.guild_id == guild_id:
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
        player = await self.fetch_player(guild_id)

        await player.disconnect()

        player.node._players.pop(guild_id)

    def walk_players(self) -> t.Iterator[Player]:
        """Walk players.

        Walk through all players, on all the currently working nodes.

        Returns
        -------
        typing.Iterator[Player]
            the players from all of the nodes.
        """
        for node in self._nodes.values():
            for player in node.players:
                yield player

    async def create_node(self, name: str) -> Node:
        """Create a node.

        Create a new node for the server.

        Parameters
        ----------
        name : str
            The name you wish to attach to the node.

        Raises
        ------
        ValueError
            When that name already exists as a node.

        Returns
        -------
        Node
            The new node that has been created.
        """
        if self._nodes.get(name) is not None:
            raise ValueError("Sorry, but this name already exists.")

        new_node = Node(self, name)

        try:
            await new_node._connect()
        except:
            raise

        self._nodes.update({name: new_node})

        return new_node

    async def fetch_node(self, name: str) -> Node:
        """Fetch a node.

        Fetch a specific node by its name.

        Parameters
        ----------
        name : str
            The name of the node.

        Raises
        ------
        ValueError
            When the node does not exist.

        Returns
        -------
        Node
            The node that has been found.
        """
        node = self._nodes.get(name)

        if node:
            return node

        raise ValueError("That node does not exist.")

    async def delete_node(self, name: str) -> None:
        """Delete a node.

        Delete a specific node by its name.

        Parameters
        ----------
        name : str
            The name of the node.

        Raises
        ------
        ValueError
            When the node does not exist.
        """
        node = self._nodes.get(name)

        if node:
            for player in node.players:
                await player.disconnect()

            await node._disconnect()

        raise ValueError("That node does not exist.")

    async def _handle_nodes(self, event: hikari.ShardEvent) -> None:
        if isinstance(event, hikari.events.ShardReadyEvent):
            new_node = Node(self, str(event.shard.id))

            self._nodes.update({event.shard.id: new_node})

            try:
                await new_node._connect()
            except Exception:
                raise

    async def _handle_shutdown(self, event: hikari.StoppingEvent):
        INTERNAL_LOGGER.info("Shutting down players...")
        for player in self.walk_players():
            await player.disconnect()

        INTERNAL_LOGGER.info("Shutdown complete.")


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
