from __future__ import annotations

import hikari
from hikari.api import VoiceConnection, VoiceComponent
import typing as t

from .events import other

from . import abc, errors, events

if t.TYPE_CHECKING:
    from .ongaku import Ongaku

    OngakuT = t.TypeVar("OngakuT", bound="Ongaku")


class Player(VoiceConnection):
    @classmethod
    async def initialize(  # type: ignore
        cls,
        channel_id: hikari.Snowflake,
        endpoint: str,
        guild_id: hikari.Snowflake,
        on_close: t.Awaitable[None],  # type: ignore TODO: This needs to be fixed, or I need to make my own player.
        owner: VoiceComponent,
        session_id: str,
        shard_id: int,
        token: str,
        user_id: hikari.Snowflake,
        *,
        bot: hikari.GatewayBot,
        ongaku: Ongaku,
    ):
        """
        Testing

        Testing something
        """

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
        on_close: t.Awaitable[None],  # type: ignore TODO: This needs to be fixed, or I need to make my own player.
        owner: VoiceComponent,
        session_id: str,
        shard_id: int,
        token: str,
        user_id: hikari.Snowflake,
    ) -> None:
        """
        GSDS

        DGHDJHSJDHGFJS


        !!! INFO
            THIS IS A TEST
        """
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

        self._queue: list[abc.Track] = []

        bot.subscribe(events.TrackEndEvent, self._track_end_event)

    @property
    def channel_id(self) -> hikari.Snowflake:
        """
        ID of the voice channel this voice connection is currently in.
        """
        return self._channel_id

    @property
    def guild_id(self) -> hikari.Snowflake:
        """
        ID of the guild this voice connection is in.
        """
        return self._guild_id

    @property
    def is_alive(self) -> bool:
        """
        Whether the current connection is alive.
        """
        return self._is_alive

    @property
    def shard_id(self) -> int:
        """
        ID of the shard that requested the connection.
        """
        return self._shard_id

    @property
    def owner(self) -> VoiceComponent:
        """
        Return the component that is managing this connection.
        """
        return self._owner

    @property
    def is_paused(self) -> bool:
        """
        Returns whether the bot is currently paused.
        """
        return self._is_paused

    @property
    def queue(self) -> tuple[abc.Track, ...]:
        """
        Returns a queue, of the current tracks that are waiting to be played. The top one is the currently playing one.
        """
        return tuple(self._queue)

    async def play(self, track: t.Optional[abc.Track] = None) -> None:
        """
        Play a track

        Allows for the user to play a track.
        The current track will be stopped, and this will replace it.

        Parameters
        ----------
        track: t.Optional[abc.Track]
            the track you wish to play. If empty, it will pull from the queue.
        
        Raises
        ------
        SessionNotStartedException
            The session id was null, or empty.
        PlayerQueueException
            The queue is empty and no track was given, so it cannot play songs.
        """
        voice = abc.Voice(
            self._token, self._endpoint[6:], self._session_id
        )  # TODO: Fix the creation of dictionaries, and make sure its sessionId not session_id

        if self._ongaku.internal.session_id == None:
            raise errors.SessionNotStartedException()

                
        if len(self.queue) > 0 and track == None:
            raise errors.PlayerQueueException("Empty Queue. Cannot play nothing.")

        if track != None:
            self._queue.insert(0, track)

        await self._ongaku.rest.internal.player.update_player(
            self.guild_id,
            self._ongaku.internal.session_id,
            track=self.queue[0],
            voice=voice,
            no_replace=False,
        )

        self._is_paused = False

    async def pause(self, value: hikari.UndefinedOr[bool] = hikari.UNDEFINED) -> None:
        """
        Pause the current track

        Allows for the user to pause the currently playing track.

        Parameters
        ----------
        value : hikari.UndefinedOr[bool]
            How you wish to pause the bot.
        
        !!! INFO
            `True` will force pause the bot, `False` will force unpause the bot, and `undefined` will toggle.

        Raises
        ------
        SessionNotStartedException
            The session id was null, or empty.

        """
        if self._ongaku.internal.session_id == None:
            raise errors.SessionNotStartedException()

        if value == hikari.UNDEFINED:
            self._is_paused = not self.is_paused
        else:
            self._is_paused = value

        await self._ongaku.rest.internal.player.update_player(
            self.guild_id, self._ongaku.internal.session_id, paused=self.is_paused
        )

    async def add(self, tracks: list[abc.Track]):
        """
        Add tracks

        Add tracks to the queue. This will not automatically start playing the songs.

        Parameters
        ----------
        tracks : list[abc.Track]
            The list of tracks you wish to add to the queue.
        """
        self._queue.extend(tracks)

    async def remove(self, value: abc.Track | int) -> None:
        """
        Remove track.

        Removes the track, or the track in that position.

        Parameters
        ----------
        value : abc.Track | int
            Remove a selected track. If `abc.Track`, then it will remove the first occurrence of that track. If `int`, it will remove the track at that number (starts at 0).

        Raises
        ------

        """

        if isinstance(value, abc.Track):
            index = self._queue.index(value)

        else:
            index = value

        try:
            self._queue.pop(index)
        except Exception as e:
            raise e

    async def skip(self, amount: int = 1) -> None:
        """
        skip songs

        skip a selected amount of songs.

        Parameters
        ----------
        amount : int
            The amount of songs you wish to skip.

        Raises
        ------
        SessionNotStartedException
            The session id was null, or empty.
        PlayerSettingException
            The amount was 0 or a negative number.
        PlayerQueueException
            The queue is already empty, so no songs can be skipped.
        """
        if self._ongaku.internal.session_id == None:
            raise errors.SessionNotStartedException()

        if amount <= 0:
            raise errors.PlayerSettingException(f"Skip amount cannot be 0 or negative. Value: {amount}")
        if len(self.queue) == 0:
            raise errors.PlayerQueueException("No tracks in queue.")

        for _ in range(amount):
            if len(self._queue) == 0:
                break
            else:
                self._queue.pop(0)

        if len(self.queue) == 0:
            await self._ongaku.rest.internal.player.update_player(
                self.guild_id,
                self._ongaku.internal.session_id,
                track=None,
            )
            return

        await self._ongaku.rest.internal.player.update_player(
            self.guild_id,
            self._ongaku.internal.session_id,
            track=self._queue[0],
            no_replace=False,
        )

    # TODO: The following things between these to do's, do not work yet.

    async def volume(self, volume: int) -> None:
        """
        change the volume

        The volume you wish to set for the bot.

        Parameters
        ----------
        volume : int
            The volume you wish to set, from 0 to 1000.

        Raises
        ------
        PlayerSettingException
            Raised if the value is above, or below 0, or 1000.
        """
        if volume < 0:
            raise errors.PlayerSettingException(f"Volume cannot be below zero. Volume: {volume}")
        if volume > 1000:
            raise errors.PlayerSettingException(f"Volume cannot be above 1000. Volume: {volume}")
        pass

    async def clear(self) -> None:
        """
        Clear the queue

        Clear the current queue, and also stop the audio from the bot.

        Raises
        ------
        SessionNotStarted
            The session is not yet started.
        """
        self._queue.clear()

        if self._ongaku.internal.session_id == None:
            raise errors.SessionNotStartedException()

        await self._ongaku.rest.internal.player.update_player(
            self.guild_id,
            self._ongaku.internal.session_id,
            track=None,
            no_replace=False,
        )

    async def position(self, value: int) -> None:
        """
        Change the track position

        Change the current track position

        Parameters
        ----------
        value : int
            The value, of the position, in milliseconds.

        Raises
        ------
        SessionNotStarted
            The session is not yet started.
        PlayerSettingException
            When the track position selected is not a valid position.
        """
        

    # TODO: The following things between these to do's, do not work yet.

    async def disconnect(self) -> None:
        """Signal the process to shut down."""
        self._is_alive = False
        await self.clear()

        if self._ongaku.internal.session_id == None:
            raise errors.SessionNotStartedException()

        await self._ongaku.rest.internal.player.delete_player(
            self._ongaku.internal.session_id, self._guild_id
        )

    async def join(self) -> None:
        """Wait for the process to halt before continuing."""
        print("joined?")

    async def notify(self, event: hikari.VoiceEvent) -> None:
        """Submit an event to the voice connection to be processed."""
        pass

    async def _track_end_event(self, event: events.TrackEndEvent):
        if self._ongaku.internal.session_id == None:
            raise errors.SessionNotStartedException()

        if int(event.guild_id) == int(self.guild_id):
            await self.remove(0)

            if len(self.queue) == 0:
                await self._bot.dispatch(
                    other.PlayerQueueEmptyEvent(self._bot, self.guild_id)
                )
                return

            await self._ongaku.rest.internal.player.update_player(
                self.guild_id,
                self._ongaku.internal.session_id,
                track=self._queue[0],
                no_replace=False,
            )
