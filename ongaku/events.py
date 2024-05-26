"""
Events.

All ongaku related events.
"""

from __future__ import annotations

import typing

import hikari

from ongaku.abc import events as events_
from ongaku.abc import statistics as stats_

if typing.TYPE_CHECKING:
    import typing_extensions as te

    from ongaku.abc import errors as errors_
    from ongaku.abc import player as player_
    from ongaku.abc import statistics as statistics_
    from ongaku.abc import track as track_
    from ongaku.client import Client
    from ongaku.session import Session

__all__ = (
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


class PayloadEvent(events_.OngakuEvent):
    """
    Payload Event.

    The event that is dispatched each time a message is received from the lavalink websocket.
    """

    def __init__(
        self, app: hikari.RESTAware, client: Client, session: Session, payload: str
    ) -> None:
        self._app = app
        self._client = client
        self._session = session
        self._payload = payload

    @classmethod
    def from_session(cls, session: Session, payload: str) -> te.Self:
        """Build the [PayloadEvent][ongaku.events.PayloadEvent] with just a session."""
        return cls(session.app, session.client, session, payload)

    @property
    def app(self) -> hikari.RESTAware:  # noqa: D102
        return self._app

    @property
    def client(self) -> Client:  # noqa: D102
        return self._client

    @property
    def session(self) -> Session:  # noqa: D102
        return self._session

    @property
    def payload(self) -> str:
        """The payload received."""
        return self._payload


class ReadyEvent(events_.OngakuEvent, events_.Ready):
    """
    Ready Event.

    The event that is dispatched when the lavalink server is ready for connections.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#ready-op)
    """

    def __init__(
        self,
        app: hikari.RESTAware,
        client: Client,
        session: Session,
        resumed: bool,
        session_id: str,
    ) -> None:
        self._app = app
        self._client = client
        self._session = session
        self._resumed = resumed
        self._session_id = session_id

    @classmethod
    def from_session(cls, session: Session, resumed: bool, session_id: str) -> te.Self:
        """Build the [PayloadEvent][ongaku.events.PayloadEvent] with just a session."""
        return cls(session.app, session.client, session, resumed, session_id)

    @property
    def app(self) -> hikari.RESTAware:  # noqa: D102
        return self._app

    @property
    def client(self) -> Client:  # noqa: D102
        return self._client

    @property
    def session(self) -> Session:  # noqa: D102
        return self._session

    @property
    def resumed(self) -> bool:  # noqa: D102
        return self._resumed

    @property
    def session_id(self) -> str:  # noqa: D102
        return self._session_id


class PlayerUpdateEvent(events_.OngakuEvent, events_.PlayerUpdate):
    """
    Player Update Event.

    The event that is dispatched when a players state has been updated.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#player-update-op)
    """

    def __init__(
        self,
        app: hikari.RESTAware,
        client: Client,
        session: Session,
        guild_id: hikari.Snowflake,
        state: player_.State,
    ) -> None:
        self._app = app
        self._client = client
        self._session = session
        self._guild_id = guild_id
        self._state = state

    @classmethod
    def from_session(
        cls, session: Session, guild_id: hikari.Snowflake, state: player_.State
    ) -> te.Self:
        """Build the [PayloadEvent][ongaku.events.PayloadEvent] with just a session."""
        return cls(session.app, session.client, session, guild_id, state)

    @property
    def app(self) -> hikari.RESTAware:  # noqa: D102
        return self._app

    @property
    def client(self) -> Client:  # noqa: D102
        return self._client

    @property
    def session(self) -> Session:  # noqa: D102
        return self._session

    @property
    def guild_id(self) -> hikari.Snowflake:  # noqa: D102
        return self._guild_id

    @property
    def state(self) -> player_.State:  # noqa: D102
        return self._state


class StatisticsEvent(events_.OngakuEvent, stats_.Statistics):
    """
    Statistics Event.

    All of the statistics about the current session.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#stats-op)
    """

    def __init__(
        self,
        app: hikari.RESTAware,
        client: Client,
        session: Session,
        players: int,
        playing_players: int,
        uptime: int,
        memory: statistics_.Memory,
        cpu: statistics_.Cpu,
        frame_statistics: statistics_.FrameStatistics | None,
    ) -> None:
        self._app = app
        self._client = client
        self._session = session
        self._players = players
        self._playing_players = playing_players
        self._uptime = uptime
        self._memory = memory
        self._cpu = cpu
        self._frame_statistics = frame_statistics

    @classmethod
    def from_session(
        cls,
        session: Session,
        players: int,
        playing_players: int,
        uptime: int,
        memory: statistics_.Memory,
        cpu: statistics_.Cpu,
        frame_statistics: statistics_.FrameStatistics | None,
    ) -> te.Self:
        """Build the [PayloadEvent][ongaku.events.PayloadEvent] with just a session."""
        return cls(
            session.app,
            session.client,
            session,
            players,
            playing_players,
            uptime,
            memory,
            cpu,
            frame_statistics,
        )

    @property
    def app(self) -> hikari.RESTAware:  # noqa: D102
        return self._app

    @property
    def client(self) -> Client:  # noqa: D102
        return self._client

    @property
    def session(self) -> Session:  # noqa: D102
        return self._session

    @property
    def players(self) -> int:  # noqa: D102
        return self._players

    @property
    def playing_players(self) -> int:  # noqa: D102
        return self._playing_players

    @property
    def uptime(self) -> int:  # noqa: D102
        return self._uptime

    @property
    def memory(self) -> statistics_.Memory:  # noqa: D102
        return self._memory

    @property
    def cpu(self) -> statistics_.Cpu:  # noqa: D102
        return self._cpu

    @property
    def frame_stats(self) -> statistics_.FrameStatistics | None:  # noqa: D102
        return self._frame_statistics


class WebsocketClosedEvent(events_.OngakuEvent, events_.WebsocketClosed):
    """
    Websocket Closed Event.

    The event that is dispatched, when a websocket to discord gets closed.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#websocketclosedevent)
    """

    def __init__(
        self,
        app: hikari.RESTAware,
        client: Client,
        session: Session,
        guild_id: hikari.Snowflake,
        code: int,
        reason: str,
        by_remote: bool,
    ) -> None:
        self._app = app
        self._client = client
        self._session = session
        self._guild_id = guild_id
        self._code = code
        self._reason = reason
        self._by_remote = by_remote

    @classmethod
    def from_session(
        cls,
        session: Session,
        guild_id: hikari.Snowflake,
        code: int,
        reason: str,
        by_remote: bool,
    ) -> te.Self:
        """Build the [PayloadEvent][ongaku.events.PayloadEvent] with just a session."""
        return cls(
            session.app, session.client, session, guild_id, code, reason, by_remote
        )

    @property
    def app(self) -> hikari.RESTAware:  # noqa: D102
        return self._app

    @property
    def client(self) -> Client:  # noqa: D102
        return self._client

    @property
    def session(self) -> Session:  # noqa: D102
        return self._session

    @property
    def guild_id(self) -> hikari.Snowflake:  # noqa: D102
        return self._guild_id

    @property
    def code(self) -> int:  # noqa: D102
        return self._code

    @property
    def reason(self) -> str:  # noqa: D102
        return self._reason

    @property
    def by_remote(self) -> bool:  # noqa: D102
        return self._by_remote


class TrackStartEvent(events_.OngakuEvent, events_.TrackStart):
    """
    Track start event.

    The event that is dispatched when a track starts playing.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#trackstartevent)
    """

    def __init__(
        self,
        app: hikari.RESTAware,
        client: Client,
        session: Session,
        guild_id: hikari.Snowflake,
        track: track_.Track,
    ) -> None:
        self._app = app
        self._client = client
        self._session = session
        self._guild_id = guild_id
        self._track = track

    @classmethod
    def from_session(
        cls, session: Session, guild_id: hikari.Snowflake, track: track_.Track
    ) -> te.Self:
        """Build the [PayloadEvent][ongaku.events.PayloadEvent] with just a session."""
        return cls(session.app, session.client, session, guild_id, track)

    @property
    def app(self) -> hikari.RESTAware:  # noqa: D102
        return self._app

    @property
    def client(self) -> Client:  # noqa: D102
        return self._client

    @property
    def session(self) -> Session:  # noqa: D102
        return self._session

    @property
    def guild_id(self) -> hikari.Snowflake:  # noqa: D102
        return self._guild_id

    @property
    def track(self) -> track_.Track:  # noqa: D102
        return self._track


class TrackEndEvent(events_.OngakuEvent, events_.TrackEnd):
    """
    Track end event.

    The event that is dispatched when a track ends.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#trackendevent)
    """

    def __init__(
        self,
        app: hikari.RESTAware,
        client: Client,
        session: Session,
        guild_id: hikari.Snowflake,
        track: track_.Track,
        reason: events_.TrackEndReasonType,
    ) -> None:
        self._app = app
        self._client = client
        self._session = session
        self._guild_id = guild_id
        self._track = track
        self._reason = reason

    @classmethod
    def from_session(
        cls,
        session: Session,
        guild_id: hikari.Snowflake,
        track: track_.Track,
        reason: events_.TrackEndReasonType,
    ) -> te.Self:
        """Build the [PayloadEvent][ongaku.events.PayloadEvent] with just a session."""
        return cls(session.app, session.client, session, guild_id, track, reason)

    @property
    def app(self) -> hikari.RESTAware:  # noqa: D102
        return self._app

    @property
    def client(self) -> Client:  # noqa: D102
        return self._client

    @property
    def session(self) -> Session:  # noqa: D102
        return self._session

    @property
    def guild_id(self) -> hikari.Snowflake:  # noqa: D102
        return self._guild_id

    @property
    def track(self) -> track_.Track:  # noqa: D102
        return self._track

    @property
    def reason(self) -> events_.TrackEndReasonType:  # noqa: D102
        return self._reason


class TrackExceptionEvent(events_.OngakuEvent, events_.TrackException):
    """
    Track exception event.

    The event that is dispatched when an exception happens with a track.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#trackexceptionevent)
    """

    def __init__(
        self,
        app: hikari.RESTAware,
        client: Client,
        session: Session,
        guild_id: hikari.Snowflake,
        track: track_.Track,
        exception: errors_.ExceptionError,
    ) -> None:
        self._app = app
        self._client = client
        self._session = session
        self._guild_id = guild_id
        self._track = track
        self._exception = exception

    @classmethod
    def from_session(
        cls,
        session: Session,
        guild_id: hikari.Snowflake,
        track: track_.Track,
        exception: errors_.ExceptionError,
    ) -> te.Self:
        """Build the [PayloadEvent][ongaku.events.PayloadEvent] with just a session."""
        return cls(session.app, session.client, session, guild_id, track, exception)

    @property
    def app(self) -> hikari.RESTAware:  # noqa: D102
        return self._app

    @property
    def client(self) -> Client:  # noqa: D102
        return self._client

    @property
    def session(self) -> Session:  # noqa: D102
        return self._session

    @property
    def guild_id(self) -> hikari.Snowflake:  # noqa: D102
        return self._guild_id

    @property
    def track(self) -> track_.Track:  # noqa: D102
        return self._track

    @property
    def exception(self) -> errors_.ExceptionError:  # noqa: D102
        return self._exception


class TrackStuckEvent(events_.OngakuEvent, events_.TrackStuck):
    """
    Track stuck event.

    The event that is dispatched when a track gets stuck.

    ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#trackstuckevent)
    """

    def __init__(
        self,
        app: hikari.RESTAware,
        client: Client,
        session: Session,
        guild_id: hikari.Snowflake,
        track: track_.Track,
        threshold_ms: int,
    ) -> None:
        self._app = app
        self._client = client
        self._session = session
        self._guild_id = guild_id
        self._track = track
        self._threshold_ms = threshold_ms

    @classmethod
    def from_session(
        cls,
        session: Session,
        guild_id: hikari.Snowflake,
        track: track_.Track,
        threshold_ms: int,
    ) -> te.Self:
        """Build the [PayloadEvent][ongaku.events.PayloadEvent] with just a session."""
        return cls(session.app, session.client, session, guild_id, track, threshold_ms)

    @property
    def app(self) -> hikari.RESTAware:  # noqa: D102
        return self._app

    @property
    def client(self) -> Client:  # noqa: D102
        return self._client

    @property
    def session(self) -> Session:  # noqa: D102
        return self._session

    @property
    def guild_id(self) -> hikari.Snowflake:  # noqa: D102
        return self._guild_id

    @property
    def track(self) -> track_.Track:  # noqa: D102
        return self._track

    @property
    def threshold_ms(self) -> int:  # noqa: D102
        return self._threshold_ms


class QueueEmptyEvent(events_.OngakuEvent, events_.QueueEmpty):
    """
    Queue empty event.

    The event that is dispatched, when a players queue is empty.
    """

    def __init__(
        self,
        app: hikari.RESTAware,
        client: Client,
        session: Session,
        guild_id: hikari.Snowflake,
        old_track: track_.Track,
    ) -> None:
        self._app = app
        self._client = client
        self._session = session
        self._guild_id = guild_id
        self._old_track = old_track

    @classmethod
    def from_session(
        cls, session: Session, guild_id: hikari.Snowflake, old_track: track_.Track
    ) -> te.Self:
        """Build the [PayloadEvent][ongaku.events.PayloadEvent] with just a session."""
        return cls(session.app, session.client, session, guild_id, old_track)

    @property
    def app(self) -> hikari.RESTAware:  # noqa: D102
        return self._app

    @property
    def client(self) -> Client:  # noqa: D102
        return self._client

    @property
    def session(self) -> Session:  # noqa: D102
        return self._session

    @property
    def guild_id(self) -> hikari.Snowflake:  # noqa: D102
        return self._guild_id

    @property
    def old_track(self) -> track_.Track:  # noqa: D102
        return self._old_track


class QueueNextEvent(events_.OngakuEvent, events_.QueueNext):
    """
    Queue next event.

    The event that is dispatched when a queue is playing the next song.
    """

    def __init__(
        self,
        app: hikari.RESTAware,
        client: Client,
        session: Session,
        guild_id: hikari.Snowflake,
        track: track_.Track,
        old_track: track_.Track,
    ) -> None:
        self._app = app
        self._client = client
        self._session = session
        self._guild_id = guild_id
        self._track = track
        self._old_track = old_track

    @classmethod
    def from_session(
        cls,
        session: Session,
        guild_id: hikari.Snowflake,
        track: track_.Track,
        old_track: track_.Track,
    ) -> te.Self:
        """Build the [PayloadEvent][ongaku.events.PayloadEvent] with just a session."""
        return cls(session.app, session.client, session, guild_id, track, old_track)

    @property
    def app(self) -> hikari.RESTAware:  # noqa: D102
        return self._app

    @property
    def client(self) -> Client:  # noqa: D102
        return self._client

    @property
    def session(self) -> Session:  # noqa: D102
        return self._session

    @property
    def guild_id(self) -> hikari.Snowflake:  # noqa: D102
        return self._guild_id

    @property
    def track(self) -> track_.Track:  # noqa: D102
        return self._track

    @property
    def old_track(self) -> track_.Track:  # noqa: D102
        return self._old_track


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
