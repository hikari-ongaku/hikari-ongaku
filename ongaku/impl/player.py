# ruff: noqa: D101, D102

from __future__ import annotations

import datetime
import typing

import hikari

from ongaku.abc import player as player_
from ongaku.abc import track as track_


class Player(player_.Player):
    def __init__(
        self,
        guild_id: hikari.Snowflake,
        track: track_.Track,
        volume: int,
        is_paused: bool,
        state: player_.State,
        voice: player_.Voice,
        filters: typing.Mapping[str, typing.Any],
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
        return self._guild_id

    @property
    def track(self) -> track_.Track | None:
        return self._track

    @property
    def volume(self) -> int:
        return self._volume

    @property
    def is_paused(self) -> bool:
        return self._is_paused

    @property
    def state(self) -> player_.State:
        return self._state

    @property
    def voice(self) -> player_.Voice:
        return self._voice

    @property
    def filters(self) -> typing.Mapping[str, typing.Any]:
        return self._filters


class State(player_.State):
    def __init__(
        self, time: datetime.datetime, position: int, connected: bool, ping: int
    ) -> None:
        self._time = time
        self._position = position
        self._connected = connected
        self._ping = ping

    @property
    def time(self) -> datetime.datetime:
        return self._time

    @property
    def position(self) -> int:
        return self._position

    @property
    def connected(self) -> bool:
        return self._connected

    @property
    def ping(self) -> int:
        return self._ping


class Voice(player_.Voice):
    def __init__(self, token: str, endpoint: str, session_id: str) -> None:
        self._token = token
        self._endpoint = endpoint
        self._session_id = session_id

    @property
    def token(self) -> str:
        return self._token

    @property
    def endpoint(self) -> str:
        return self._endpoint

    @property
    def session_id(self) -> str:
        return self._session_id