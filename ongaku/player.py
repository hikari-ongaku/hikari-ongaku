# MIT License

# Copyright (c) 2023-present MPlatypus

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
"""Player and entities related to Lavalink player objects."""

from __future__ import annotations

import asyncio
import datetime
import logging
import random
import typing

import hikari

from ongaku import errors
from ongaku import events
from ongaku import playlist
from ongaku import track
from ongaku.internal.logging import TRACE_LEVEL

if typing.TYPE_CHECKING:
    from ongaku import filters
    from ongaku import session
    from ongaku.api import builders


__all__: typing.Sequence[str] = (
    "ControllablePlayer",
    "Player",
    "State",
    "Voice",
)

_logger: typing.Final[logging.Logger] = logging.getLogger("ongaku.player")


class Player:
    """Player.

    All of the information about the player, for the specified guild.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#player)
    """

    __slots__: typing.Sequence[str] = (
        "_filters",
        "_guild_id",
        "_is_paused",
        "_state",
        "_track",
        "_voice",
        "_volume",
    )

    def __init__(
        self,
        *,
        guild_id: hikari.Snowflake,
        track: track.Track | None,
        volume: int,
        is_paused: bool,
        state: State,
        voice: Voice,
        filters: filters.Filters | None,
    ) -> None:
        self._guild_id = guild_id
        self._track = track
        self._volume = volume
        self._is_paused = is_paused
        self._state = state
        self._voice = voice
        self._filters = filters

    @property
    def guild_id(self) -> hikari.Snowflake:
        """The guild id this player is attached too."""
        return self._guild_id

    @property
    def track(self) -> track.Track | None:
        """The track the player is currently playing.

        !!! note
            If the track is `None` then there is no current track playing.
        """
        return self._track

    @property
    def volume(self) -> int:
        """The volume of the player."""
        return self._volume

    @property
    def is_paused(self) -> bool:
        """Whether the player is paused."""
        return self._is_paused

    @property
    def state(self) -> State:
        """The player's state."""
        return self._state

    @property
    def voice(self) -> Voice:
        """The player's voice state."""
        return self._voice

    @property
    def filters(self) -> filters.Filters | None:
        """The filter object."""
        return self._filters

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Player):
            return False

        return (
            self.guild_id == other.guild_id
            and self.track == other.track
            and self.volume == other.volume
            and self.is_paused == other.is_paused
            and self.state == other.state
            and self.voice == other.voice
            and self.filters == other.filters
        )


class State:
    """State.

    All the information for the players current state.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#player-state)
    """

    _test: typing.Mapping[str, typing.Any] = {}

    __slots__: typing.Sequence[str] = (
        "_connected",
        "_ping",
        "_position",
        "_time",
    )

    def __init__(
        self,
        *,
        time: datetime.datetime,
        position: int,
        connected: bool,
        ping: int,
    ) -> None:
        self._time = time
        self._position = position
        self._connected = connected
        self._ping = ping

    @classmethod
    def empty(cls) -> State:
        """Empty.

        Build an empty [State][ongaku.player.State] object.
        """
        return cls(
            time=datetime.datetime.fromtimestamp(0, tz=datetime.timezone.utc),
            position=0,
            connected=False,
            ping=-1,
        )

    @property
    def time(self) -> datetime.datetime:
        """The current datetime."""
        return self._time

    @property
    def position(self) -> int:
        """The position of the track in milliseconds."""
        return self._position

    @property
    def connected(self) -> bool:
        """Whether Lavalink is connected to the voice gateway."""
        return self._connected

    @property
    def ping(self) -> int:
        """Ping.

        The ping of the session to the Discord voice server.
        This value is in milliseconds.

        !!! note
            If this value is `-1`, then the player is not connected.
        """
        return self._ping

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, State):
            return False

        return (
            self.time == other.time
            and self.position == other.position
            and self.connected == other.connected
            and self.ping == other.ping
        )


