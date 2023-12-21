import hikari
from hikari.api import VoiceConnection, VoiceComponent
import typing as t

from . import models, error

class CustPlayer(VoiceConnection):

    @classmethod
    async def initialize(
        cls,
        channel_id: hikari.Snowflake,
        endpoint: str,
        guild_id: hikari.Snowflake,
        on_close,
        owner: VoiceComponent,
        session_id: str,
        shard_id: int,
        token: str,
        user_id: hikari.Snowflake,
        *,
        bot: hikari.GatewayBot,
        ongaku,
    ):
        from .ongaku import Ongaku
        cls._channel_id = channel_id
        cls._endpoint = endpoint
        cls._guild_id = guild_id
        cls._on_close = on_close
        cls._owner = owner
        cls._session_id = session_id
        cls._shard_id = shard_id
        cls._token = token
        cls._user_id = user_id
        cls._bot = bot
        cls._ongaku: Ongaku = ongaku


        # Create a connection between discord, and lavalink (feed lavalink the sessionid, token, and ws uri) if successful, make is alive true.
        cls._is_alive = True

    def __init__(
        self,
        *,
        bot: hikari.GatewayBot,
        ongaku,
        channel_id: hikari.Snowflake,
        endpoint: str,
        guild_id: hikari.Snowflake,
        on_close,
        owner: VoiceComponent,
        session_id: str,
        shard_id: int,
        token: str,
        user_id: hikari.Snowflake,          
    ) -> None:
        from .ongaku import Ongaku
        self._bot = bot
        self._ongaku: Ongaku = ongaku
        self._channel_id = channel_id
        self._endpoint = endpoint
        self._guild_id = guild_id
        self._on_close = on_close
        self._owner = owner
        self._session_id = session_id
        self._shard_id = shard_id
        self._token = token
        self._user_id = user_id

    @property
    def channel_id(self) -> hikari.Snowflake:
        """ID of the voice channel this voice connection is in."""
        return self._channel_id

    @property
    def guild_id(self) -> hikari.Snowflake:
        """ID of the guild this voice connection is in."""
        return self._guild_id

    @property
    def is_alive(self) -> bool:
        """Whether the connection is alive."""
        return self._is_alive
    
    @property
    def shard_id(self) -> int:
        """ID of the shard that requested the connection."""
        return self._shard_id

    @property
    def owner(self) -> VoiceComponent:
        """Return the component that is managing this connection."""
        return self._owner

    async def play(self, track: models.Track) -> None:
        await self._ongaku.rest.internal.player.play_track(self.guild_id, track)

    async def disconnect(self) -> None:
        """Signal the process to shut down."""
        print("disconnected?")
        self._is_alive = False
        pass

    async def join(self) -> None:
        """Wait for the process to halt before continuing."""
        print("joined?")

    async def notify(self, event: hikari.VoiceEvent) -> None:
        """Submit an event to the voice connection to be processed."""
        pass

class Player:
    """
    The voice connection to the discord bot.
    """
    def __init__(self, app: hikari.GatewayBot, guild_id: hikari.Snowflake) -> None:
        self._app = app
        self._guild_id = guild_id
        self._channel_id = None

        self._queue: list[models.Track] = []

    @property
    def queue(self) -> list[models.Track]:
        return self._queue

    async def play(self, track: models.Track) -> None:
        """
        Play the selected song.
        """
        self._queue.insert(0, track)

        return
    
    async def add(self, tracks: list[models.Track]) -> None:
        """
        Adds selected songs to the queue.
        """
        self._queue.extend(tracks)

    async def pause(self, toggle: t.Optional[bool] = None) -> None:
        """
        Pauses or unpauses the current track.

        * If toggle is true, then it force pauses, if toggle is false, it force unpauses, and if None, will toggle the value.
        """

    async def skip(self, amount: int = 1) -> None:
        """
        Skips the selected amount of songs. default is 1.
        """

    async def clear(self) -> None:
        """
        Clears the entire queue.
        """
        self._queue.clear()

    async def stop(self) -> None:
        """
        Clears the queue, and stops the audio.
        """
        
        await self.clear()
        await self.pause(True)

    async def volume(self, level: int) -> None:
        """
        Changes the volume of the bot.

        --------
        RAISES
        * PlayerVolumeLevelException: Raised when a value (outside of 0-100) is sent.
        """

        if level > 100 or level < 0:
            error.PlayerVolumeLevelException(level)

    async def mute(self) -> None:
        """
        Mutes the bot. DOES NOT STOP AUDIO FROM PLAYING.
        """
