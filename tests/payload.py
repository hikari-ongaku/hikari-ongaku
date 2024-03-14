"""Payloads.

This is where all payloads are stored, and accessed for easy modification and updating.
"""

from __future__ import annotations

import typing as t

import ujson


def convert(object: dict[str, t.Any]) -> str:  # noqa: D103
    return ujson.dumps(object)


# ╔════════╗
# ║ Errors ║
# ╚════════╝

EXCEPTION: dict[str, str] = {
    "message": "test_message",
    "severity": "common",
    "cause": "test_cause",
}

REST_EXCEPTION: dict[str, str | int] = {
    "timestamp": 1667857581613,
    "status": 404,
    "error": "Not Found",
    "trace": "...",
    "message": "Session not found",
    "path": "/v4/sessions/test_session",
}

# ╔════════╗
# ║ Tracks ║
# ╚════════╝

TRACK_INFO: dict[str, str | int | bool | None] = {
    "identifier": "test_identifier",
    "isSeekable": False,
    "author": "test_author",
    "length": 1234567890,
    "isStream": False,
    "position": 1234567890,
    "title": "test_title",
    "uri": "https://www.youtube.com/watch?=test",
    "artworkUrl": "https://i.ytimg.com/test.jpg",
    "isrc": None,
    "sourceName": "test_source_name",
}

TRACK: dict[str, str | dict[str, t.Any]] = {
    "encoded": "test_encoded",
    "info": TRACK_INFO,
    "pluginInfo": {},
}

PLAYLIST_INFO: dict[str, str | int] = {"name": "test_name", "selectedTrack": -1}

PLAYLIST: dict[str, dict[str, str | int] | list[dict[str, str | dict[str, t.Any]]]] = {
    "info": PLAYLIST_INFO,
    "pluginInfo": {},
    "tracks": [TRACK],
}

# ╔═════════╗
# ║ Players ║
# ╚═════════╝

PLAYER_STATE: dict[str, int | bool] = {
    "time": 1234567890,
    "position": 1234567890,
    "connected": False,
    "ping": 1234567890,
}

PLAYER_VOICE: dict[str, str] = {
    "token": "test_token",
    "endpoint": "test_end_point",
    "sessionId": "test_session_id",
}

PLAYER: dict[str, str | int | bool | dict[str, t.Any]] = {
    "guildId": "1234567890",
    "track": TRACK,
    "volume": 1234567890,
    "paused": False,
    "state": PLAYER_STATE,
    "voice": PLAYER_VOICE,
    "filters": {},
}

# ╔═══════════╗
# ║ Websocket ║
# ╚═══════════╝

READY_OP: dict[str, str | bool] = {
    "op": "ready",
    "resumed": False,
    "sessionId": "test_session_id",
}

PLAYER_UPDATE_OP: dict[str, str | dict[str, int | bool]] = {
    "op": "playerUpdate",
    "guildId": "1234567890",
    "state": {"time": 1500467109, "position": 60000, "connected": True, "ping": 50},
}

STATS_MEMORY: dict[str, int] = {
    "free": 123456789,
    "used": 123456789,
    "allocated": 123456789,
    "reservable": 123456789,
}

STATS_CPU: dict[str, int | float] = {
    "cores": 1234567890,
    "systemLoad": 12345.67890,
    "lavalinkLoad": 12345.67890,
}

STATS_FRAME_STATS: dict[str, int] = {
    "sent": 1234567890,
    "nulled": 1234567890,
    "deficit": 1234567890,
}

STATS_OP: dict[str, str | int | dict[str, int] | dict[str, int | float]] = {
    "op": "stats",
    "players": 1234567890,
    "playingPlayers": 1234567890,
    "uptime": 123456789,
    "memory": STATS_MEMORY,
    "cpu": STATS_CPU,
    "frameStats": STATS_FRAME_STATS,
}

TRACK_START_EVENT_OP: dict[str, str | dict[str, str | dict[str, t.Any]]] = {
    "op": "event",
    "type": "TrackStartEvent",
    "guildId": "1234567890",
    "track": TRACK,
}

TRACK_END_EVENT_OP: dict[str, str | dict[str, str | dict[str, t.Any]]] = {
    "op": "event",
    "type": "TrackEndEvent",
    "guildId": "1234567890",
    "track": TRACK,
    "reason": "finished",
}

TRACK_EXCEPTION_EVENT_OP: dict[
    str, str | dict[str, str | dict[str, t.Any]] | dict[str, str]
] = {
    "op": "event",
    "type": "TrackExceptionEvent",
    "guildId": "1234567890",
    "track": TRACK,
    "exception": EXCEPTION,
}

