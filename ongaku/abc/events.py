"""
Event ABC's and Events.

The session abstract classes and hikari events.
"""

from __future__ import annotations

import typing as t

from hikari import Snowflake
from pydantic import Field
from pydantic import WrapSerializer
from pydantic import WrapValidator

from ..enums import TrackEndReasonType
from .bases import PayloadBaseApp
from .bases import _snowflake_to_string
from .bases import _string_to_snowflake
from .lavalink import ExceptionError
from .player import PlayerState
from .track import Track
from .statistics import Statistics

__all__ = (
    "ReadyEvent",
    "PlayerUpdateEvent",
    "StatisticsEvent",
    "WebsocketClosedEvent",
    "TrackBase",
    "TrackStartEvent",
    "TrackEndEvent",
    "TrackExceptionEvent",
    "TrackStuckEvent",
    "PlayerBase",
    "QueueEmptyEvent",
    "QueueNextEvent",
)



class ReadyEvent(PayloadBaseApp):
    """
    Ready event.

    The event that is dispatched when lavalink is ready for new players, discord connections, and song requests.
    """

    resumed: bool
    """Whether or not the session has been resumed, or is a new session."""
    session_id: t.Annotated[str, Field(alias="sessionId")]
    """The lavalink session id, for the current session."""


class PlayerUpdateEvent(PayloadBaseApp):
    """
    Player update event.

    The event that is dispatched when a player is updated.
    """

    guild_id: t.Annotated[
        Snowflake,
        WrapValidator(_string_to_snowflake),
        WrapSerializer(_snowflake_to_string),
        Field(alias="guildId"),
    ]

    state: PlayerState


class StatisticsEvent(PayloadBaseApp, Statistics):
    """
    Statistics Event.

    The event that is dispatched when the statistics of the server is updated.

    Includes this information from [Statistics][ongaku.abc.statistics.Statistics].

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/websocket.html#stats-object)
    """


class WebsocketClosedEvent(PayloadBaseApp):
    """
    Websocket closed event.

    The event that is dispatched when a discord websocket closes.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/websocket.html#websocketclosedevent)
    """

    guild_id: t.Annotated[
        Snowflake,
        WrapValidator(_string_to_snowflake),
        WrapSerializer(_snowflake_to_string),
        Field(alias="guildId"),
    ]
    """The guild that had their websocket closed in."""
    code: int
    """The discord error code that [discord](https://discord.com/developers/docs/topics/opcodes-and-status-codes#voice-voice-close-event-codes) responded with."""
    reason: str
    """The close reason."""
    by_remote: t.Annotated[bool, Field(alias="byRemote")]
    """Whether the connection was closed by Discord."""


class TrackBase(PayloadBaseApp):
    """
    Base track class.

    The class that all Track based events, inherit.
    """

    guild_id: t.Annotated[
        Snowflake,
        WrapValidator(_string_to_snowflake),
        WrapSerializer(_snowflake_to_string),
        Field(alias="guildId"),
    ]
    """The guild the track is playing in."""
    track: Track
    """The track that the event is attached too."""


class TrackStartEvent(TrackBase):
    """
    Track start event.

    The event that is dispatched when a track starts playing.
    """


class TrackEndEvent(TrackBase):
    """
    Track end event.

    The event that is dispatched when a track ends.
    """

    reason: TrackEndReasonType
    """The reason for the track ending."""


class TrackExceptionEvent(TrackBase):
    """
    Track exception event.

    The event that is dispatched when an exception happens with a track.
    """

    exception: ExceptionError
    """The exception error that was returned."""


class TrackStuckEvent(TrackBase):
    """
    Track stuck event.

    The event that is dispatched when a track gets stuck.
    """

    threshold_ms: t.Annotated[int, Field(alias="thresholdMs")]
    """The threshold in milliseconds that was exceeded."""


class PlayerBase(PayloadBaseApp):
    """
    Player base.

    This is the base player object for all Ongaku player events.

    !!! note
        All player based events, are ongaku related. Not lavalink related.
    """

    guild_id: t.Annotated[
        Snowflake,
        WrapValidator(_string_to_snowflake),
        WrapSerializer(_snowflake_to_string),
        Field(alias="guildId"),
    ]
    """The guild id of the player."""


class QueueEmptyEvent(PlayerBase):
    """
    Queue empty event.

    The event that is dispatched, when a players queue is empty.
    """


class QueueNextEvent(PlayerBase):
    """
    Queue next event.

    The event that is dispatched when a queue is playing the next song.
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
