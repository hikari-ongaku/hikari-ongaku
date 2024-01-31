"""Events.

All of the hikari events for ongaku, are here!
"""

from __future__ import annotations

import typing as t

import attrs
import hikari

from .base import PayloadBase
from .base import PayloadBaseApp
from .track import Track
from .. import enums
from .lavalink import ExceptionError

__all__ = (
    "OngakuEvent",
    "ReadyEvent",
    "StatsMemory",
    "StatsCpu",
    "StatsFrameStatistics",
    "StatisticsEvent",
    "WebsocketClosedEvent",
    "TrackStartEvent",
    "TrackEndEvent",
    "TrackExceptionEvent",
    "TrackStuckEvent",
    "QueueEmptyEvent",
    "QueueNextEvent",
)


@attrs.define
class OngakuEvent(hikari.Event):
    """Ongaku Event.

    The base event, that all other Ongaku events are attached too.
    """

    _app: hikari.RESTAware

    @property
    def app(self) -> hikari.RESTAware:
        """The application or bot, that this event is attached too."""
        return self._app


@attrs.define
class ReadyEvent(OngakuEvent, PayloadBaseApp[dict[str, t.Any]]):
    """Ready event.

    The event that is dispatched, when lavalink is ready for new players, discord connections, and song requests.
    """

    resumed: bool
    """Whether or not the session has been resumed, or is a new session."""
    session_id: str
    """The lavalink session id, for the current session."""

    @classmethod
    def _from_payload(
        cls, payload: t.Mapping[str, t.Any], *, app: hikari.RESTAware
    ) -> ReadyEvent:
        resumed = payload.get("resumed")
        if resumed is None:
            raise ValueError("resumed cannot be none.")
        if not isinstance(resumed, bool):
            raise TypeError("resumed must be a boolean.")
        
        session_id = payload.get("sessionId")
        if session_id is None:
            raise ValueError("sessionId cannot be none.")
        if not isinstance(session_id, str):
            raise TypeError("sessionId must be a string.")

        return cls(app, resumed, session_id)


@attrs.define
class StatsMemory(PayloadBase[dict[str, t.Any]]):
    """
    All of the Statistics Memory information.

    Find out more [here](https://lavalink.dev/api/websocket.html#memory).
    """

    free: int
    """The amount of free memory in bytes"""
    used: int
    """The amount of used memory in bytes"""
    allocated: int
    """The amount of allocated memory in bytes"""
    reservable: int
    """The amount of reservable memory in bytes"""

    @classmethod
    def _from_payload(cls, payload: t.Mapping[str, t.Any]) -> StatsMemory:
        free = payload.get("free")
        if free is None:
            raise ValueError("free cannot be none.")
        if not isinstance(free, int):
            raise TypeError("free must be a integer.")
        
        used = payload.get("used")
        if used is None:
            raise ValueError("used cannot be none.")
        if not isinstance(used, int):
            raise TypeError("used must be a integer.")
        
        allocated = payload.get("allocated")
        if allocated is None:
            raise ValueError("allocated cannot be none.")
        if not isinstance(allocated, int):
            raise TypeError("allocated must be a integer.")
        
        reservable = payload.get("reservable")
        if reservable is None:
            raise ValueError("reservable cannot be none.")
        if not isinstance(reservable, int):
            raise TypeError("reservable must be a integer.")

        return cls(
            free, 
            used, 
            allocated, 
            reservable
        )


@attrs.define
class StatsCpu(PayloadBase[dict[str, t.Any]]):
    """
    All of the Statistics CPU information.

    Find out more [here](https://lavalink.dev/api/websocket.html#cpu).
    """

    cores: int
    """The amount of cores the server has."""
    system_load: float
    """The system load of the server."""
    lavalink_load: float
    """The load of Lavalink on the server."""

    @classmethod
    def _from_payload(cls, payload: t.Mapping[str, t.Any]) -> StatsCpu:
        cores = payload.get("cores")
        if cores is None:
            raise ValueError("cores cannot be none.")
        if not isinstance(cores, int):
            raise TypeError("cores must be a integer.")

        system_load = payload.get("systemLoad")
        if system_load is None:
            raise ValueError("systemLoad cannot be none.")
        if isinstance(system_load, (int, float)):
            system_load = float(system_load)
        else:
            raise TypeError("systemLoad must be a float.")
        
        lavalink_load = payload.get("lavalinkLoad")
        if lavalink_load is None:
            raise ValueError("lavalinkLoad cannot be none.")
        if isinstance(lavalink_load, (int, float)):
            lavalink_load = float(lavalink_load)
        else:
            raise TypeError("lavalinkLoad must be a float.")

        return cls(cores, system_load, lavalink_load)


