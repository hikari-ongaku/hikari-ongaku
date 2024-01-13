from __future__ import annotations

from hikari import Snowflake, GatewayBot, UndefinedOr, UNDEFINED
from hikari.events import VoiceServerUpdateEvent, VoiceStateUpdateEvent
import typing as t
import asyncio

from .errors import (
    SessionNotStartedException,
    PlayerQueueException,
    PlayerSettingException,
    PlayerException,
    TimeoutException,
    BuildException,
)
from .abc.track import Track
from .abc.events import TrackEndEvent, QueueEmptyEvent, QueueNextEvent
from .abc.player import PlayerVoice
from .abc.filters import Filter

if t.TYPE_CHECKING:
    from .node import Node


class Player:
    def __init__(
        self,
        bot: GatewayBot,
        node: Node,
        guild_id: Snowflake,
    ) -> None:
        """
        Base player class

        The class that allows the player, to play songs, and more.
        """
        self._bot = bot
        self._node = node
        self._guild_id = guild_id
        self._channel_id = None

        self._is_alive = False
        self._is_paused = True

        self._queue: list[Track] = []

        self._voice: PlayerVoice | None = None

        self._session_id: str | None = None

        self._connected: bool = False

        self._filter: Filter | None = None

        bot.subscribe(TrackEndEvent, self._track_end_event)

    @property
    def node(self) -> Node:
        """The node that this guild is connected too."""
        return self._node

    @property
    def channel_id(self) -> Snowflake | None:
        """
        ID of the voice channel this voice connection is currently in.

        Returns
        -------
        hikari.Snowflake
            The channel id.
        None
            The bot is not currently connected to a channel.
        """
        return self._channel_id

    @property
    def guild_id(self) -> Snowflake:
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
    def is_paused(self) -> bool:
        """
        Returns whether the bot is currently paused.
        """
        return self._is_paused

    @property
    def connected(self) -> bool:
        """
        Whether or not the bot is connected to a voice channel.
        """
        return self._connected

    @property
    def queue(self) -> tuple[Track, ...]:
        """
        Returns a queue, of the current tracks that are waiting to be played. The top one is the currently playing one.
        """
        return tuple(self._queue)

    @property
    def audio_filter(self) -> Filter | None:
        """
        The current filter applied to this bot.
        """
        return self._filter

    async def play(
        self, track: Track | None = None, requestor: Snowflake | None = None
    ) -> None:
        """
        Play a track

        Allows for the user to play a track.
        The current track will be stopped, and this will replace it.

        Parameters
        ----------
        track : abc.Track | None
            the track you wish to play. If empty, it will pull from the queue.
        requestor : Snowflake | None
            The user/member id that requested the song.

        Raises
        ------
        SessionNotStartedException
            The session id was null, or empty.
        PlayerQueueException
            The queue is empty and no track was given, so it cannot play songs.
        """
        if self._voice is None or self._channel_id is None:
            raise PlayerException("Player is not connected to a channel.")

        if self.node._internal.session_id is None:
            raise SessionNotStartedException()

        if len(self.queue) > 0 and track is None:
            raise PlayerQueueException("Empty Queue. Cannot play nothing.")

        if track:
            if requestor:
                track.requestor = requestor

            self._queue.insert(0, track)

        try:
            await self.node.ongaku.rest.player.update(
                self.guild_id,
                self.node._internal.session_id,
                track=self.queue[0],
                voice=self._voice,
                no_replace=False,
            )
        except Exception as e:
            raise e

        self._is_paused = False

    async def add(
        self, tracks: t.Sequence[Track], requestor: Snowflake | None = None
    ) -> None:
        """
        Add tracks

        Add tracks to the queue. This will not automatically start playing the songs.

        Parameters
        ----------
        tracks : list[abc.Track]
            The list of tracks you wish to add to the queue.
        requestor : Snowflake | None
            The user/member id that requested the song.
        """
        for track in tracks:
            if requestor:
                track.requestor = requestor
            self._queue.append(track)

    async def pause(self, value: UndefinedOr[bool] = UNDEFINED) -> None:
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
        if self.node._internal.session_id is None:
            raise SessionNotStartedException()

        if value == UNDEFINED:
            self._is_paused = not self.is_paused
        else:
            self._is_paused = value

        await self.node.ongaku.rest.player.update(
            self.guild_id, self.node._internal.session_id, paused=self.is_paused
        )

    async def remove(self, value: Track | int) -> None:
        """
        Remove track.

        Removes the track, or the track in that position.

        Parameters
        ----------
        value : abc.Track | int
            Remove a selected track. If `abc.Track`, then it will remove the first occurrence of that track. If `int`, it will remove the track at that number (starts at 0).

        Raises
        ------
        PlayerSettingException
            The queue is empty.
        SessionNotStartedException
            No session id provided, or the session id is null.
        """
        if len(self.queue) == 0:
            raise PlayerSettingException("Queue is empty.")

        if self.node._internal.session_id is None:
            raise SessionNotStartedException()

        if isinstance(value, Track):
            index = self._queue.index(value)

        else:
            index = value

        try:
            self._queue.pop(index)
        except Exception as e:
            raise PlayerException(f"Failed to remove a song: {e}")

        if index == 0:
            if len(self.queue) == 0:
                await self.node.ongaku.rest.player.update(
                    self.guild_id, self.node._internal.session_id, track=None
                )
            else:
                await self.play()

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
        if self.node._internal.session_id is None:
            raise SessionNotStartedException()

        if amount <= 0:
            raise PlayerSettingException(
                f"Skip amount cannot be 0 or negative. Value: {amount}"
            )
        if len(self.queue) == 0:
            raise PlayerQueueException("No tracks in queue.")

        for _ in range(amount):
            if len(self._queue) == 0:
                break
            else:
                self._queue.pop(0)

        if len(self.queue) == 0:
            await self.node.ongaku.rest.player.update(
                self.guild_id,
                self.node._internal.session_id,
                track=None,
            )
            return

    async def seek(self, value: int) -> None:
        """
        Seek the track

        Allows for seeking the track, by a certain amount

        Parameters
        ----------
        value : int
            The value, in milliseconds of how far into the track you wish to seek

        Raises
        ------
        SessionNotStartedException
            The session has not been yet started.
        PlayerQueueException
            The queue is empty, so no track can be sought.
        ValueError
            Raised when the value, is well beyond how long the track is.
        """
        if self.node._internal.session_id is None:
            raise SessionNotStartedException()

        if value < 0:
            raise ValueError("Sorry, but a negative value is not allowed.")

        if len(self.queue) < 0:
            raise PlayerQueueException("The queue is empty.")

        await self.node.ongaku.rest.player.update(
            self.guild_id,
            self.node._internal.session_id,
            position=value,
            no_replace=False,
        )

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
        SessionNotStartedException
            The session has not been yet started.
        PlayerSettingException
            Raised if the value is above, or below 0, or 1000.
        """

        if self.node._internal.session_id is None:
            raise SessionNotStartedException()

        if volume < 0:
            raise PlayerSettingException(
                f"Volume cannot be below zero. Volume: {volume}"
            )
        if volume > 1000:
            raise PlayerSettingException(
                f"Volume cannot be above 1000. Volume: {volume}"
            )

        await self.node.ongaku.rest.player.update(
            self.guild_id,
            self.node._internal.session_id,
            volume=volume,
            no_replace=False,
        )

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

        if self.node._internal.session_id is None:
            raise SessionNotStartedException()

        await self.node.ongaku.rest.player.update(
            self.guild_id,
            self.node._internal.session_id,
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
        SessionNotStartedException
            The session is not yet started.
        PlayerSettingException
            When the track position selected is not a valid position.
        PlayerSettingException
            The queue is empty.
        """
        if self.node._internal.session_id is None:
            raise SessionNotStartedException()

        if self.queue[0].info.length < value:
            raise PlayerSettingException(
                "Length is longer than currently playing song!"
            )

        await self.node.ongaku.rest.player.update(
            self.guild_id, self.node._internal.session_id, position=value
        )

    async def filter(self, filter: Filter | None = None):
        """
        Filter

        Set, or remove a filter.

        Parameters
        ----------
        filter : Filter
            the filter you wish to add.
        """
        if self.node._internal.session_id is None:
            raise SessionNotStartedException()

        self._filter = filter

        try:
            await self.node.ongaku.rest.player.update(
                self.guild_id,
                self.node._internal.session_id,
                filter=filter,
                no_replace=False,
            )
        except Exception:
            raise

    async def connect(
        self,
        channel_id: Snowflake,
        *,
        mute: UndefinedOr[bool] = UNDEFINED,
        deaf: UndefinedOr[bool] = UNDEFINED,
        timeout: int = 5,
    ) -> None:
        """
        Connect to a channel

        Connect your bot, to a channel, to be able to start playing music.

        Parameters
        ----------
        channel_id : Snowflake
            The channel you wish to connect the bot too.
        mute : UndefinedOr[bool]
            Whether or not to mute the bot.
        deaf : UndefinedOr[bool]
            Whether or not to deafen the bot.
        timeout : int
            The amount of time to wait for the events.

        !!! INFO
            If you set mute to True, the bot will not be able to transmit audio.

        Raises
        ------
        ConnectionError
            When it fails to connect to the voice server.
        SessionNotStartedException
            When the lavalink session has not yet started.
        TimeoutException
            Raised when the events fail to respond in time.
        PlayerException
            Raised when the endpoint in the event is none.
        BuildException
            When attempting to build the [PlayerVoice][ongaku.abc.player.PlayerVoice] and fails to build.
        """
        if self.node._internal.session_id is None:
            raise SessionNotStartedException()

        self._channel_id = channel_id
        try:
            await self._bot.update_voice_state(
                self.guild_id, self._channel_id, self_mute=mute, self_deaf=deaf
            )
        except Exception as e:
            raise ConnectionError(e)

        try:
            state_event, server_event = await asyncio.gather(
                self._bot.wait_for(
                    VoiceStateUpdateEvent,
                    timeout=timeout,
                ),
                self._bot.wait_for(
                    VoiceServerUpdateEvent,
                    timeout=timeout,
                ),
            )
        except asyncio.TimeoutError as e:
            raise TimeoutException(
                f"Could not connect to voice channel {channel_id} in guild {self.guild_id} due to events not being received."
            ) from e

        if server_event.endpoint is None:
            raise PlayerException(
                f"Endpoint missing for attempted server connection in {channel_id}, for guild {self.guild_id}"
            )

        try:
            self._voice = PlayerVoice(
                server_event.token, server_event.endpoint, state_event.state.session_id
            )
        except Exception as e:
            raise BuildException(f"Failed to build player voice: {e}")

        try:
            await self.node.ongaku.rest.player.update(
                self.guild_id,
                self.node._internal.session_id,
                voice=self._voice,
                no_replace=False,
            )
        except Exception:
            raise

    async def disconnect(self) -> None:
        """Do docs"""
        self._is_alive = False
        await self.clear()

        if self.node._internal.session_id is None:
            raise SessionNotStartedException()

        await self.node.ongaku.rest.player.delete(
            self.node._internal.session_id, self._guild_id
        )

    async def _track_end_event(self, event: TrackEndEvent) -> None:
        if self.node._internal.session_id is None:
            raise SessionNotStartedException()

        if int(event.guild_id) == int(self.guild_id):
            try:
                await self.remove(0)
            except Exception:
                await self._bot.dispatch(QueueEmptyEvent(self._bot, self.guild_id))
                return

            if len(self.queue) == 0:
                await self._bot.dispatch(QueueEmptyEvent(self._bot, self.guild_id))
                return

            await self.node.ongaku.rest.player.update(
                self.guild_id,
                self.node._internal.session_id,
                track=self._queue[0],
                no_replace=False,
            )

            await self._bot.dispatch(
                QueueNextEvent(self._bot, self.guild_id, self._queue[0], event.track)
            )
