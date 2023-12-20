import hikari, lightbulb
from hikari.api import VoiceConnection, VoiceComponent
import typing as t

from . import models

class Player(VoiceConnection):
    """
    The voice connection to the discord bot.
    """
    @classmethod
    async def initialize(
        cls,
        bot: hikari.GatewayBot,
        channel_id: int,
        guild_id: int,
        end_point: str,
        session_id: str,
        user_id: int
    ):
        """
        Initialize the voice connection.
        """
        cls._bot = bot
        cls._channel_id = channel_id
        cls._guild_id = guild_id
        cls._end_point = end_point
        cls._session_id = session_id
        cls._user_id = user_id
        cls._is_alive = True

        return await bot.voice.connect_to(
            guild_id,
            channel_id,
            cls
        )

    @property
    def guild_id(self) -> int:
        return self._guild_id
    
    @property
    def channel_id(self) -> int:
        return self._channel_id
    
    @property
    def is_alive(self) -> bool:
        return self._is_alive
    
    @property
    def shard_id(self) -> int:
        return 0
    
    @property
    def owner(self) -> int:
        return 0
    
    @classmethod
    async def join(cls):
        return
    
    @classmethod
    async def disconnect(cls):
        return
    
    @classmethod
    async def notify(cls, event: hikari.Event):
        return