import hikari, lightbulb
from hikari.api import VoiceConnection, VoiceComponent
import typing as t

from . import models, error

class Player:
    """
    The voice connection to the discord bot.
    """
    def __init__(self, app: hikari.GatewayBot, guild_id: hikari.Snowflake, channel_id: hikari.Snowflake) -> None:
        self._app = app
        self._guild_id = guild_id
        self._channel_id = channel_id

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
