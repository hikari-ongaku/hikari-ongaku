
from __future__ import annotations

import typing
import hikari
import datetime

from ongaku.internal.converters import DumpType, LoadType, json_dumps, json_loads
from ongaku.internal import types
from ongaku.abc import error as error_
from ongaku.abc import events as events_
from ongaku.abc import track as track_
from ongaku.abc import info as info_
from ongaku.abc import player as player_
from ongaku.abc import playlist as playlist_
from ongaku.abc import route_planner as route_planner_
from ongaku.abc import session as session_
from ongaku.abc import statistics as statistics_
from ongaku import enums

from ongaku import events

if typing.TYPE_CHECKING:
    from ongaku.session import Session

class EntityBuilder: # noqa: D101
    def __init__(
        self,
        dumps: DumpType = json_dumps,
        loads: LoadType = json_loads
    ) -> None:
        self._dumps = dumps
        self._loads = loads

    def _ensure_mapping(self, payload: types.PayloadMappingT) -> typing.Mapping[str, typing.Any]:
        if isinstance(payload, str | bytes):
            data = self._loads(payload)
            if isinstance(data, typing.Sequence):
                raise TypeError("Mapping is required.")
            return data
        
        return payload

    # error

    def build_rest_error(self, payload: types.PayloadMappingT) -> error_.RestError: # noqa: D102
        data = self._ensure_mapping(payload)

        return error_.RestError(
            datetime.datetime.fromtimestamp(data["timestamp"]),
            data["status"],
            data["error"],
            data["message"],
            data["path"],
            data.get("trace", None)
        )
    
    def build_exception_error(self, payload: types.PayloadMappingT) -> error_.ExceptionError: # noqa: D102
        data = self._ensure_mapping(payload)

        return error_.ExceptionError(
            data["message"],
            enums.SeverityType(data["severity"]),
            data["cause"]
        )

    # events

    def build_ready_event(self, payload: types.PayloadMappingT) -> events_.Ready: # noqa: D102
        data = self._ensure_mapping(payload)

        return events_.Ready(
            data["ready"],
            data["sessionId"]
        )
    
    def build_player_update_event(self, payload: types.PayloadMappingT) -> events_.PlayerUpdate: # noqa: D102
        data = self._ensure_mapping(payload)

        return events_.PlayerUpdate(
            data["guildId"],
            self.build_player_state(data["state"])
        )
    
    def build_websocket_closed_event(self, payload: types.PayloadMappingT) -> events_.WebsocketClosed: # noqa: D102
        data = self._ensure_mapping(payload)

        return events_.WebsocketClosed(
            data["guildId"],
            data["code"],
            data["reason"],
            data["byRemote"]
        )

    def build_track_start_event(self, payload: types.PayloadMappingT) -> events_.TrackStart: # noqa: D102
        data = self._ensure_mapping(payload)

        return events_.TrackStart(
            data["guildId"],
            self.build_track(data["track"])
        )
    
    def build_track_end_event(self, payload: types.PayloadMappingT) -> events_.TrackEnd: # noqa: D102
        data = self._ensure_mapping(payload)

        return events_.TrackEnd(
            data["guildId"],
            self.build_track(data["track"]),
            enums.TrackEndReasonType(data["reason"])
        )
    
    def build_track_exception_event(self, payload: types.PayloadMappingT) -> events_.TrackException: # noqa: D102
        data = self._ensure_mapping(payload)

        return events_.TrackException(
            data["guildId"],
            self.build_track(data["track"]),
            self.build_exception_error(data["exception"])
        )

    def build_track_stuck_event(self, payload: types.PayloadMappingT) -> events_.TrackStuck: # noqa: D102
        data = self._ensure_mapping(payload)

        return events_.TrackStuck(
            data["guildId"],
            self.build_track(data["track"]),
            data["thresholdMs"]
        )

    # info

    def build_info(self, payload: types.PayloadMappingT) -> info_.Info: # noqa: D102
        data = self._ensure_mapping(payload)

        source_managers: list[str] = []

        for manager in data["sourceManagers"]:
            source_managers.append(manager)

        filters: list[str] = []

        for filter in data["filters"]:
            filters.append(filter)

        plugins: list[info_.Plugin] = []

        for plugin in data["plugin"]:
            plugins.append(self.build_info_plugin(plugin))

        return info_.Info(
            self.build_info_version(data["version"]),
            datetime.datetime.fromtimestamp(data["buildTime"]),
            self.build_info_git(data["git"]),
            data["jvm"],
            data["lavaplayer"],
            source_managers,
            filters,
            plugins
        )
    
    def build_info_version(self, payload: types.PayloadMappingT) -> info_.Version: # noqa: D102
        data = self._ensure_mapping(payload)

        return info_.Version(
            data["semver"],
            data["major"],
            data["minor"],
            data["patch"],
            data["preRelease"],
            data.get("build", None)
        )

    def build_info_git(self, payload: types.PayloadMappingT) -> info_.Git: # noqa: D102
        data = self._ensure_mapping(payload)

        return info_.Git(
            data["branch"],
            data["commit"],
            datetime.datetime.fromtimestamp(data["commitTime"])
        )

    def build_info_plugin(self, payload: types.PayloadMappingT) -> info_.Plugin: # noqa: D102
        data = self._ensure_mapping(payload)

        return info_.Plugin(
            data["name"],
            data["version"]
        )
    
    # Player

    def build_player(self, payload: types.PayloadMappingT) -> player_.Player: # noqa: D102
        data = self._ensure_mapping(payload)

        return player_.Player(
            data["guildId"],
            self.build_track(data["track"]),
            data["volume"],
            data["paused"],
            self.build_player_state(data["state"]),
            self.build_player_voice(data["voice"]),
            data["filters"]
        )

    def build_player_state(self, payload: types.PayloadMappingT) -> player_.State: # noqa: D102
        data = self._ensure_mapping(payload)

        return player_.State(
            datetime.datetime.fromtimestamp(data["time"]),
            data["position"],
            data["connection"],
            data["ping"]
        )
    
    def build_player_voice(self, payload: types.PayloadMappingT) -> player_.Voice: # noqa: D102
        data = self._ensure_mapping(payload)

        return player_.Voice(
            data["token"],
            data["endpoint"],
            data["sessionId"]
        )
    
    # playlist

    def build_playlist(self, payload: types.PayloadMappingT) -> playlist_.Playlist: # noqa: D102
        data = self._ensure_mapping(payload)

        tracks: list[track_.Track] = []

        for track in data["tracks"]:
            tracks.append(self.build_track(track))

        return playlist_.Playlist(
            self.build_playlist_info(data["info"]),
            tracks,
            data["pluginInfo"]
        )
    
    def build_playlist_info(self, payload: types.PayloadMappingT) -> playlist_.PlaylistInfo: # noqa: D102
        data = self._ensure_mapping(payload)

        return playlist_.PlaylistInfo(
            data["name"],
            data["selectedTrack"]
        )

    # route planner

    def build_routeplanner_status(self, payload: types.PayloadMappingT) -> route_planner_.RoutePlannerStatus: # noqa: D102
        data = self._ensure_mapping(payload)

        return route_planner_.RoutePlannerStatus(
            enums.RoutePlannerType(data["class"]),
            self.build_routeplanner_details(data["details"])
        )
    
    def build_routeplanner_details(self, payload: types.PayloadMappingT) -> route_planner_.RoutePlannerDetails: # noqa: D102
        data = self._ensure_mapping(payload)

        failing_addresses: list[route_planner_.FailingAddress] = []

        for failing_address in data["failingAddresses"]:
            failing_addresses.append(self.build_routeplanner_failing_address(failing_address))


        return route_planner_.RoutePlannerDetails(
            self.build_routeplanner_ipblock(data["ipBlock"]),
            failing_addresses,
            data.get("rotateIndex", None),
            data.get("ipIndex", None),
            data.get("currentAddress", None),
            data.get("currentAddressIndex", None),
            data.get("blockIndex", None)

        )
    
    def build_routeplanner_ipblock(self, payload: types.PayloadMappingT) -> route_planner_.IPBlock: # noqa: D102
        data = self._ensure_mapping(payload)

        return route_planner_.IPBlock(
            enums.IPBlockType(data["type"]),
            data["size"]
        )

    def build_routeplanner_failing_address(self, payload: types.PayloadMappingT) -> route_planner_.FailingAddress: # noqa: D102
        data = self._ensure_mapping(payload)

        return route_planner_.FailingAddress(
            data["failingAddress"],
            datetime.datetime.fromtimestamp(data["failingTimestamp"]),
            data["failingTime"]
        )

    # session

    def build_session(self, payload: types.PayloadMappingT) -> session_.Session: # noqa: D102
        data = self._ensure_mapping(payload)

        return session_.Session(
            data["resuming"],
            data["timeout"]
        )

    # statistics
    
    def build_statistics(self, payload: types.PayloadMappingT) -> statistics_.Statistics: # noqa: D102
        data = self._ensure_mapping(payload)

        return statistics_.Statistics(
            data["players"],
            data["playingPlayers"],
            data["uptime"],
            self.build_statistics_memory(data["memory"]),
            self.build_statistics_cpu(data["cpu"]),
            self.build_statistics_frame_statistics(data["frameStats"]) if data.get("frameStats", None) is not None else None
        )
    
    def build_statistics_memory(self, payload: types.PayloadMappingT) -> statistics_.Memory: # noqa: D102
        data = self._ensure_mapping(payload)

        return statistics_.Memory(
            data["free"],
            data["used"],
            data["allocated"],
            data["reservable"]
        )

    def build_statistics_cpu(self, payload: types.PayloadMappingT) -> statistics_.Cpu: # noqa: D102
        data = self._ensure_mapping(payload)
        
        return statistics_.Cpu(
            data["cores"],
            data["systemLoad"],
            data["lavalinkLoad"]
        )

    def build_statistics_frame_statistics(self, payload: types.PayloadMappingT) -> statistics_.FrameStatistics: # noqa: D102
        data = self._ensure_mapping(payload)

        return statistics_.FrameStatistics(
            data["sent"],
            data["nulled"],
            data["deficit"]
        )

    # track

    def build_track(self, payload: types.PayloadMappingT) -> track_.Track: # noqa: D102
        data = self._ensure_mapping(payload)

        return track_.Track(
            data["encoded"],
            self.build_track_info(data["info"]),
            data["pluginInfo"],
            data["userData"]
        )
    
    def build_track_info(self, payload: types.PayloadMappingT) -> track_.TrackInfo: # noqa: D102
        data = self._ensure_mapping(payload)

        return track_.TrackInfo(
            data["identifier"],
            data["isSeekable"],
            data["author"],
            data["length"],
            data["isStream"],
            data["position"],
            data["title"],
            data["sourceName"],
            data.get("uri", None),
            data.get("artworkUrl", None),
            data.get("isrc", None),
        )


