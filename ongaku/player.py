import hikari
from hikari.api import VoiceConnection, VoiceComponent
import typing as t

from . import models

class Player(VoiceConnection):
    def __init__(self, link, guild_id: int, channel_id) -> None:
        from .ongaku import Ongaku # this is probably a bad thing to do.
        self._bot: hikari.GatewayBot = link._bot
        self._link: Ongaku = link
        self._guild_id = guild_id
        self._channel_id = channel_id

        self._queue: list[models.Track] = []

        self._connection: t.Optional[Player] = None
    

    async def initialize(self):
        

        return await self._bot.voice.connect_to(
            self._guild_id,
            self._channel_id,
            voice_connection_type=Player
        )




    async def play(self, track: models.Track, author_id: int) -> None:
        """
        Plays a track on the designated player. If a queue exists, it will push the currently playing song back, and play this song first.
        """

        self._queue.insert(0, track)

        await self._link.rest.load_track(track, self.guild_id)

    async def add(self, track: models.Track | list[models.Track]) -> None:
        """
        Adds song(s) to the queue.
        """
        if isinstance(track, models.Track):
            self._queue.append(track)
        
        else:
            self._queue.extend(track)

    @property
    def channel_id(self) -> hikari.Snowflake:
        """Return the ID of the voice channel this voice connection is in."""
        return self.channel_id

    @property
    def guild_id(self) -> hikari.Snowflake:
        """Return the ID of the guild this voice connection is in."""
        return self.guild_id

    @property
    def is_alive(self) -> bool:
        """Return `builtins.True` if the connection is alive."""
        return self.is_alive

    @property
    def shard_id(self) -> int:
        """Return the ID of the shard that requested the connection."""
        return self.shard_id

    @property
    def owner(self) -> VoiceComponent:
        """Return the component that is managing this connection."""
        return self.owner

    async def disconnect(self) -> None:
        """Signal the process to shut down."""
        self._is_alive = False

    async def leave(self) -> None:
        """Does the same thing as disconnect"""
        await self.disconnect()

    async def join(self) -> None:
        """Wait for the process to halt before continuing."""

    async def notify(self, event: hikari.VoiceEvent) -> None:
        """Submit an event to the voice connection to be processed."""