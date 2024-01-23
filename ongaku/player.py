"""Player.

The player function, for all player related things.
"""

from __future__ import annotations

import asyncio
import typing as t

from hikari import UNDEFINED
from hikari import GatewayBot
from hikari import Snowflake
from hikari import UndefinedOr
from hikari.events import VoiceServerUpdateEvent
from hikari.events import VoiceStateUpdateEvent

from .abc import player
from .abc.events import QueueEmptyEvent
from .abc.events import QueueNextEvent
from .abc.events import TrackEndEvent
from .abc.filters import Filter
from .abc.player import PlayerVoice
from .abc.track import Track
from .errors import BuildException
from .errors import LavalinkException
from .errors import PlayerException
from .errors import PlayerQueueException
from .errors import SessionStartException
from .errors import TimeoutException

if t.TYPE_CHECKING:
    from .node import Node


class Player:
    """Base player.

    The class that allows the player, to play songs, and more.

    Parameters
    ----------
    node : Node
        The node that the player is attached too.
    guild_id : hikari.Snowflake
        The Guild ID the bot is attached too.
    """

    def __init__(
        self,
        node: Node,
        guild_id: Snowflake,
    ):
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

        self._volume: int = -1

        self.bot.subscribe(TrackEndEvent, self._track_end_event)

    @property
    def node(self) -> Node:
        """The node that this guild is attached to."""
        return self._node

    @property
    def bot(self) -> GatewayBot:
        """The bot that the server is on."""
        return self.node.client.bot

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
        """The guild id, that this player is playing in."""
        return self._guild_id

    @property
    def is_alive(self) -> bool:
        """Whether the current connection is alive."""
        return self._is_alive

    @property
    def volume(self) -> int:
        """The volume of the player.

        !!! warning
            If volume is -1, it has either not been updated, or connected to lavalink.
        """
        return self._volume

    @property
    def is_paused(self) -> bool:
        """Whether the bot is paused or not."""
        return self._is_paused

    @property
    def connected(self) -> bool:
        """Whether or not the bot is connected to a voice channel."""
        return self._connected

    @property
    def queue(self) -> t.Sequence[Track]:
        """Returns a queue, of the current tracks that are waiting to be played. The top one is the currently playing one, if not paused."""
        return self._queue

    @property
    def audio_filter(self) -> Filter | None:
        """The current filter applied to this player."""
        return self._filter

    async def connect(
        self,
        channel_id: Snowflake,
        *,
        mute: UndefinedOr[bool] = UNDEFINED,
        deaf: UndefinedOr[bool] = UNDEFINED,
        timeout: int = 5,
    ) -> None:
        """Connect to a channel.

        Connect your bot, to a channel, to be able to start playing music.

        !!! WARNING
            If you set the `mute` parameter to True, the bot will not be able to transmit audio.

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

        Raises
        ------
        SessionStartException
            The session id was null, or empty.
        ConnectionError
            When it fails to connect to the voice server.
        TimeoutException
            Raised when the events fail to respond in time.
        PlayerException
            Raised when the endpoint in the event is none.
        LavalinkException
            If an error code of 4XX or 5XX is received, if if no data is received at all, when data was expected.
        BuildException
            Failure to build the player object.
        """
        if self.node._internal.session_id is None:
            raise SessionStartException()

        self._channel_id = channel_id
        try:
            await self.bot.update_voice_state(
                self.guild_id, self._channel_id, self_mute=mute, self_deaf=deaf
            )
        except Exception as e:
            raise ConnectionError(e)

        try:
            state_event, server_event = await asyncio.gather(
                self.bot.wait_for(
                    VoiceStateUpdateEvent,
                    timeout=timeout,
                ),
                self.bot.wait_for(
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
            player = await self.node.client.rest.player.update(
                self.guild_id,
                self.node._internal.session_id,
                voice=self._voice,
                no_replace=False,
            )
        except LavalinkException:
            raise
        except BuildException:
            raise

        await self._update(player)

    async def disconnect(self) -> None:
        """Disconnect player.

        Disconnect the player from the lavalink server, and discord.

        Raises
        ------
        SessionStartException
            The session id was null, or empty.
        """
        self._is_alive = False
        await self.clear()

        if self.node._internal.session_id is None:
            raise SessionStartException()

        try:
            await self.node.client.rest.player.delete(
                self.node._internal.session_id, self._guild_id
            )
        except LavalinkException:
            raise
        except ValueError:
            raise
        except BuildException:
            raise

        await self.bot.update_voice_state(self.guild_id, None)

    async def play(
        self, track: Track | None = None, requestor: Snowflake | None = None
    ) -> None:
        """Play a track.

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
        SessionStartException
            The session id was null, or empty.
        PlayerQueueException
            The queue is empty and no track was given, so it cannot play songs.
        LavalinkException
            If an error code of 4XX or 5XX is received, if if no data is received at all, when data was expected.
        BuildException
            Failure to build the player object.
        """
        if self._voice is None or self._channel_id is None:
            raise PlayerException("Player is not connected to a channel.")

        if self.node._internal.session_id is None:
            raise SessionStartException()

        if len(self.queue) > 0 and track is None:
            raise PlayerQueueException("Empty Queue. Cannot play nothing.")

        if track:
            if requestor:
                track.requestor = requestor

            self._queue.insert(0, track)

        try:
            player = await self.node.client.rest.player.update(
                self.guild_id,
                self.node._internal.session_id,
                track=self.queue[0],
                voice=self._voice,
                no_replace=False,
            )
        except LavalinkException:
            raise
        except BuildException:
            raise

        self._is_paused = False

        await self._update(player)

    async def add(
        self, tracks: t.Sequence[Track], requestor: Snowflake | None = None
    ) -> None:
        """Add tracks.

        Add tracks to the queue. This will not automatically start playing the songs.

        Parameters
        ----------
        tracks : t.Sequence[abc.Track]
            The list of tracks you wish to add to the queue.
        requestor : Snowflake | None
            The user/member id that requested the song.

        Raises
        ------
        SessionStartException
            The session id was null, or empty.
        LavalinkException
            If an error code of 4XX or 5XX is received, if if no data is received at all, when data was expected.
        BuildException
            Failure to build the player object.
        """
        for track in tracks:
            if requestor:
                track.requestor = requestor
            self._queue.append(track)

        if self.node._internal.session_id is None:
            raise SessionStartException()

        try:
            player = await self.node.client.rest.player.update(
                self.guild_id,
                self.node._internal.session_id,
                track=self.queue[0],
                no_replace=False,
            )
        except LavalinkException:
            raise
        except BuildException:
            raise

        await self._update(player)

    async def pause(self, value: UndefinedOr[bool] = UNDEFINED) -> None:
        """Pause the player.

        Allows for the user to pause the currently playing track on this player.

        !!! INFO
            `True` will force pause the bot, `False` will force unpause the bot. Leaving it empty, will toggle it.

        Parameters
        ----------
        value : hikari.UndefinedOr[bool]
            How you wish to pause the bot.

        Raises
        ------
        SessionStartException
            The session id was null, or empty.
        LavalinkException
            If an error code of 4XX or 5XX is received, if if no data is received at all, when data was expected.
        BuildException
            Failure to build the player object.
        """
        if self.node._internal.session_id is None:
            raise SessionStartException()

        if value == UNDEFINED:
            self._is_paused = not self.is_paused
        else:
            self._is_paused = value

        try:
            player = await self.node.client.rest.player.update(
                self.guild_id, self.node._internal.session_id, paused=self.is_paused
            )
        except LavalinkException:
            raise
        except BuildException:
            raise

        await self._update(player)

    async def position(self, value: int) -> None:
        """Change the track position.

        Change the currently playing track's position.

        Parameters
        ----------
        value : int
            The value, of the position, in milliseconds.

        Raises
        ------
        SessionStartException
            The session is not yet started.
        PlayerQueueException
            When the queue is empty.
        ValueError
            When the track position selected is not a valid position.
        """
        if self.node._internal.session_id is None:
            raise SessionStartException()

        if value < 0:
            raise ValueError("Sorry, but a negative value is not allowed.")

        if len(self.queue) <= 0:
            raise PlayerQueueException("The queue is empty.")

        try:
            player = await self.node.client.rest.player.update(
                self.guild_id,
                self.node._internal.session_id,
                position=value,
                no_replace=False,
            )
        except LavalinkException:
            raise
        except BuildException:
            raise

        await self._update(player)

    async def skip(self, amount: int = 1) -> None:
        """Skip songs.

        skip a selected amount of songs in the queue.

        Parameters
        ----------
        amount : int
            The amount of songs you wish to skip.

        Raises
        ------
        SessionStartException
            The session id was null, or empty.
        ValueError
            The amount was 0 or a negative number.
        PlayerQueueException
            The queue is already empty, so no songs can be skipped.
        LavalinkException
            If an error code of 4XX or 5XX is received, if if no data is received at all, when data was expected.
        BuildException
            Failure to build the player object.
        """
        if self.node._internal.session_id is None:
            raise SessionStartException()

        if amount <= 0:
            raise ValueError(f"Skip amount cannot be 0 or negative. Value: {amount}")
        if len(self.queue) == 0:
            raise PlayerQueueException("No tracks in queue.")

        for _ in range(amount):
            if len(self._queue) == 0:
                break
            else:
                self._queue.pop(0)

        if len(self.queue) == 0:
            try:
                player = await self.node.client.rest.player.update(
                    self.guild_id,
                    self.node._internal.session_id,
                    track=None,
                )
            except LavalinkException:
                raise
            except BuildException:
                raise

            await self._update(player)

    async def set_volume(self, volume: int) -> None:
        """Set the volume.

        The volume you wish to set for the player.

        Parameters
        ----------
        volume : int
            The volume you wish to set, from 0 to 1000.

        Raises
        ------
        SessionStartException
            The session has not been yet started.
        ValueError
            Raised if the value is above, or below 0, or 1000.
        LavalinkException
            If an error code of 4XX or 5XX is received, if if no data is received at all, when data was expected.
        BuildException
            Failure to build the player object.
        """
        if self.node._internal.session_id is None:
            raise SessionStartException()

        if volume < 0:
            raise ValueError(f"Volume cannot be below zero. Volume: {volume}")
        if volume > 1000:
            raise ValueError(f"Volume cannot be above 1000. Volume: {volume}")

        try:
            player = await self.node.client.rest.player.update(
                self.guild_id,
                self.node._internal.session_id,
                volume=volume,
                no_replace=False,
            )
        except LavalinkException:
            raise
        except BuildException:
            raise

        await self._update(player)

    async def remove(self, value: Track | int) -> None:
        """
        Remove track.

        Removes the track, or the track in that position.

        Parameters
        ----------
        value : abc.Track | int
            Remove a selected track. If [Track][ongaku.abc.track.Track], then it will remove the first occurrence of that track. If an integer, it will remove the track at that number.

        Raises
        ------
        SessionStartException
            The session id was null, or empty.
        ValueError
            The queue is empty.
        PlayerException
            The song did not exist, or the position was out of the length of the queue.
        LavalinkException
            If an error code of 4XX or 5XX is received, if if no data is received at all, when data was expected.
        BuildException
            Failure to build the player object.
        """
        if len(self.queue) == 0:
            raise ValueError("Queue is empty.")

        if self.node._internal.session_id is None:
            raise SessionStartException("Session has not been started for this player.")

        if isinstance(value, Track):
            index = self._queue.index(value)

        else:
            index = value

        try:
            self._queue.pop(index)
        except KeyError:
            if isinstance(value, Track):
                raise PlayerException(f"Failed to remove a song: {value.info.title}")
            else:
                raise PlayerException(f"Failed to remove song in position {value}")

        if index == 0:
            if len(self.queue) == 0:
                try:
                    player = await self.node.client.rest.player.update(
                        self.guild_id, self.node._internal.session_id, track=None
                    )
                except LavalinkException:
                    raise
                except BuildException:
                    raise
                await self._update(player)
            else:
                await self.play()

    async def clear(self) -> None:
        """Clear the queue.

        Clear the current queue, and also stop the audio from the player.

        Raises
        ------
        SessionStartException
            The session is not yet started.
        LavalinkException
            If an error code of 4XX or 5XX is received, if if no data is received at all, when data was expected.
        BuildException
            Failure to build the player object.
        """
        self._queue.clear()

        if self.node._internal.session_id is None:
            raise SessionStartException()

        try:
            player = await self.node.client.rest.player.update(
                self.guild_id,
                self.node._internal.session_id,
                track=None,
                no_replace=False,
            )
        except LavalinkException:
            raise
        except BuildException:
            raise

        await self._update(player)

    async def filter(self, filter: Filter | None = None):
        """Filter.

        Set, or remove a filter for the player.

        Parameters
        ----------
        filter : Filter
            the filter you wish to add.

        Raises
        ------
        SessionStartException
            The session id was null, or empty.
        LavalinkException
            If an error code of 4XX or 5XX is received, if if no data is received at all, when data was expected.
        BuildException
            Failure to build the player object.
        """
        if self.node._internal.session_id is None:
            raise SessionStartException()

        self._filter = filter

        try:
            player = await self.node.client.rest.player.update(
                self.guild_id,
                self.node._internal.session_id,
                filter=filter,
                no_replace=False,
            )
        except LavalinkException:
            raise
        except BuildException:
            raise

        await self._update(player)

    async def _update(self, player: player.Player) -> None:
        # TODO: Somehow do the filter and the track.

        self._is_paused = player.paused
        self._voice = player.voice
        self._volume = player.volume

    async def _track_end_event(self, event: TrackEndEvent) -> None:
        if self.node._internal.session_id is None:
            raise SessionStartException()

        if int(event.guild_id) == int(self.guild_id):
            try:
                await self.remove(0)
            except Exception:
                await self.bot.dispatch(QueueEmptyEvent(self.bot, self.guild_id))
                return

            if len(self.queue) == 0:
                await self.bot.dispatch(QueueEmptyEvent(self.bot, self.guild_id))
                return

            try:
                player = await self.node.client.rest.player.update(
                    self.guild_id,
                    self.node._internal.session_id,
                    track=self._queue[0],
                    no_replace=False,
                )
            except LavalinkException:
                raise
            except BuildException:
                raise

            await self._update(player)

            await self.bot.dispatch(
                QueueNextEvent(self.bot, self.guild_id, self._queue[0], event.track)
            )