class EventBuilder: # noqa: D101

    def build_payload_event(self, payload: str, session: Session) -> events.PayloadEvent: # noqa: D102
        event = events.PayloadEvent(payload)

        event._app = session.app
        event._client = session.client
        event._session = session

        return event
    
    def build_ready_event(self, resumed: bool, session_id: str, session: Session) -> events.ReadyEvent: # noqa: D102
        event = events.ReadyEvent(
            resumed, session_id
        )

        event._app = session.app
        event._client = session.client
        event._session = session

        return event
    
    def build_player_update_event(self, guild: hikari.SnowflakeishOr[hikari.Guild], state: player_.State, session: Session) -> events.PlayerUpdateEvent: # noqa: D102
        event = events.PlayerUpdateEvent(
            hikari.Snowflake(guild), state
        )

        event._app = session.app
        event._client = session.client
        event._session = session

        return event
    
    def build_statistics_event( # noqa: D102
        self, 
        players: int, 
        playing_players: int,
        uptime: int,
        memory: statistics_.Memory,
        cpu: statistics_.Cpu,
        frame_statistics: statistics_.FrameStatistics | None,
        session: Session
    ) -> events.StatisticsEvent: 
        event = events.StatisticsEvent(
            players, playing_players, uptime, memory, cpu, frame_statistics
        )

        event._app = session.app
        event._client = session.client
        event._session = session

        return event
    
    def build_websocket_closed_event( # noqa: D102
        self, 
        guild: hikari.SnowflakeishOr[hikari.Guild],
        code: int,
        reason: str,
        by_remote: bool,
        session: Session
    ) -> events.WebsocketClosedEvent: # noqa: D102
        event = events.WebsocketClosedEvent(
            hikari.Snowflake(guild), code, reason, by_remote
        )

        event._app = session.app
        event._client = session.client
        event._session = session

        return event
    
    def build_track_start_event(self, guild: hikari.SnowflakeishOr[hikari.Guild], track: track_.Track, session: Session) -> events.TrackStartEvent: # noqa: D102
        event = events.TrackStartEvent(
            hikari.Snowflake(guild), track
        )

        event._app = session.app
        event._client = session.client
        event._session = session

        return event
    
    def build_track_end_event( # noqa: D102
        self, 
        guild: hikari.SnowflakeishOr[hikari.Guild], 
        track: track_.Track, 
        reason: enums.TrackEndReasonType, 
        session: Session
    ) -> events.TrackEndEvent:
        event = events.TrackEndEvent(
            hikari.Snowflake(guild), track, reason
        )

        event._app = session.app
        event._client = session.client
        event._session = session

        return event
    
    def build_track_exception_event( # noqa: D102
        self, 
        guild: hikari.SnowflakeishOr[hikari.Guild], 
        track: track_.Track, 
        exception: error_.ExceptionError, 
        session: Session
    ) -> events.TrackExceptionEvent:
        event = events.TrackExceptionEvent(
            hikari.Snowflake(guild), track, exception
        )

        event._app = session.app
        event._client = session.client
        event._session = session

        return event
    
    def build_track_stuck_event( # noqa: D102
        self, guild: hikari.SnowflakeishOr[hikari.Guild], 
        track: track_.Track, 
        threshold_ms: int, 
        session: Session
    ) -> events.TrackStuckEvent:
        event = events.TrackStuckEvent(
            hikari.Snowflake(guild), track, threshold_ms
        )

        event._app = session.app
        event._client = session.client
        event._session = session

        return event
    
    def build_queue_empty_event( # noqa: D102
        self, guild: hikari.SnowflakeishOr[hikari.Guild],
        session: Session
    ) -> events.QueueEmptyEvent:
        event = events.QueueEmptyEvent(
            hikari.Snowflake(guild)
        )

        event._app = session.app
        event._client = session.client
        event._session = session

        return event
    
    def build_queue_next_event( # noqa: D102
        self, guild: hikari.SnowflakeishOr[hikari.Guild], 
        track: track_.Track,
        old_track: track_.Track,
        session: Session
    ) -> events.QueueNextEvent:
        event = events.QueueNextEvent(
            hikari.Snowflake(guild), track, old_track
        )

        event._app = session.app
        event._client = session.client
        event._session = session

        return event