@attrs.define
class StatsFrameStatistics(PayloadBase[dict[str, t.Any]]):
    """
    All of the Statistics frame statistics information.

    Find out more [here](https://lavalink.dev/api/websocket.html#frame-stats).
    """

    sent: int
    """The amount of frames sent to Discord."""
    nulled: int
    """The amount of frames that were nulled."""
    deficit: int
    """The difference between sent frames and the expected amount of frames."""

    @classmethod
    def _from_payload(cls, payload: t.Mapping[str, t.Any]) -> StatsFrameStatistics:
        sent = payload.get("sent")
        if sent is None:
            raise ValueError("sent cannot be none.")
        if not isinstance(sent, int):
            raise TypeError("sent must be a integer.")
        
        nulled = payload.get("nulled")
        if nulled is None:
            raise ValueError("nulled cannot be none.")
        if not isinstance(nulled, int):
            raise TypeError("nulled must be a integer.")
        
        deficit = payload.get("deficit")
        if deficit is None:
            raise ValueError("deficit cannot be none.")
        if not isinstance(deficit, int):
            raise TypeError("deficit must be a integer.")

        return cls(sent, nulled, deficit)


@attrs.define
class StatisticsEvent(OngakuEvent, PayloadBaseApp[dict[str, t.Any]]):
    """
    All of the Statistics information.

    Find out more [here](https://lavalink.dev/api/websocket.html#stats-object).
    """

    _app: hikari.RESTAware

    players: int
    """The amount of players connected to the session."""
    playing_players: int
    """The amount of players playing a track."""
    uptime: int
    """The uptime of the session in milliseconds."""
    memory: StatsMemory
    """The memory stats of the session."""
    cpu: StatsCpu
    """The cpu stats of the session."""
    frame_statistics: StatsFrameStatistics | None
    """The frame stats of the session."""

    @classmethod
    def _from_payload(cls, payload: t.Mapping[str, t.Any], *, app: hikari.RESTAware):
        players = payload.get("players")
        if players is None:
            raise ValueError("players cannot be none.")
        if not isinstance(players, int):
            raise TypeError("players must be a integer.")
        
        playing_players = payload.get("playingPlayers")
        if playing_players is None:
            raise ValueError("playingPlayers cannot be none.")
        if not isinstance(playing_players, int):
            raise TypeError("playingPlayers must be a integer.")
        
        uptime = payload.get("uptime")
        if uptime is None:
            raise ValueError("uptime cannot be none.")
        if not isinstance(uptime, int):
            raise TypeError("uptime must be a integer.")

        memory = payload.get("memory")
        if memory is None:
            raise ValueError("memory cannot be none.")
        try:
            memory = StatsMemory._from_payload(memory)
        except TypeError:
            raise
        except ValueError:
            raise

        cpu = payload.get("cpu")
        if cpu is None:
            raise ValueError("cpu cannot be none.")
        try:
            cpu = StatsCpu._from_payload(cpu)
        except TypeError:
            raise
        except ValueError:
            raise
        
        frame_statistics = payload.get("frameStats")

        if frame_statistics is not None:
            try:
                frame_statistics = StatsFrameStatistics._from_payload(frame_statistics)
            except TypeError:
                raise
            except ValueError:
                raise

        return cls(app, players, playing_players, uptime, memory, cpu, frame_statistics)


@attrs.define
class WebsocketClosedEvent(OngakuEvent, PayloadBaseApp[dict[str, t.Any]]):
    """Websocket closed event.

    The event that is sent out, when a websocket closes.
    """

    _app: hikari.RESTAware

    guild_id: hikari.Snowflake
    """The guild that had their websocket closed in."""
    code: int
    """The discord error code that [discord](https://discord.com/developers/docs/topics/opcodes-and-status-codes#voice-voice-close-event-codes) responded with."""
    reason: str
    """	The close reason."""
    by_remote: bool
    """Whether the connection was closed by Discord."""

    @classmethod
    def _from_payload(
        cls, payload: t.Mapping[str, t.Any], *, app: hikari.RESTAware
    ) -> WebsocketClosedEvent:
        guild_id = payload.get("guildId")
        if guild_id is None:
            raise ValueError("guildId cannot be none.")
        if isinstance(guild_id, (str, int)):
            guild_id = int(guild_id)
        else:
            raise TypeError("guildId must be a integer.")
        
        code = payload.get("code")
        if code is None:
            raise ValueError("code cannot be none.")
        if not isinstance(code, int):
            raise TypeError("code must be a integer.")
        
        reason = payload.get("reason")
        if reason is None:
            raise ValueError("reason cannot be none.")
        if not isinstance(reason, str):
            raise TypeError("reason must be a string.")
        
        by_remote = payload.get("byRemote")
        if by_remote is None:
            raise ValueError("byRemote cannot be none.")
        if not isinstance(by_remote, bool):
            raise TypeError("byRemote must be a boolean.")
        

        return cls(app, hikari.Snowflake(guild_id), code, reason, by_remote) 


