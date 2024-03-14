"""Player.

The player function, for all player related things.
"""

from __future__ import annotations

import typing as t
from asyncio import TimeoutError
from asyncio import gather

from hikari import UNDEFINED
from hikari import GatewayBot
from hikari import Snowflake
from hikari import UndefinedOr
from hikari.events import VoiceServerUpdateEvent
from hikari.events import VoiceStateUpdateEvent

from .abc.events import PlayerUpdateEvent
from .abc.events import QueueEmptyEvent
from .abc.events import QueueNextEvent
from .abc.events import TrackEndEvent
from .abc.filters import Filter
from .abc.player import Player as ABCPlayer
from .abc.player import PlayerVoice
from .abc.track import Track
from .enums import TrackEndReasonType
from .exceptions import BuildException
from .exceptions import LavalinkException
from .exceptions import PlayerConnectException
from .exceptions import PlayerQueueException
from .internal import Trace
from .internal import logger

if t.TYPE_CHECKING:
    from .session import Session

_logger = logger.getChild("player")

__all__ = ("Player",)


class Player:
    """Base player.

    The class that allows the player, to play songs, and more.

    Parameters
    ----------
    session : Session
        The session that the player is attached too.
    guild_id : hikari.Snowflake
        The Guild ID the bot is attached too.
    """

    def __init__(
        self,
        session: Session,
        guild_id: Snowflake,
    ):
        self._session = session
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

        self._auto_play = True

        self._position: int = 0

        self.bot.subscribe(TrackEndEvent, self._track_end_event)
        self.bot.subscribe(PlayerUpdateEvent, self._player_update)

    @property
    def session(self) -> Session:
        """The session that this guild is attached to."""
        return self._session

    @property
    def bot(self) -> GatewayBot:
        """The bot that the server is on."""
        return self.session.client.bot

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
        """The guild id, that this player is attached to."""
        return self._guild_id

    @property
    def is_alive(self) -> bool:
        """Whether the current connection is alive."""
        return self._is_alive

    @property
    def position(self) -> int:
        """The position of the track in milliseconds."""
        return self._position

    @property
    def volume(self) -> int:
        """The volume of the player.

        !!! warning
            If volume is -1, it has either not been updated, or connected to lavalink.
        """
        return self._volume

    @property
    def is_paused(self) -> bool:
        """Whether the player is paused or not."""
        return self._is_paused

    @property
    def auto_play(self) -> bool:
        """Whether or not the next song will play, when this song ends."""
        return self._auto_play

    @property
    def connected(self) -> bool:
        """Whether or not the bot is connected to a voice channel."""
        return self._connected

    @property
    def queue(self) -> t.Sequence[Track]:
        """Returns the current queue of tracks."""
        return self._queue

    @property
    def audio_filter(self) -> Filter | None:
        """The current filters applied to this player."""
        return self._filter

    async def _transfer_player(self, session: Session) -> Player:
        """
        Transfer player.

        Transfers this player to another server. This will shutdown the current player, and makes sure the old one is dead.
        """
        new_player = Player(session, self.guild_id)

        await new_player.add(self.queue)

        if self.connected and self.channel_id:
            await self.disconnect()

            await new_player.connect(self.channel_id)

            if not self.is_paused:
                await new_player.play()
                await new_player.set_position(self.position)

        return new_player

    async def connect(
        self,
        channel_id: Snowflake,
        *,
        mute: UndefinedOr[bool] = UNDEFINED,
        deaf: UndefinedOr[bool] = UNDEFINED,
        timeout: int = 5,
    ) -> None:
        """
        Connect to a channel.

        Connect this player to the specified channel.

        !!! WARNING
            If you set the `mute` parameter to True, the bot will not be able to transmit audio.

        Parameters
        ----------
        channel_id : Snowflake
            The channel ID you wish to connect the bot too.
        mute : UndefinedOr[bool]
            Whether or not to mute the bot.
        deaf : UndefinedOr[bool]
            Whether or not to deafen the bot.
        timeout : int
            The amount of time to wait for the events.

        Raises
        ------
        SessionConnectionException
            The session id was null, or empty.
        ConnectionError
            When it fails to connect to the voice server.
        PlayerConnectionException
            Raised when the endpoint in the event is none.
        PlayerConnectionException
            Raised when the events fail to respond in time.
        LavalinkException
            Raise when a invalid response type is received.
        ValueError
            Raised when a return type is set, and no data was received.
        BuildException
            Raised when the object could not be built.
        """
        session = self.session._get_session_id()

        _logger.log(
            Trace.LEVEL,
            f"Attempting connection to voice channel: {channel_id} in guild: {self.guild_id}",
        )

        self._channel_id = channel_id

        try:
            await self.bot.update_voice_state(
                self.guild_id, self._channel_id, self_mute=mute, self_deaf=deaf
            )
        except Exception as e:
            raise ConnectionError(e)

        _logger.log(
            Trace.LEVEL,
            "waiting for voice events for channel: {channel_id} in guild: {self.guild_id}",
        )

        try:
            state_event, server_event = await gather(
                self.bot.wait_for(
                    VoiceStateUpdateEvent,
                    timeout=timeout,
                ),
                self.bot.wait_for(
                    VoiceServerUpdateEvent,
                    timeout=timeout,
                ),
            )
        except TimeoutError as e:
            raise PlayerConnectException(
                self.guild_id,
                f"Could not connect to voice channel {channel_id} due to events not being received.",
            )

        if server_event.endpoint is None:
            raise PlayerConnectException(
                self.guild_id,
                f"Endpoint missing for attempted server connection in {channel_id}",
            )

        _logger.log(
            Trace.LEVEL,
            f"Successfully received events for channel: {channel_id} in guild: {self.guild_id}",
        )

        try:
            self._voice = PlayerVoice(
                token=server_event.token,
                endpoint=server_event.endpoint,
                session_id=state_event.state.session_id,
            )
        except Exception as e:
            raise BuildException(f"Failed to build player voice: {e}")

        try:
            player = await self.session.client.rest.player.update(
                self.guild_id,
                session,
                voice=self._voice,
                no_replace=False,
            )
        except LavalinkException:
            raise
        except BuildException:
            raise
        except ValueError:
            raise

        self._connected = True

        _logger.log(
            Trace.LEVEL,
            f"Successfully connected, and sent data to lavalink for channel: {channel_id} in guild: {self.guild_id}",
        )

        await self._update(player)

    async def disconnect(self) -> None:
        """
        Disconnect player.

        Disconnect the player from the lavalink server, and discord.

        Raises
        ------
        SessionConnectionException
            The session id was null, or empty.
        LavalinkException
            Raise when a invalid response type is received.
        """
        session = self.session._get_session_id()

        self._is_alive = False
        await self.clear()

        _logger.log(
            Trace.LEVEL,
            f"Attempting to delete player for channel: {self.channel_id} in guild: {self.guild_id}",
        )

        try:
            await self.session.client.rest.player.delete(session, self._guild_id)
        except LavalinkException:
            raise

        _logger.log(
            Trace.LEVEL,
            f"Successfully deleted player for channel: {self.channel_id} in guild: {self.guild_id}",
        )

        self._connected = False

        _logger.log(
            Trace.LEVEL,
            f"Updating voice state for channel: {self.channel_id} in guild: {self.guild_id}",
        )

        await self.bot.update_voice_state(self.guild_id, None)

        _logger.log(
            Trace.LEVEL,
            f"Successfully updated voice state for channel: {self.channel_id} in guild: {self.guild_id}",
        )

    async def play(
        self, track: Track | None = None, requestor: Snowflake | None = None
    ) -> None:
        """
        Play a track.

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
        SessionConnectionException
            The session id was null, or empty.
        PlayerQueueException
            The queue is empty and no track was given, so it cannot play songs.
        PlayerConnectException
            The bot is not connected to a channel.
        LavalinkException
            Raise when a invalid response type is received.
        ValueError
            Raised when a return type is set, and no data was received.
        BuildException
            Raised when the object could not be built.
        """
        session = self.session._get_session_id()

        if self.channel_id is None:
            raise PlayerConnectException(self.guild_id, "Not connected to a channel.")

        if len(self.queue) <= 0 and track == None:
            raise PlayerQueueException(
                self.guild_id, "You must provide a track if no tracks are in the queue."
            )

        if track:
            if requestor:
                track.requestor = requestor

            self._queue.insert(0, track)

        try:
            player = await self.session.client.rest.player.update(
                self.guild_id,
                session,
                track=self.queue[0],
                no_replace=False,
            )
        except LavalinkException:
            raise
        except BuildException:
            raise
        except ValueError:
            raise

        self._is_paused = False

        await self._update(player)

    async def add(
        self, tracks: t.Sequence[Track] | Track, requestor: Snowflake | None = None
    ) -> None:
        """
        Add tracks.

        Add tracks to the queue. This will not automatically start playing the songs. please call `.play()` after, with no track.

        Parameters
        ----------
        tracks : t.Sequence[abc.Track] | Track
            The list of tracks or a singular track you wish to add to the queue.
        requestor : Snowflake | None
            The user/member id that requested the song.
        """
        if isinstance(tracks, Track):
            tracks.requestor = requestor
            self._queue.append(tracks)
            return

        for track in tracks:
            if requestor:
                track.requestor = requestor
            self._queue.append(track)

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
        SessionConnectionException
            The session id was null, or empty.
        LavalinkException
            Raise when a invalid response type is received.
        ValueError
            Raised when a return type is set, and no data was received.
        BuildException
            Raised when the object could not be built.
        """
        session = self.session._get_session_id()

        if value == UNDEFINED:
            self._is_paused = not self.is_paused
        else:
            self._is_paused = value

        try:
            player = await self.session.client.rest.player.update(
                self.guild_id, session, paused=self.is_paused
            )
        except LavalinkException:
            raise
        except BuildException:
            raise
        except ValueError:
            raise

        await self._update(player)

    async def stop(self) -> None:
        """
        Stop current track.

        Stops the audio, by setting the song to none.
        This does not touch the queue.
        To start playing again, run .play() without a track.

        Raises
        ------
        SessionConnectionException
            The session id was null, or empty.
        LavalinkException
            Raise when a invalid response type is received.
        ValueError
            Raised when a return type is set, and no data was received.
        BuildException
            Raised when the object could not be built.
        """
        session = self.session._get_session_id()

        try:
            player = await self.session.client.rest.player.update(
                self.guild_id,
                session,
                track=None,
                no_replace=False,
            )
        except LavalinkException:
            raise
        except BuildException:
            raise
        except ValueError:
            raise

        self._is_paused = True

        await self._update(player)

    async def skip(self, amount: int = 1) -> None:
        """
        Skip songs.

        skip a selected amount of songs in the queue.

        Parameters
        ----------
        amount : int
            The amount of songs you wish to skip.

        Raises
        ------
        SessionConnectionException
            The session id was null, or empty.
        LavalinkException
            Raise when a invalid response type is received.
        ValueError
            Raised when a return type is set, and no data was received.
        BuildException
            Raised when the object could not be built.  
        """
        session = self.session._get_session_id()

        if amount <= 0:
            raise ValueError(f"Skip amount cannot be 0 or negative. Value: {amount}")
        if len(self.queue) == 0:
            raise PlayerQueueException(self.guild_id, "No tracks in queue.")

        for _ in range(amount):
            if len(self._queue) == 0:
                break
            else:
                self._queue.pop(0)

        if len(self.queue) <= 0:
            try:
                player = await self.session.client.rest.player.update(
                    self.guild_id,
                    session,
                    track=None,
                    no_replace=False,
                )
            except LavalinkException:
                raise
            except BuildException:
                raise
            except ValueError:
                raise

            await self._update(player)
        else:
            try:
                player = await self.session.client.rest.player.update(
                    self.guild_id,
                    session,
                    track=self.queue[0],
                    no_replace=False,
                )
            except LavalinkException:
                raise
            except BuildException:
                raise
            except ValueError:
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
        SessionConnectionException
            The session id was null, or empty.
        LavalinkException
            Raise when a invalid response type is received.
        ValueError
            Raised when a return type is set, and no data was received.
        ValueError
            The track specified, does not exist in the current queue.
        ValueError
            The queue is empty.
        BuildException
            Raised when the object could not be built.  
        """
        if len(self.queue) == 0:
            raise ValueError("Queue is empty.")

        if isinstance(value, Track):
            index = self._queue.index(value)

        else:
            index = value

        try:
            self._queue.pop(index)
        except KeyError:
            if isinstance(value, Track):
                raise PlayerQueueException(
                    self.guild_id, f"Failed to remove song: {value.info.title}"
                )
            else:
                raise PlayerQueueException(
                    self.guild_id, f"Failed to remove song in position {value}"
                )

    async def clear(self) -> None:
        """
        Clear the queue.

        Clear the current queue, and also stop the audio from the player.

        Raises
        ------
        SessionConnectionException
            The session id was null, or empty.
        LavalinkException
            Raise when a invalid response type is received.
        ValueError
            Raised when a return type is set, and no data was received.
        BuildException
            Raised when the object could not be built.  
        """
        self._queue.clear()

        session = self.session._get_session_id()

        try:
            player = await self.session.client.rest.player.update(
                self.guild_id,
                session,
                track=None,
                no_replace=False,
            )
        except LavalinkException:
            raise
        except BuildException:
            raise

        await self._update(player)

    async def filter(self, filter: Filter | None = None):
        """
        Filter.

        Set, or remove a filter for the player.

        Parameters
        ----------
        filter : Filter
            the filter you wish to add.

        Raises
        ------
        SessionConnectionException
            The session id was null, or empty.
        LavalinkException
            Raise when a invalid response type is received.
        ValueError
            Raised when a return type is set, and no data was received.
        BuildException
            Raised when the object could not be built.  
        """
        session = self.session._get_session_id()

        self._filter = filter

        try:
            player = await self.session.client.rest.player.update(
                self.guild_id,
                session,
                filter=filter,
                no_replace=False,
            )
        except LavalinkException:
            raise
        except BuildException:
            raise

        await self._update(player)

    async def set_auto_play(self, toggle: UndefinedOr[bool] = UNDEFINED) -> bool:
        """Set auto play.

        whether or not to enable or disable auto play.

        Parameters
        ----------
        toggle : hikari.UndefinedOr[bool]
            Whether or not to toggle the auto play on or off. If left empty, it will toggle the current status.
        """
        if toggle == UNDEFINED:
            self._auto_play = not self._auto_play
            return self._auto_play

        self._auto_play = toggle
        return self._auto_play

    async def set_volume(self, volume: int) -> None:
        """Set the volume.

        The volume you wish to set for the player.

        Parameters
        ----------
        volume : int
            The volume you wish to set, from 0 to 1000.

        Raises
        ------
        SessionConnectionException
            The session id was null, or empty.
        LavalinkException
            Raise when a invalid response type is received.
        ValueError
            Raised when a return type is set, and no data was received.
        ValueError
            Raised if the value is above, or below 0, or 1000.
        BuildException
            Raised when the object could not be built.  
        """
        session = self.session._get_session_id()

        if volume < 0:
            raise ValueError(f"Volume cannot be below zero. Volume: {volume}")
        if volume > 1000:
            raise ValueError(f"Volume cannot be above 1000. Volume: {volume}")

        try:
            player = await self.session.client.rest.player.update(
                self.guild_id,
                session,
                volume=volume,
                no_replace=False,
            )
        except LavalinkException:
            raise
        except BuildException:
            raise
        except ValueError:
            raise

        await self._update(player)

    async def set_position(self, value: int) -> None:
        """Change the track position.

        Change the currently playing track's position.

        Parameters
        ----------
        value : int
            The value, of the position, in milliseconds.

        Raises
        ------
        SessionConnectionException
            The session id was null, or empty.
        LavalinkException
            Raise when a invalid response type is received.
        ValueError
            Raised when a return type is set, and no data was received.
        ValueError
            When the track position selected is not a valid position.
        BuildException
            Raised when the object could not be built.            
        """
        session = self.session._get_session_id()

        if value < 0:
            raise ValueError("Sorry, but a negative value is not allowed.")

        if len(self.queue) <= 0:
            raise PlayerQueueException(self.guild_id, "The queue is empty.")

        try:
            player = await self.session.client.rest.player.update(
                self.guild_id,
                session,
                position=value,
                no_replace=False,
            )
        except LavalinkException:
            raise
        except BuildException:
            raise
        except ValueError:
            raise

        await self._update(player)

    async def _update(self, player: ABCPlayer) -> None:
        # TODO: Somehow do the filter and the track.

        _logger.log(
            Trace.LEVEL,
            f"Updating player for channel: {self.channel_id} in guild: {self.guild_id}",
        )

        self._is_paused = player.is_paused
        self._voice = player.voice
        self._volume = player.volume

    async def _track_end_event(self, event: TrackEndEvent) -> None:
        self.session._get_session_id()

        if not self._auto_play:
            return

        if event.reason != TrackEndReasonType.FINISHED:
            return

        _logger.log(
            Trace.LEVEL,
            f"Auto-playing track for channel: {self.channel_id} in guild: {self.guild_id}",
        )

        if int(event.guild_id) == int(self.guild_id):
            _logger.log(
                Trace.LEVEL,
                f"Removing current track from queue for channel: {self.channel_id} in guild: {self.guild_id}",
            )
            try:
                await self.remove(0)
            except ValueError:
                await self.bot.dispatch(
                    QueueEmptyEvent(
                        _client=event.client, _session=event.session, _app=self.bot, guild_id=self.guild_id
                    )
                )
                return

            if len(self.queue) <= 0:
                _logger.log(
                    Trace.LEVEL,
                    f"Auto-play has empty queue for channel: {self.channel_id} in guild: {self.guild_id}",
                )
                await self.bot.dispatch(
                    QueueEmptyEvent(
                        _client=event.client, _session=event.session, _app=self.bot, guild_id=self.guild_id
                    )
                )
                return

            _logger.log(
                Trace.LEVEL,
                f"Auto-playing next track for channel: {self.channel_id} in guild: {self.guild_id}. Track title: {self.queue[0].info.title}",
            )

            await self.play()

            await self.bot.dispatch(
                QueueNextEvent(
                    _client=event.client,
                    _session=event.session,
                    _app=self.bot,
                    guild_id=self.guild_id,
                    track=self._queue[0],
                    old_track=event.track,
                )
            )

            _logger.log(
                Trace.LEVEL,
                f"Auto-playing successfully completed for channel: {self.channel_id} in guild: {self.guild_id}",
            )

    async def _player_update(self, event: PlayerUpdateEvent) -> None:
        if event.guild_id != self.guild_id:
            return

        self.position
        event.state.position


# MIT License

# Copyright (c) 2023 MPlatypus

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
