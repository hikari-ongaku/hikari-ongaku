"""
Event ABC's and Events.

The session abstract classes and hikari events.
"""

from __future__ import annotations

import hikari
import msgspec

from ongaku.abc.bases import PayloadBase
from ongaku.abc.error import ExceptionError
from ongaku.abc.player import PlayerState
from ongaku.abc.track import Track
from ongaku.enums import TrackEndReasonType

__all__ = (
    "Ready",
    "PlayerUpdate",
    "WebsocketClosed",
    "TrackStart",
    "TrackEnd",
    "TrackException",
    "TrackStuck",
)


class Ready(PayloadBase):
    """
    Ready Event Base.

    The base for the ready event.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/websocket.html#ready-op)
    """

    resumed: bool
    """Whether or not the session has been resumed, or is a new session."""
    session_id: str = msgspec.field(name="sessionId")
    """The lavalink session id, for the current session."""


class PlayerUpdate(PayloadBase):
    """
    Player update event base.

    The base for the player update event.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/websocket.html#player-update-op)
    """

    guild_id: hikari.Snowflake = msgspec.field(name="guildId")
    """The guild related to this event."""

    state: PlayerState
    """The player state."""


class WebsocketClosed(PayloadBase):
    """
    Websocket closed event base.

    The base for the websocket closed event.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/websocket.html#websocketclosedevent)
    """

    guild_id: hikari.Snowflake = msgspec.field(name="guildId")
    """The guild related to this event."""
    code: int
    """The discord error code that [discord](https://discord.com/developers/docs/topics/opcodes-and-status-codes#voice-voice-close-event-codes) responded with."""
    reason: str
    """The close reason."""
    by_remote: bool = msgspec.field(name="byRemote")
    """Whether the connection was closed by Discord."""


class TrackStart(PayloadBase):
    """
    Track start event base.

    The base for the track start event.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/websocket.html#trackstartevent)
    """

    guild_id: hikari.Snowflake = msgspec.field(name="guildId")
    """The guild related to this event."""
    track: Track
    """The track related to this event."""


class TrackEnd(PayloadBase):
    """
    Track end event base.

    The base for the track end event.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/websocket.html#trackendevent)
    """

    guild_id: hikari.Snowflake = msgspec.field(name="guildId")
    """The guild related to this event."""
    track: Track
    """The track related to this event."""
    reason: TrackEndReasonType
    """The reason for the track ending."""


class TrackException(PayloadBase):
    """
    Track exception event base.

    The base for track exception event.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/websocket.html#trackexceptionevent)
    """

    guild_id: hikari.Snowflake = msgspec.field(name="guildId")
    """The guild related to this event."""
    track: Track
    """The track related to this event."""
    exception: ExceptionError
    """The exception error that was returned."""


class TrackStuck(PayloadBase):
    """
    Track stuck event base.

    The base for track stuck event.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/websocket.html#trackstuckevent)
    """

    guild_id: hikari.Snowflake = msgspec.field(name="guildId")
    """The guild related to this event."""
    track: Track
    """The track related to this event."""
    threshold_ms: int = msgspec.field(name="thresholdMs")
    """The threshold in milliseconds that was exceeded."""


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