@attrs.define
class TrackBase(OngakuEvent, PayloadBaseApp[dict[str, t.Any]]):
    """Base track class.

    The class that all Track based classes, inherit.
    """

    guild_id: hikari.Snowflake
    """The guild the track is playing in."""
    track: Track
    """The track that the event is attached too."""

    @classmethod
    def _from_payload(
        cls, payload: t.Mapping[str, t.Any], *, app: hikari.RESTAware
    ) -> TrackBase:
        guild_id = payload.get("guildId")
        if guild_id is None:
            raise ValueError("guildId cannot be none.")
        if isinstance(guild_id, (str, int)):
            guild_id = int(guild_id)
        else:
            raise TypeError("guildId must be a integer.")
        
        track = payload.get("track")
        if track is None:
            raise ValueError("track cannot be none.")
        try:
            track = Track._from_payload(track)
        except TypeError:
            raise
        except ValueError:
            raise

        return cls(app, hikari.Snowflake(guild_id), track)


@attrs.define
class TrackStartEvent(TrackBase, OngakuEvent):
    """Track start event.

    The track start event that is dispatched when a track starts on a player.
    """

    @classmethod
    def _from_payload(
        cls, payload: t.Mapping[str, t.Any], *, app: hikari.RESTAware
    ) -> TrackStartEvent:
        try:
            base = TrackBase._from_payload(payload, app=app)
        except TypeError:
            raise
        except ValueError:
            raise

        return cls(
            base.app, 
            base.guild_id, 
            base.track
        )


@attrs.define
class TrackEndEvent(TrackBase, OngakuEvent):
    """Track end event.

    The track end event that is dispatched when a track ends.
    """

    reason: enums.TrackEndReasonType
    """The reason for the track ending."""

    @classmethod
    def _from_payload(cls, payload: t.Mapping[str, t.Any], *, app: hikari.RESTAware):
        try:
            base = TrackBase._from_payload(payload, app=app)
        except TypeError:
            raise
        except ValueError:
            raise

        reason = payload.get("reason")
        if reason is None:
            raise ValueError("reason cannot be none.")
        if not isinstance(reason, str):
            raise TypeError("reason must be a integer.")

        return cls(
            base.app, 
            base.guild_id, 
            base.track,
            enums.TrackEndReasonType(reason)
        )


@attrs.define
class TrackExceptionEvent(TrackBase, OngakuEvent):
    """Track exception event.

    This event is dispatched when a track gets stuck.
    """

    exception: ExceptionError
    """The exception error that was returned."""

    @classmethod
    def _from_payload(cls, payload: t.Mapping[str, t.Any], *, app: hikari.RESTAware):
        try:
            base = TrackBase._from_payload(payload, app=app)
        except TypeError:
            raise
        except ValueError:
            raise

        exception = payload.get("exception")
        if exception is None:
            raise ValueError("exception cannot be none.")
        try:
            exception = ExceptionError._from_payload(exception)
        except TypeError:
            raise
        except ValueError:
            raise

        return cls(
            base.app, 
            base.guild_id, 
            base.track,
            exception,
        )


@attrs.define
class TrackStuckEvent(TrackBase, OngakuEvent):
    """Track stuck event.

    This event is dispatched when a track gets stuck.
    """

    threshold_ms: int
    """The threshold in milliseconds that was exceeded."""

    @classmethod
    def _from_payload(cls, payload: t.Mapping[str, t.Any], *, app: hikari.RESTAware):
        try:
            base = TrackBase._from_payload(payload, app=app)
        except TypeError:
            raise
        except ValueError:
            raise

        threshold_ms = payload.get("thresholdMs")
        if threshold_ms is None:
            raise ValueError("thresholdMs cannot be none.")
        if not isinstance(threshold_ms, int):
            raise TypeError("thresholdMs must be a integer.")
        

        return cls(
            base.app, 
            base.guild_id, 
            base.track,
            threshold_ms,
        )


@attrs.define
class PlayerBase(OngakuEvent):
    """Player base.

    This is the base player object for all Ongaku player events.
    """

    guild_id: hikari.Snowflake
    """The guild id of the player."""

    @classmethod
    def _from_payload(
        cls, payload: t.Mapping[str, t.Any], *, app: hikari.RESTAware
    ) -> PlayerBase:
        guild_id = payload.get("guildId")
        if guild_id is None:
            raise ValueError("guildId cannot be none.")
        if isinstance(guild_id, (str, int)):
            guild_id = int(guild_id)
        else:
            raise TypeError("guildId must be a integer.")

        return cls(app, hikari.Snowflake(guild_id))


@attrs.define
class QueueEmptyEvent(PlayerBase, OngakuEvent):
    """Queue empty event.

    This event is dispatched when the player queue is empty, and no more songs are available.
    """

@attrs.define
class QueueNextEvent(PlayerBase, OngakuEvent):
    """Queue next event.

    The event that is dispatched, when a new song is played in a player, from the queue.
    """

    track: Track
    """The track that is now playing."""
    old_track: Track
    """The track that was playing."""


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