class Voice:
    """Voice.

    All of the Player Voice information.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#voice-state)
    """

    __slots__: typing.Sequence[str] = (
        "_endpoint",
        "_session_id",
        "_token",
    )

    def __init__(self, *, token: str, endpoint: str, session_id: str) -> None:
        self._token = token
        self._endpoint = endpoint
        self._session_id = session_id

    @classmethod
    def empty(cls) -> Voice:
        """Empty.

        Build an empty [Voice][ongaku.player.Voice] object.
        """
        return cls(token="", endpoint="", session_id="")

    @property
    def token(self) -> str:
        """The Discord voice token to authenticate with."""
        return self._token

    @property
    def endpoint(self) -> str:
        """The Discord voice endpoint to connect to."""
        return self._endpoint

    @property
    def session_id(self) -> str:
        """The Discord voice session id to authenticate with."""
        return self._session_id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Voice):
            return False

        return (
            self.token == other.token
            and self.endpoint == other.endpoint
            and self.session_id == other.session_id
        )


class ControllablePlayer(Player):
    """Controllable Player.

    A player object that can be controlled and manipulated.
    """

    def __init__(
        self,
        session: session.ControllableSession,
        guild: hikari.SnowflakeishOr[hikari.Guild],
    ) -> None:
        self._session = session
        self._guild_id = hikari.Snowflake(guild)
        self._channel_id = None
        self._is_alive = False
        self._is_paused = True
        self._voice: Voice = Voice.empty()
        self._state: State = State.empty()
        self._queue: typing.MutableSequence[track.Track] = []
        self._filters: filters.Filters | None = None
        self._connected: bool = False
        self._session_id: str | None = None
        self._volume: int = -1
        self._autoplay: bool = True
        self._position: int = 0
        self._loop = False
        self._track = None

        session.app.event_manager.subscribe(events.TrackEndEvent, self._track_end_event)
        session.app.event_manager.subscribe(
            events.PlayerUpdateEvent,
            self._player_update_event,
        )

    @property
    def session(self) -> session.ControllableSession:
        """The session this player is included in."""
        return self._session

    @property
    def app(self) -> hikari.GatewayBotAware:
        """The session this player is included in."""
        return self._session.app

    @property
    def channel_id(self) -> hikari.Snowflake | None:
        """The `channel id` this player is attached too.

        `None` if not connected to a channel.
        """
        return self._channel_id

    @property
    def is_alive(self) -> bool:
        """Is alive.

        Whether the player is alive and attached to lavalink.
        """
        return self._is_alive

    @property
    def position(self) -> int:
        """Position.

        The position of the track in milliseconds.
        """
        return self._position

    @property
    def autoplay(self) -> bool:
        """Autoplay.

        Whether or not the next song will play, when this song ends.
        """
        return self._autoplay

    @property
    def loop(self) -> bool:
        """Whether the current track will play again."""
        return self._loop

    @property
    def connected(self) -> bool:
        """Connected.

        Whether or not the player is connected to discords gateway.
        """
        return self._connected

    @property
    def queue(self) -> typing.Sequence[track.Track]:
        """The current queue of tracks."""
        return self._queue

    async def connect(
        self,
        channel: hikari.SnowflakeishOr[hikari.GuildVoiceChannel],
        /,
        *,
        mute: bool = False,
        deaf: bool = True,
    ) -> None:
        """Connect.

        Connect the current player to a voice channel.

        Example
        -------
        ```py
        await player.connect(channel_id)
        ```

        Parameters
        ----------
        channel
            The channel (or channel id) that you wish to connect the bot to.
        mute
            Whether or not to mute the player.
        deaf
            Whether or not to deafen the player.

        Raises
        ------
        SessionStartError
            Raised when the players session has not yet been started.
        PlayerConnectError
            Raised when the voice state of the bot cannot be updated,
            or the voice events required could not be received.
        RestEmptyError
            Raised when a return type was requested, yet nothing was received.
        RestStatusError
            Raised when nothing was received, but a 4XX/5XX error was reported.
        RestRequestError
            Raised when a rest error is returned with a 4XX/5XX error.
        BuildError
            Raised when a construction of a ABC class fails.
        """
        session_id = self.session.session_id
        if session_id is None:
            raise errors.SessionStartError

        _logger.log(
            TRACE_LEVEL,
            "Attempting connection to voice channel: %s in guild: %s",
            hikari.Snowflake(channel),
            self.guild_id,
        )

        self._channel_id = hikari.Snowflake(channel)

        try:
            await self.app.update_voice_state(
                self.guild_id,
                self._channel_id,
                self_mute=mute,
                self_deaf=deaf,
            )
        except Exception as err:
            raise errors.PlayerConnectError(str(err)) from err

        _logger.log(
            TRACE_LEVEL,
            "waiting for voice events for channel: %s in guild: %s",
            self.channel_id,
            self.guild_id,
        )

        try:
            state_event, server_event = await asyncio.gather(
                self.app.event_manager.wait_for(
                    hikari.VoiceStateUpdateEvent,
                    timeout=5,
                ),
                self.app.event_manager.wait_for(
                    hikari.VoiceServerUpdateEvent,
                    timeout=5,
                ),
            )
        except TimeoutError as err:
            raise errors.PlayerConnectError(
                "Could not connect to voice channel due to unreceived events.",
            ) from err

        if server_event.raw_endpoint is None:
            raise errors.PlayerConnectError(
                "Endpoint missing for attempted server connection.",
            ) from None

        _logger.log(
            TRACE_LEVEL,
            "Successfully received events for channel: %s in guild: %s",
            self.channel_id,
            self.guild_id,
        )

        new_voice = Voice(
            token=server_event.token,
            endpoint=server_event.raw_endpoint,
            session_id=state_event.state.session_id,
        )

        self._voice = new_voice

        player = await self.session.client.rest.update_player(
            session_id,
            self.guild_id,
            voice=new_voice,
            no_replace=False,
            session=self.session,
        )

        self._is_alive = True

        _logger.log(
            TRACE_LEVEL,
            "Successfully connected to channel: %s in guild: %s",
            self.channel_id,
            self.guild_id,
        )

        self._update(player)

    async def disconnect(self) -> None:
        """
        Disconnect.

        Disconnect the player from the discord channel,
        and stop the currently playing track.

        Example
        -------
        ```py
        await player.disconnect()
        ```

        Raises
        ------
        SessionStartError
            Raised when the players session has not yet been started.
        RestEmptyError
            Raised when a return type was requested, yet nothing was received.
        RestStatusError
            Raised when nothing was received, but a 4XX/5XX error was reported.
        RestRequestError
            Raised when a rest error is returned with a 4XX/5XX error.
        BuildError
            Raised when a construction of a ABC class fails.
        """
        session_id = self.session.session_id
        if session_id is None:
            raise errors.SessionStartError

        await self.clear()

        _logger.log(
            TRACE_LEVEL,
            "Attempting to delete player for channel: %s in guild: %s",
            self.channel_id,
            self.guild_id,
        )

        await self.session.client.rest.delete_player(
            session_id,
            self._guild_id,
            session=self.session,
        )

        _logger.log(
            TRACE_LEVEL,
            "Successfully deleted player for channel: %s in guild: %s",
            self.channel_id,
            self.guild_id,
        )

        self._is_alive = False

        _logger.log(
            TRACE_LEVEL,
            "Updating voice state for channel: %s in guild: %s",
            self.channel_id,
            self.guild_id,
        )

        await self.app.update_voice_state(self.guild_id, None)

        _logger.log(
            TRACE_LEVEL,
            "Successfully updated voice state for channel: %s in guild: %s",
            self.channel_id,
            self.guild_id,
        )

    async def play(
        self,
        track: track.Track | None = None,
        /,
        *,
        requestor: hikari.SnowflakeishOr[hikari.PartialUser] | None = None,
    ) -> None:
        """Play.

        Play a new track, or start the playing of the queue.

        Example
        -------
        ```py
        await player.play(track)
        ```

        Parameters
        ----------
        track
            The track you wish to play. If none, pulls from the queue.
        requestor
            The member who requested the track.

        Raises
        ------
        SessionStartError
            Raised when the players session has not yet been started.
        PlayerConnectError
            Raised when the player is not connected to a channel.
        RestEmptyError
            Raised when a return type was requested, yet nothing was received.
        RestStatusError
            Raised when nothing was received, but a 4XX/5XX error was reported.
        RestRequestError
            Raised when a rest error is returned with a 4XX/5XX error.
        BuildError
            Raised when a construction of a ABC class fails.
        """
        session_id = self.session.session_id
        if session_id is None:
            raise errors.SessionStartError

        if self.channel_id is None:
            raise errors.PlayerConnectError("Not connected to a channel.")

        if len(self.queue) == 0 and track is None:
            raise errors.PlayerQueueError("Queue is empty.")

        if track:
            if requestor:
                track._requestor = hikari.Snowflake(requestor)

            self._queue.insert(0, track)

        player = await self.session.client.rest.update_player(
            session_id,
            self.guild_id,
            track=self.queue[0],
            no_replace=False,
            session=self.session,
        )

        self._is_paused = False

        self._update(player)

    def add(
        self,
        tracks: typing.Sequence[track.Track] | playlist.Playlist | track.Track,
        *,
        requestor: hikari.SnowflakeishOr[hikari.PartialUser] | None = None,
    ) -> None:
        """
        Add tracks.

        Add tracks to the queue.

        !!! note
            This will not automatically start playing the songs.
            please call `.play()` after, with no track,
            if the player is not already playing.

        Example
        -------
        ```py
        await player.add(tracks)
        ```

        Parameters
        ----------
        tracks
            The list of tracks or a singular track you wish to add to the queue.
        requestor
            The user/member who requested the song.
        """
        new_requestor = None

        if requestor:
            new_requestor = hikari.Snowflake(requestor)

        track_count = 0

        if isinstance(tracks, track.Track):
            if new_requestor:
                tracks._requestor = new_requestor
            self._queue.append(tracks)
            track_count = 1
            return

        if isinstance(tracks, playlist.Playlist):
            tracks = tracks.tracks

        for t in tracks:
            if new_requestor:
                t._requestor = new_requestor
            self._queue.append(t)
            track_count += 1

        _logger.log(
            TRACE_LEVEL,
            "Successfully added %s track(s) to %s",
            track_count,
            self.guild_id,
        )

    async def pause(self, value: bool | None = None, /) -> None:
        """
        Pause the player.

        Allows for the user to pause the currently playing track on this player.

        !!! info
            `True` will force pause the player, `False` will force unpause the player.
            Leaving it empty, will toggle it from its current state.

        Example
        -------
        ```py
        await player.pause()
        ```

        Parameters
        ----------
        value
            How you wish to pause the bot.

        Raises
        ------
        SessionStartError
            Raised when the players session has not yet been started.
        RestEmptyError
            Raised when a return type was requested, yet nothing was received.
        RestStatusError
            Raised when nothing was received, but a 4XX/5XX error was reported.
        RestRequestError
            Raised when a rest error is returned with a 4XX/5XX error.
        BuildError
            Raised when a construction of a ABC class fails.
        """
        session_id = self.session.session_id
        if session_id is None:
            raise errors.SessionStartError

        if value:
            self._is_paused = value
        else:
            self._is_paused = not self.is_paused

        player = await self.session.client.rest.update_player(
            session_id,
            self.guild_id,
            paused=self.is_paused,
            session=self.session,
        )

        _logger.log(
            TRACE_LEVEL,
            "Successfully set paused state to %s in guild %s",
            self.is_paused,
            self.guild_id,
        )

        self._update(player)

    async def stop(self) -> None:
        """
        Stop current track.

        Stops the audio, by setting the song to none.

        !!! note
            This does not touch the current queue, just clears the player of its track.

        Example
        -------
        ```py
        await player.stop()
        ```

        Raises
        ------
        SessionStartError
            Raised when the players session has not yet been started.
        RestEmptyError
            Raised when a return type was requested, yet nothing was received.
        RestStatusError
            Raised when nothing was received, but a 4XX/5XX error was reported.
        RestRequestError
            Raised when a rest error is returned with a 4XX/5XX error.
        BuildError
            Raised when a construction of a ABC class fails.
        """
        session_id = self.session.session_id
        if session_id is None:
            raise errors.SessionStartError

        player = await self.session.client.rest.update_player(
            session_id,
            self.guild_id,
            track=None,
            no_replace=False,
            session=self.session,
        )

        self._is_paused = True

        _logger.log(
            TRACE_LEVEL,
            "Successfully stopped track in guild %s",
            self.guild_id,
        )

        self._update(player)

    def shuffle(self) -> None:
        """Shuffle.

        Shuffle the current queue.

        !!! note
            This will not touch the first track.

        Raises
        ------
        PlayerQueueError
            Raised when the queue has 2 or less tracks in it.
        """
        if len(self.queue) <= 2:
            raise errors.PlayerQueueError(
                "Queue must have more than 2 tracks to shuffle.",
            )

        new_queue = list(self.queue)

        first_track = new_queue.pop(0)

        random.shuffle(new_queue)

        new_queue.insert(0, first_track)

        self._queue = new_queue

        _logger.log(
            TRACE_LEVEL,
            "Successfully shuffled queue in guild %s",
            self.guild_id,
        )

    async def skip(self, amount: int = 1, /) -> None:
        """
        Skip songs.

        skip a selected amount of songs in the queue.

        Example
        -------
        ```py
        await player.skip()
        ```

        Parameters
        ----------
        amount
            The amount of songs you wish to skip.

        Raises
        ------
        SessionStartError
            Raised when the players session has not yet been started.
        ValueError
            Raised when the amount set is 0 or negative.
        PlayerQueueError
            Raised when the queue is empty.
        RestEmptyError
            Raised when a return type was requested, yet nothing was received.
        RestStatusError
            Raised when nothing was received, but a 4XX/5XX error was reported.
        RestRequestError
            Raised when a rest error is returned with a 4XX/5XX error.
        BuildError
            Raised when a construction of a ABC class fails.
        """
        if amount <= 0:
            raise ValueError(
                amount,
            )  # FIXME: Not sure if I like this.  # noqa: TD001, TD002, TD003
        if len(self.queue) == 0:
            raise errors.PlayerQueueError("Queue is empty.")

        removed_tracks = 0
        for _ in range(amount):
            if len(self._queue) == 0:
                break
            self._queue.pop(0)
            removed_tracks += 1

        _logger.log(
            TRACE_LEVEL,
            "Successfully removed %s track(s) out of %s in guild %s",
            removed_tracks,
            amount,
            self.guild_id,
        )

        session_id = self.session.session_id
        if session_id is None:
            raise errors.SessionStartError

        if len(self.queue) <= 0:
            player = await self.session.client.rest.update_player(
                session_id,
                self.guild_id,
                track=None,
                no_replace=False,
                session=self.session,
            )

            self._update(player)
        else:
            player = await self.session.client.rest.update_player(
                session_id,
                self.guild_id,
                track=self.queue[0],
                no_replace=False,
                session=self.session,
            )

            self._update(player)

        _logger.log(TRACE_LEVEL, "Successfully skipped track in %s", self.guild_id)

    def remove(self, value: track.Track | int, /) -> None:
        """Remove track.

        Removes the track, or the track in that position.

        !!! warning
            This does not stop the track if its in the first position.

        Example
        -------
        ```py
        await player.remove()
        ```

        Parameters
        ----------
        value
            Remove a selected track. If [Track][ongaku.track.Track],
            then it will remove the first occurrence of that track.
            If an integer, it will remove the track at that position.

        Raises
        ------
        PlayerQueueError
            Raised when the removal of a track fails.
        """
        if len(self.queue) == 0:
            raise errors.PlayerQueueError("Queue is empty.")

        try:
            index = (
                self._queue.index(value) if isinstance(value, track.Track) else value
            )
        except ValueError as err:
            raise errors.PlayerQueueError(
                "Failed to remove song.",
            ) from err

        try:
            self._queue.pop(index)
        except IndexError as err:
            raise errors.PlayerQueueError(
                "Failed to remove song in specified position.",
            ) from err

        _logger.log(TRACE_LEVEL, "Successfully removed track in %s", self.guild_id)

    async def clear(self) -> None:
        """
        Clear the queue.

        Clear the current queue, and also stop the audio from the player.

        Example
        -------
        ```py
        player.clear()
        ```

        Raises
        ------
        SessionStartError
            Raised when the players session has not yet been started.
        RestEmptyError
            Raised when a return type was requested, yet nothing was received.
        RestStatusError
            Raised when nothing was received, but a 4XX/5XX error was reported.
        RestRequestError
            Raised when a rest error is returned with a 4XX/5XX error.
        BuildError
            Raised when a construction of a ABC class fails.
        """
        self._queue.clear()

        session_id = self.session.session_id
        if session_id is None:
            raise errors.SessionStartError

        player = await self.session.client.rest.update_player(
            session_id,
            self.guild_id,
            track=None,
            no_replace=False,
            session=self.session,
        )

        self._update(player)

        _logger.log(TRACE_LEVEL, "Successfully cleared queue in %s", self.guild_id)

    def set_autoplay(self, enable: bool | None = None, /) -> bool:
        """
        Set autoplay.

        whether to enable or disable autoplay.

        Example
        -------
        ```py
        await player.set_autoplay()
        ```

        Parameters
        ----------
        enable
            Whether or not to enable autoplay.
            If left empty, it will toggle the current status.
        """
        if enable:
            self._autoplay = enable
            return self._autoplay

        self._autoplay = not self._autoplay

        return self._autoplay

    async def set_volume(self, volume: int = 100, /) -> None:
        """
        Set the volume.

        The volume you wish to set for the player.

        Example
        -------
        ```py
        await player.set_volume(10)
        ```

        !!! note
            If you don't set a value to volume, it will simply become 100 (The default.)

        Parameters
        ----------
        volume
            The volume you wish to set, from 0 to 1000.

        Raises
        ------
        SessionStartError
            Raised when the players session has not yet been started.
        ValueError
            Raised when the value is below 0, or above 1000.
        RestEmptyError
            Raised when a return type was requested, yet nothing was received.
        RestStatusError
            Raised when nothing was received, but a 4XX/5XX error was reported.
        RestRequestError
            Raised when a rest error is returned with a 4XX/5XX error.
        BuildError
            Raised when a construction of a ABC class fails.
        """
        session_id = self.session.session_id
        if session_id is None:
            raise errors.SessionStartError

        if volume:
            if volume < 0:
                raise ValueError("Volume cannot be below zero.")
            if volume > 1000:
                raise ValueError("Volume cannot be above 1000.")

        player = await self.session.client.rest.update_player(
            session_id,
            self.guild_id,
            volume=volume,
            no_replace=False,
            session=self.session,
        )

        self._update(player)

        _logger.log(
            TRACE_LEVEL,
            "Successfully set volume to %s in %s",
            volume,
            self.guild_id,
        )

    async def set_position(self, value: int, /) -> None:
        """
        Set the position.

        Change the currently playing track's position.

        Example
        -------
        ```py
        await player.set_position(10000)
        ```

        Parameters
        ----------
        value
            The value, of the position, in milliseconds.

        Raises
        ------
        SessionStartError
            Raised when the players session has not yet been started.
        ValueError
            Raised when the position given is negative,
            or the current tracks length is greater than the length given.
        PlayerQueueError
            Raised when the queue is empty.
        RestEmptyError
            Raised when a return type was requested, yet nothing was received.
        RestStatusError
            Raised when nothing was received, but a 4XX/5XX error was reported.
        RestRequestError
            Raised when a rest error is returned with a 4XX/5XX error.
        BuildError
            Raised when a construction of a ABC class fails.
        """
        session_id = self.session.session_id
        if session_id is None:
            raise errors.SessionStartError

        if value <= 0:
            raise ValueError("Negative value is not allowed.")

        if len(self.queue) <= 0:
            raise errors.PlayerQueueError("Queue is empty.")

        if self.queue[0].info.length < value:
            raise ValueError(
                "A value greater than the current tracks length is not allowed.",
            )

        player = await self.session.client.rest.update_player(
            session_id,
            self.guild_id,
            position=value,
            no_replace=False,
            session=self.session,
        )

        self._update(player)

        _logger.log(
            TRACE_LEVEL,
            "Successfully set position (%s) to track in %s",
            value,
            self.guild_id,
        )

    async def set_filters(
        self,
        filters: builders.FiltersBuilder | None = None,
        /,
    ) -> None:
        """Set Filters.

        Set a new filter for the player.

        Parameters
        ----------
        filters
            The filter to set the player with.
        """
        session_id = self.session.session_id
        if session_id is None:
            raise errors.SessionStartError

        player = await self.session.client.rest.update_player(
            session_id,
            self.guild_id,
            filters=filters,
            session=self.session,
        )

        _logger.log(
            TRACE_LEVEL,
            "Successfully updated filters in guild %s",
            self.guild_id,
        )

        self._update(player)

    def set_loop(self, enable: bool | None = None, /) -> bool:
        """
        Set loop.

        whether to enable or disable looping of the current track.

        Example
        -------
        ```py
        await player.set_loop()
        ```

        Parameters
        ----------
        enable
            Whether or not to enable looping.
            If left empty, it will toggle the current status.
        """
        if enable:
            self._loop = enable
            return self._loop

        self._loop = not self._loop

        return self._loop

    async def transfer(
        self,
        *,
        session: session.ControllableSession,
    ) -> ControllablePlayer:
        """Transfer.

        Transfer this player to another session.

        !!! warning
            This will kill the current player, and return a new player.

        Parameters
        ----------
        session
            The session you wish to add the new player to.

        Returns
        -------
        Player
            The new player.
        """
        _logger.log(
            TRACE_LEVEL,
            "Attempting to transfer player in %s from session (%s) to session (%s)",
            self.guild_id,
            self.session.name,
            session.name,
        )

        new_player = ControllablePlayer(session, self.guild_id)

        new_player.add(self.queue)

        if self.connected and self.channel_id:
            await self.disconnect()

            await new_player.connect(self.channel_id)
            if self.is_paused is False:
                await new_player.play()
                await new_player.set_position(self.position)

        _logger.log(
            TRACE_LEVEL,
            "Successfully transferred player in %s from session (%s) to session (%s)",
            self.guild_id,
            self.session.name,
            session.name,
        )

        return new_player

    def _update(self, player: Player, /) -> None:
        _logger.log(
            TRACE_LEVEL,
            "Updating player for channel: %s in guild: %s",
            self.channel_id,
            self.guild_id,
        )

        self._volume = player.volume
        self._is_paused = player.is_paused
        self._state = player.state
        self._voice = player.voice
        self._filters = player.filters
        self._connected = player.state.connected
        self._track = player.track

    async def _track_end_event(self, event: events.TrackEndEvent) -> None:
        session_id = self.session.session_id
        if session_id is None:
            raise errors.SessionStartError

        if event.guild_id != self.guild_id:
            return

        self._track = None

        if not self.autoplay:
            return

        if event.reason not in (
            track.TrackEndReasonType.FINISHED,
            track.TrackEndReasonType.LOADFAILED,
        ):
            return

        _logger.log(
            TRACE_LEVEL,
            "Auto-playing track for channel: %s in guild: %s",
            self.channel_id,
            self.guild_id,
        )

        if len(self.queue) == 0:
            _logger.log(
                TRACE_LEVEL,
                "queue is empty for channel: %s in guild: %s. Skipping.",
                self.channel_id,
                self.guild_id,
            )
            return

        if len(self.queue) == 1 and not self.loop:
            _logger.log(
                TRACE_LEVEL,
                "queue is empty for channel: %s in guild: %s.",
                self.channel_id,
                self.guild_id,
            )
            new_event = events.QueueEmptyEvent.from_session(
                self.session,
                guild_id=self.guild_id,
                old_track=self.queue[0],
            )

            self.remove(0)

            self.app.event_manager.dispatch(new_event, return_tasks=False)

            return

        if not self.loop:
            _logger.log(
                TRACE_LEVEL,
                "Autoplay for channel: %s in guild: %s. Removing old song.",
                self.channel_id,
                self.guild_id,
            )
            self.remove(0)

        _logger.log(
            TRACE_LEVEL,
            "Auto-playing next track for channel: %s in guild: %s. Track title: %s",
            self.channel_id,
            self.guild_id,
            self.queue[0].info.title,
        )

        await self.play()

        queue_next_event = events.QueueNextEvent.from_session(
            self.session,
            guild_id=self.guild_id,
            track=self._queue[0],
            old_track=event.track,
        )

        self.app.event_manager.dispatch(
            queue_next_event,
            return_tasks=False,
        )

        _logger.log(
            TRACE_LEVEL,
            "Auto-playing successfully completed for channel: %s in guild: %s",
            self.channel_id,
            self.guild_id,
        )

    async def _player_update_event(self, event: events.PlayerUpdateEvent) -> None:
        if event.guild_id != self.guild_id:
            return

        _logger.log(
            TRACE_LEVEL,
            "Updating player state in %s",
            self.guild_id,
        )

        if not event.state.connected and self.connected:
            await self.stop()

        _logger.log(
            TRACE_LEVEL,
            "Successfully updated player state in %s",
            self.guild_id,
        )

        self._state = event.state
        self._connected = event.state.connected