TRACK_STUCK_EVENT_OP: dict[str, str | int | dict[str, str | dict[str, t.Any]]] = {
    "op": "event",
    "type": "TrackStuckEvent",
    "guildId": "1234567890",
    "track": TRACK,
    "thresholdMs": 1234567890,
}

WEBSOCKET_CLOSED_EVENT_OP: dict[str, str | int | bool] = {
    "op": "event",
    "type": "WebSocketClosedEvent",
    "guildId": "1234567890",
    "code": 4006,
    "reason": "test_reason",
    "byRemote": False,
}

# ╔══════╗
# ║ REST ║
# ╚══════╝

REST_TRACK_LOAD_TRACK: dict[str, str | dict[str, str | dict[str, t.Any]]] = {
    "loadType": "track",
    "data": TRACK,
}

REST_TRACK_LOAD_PLAYLIST: dict[
    str, str | dict[str, dict[str, str | int] | list[dict[str, str | dict[str, t.Any]]]]
] = {"loadType": "playlist", "data": PLAYLIST}

REST_TRACK_LOAD_SEARCH: dict[str, str | list[dict[str, str | dict[str, t.Any]]]] = {
    "loadType": "search",
    "data": [TRACK],
}

REST_TRACK_LOAD_EMPTY: dict[str, str | dict[None, None]] = {
    "loadType": "empty",
    "data": {},
}

REST_TRACK_LOAD_ERROR: dict[str, str | dict[str, str]] = {
    "loadType": "error",
    "data": EXCEPTION,
}

REST_DECODE_TRACK: dict[str, str | dict[str, t.Any]] = TRACK

REST_DECODE_TRACKS: list[dict[str, str | dict[str, t.Any]]] = [TRACK]

REST_PLAYER_GET_PLAYERS: list[dict[str, str | int | bool | dict[str, t.Any]]] = [PLAYER]

REST_PLAYER_GET_PLAYER: dict[str, str | int | bool | dict[str, t.Any]] = PLAYER

REST_PLAYER_UPDATE: dict[str, str | int | bool | dict[str, t.Any]] = PLAYER

REST_SESSION_UPDATE: dict[str, int | bool] = {"resuming": False, "timeout": 1234567890}

INFO_VERSION: dict[str, str | int] = {
    "semver": "test_semver",
    "major": 1234567890,
    "minor": 1234567890,
    "patch": 1234567890,
    "preRelease": "test_pre_release",
    "build": "test_build",
}

INFO_GIT: dict[str, str | int] = {
    "branch": "master",
    "commit": "85c5ab5",
    "commitTime": 1234567890,
}

INFO_PLUGIN: dict[str, str] = {"name": "test_name", "version": "test_version"}

REST_INFO: dict[
    str, str | int | dict[str, str | int] | list[str] | list[dict[str, str]]
] = {
    "version": INFO_VERSION,
    "buildTime": 1234567890,
    "git": INFO_GIT,
    "jvm": "test_jvm",
    "lavaplayer": "test_lavaplayer",
    "sourceManagers": ["test_source_manager"],
    "filters": ["equalizer", "karaoke", "timescale", "channelMix"],
    "plugins": [INFO_PLUGIN],
}

REST_STATS: dict[str, int | dict[str, int] | dict[str, int | float]] = {
    "players": 1,
    "playingPlayers": 1,
    "uptime": 123456789,
    "memory": STATS_MEMORY,
    "cpu": STATS_CPU,
}

ROUTEPLANNER_IP_BLOCK: dict[str, str] = {"type": "Inet6Address", "size": "1234567890"}

ROUTEPLANNER_FAILING_ADDRESS: dict[str, str | int] = {
    "failingAddress": "test_failing_address",
    "failingTimestamp": 1234567890,
    "failingTime": "test_failing_time",
}

ROUTEPLANNER_DETAILS: dict[str, str | dict[str, str] | list[dict[str, str | int]]] = {
    "ipBlock": ROUTEPLANNER_IP_BLOCK,
    "failingAddresses": [ROUTEPLANNER_FAILING_ADDRESS],
    "blockIndex": "0",
    "currentAddressIndex": "36792023813",
}

REST_ROUTEPLANNER_STATUS: dict[
    str, str | dict[str, str | dict[str, str] | list[dict[str, str | int]]]
] = {"class": "RotatingNanoIpRoutePlanner", "details": ROUTEPLANNER_DETAILS}
