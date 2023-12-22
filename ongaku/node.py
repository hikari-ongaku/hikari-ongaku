import hikari
from . import models, player
import typing as t

class Node:
    """
    A node for your bot. (use one per shard.)
    """
    def __init__(
        self,
        bot: hikari.GatewayBotAware,
        *,
        host: str = "localhost",
        port: int = 2333,
        password: str | None = None,
        version: models.VersionType = models.VersionType.V4,
    ) -> None:
        self._bot = bot

        self._default_uri = f"http://{host}:{port}/{version.value}"

        self._headers: dict[str, t.Any] = {}

        if password:
            self._headers.update({"Authorization": password})

        self._players: list[player.Player] = []