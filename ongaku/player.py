from __future__ import annotations

import hikari
from hikari.api import VoiceConnection, VoiceComponent
import typing as t

from . import models, error, events

if t.TYPE_CHECKING:
    from .ongaku import Ongaku

    OngakuT = t.TypeVar("OngakuT", bound="Ongaku")


class Player(VoiceConnection):
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
        ongaku: Ongaku,
    ):
        init_player = Player(
            bot=bot,
            ongaku=ongaku,
            channel_id=channel_id,
            endpoint=endpoint,
            guild_id=guild_id,
            on_close=on_close,
            owner=owner,
            session_id=session_id,
            shard_id=shard_id,
            token=token,
            user_id=user_id,
        )

        return init_player

    def __init__(
        self,
        *,
        bot: hikari.GatewayBot,
        ongaku: Ongaku,
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
        self._bot = bot
        self._ongaku = ongaku
        self._channel_id = channel_id
        self._endpoint = endpoint
        self._guild_id = guild_id
        self._on_close = on_close
        self._owner = owner
        self._session_id = session_id
        self._shard_id = shard_id
        self._token = token
        self._user_id = user_id

        self._is_paused = True

        self._queue: list[models.Track] = []

        bot.subscribe(events.TrackEndEvent, self.track_end_event)

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

    @property
    def is_paused(self) -> bool:
        """
        Returns whether the bot is paused or not.
        """
        return self._is_paused

    @property
    def queue(self) -> list[models.Track]:
        """
        View all the tracks that currently exist.
        """
        return tuple(self._queue)

    async def play(self, track: models.Track) -> None:
        voice = models.Voice(
            {
                "token": self._token,
                "endpoint": self._endpoint[6:],
                "sessionId": self._session_id,
            }
        )

        if self._ongaku._session_id == None:
            raise error.SessionNotStartedException()

        await self._ongaku.rest.internal.player.update_player(
            self.guild_id,
            self._ongaku._session_id,
            track=track,
            voice=voice,
            no_replace=False,
        )

        self._is_paused = False

    async def pause(self, value: hikari.UndefinedOr[bool] = hikari.UNDEFINED) -> None:
        if self._ongaku._session_id == None:
            raise error.SessionNotStartedException()

        if value == hikari.UNDEFINED:
            self._is_paused = not self.is_paused
        else:
            self._is_paused = value

        await self._ongaku.rest.internal.player.update_player(
            self.guild_id, self._ongaku._session_id, paused=self.is_paused
        )

    async def add(self, tracks: list[models.Track]):
        self._queue.extend(tracks)

    async def remove(self, value: models.Track | int) -> None:
        if isinstance(value, models.Track):
            index = self._queue.index(value)

        else:
            index = value

        try:
            self._queue.pop(index)
        except Exception as e:
            raise e

    async def skip(self, amount: int) -> None:
        if amount == 0:
            return
        if len(self.queue) == 0:
            raise error.PlayerEmptyQueueException(0)

        for item in range(amount):
            if len(self._queue) == 0:
                break
            else:
                self._queue.pop(0)

        if len(self.queue) == 0:
            self._ongaku.rest.internal.player.update_player(
                self.guild_id, self._ongaku._session_id, track=None, 
            )
            return
        
        self._ongaku.rest.internal.player.update_player(
            self.guild_id, self._ongaku._session_id, track=self._queue[0], no_replace=False
        )

    async def track_end_event(self, event: events.TrackEndEvent):
        if int(event.guild_id) == int(self.guild_id):
            await self.remove(0)
            
            if len(self.queue) == 0:
                await self._bot.dispatch(events.PlayerQueueEmptyEvent(self._bot, self.guild_id))
                return
            
            self._ongaku.rest.internal.player.update_player(
                self.guild_id, self._ongaku._session_id, track=self._queue[0], no_replace=False
            )

    # TODO: The following things between these to do's, do not work yet.

    async def volume(self, volume: int) -> None:
        if volume < 0 or volume > 1000:
            raise error.PlayerInvalidVolumeException(volume)
        pass

    async def clear(self) -> None:
        """
        Clears the queue, and stops the current song.
        """
        self._queue.clear()
        self._ongaku.rest.internal.player.update_player(
            self.guild_id, self._ongaku._session_id, track=None, no_replace=False
        )

    async def position(self, value: int) -> None:
        """
        Change the tracks position in ms.
        
        Raises
        ------
        PlayerInvalidPosition: When the track position selected is not a valid position.
        """
        pass

    # TODO: The following things between these to do's, do not work yet.

    async def disconnect(self) -> None:
        """Signal the process to shut down."""
        self._is_alive = False
        await self.clear()
        await self._ongaku.rest.internal.player.delete_player(
            self._ongaku._session_id, self._guild_id
        )

    async def join(self) -> None:
        """Wait for the process to halt before continuing."""
        print("joined?")

    async def notify(self, event: hikari.VoiceEvent) -> None:
        """Submit an event to the voice connection to be processed."""
        pass
