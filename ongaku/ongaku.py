from . import error, models, events, node, player
from . import rest
import typing as t
import enum as e
import aiohttp
import hikari
import logging


class Ongaku:
    def __init__(
        self,
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
        self._nodes: t.Dict[hikari.Snowflake | int, node.Node] = {}
        
        self._default_uri = f"http://{host}:{port}/{version.value}"

        self._headers: dict[str, t.Any] = {}

        if password:
            self._headers.update({"Authorization": password})

        self._rest = rest.RestApi(self)

    @property
    def nodes(self) -> list[node.Node]:
        """
        Nodes

        A property of all nodes.
        """
        return list(self._nodes.values())

    @property
    def rest(self) -> rest.RestApi:
        return self._rest

    async def create_node(
        self,
        bot: hikari.GatewayBot,
        shard_id: int,
        user_id: hikari.Snowflake,
    ) -> node.Node:
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
        new_node = node.Node(
            bot=bot,
            shard_id=shard_id,
            user_id=user_id,
            uri=self._default_uri,
            headers=self._headers,
            rest=self.rest,
        )

        try:
            await new_node.start()
        except Exception as e:
            raise e

        self._nodes.update({shard_id: new_node})

        return new_node

    async def fetch_node(self, shard_id: hikari.Snowflake) -> node.Node:
        try:
            return_node = self._nodes[shard_id]
        except Exception as e:
            raise error.NodeMissingException(e)

        return return_node

    async def delete_node(self, shard_id: hikari.Snowflake) -> None:
        try:
            self._nodes.pop(shard_id)
        except Exception as e:
            error.NodeMissingException(e)

    async def fetch_player(self, guild_id: hikari.Snowflake) -> player.Player:
        for node in self.nodes:
            print(node.players)
            try:
                node_player = node._players.get(guild_id)
            except:
                continue

            if node_player == None:
                continue
            
            return node_player
        else:
            raise error.PlayerMissingException()
