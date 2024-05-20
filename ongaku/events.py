"""
Events.

All ongaku related events.
"""

from __future__ import annotations

import typing

import attrs
import hikari
from ongaku.abc import events as events_
from ongaku.abc import statistics as stats_

if typing.TYPE_CHECKING:
    from ongaku.client import Client
    from ongaku.session import Session

__all__ = (
    "OngakuEvent",
    "PayloadEvent",
    "ReadyEvent",
    "PlayerUpdateEvent",
    "StatisticsEvent",
    "WebsocketClosedEvent",
    "TrackStartEvent",
    "TrackEndEvent",
    "TrackExceptionEvent",
    "TrackStuckEvent",
    "QueueEmptyEvent",
    "QueueNextEvent",
)


class OngakuEvent(hikari.Event):
    """The base ongaku event, that all events subclass."""

    _app: hikari.RESTAware = attrs.field(alias="app")
    _client: Client = attrs.field(alias="client")
    _session: Session = attrs.field(alias="session")

    @property
    def app(self) -> hikari.RESTAware:
        """The application attached to the event."""
        return self._app

    @property
    def client(self) -> Client:
        """The ongaku client attached to the event."""
        return self._client

    @property
    def session(self) -> Session:
        """The session attached to the event."""
        return self._session


@attrs.define
class PayloadEvent(OngakuEvent):
    """
    Payload Event.

    The event that is dispatched each time a message is received from the lavalink websocket.
    """

    payload: str
    """The payload received."""


@attrs.define
class ReadyEvent(OngakuEvent, events_.Ready):
    """
    Ready Event.

    The event that is dispatched when the lavalink server is ready for connections.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#ready-op)
    """


@attrs.define
class PlayerUpdateEvent(OngakuEvent, events_.PlayerUpdate):
    """
    Player Update Event.

    The event that is dispatched when a players state has been updated.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#player-update-op)
    """


@attrs.define
class StatisticsEvent(OngakuEvent, stats_.Statistics):
    """
    Statistics Event.

    All of the statistics about the current session.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#stats-op)
    """


@attrs.define
class WebsocketClosedEvent(OngakuEvent, events_.WebsocketClosed):
    """
    Websocket Closed Event.

    The event that is dispatched, when a websocket to discord gets closed.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#websocketclosedevent)
    """


@attrs.define
class TrackStartEvent(OngakuEvent, events_.TrackStart):
    """
    Track start event.

    The event that is dispatched when a track starts playing.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#trackstartevent)
    """


@attrs.define
class TrackEndEvent(OngakuEvent, events_.TrackEnd):
    """
    Track end event.

    The event that is dispatched when a track ends.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#trackendevent)
    """


@attrs.define
class TrackExceptionEvent(OngakuEvent, events_.TrackException):
    """
    Track exception event.

    The event that is dispatched when an exception happens with a track.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#trackexceptionevent)
    """


@attrs.define
class TrackStuckEvent(OngakuEvent, events_.TrackStuck):
    """
    Track stuck event.

    The event that is dispatched when a track gets stuck.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#trackstuckevent)
    """


@attrs.define
class QueueEmptyEvent(OngakuEvent, events_.QueueEmpty):
    """
    Queue empty event.

    The event that is dispatched, when a players queue is empty.
    """


@attrs.define
class QueueNextEvent(OngakuEvent, events_.QueueNext):
    """
    Queue next event.

    The event that is dispatched when a queue is playing the next song.
    """


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
