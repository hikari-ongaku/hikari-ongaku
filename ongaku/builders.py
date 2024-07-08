"""Builder.

The builder, to convert most abstract classes from a payload.
"""

from __future__ import annotations

import datetime
import typing

import hikari

from ongaku import events
from ongaku.abc import errors as errors_
from ongaku.abc import events as events_
from ongaku.abc import filters as filters_
from ongaku.abc import info as info_
from ongaku.abc import player as player_
from ongaku.abc import playlist as playlist_
from ongaku.abc import routeplanner as routeplanner_
from ongaku.abc import session as session_
from ongaku.abc import statistics as statistics_
from ongaku.abc import track as track_
from ongaku.errors import RestExceptionError
from ongaku.errors import RestRequestError
from ongaku.impl import filters
from ongaku.impl import info
from ongaku.impl import player
from ongaku.impl import playlist
from ongaku.impl import routeplanner
from ongaku.impl import session
from ongaku.impl import statistics
from ongaku.impl import track
from ongaku.internal.converters import DumpType
from ongaku.internal.converters import LoadType
from ongaku.internal.converters import json_dumps
from ongaku.internal.converters import json_loads
from ongaku.internal.logger import TRACE_LEVEL
from ongaku.internal.logger import logger

if typing.TYPE_CHECKING:
    from ongaku.internal import types
    from ongaku.session import Session

_logger = logger.getChild("builders")


class EntityBuilder:
    """Entity Builder.

    The class that allows for converting payloads (str, sequence, mapping, etc) into their respective classes.

    Parameters
    ----------
    dumps
        The dumping method to use when dumping payloads.
    loads
        The loading method to use when loading payloads.
    """

    __slots__: typing.Sequence[str] = (
        "_dumps",
        "_loads",
    )

    def __init__(
        self,
        *,
        dumps: DumpType = json_dumps,
        loads: LoadType = json_loads,
    ) -> None:
        self._dumps = dumps
        self._loads = loads

    def _ensure_mapping(
        self, payload: types.PayloadMappingT, /
    ) -> typing.Mapping[str, typing.Any]:
        if isinstance(payload, str | bytes):
            data = self._loads(payload)
            if isinstance(data, typing.Sequence):
                raise TypeError("Mapping is required.")
            return data

        return payload

    def _ensure_sequence(
        self, payload: types.PayloadSequenceT
    ) -> typing.Sequence[typing.Any]:
        if isinstance(payload, str | bytes):
            data = self._loads(payload)
            if isinstance(data, typing.Mapping):
                raise TypeError("Sequence is required.")
            return data

        return payload

    # errors

    def build_rest_error(self, payload: types.PayloadMappingT, /) -> RestRequestError:
        """Build Rest Request Error.

        Builds a [`RestRequestError`][ongaku.errors.RestRequestError] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.

        Returns
        -------
        RestRequestError
            The object from the payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into RestError")

        return RestRequestError(
            datetime.datetime.fromtimestamp(
                int(data["timestamp"]) / 1000, datetime.timezone.utc
            ),
            data["status"],
            data["error"],
            data["message"],
            data["path"],
            data.get("trace", None),
        )

    def build_exception_error(
        self, payload: types.PayloadMappingT, /
    ) -> RestExceptionError:
        """Build Rest Exception Error.

        Builds a [`RestExceptionError`][ongaku.errors.RestExceptionError] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.

        Returns
        -------
        RestExceptionError
            The object from the payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into ExceptionError")

        return RestExceptionError(
            data.get("message", None),
            errors_.SeverityType(data["severity"]),
            data["cause"],
        )

    # Events

    def build_ready_event(
        self, payload: types.PayloadMappingT, /, *, session: Session
    ) -> events.ReadyEvent:
        """Build Ready Event.

        Builds a [`Ready`][ongaku.events.ReadyEvent] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.
        session
            The session attached to this event.

        Returns
        -------
        events.ReadyEvent
            The object from the payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into Ready")

        return events.ReadyEvent.from_session(
            session, resumed=data["resumed"], session_id=data["sessionId"]
        )

    def build_player_update_event(
        self, payload: types.PayloadMappingT, /, *, session: Session
    ) -> events.PlayerUpdateEvent:
        """Build Player Update Event.

        Builds a [`PlayerUpdateEvent`][ongaku.events.PlayerUpdateEvent] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.
        session
            The session attached to this event.

        Returns
        -------
        events.PlayerUpdateEvent
            The object from the payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into PlayerUpdate")

        return events.PlayerUpdateEvent.from_session(
            session,
            guild_id=hikari.Snowflake(int(data["guildId"])),
            state=self.build_player_state(data["state"]),
        )

    def build_statistics_event(
        self, payload: types.PayloadMappingT, /, *, session: Session
    ) -> events.StatisticsEvent:
        """Build Statistics Event.

        Builds a [`StatisticsEvent`][ongaku.events.StatisticsEvent] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.
        session
            The session attached to this event.

        Returns
        -------
        events.StatisticsEvent
            The object from the payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        statistics = self.build_statistics(payload)

        return events.StatisticsEvent.from_session(
            session,
            players=statistics.players,
            playing_players=statistics.playing_players,
            uptime=statistics.uptime,
            memory=statistics.memory,
            cpu=statistics.cpu,
            frame_statistics=statistics.frame_stats,
        )

    def build_track_start_event(
        self, payload: types.PayloadMappingT, /, *, session: Session
    ) -> events.TrackStartEvent:
        """Build Track Start Event.

        Builds a [`TrackStartEvent`][ongaku.events.TrackStartEvent] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.
        session
            The session attached to this event.

        Returns
        -------
        events.TrackStartEvent
            The object from the payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into TrackStart")

        return events.TrackStartEvent.from_session(
            session,
            guild_id=hikari.Snowflake(int(data["guildId"])),
            track=self.build_track(data["track"]),
        )

    def build_track_end_event(
        self, payload: types.PayloadMappingT, /, *, session: Session
    ) -> events.TrackEndEvent:
        """Build Track End Event.

        Builds a [`TrackEndEvent`][ongaku.events.TrackEndEvent] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.
        session
            The session attached to this event.

        Returns
        -------
        events.TrackEndEvent
            The object from the payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into TrackEnd")

        return events.TrackEndEvent.from_session(
            session,
            guild_id=hikari.Snowflake(int(data["guildId"])),
            track=self.build_track(data["track"]),
            reason=events_.TrackEndReasonType(data["reason"]),
        )

    def build_track_exception(
        self, payload: types.PayloadMappingT, /
    ) -> events.TrackException:
        """Build Track Exception.

        Builds a [`TrackException`][ongaku.events.TrackException] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.

        Returns
        -------
        events.TrackException
            The object from the payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        data = self._ensure_mapping(payload)

        return events.TrackException(
            message=data.get("message", None),
            severity=errors_.SeverityType(data["severity"]),
            cause=data["cause"],
        )

    def build_track_exception_event(
        self, payload: types.PayloadMappingT, /, *, session: Session
    ) -> events.TrackExceptionEvent:
        """Build Track Exception Event.

        Builds a [`TrackExceptionEvent`][ongaku.events.TrackExceptionEvent] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.
        session
            The session attached to this event.

        Returns
        -------
        events.TrackExceptionEvent
            The object from the payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into TrackException")

        return events.TrackExceptionEvent.from_session(
            session,
            guild_id=hikari.Snowflake(int(data["guildId"])),
            track=self.build_track(data["track"]),
            exception=self.build_track_exception(data["exception"]),
        )

    def build_track_stuck_event(
        self, payload: types.PayloadMappingT, /, *, session: Session
    ) -> events.TrackStuckEvent:
        """Build Track Stuck Event.

        Builds a [`TrackStuckEvent`][ongaku.events.TrackStuckEvent] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.
        session
            The session attached to this event.

        Returns
        -------
        events.TrackStuckEvent
            The object from the payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into TrackStuck")

        return events.TrackStuckEvent.from_session(
            session,
            guild_id=hikari.Snowflake(int(data["guildId"])),
            track=self.build_track(data["track"]),
            threshold_ms=data["thresholdMs"],
        )

    def build_websocket_closed_event(
        self, payload: types.PayloadMappingT, /, *, session: Session
    ) -> events.WebsocketClosedEvent:
        """Build Websocket Closed Event.

        Builds a [`WebsocketClosedEvent`][ongaku.events.WebsocketClosedEvent] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.
        session
            The session attached to this event.

        Returns
        -------
        events.WebsocketClosedEvent
            The object from the payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into WebsocketClosed")

        return events.WebsocketClosedEvent.from_session(
            session,
            guild_id=hikari.Snowflake(int(data["guildId"])),
            code=data["code"],
            reason=data["reason"],
            by_remote=data["byRemote"],
        )

    # Filters

    def build_filters(self, payload: types.PayloadMappingT, /) -> filters_.Filters:
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into Filters")

        equalizer: list[filters_.Equalizer] = []

        if data.get("equalizer", None) is not None:
            for eq in data["equalizer"]:
                equalizer.append(self.build_filters_equalizer(eq))

        return filters.Filters(
            volume=data.get("volume", None),
            equalizer=equalizer,
            karaoke=self.build_filters_karaoke(data["karaoke"])
            if data.get("karaoke", None)
            else None,
            timescale=self.build_filters_timescale(data["timescale"])
            if data.get("timescale", None)
            else None,
            tremolo=self.build_filters_tremolo(data["tremolo"])
            if data.get("tremolo", None)
            else None,
            vibrato=self.build_filters_vibrato(data["vibrato"])
            if data.get("vibrato", None)
            else None,
            rotation=self.build_filters_rotation(data["rotation"])
            if data.get("rotation", None)
            else None,
            distortion=self.build_filters_distortion(data["distortion"])
            if data.get("distortion", None)
            else None,
            channel_mix=self.build_filters_channel_mix(data["channelMix"])
            if data.get("channelMix", None)
            else None,
            low_pass=self.build_filters_low_pass(data["lowPass"])
            if data.get("lowPass", None)
            else None,
            plugin_filters=data.get("pluginFilters", None),
        )

    def build_filters_equalizer(
        self, payload: types.PayloadMappingT, /
    ) -> filters_.Equalizer:
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into Filters Equalizer")

        return filters.Equalizer(
            band=filters_.BandType(data["band"]), gain=data["gain"]
        )

    def build_filters_karaoke(
        self, payload: types.PayloadMappingT, /
    ) -> filters_.Karaoke:
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into Filters Karaoke")

        return filters.Karaoke(
            level=data.get("level", None),
            mono_level=data.get("monoLevel", None),
            filter_band=data.get("filterBand", None),
            filter_width=data.get("filterWidth", None),
        )

    def build_filters_timescale(
        self, payload: types.PayloadMappingT, /
    ) -> filters_.Timescale:
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into Filters Timescale")

        return filters.Timescale(
            speed=data.get("speed", None),
            pitch=data.get("pitch", None),
            rate=data.get("rate", None),
        )

    def build_filters_tremolo(
        self, payload: types.PayloadMappingT, /
    ) -> filters_.Tremolo:
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into Filters Tremolo")

        return filters.Tremolo(
            frequency=data.get("frequency", None),
            depth=data.get("depth", None),
        )

    def build_filters_vibrato(
        self, payload: types.PayloadMappingT, /
    ) -> filters_.Vibrato:
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into Filters Vibrato")

        return filters.Vibrato(
            frequency=data.get("frequency", None),
            depth=data.get("depth", None),
        )

    def build_filters_rotation(
        self, payload: types.PayloadMappingT, /
    ) -> filters_.Rotation:
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into Filters Rotation")

        return filters.Rotation(
            rotation_hz=data.get("rotationHz", None),
        )

    def build_filters_distortion(
        self, payload: types.PayloadMappingT, /
    ) -> filters_.Distortion:
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into Filters Distortion")

        return filters.Distortion(
            sin_offset=data.get("sinOffset", None),
            sin_scale=data.get("sinScale", None),
            cos_offset=data.get("cosOffset", None),
            cos_scale=data.get("cosScale", None),
            tan_offset=data.get("tanOffset", None),
            tan_scale=data.get("tanScale", None),
            offset=data.get("offset", None),
            scale=data.get("scale", None),
        )

    def build_filters_channel_mix(
        self, payload: types.PayloadMappingT, /
    ) -> filters_.ChannelMix:
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into Filters ChannelMix")

        return filters.ChannelMix(
            left_to_left=data.get("leftToLeft", None),
            left_to_right=data.get("leftToRight", None),
            right_to_left=data.get("rightToLeft", None),
            right_to_right=data.get("rightToRight", None),
        )

    def build_filters_low_pass(
        self, payload: types.PayloadMappingT, /
    ) -> filters_.LowPass:
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into Filters LowPass")

        return filters.LowPass(
            smoothing=data.get("smoothing", None),
        )

    # info

    def build_info(self, payload: types.PayloadMappingT, /) -> info_.Info:
        """Build Information.

        Builds a [`Information`][ongaku.abc.info.Info] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.

        Returns
        -------
        info_.Info
            The object from the payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into Info")

        source_managers: list[str] = []

        for manager in data["sourceManagers"]:
            source_managers.append(manager)

        filters: list[str] = []

        for filter in data["filters"]:
            filters.append(filter)

        plugins: list[info_.Plugin] = []

        for plugin in data["plugins"]:
            plugins.append(self.build_info_plugin(plugin))

        return info.Info(
            version=self.build_info_version(data["version"]),
            build_time=datetime.datetime.fromtimestamp(
                int(data["buildTime"]) / 1000, datetime.timezone.utc
            ),
            git=self.build_info_git(data["git"]),
            jvm=data["jvm"],
            lavaplayer=data["lavaplayer"],
            source_managers=source_managers,
            filters=filters,
            plugins=plugins,
        )

    def build_info_version(self, payload: types.PayloadMappingT, /) -> info_.Version:
        """Build Version Information.

        Builds a [`Version`][ongaku.abc.info.Version] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.

        Returns
        -------
        info_.Version
            The object from the payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        data = self._ensure_mapping(payload)

        _logger.log(
            TRACE_LEVEL, f"Decoding payload: {payload} into Information Version"
        )

        return info.Version(
            semver=data["semver"],
            major=data["major"],
            minor=data["minor"],
            patch=data["patch"],
            pre_release=data["preRelease"],
            build=data.get("build", None),
        )

    def build_info_git(self, payload: types.PayloadMappingT, /) -> info_.Git:
        """Build Git Information.

        Builds a [`Git`][ongaku.abc.info.Git] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.

        Returns
        -------
        info_.Info
            The object from the payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into Information Git")

        return info.Git(
            branch=data["branch"],
            commit=data["commit"],
            commit_time=datetime.datetime.fromtimestamp(
                int(data["commitTime"]) / 1000, datetime.timezone.utc
            ),
        )

    def build_info_plugin(self, payload: types.PayloadMappingT, /) -> info_.Plugin:
        """Build Plugin Information.

        Builds a [`Plugin`][ongaku.abc.info.Plugin] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.

        Returns
        -------
        info_.Plugin
            The object from the payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into Information Plugin")

        return info.Plugin(name=data["name"], version=data["version"])

    # Player

    def build_player(self, payload: types.PayloadMappingT, /) -> player_.Player:
        """Build Player.

        Builds a [`Player`][ongaku.abc.player.Player] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.

        Returns
        -------
        player_.Player
            The object from the payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into Player")

        return player.Player(
            guild_id=hikari.Snowflake(int(data["guildId"])),
            track=self.build_track(data["track"]) if data.get("track", None) else None,
            volume=data["volume"],
            is_paused=data["paused"],
            state=self.build_player_state(data["state"]),
            voice=self.build_player_voice(data["voice"]),
            filters=self.build_filters(data["filters"])
            if data.get("filters", False)
            else None,
        )

    def build_player_state(self, payload: types.PayloadMappingT, /) -> player_.State:
        """Build Player State.

        Builds a [`State`][ongaku.abc.player.State] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.

        Returns
        -------
        player_.State
            The [`State`][ongaku.abc.player.State] object.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into Player State")

        return player.State(
            time=datetime.datetime.fromtimestamp(
                int(data["time"]) / 1000, datetime.timezone.utc
            ),
            position=data["position"],
            connected=data["connected"],
            ping=data["ping"],
        )

    def build_player_voice(self, payload: types.PayloadMappingT, /) -> player_.Voice:
        """Build Player Voice.

        Builds a [`Voice`][ongaku.abc.player.Voice] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.

        Returns
        -------
        player_.Voice
            The object from the payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into Player Voice")

        return player.Voice(
            token=data["token"], endpoint=data["endpoint"], session_id=data["sessionId"]
        )

    # playlist

    def build_playlist(self, payload: types.PayloadMappingT, /) -> playlist_.Playlist:
        """Build Playlist.

        Builds a [`Playlist`][ongaku.abc.playlist.Playlist] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.

        Returns
        -------
        playlist_.Playlist
            The object from the payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into Playlist")

        tracks: list[track_.Track] = []

        for track_payload in data["tracks"]:
            tracks.append(self.build_track(track_payload))

        return playlist.Playlist(
            info=self.build_playlist_info(data["info"]),
            tracks=tracks,
            plugin_info=data["pluginInfo"],
        )

    def build_playlist_info(
        self, payload: types.PayloadMappingT, /
    ) -> playlist_.PlaylistInfo:
        """Build Playlist Info.

        Builds a [`PlaylistInfo`][ongaku.abc.playlist.PlaylistInfo] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.

        Returns
        -------
        playlist_.PlaylistInfo
            The object from the payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into Playlist Info")

        return playlist.PlaylistInfo(
            name=data["name"], selected_track=data["selectedTrack"]
        )

    # route planner

    def build_routeplanner_status(
        self, payload: types.PayloadMappingT, /
    ) -> routeplanner_.RoutePlannerStatus:
        """Build Route Planner Status.

        Builds a [`RoutePlannerStatus`][ongaku.abc.routeplanner.RoutePlannerStatus] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.

        Returns
        -------
        routeplanner_.RoutePlannerStatus
            The object from the payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into RoutePlannerStatus")

        return routeplanner.RoutePlannerStatus(
            cls=routeplanner_.RoutePlannerType(data["class"]),
            details=self.build_routeplanner_details(data["details"]),
        )

    def build_routeplanner_details(
        self, payload: types.PayloadMappingT, /
    ) -> routeplanner_.RoutePlannerDetails:
        """Build Route Planner Details.

        Builds a [`RoutePlannerDetails`][ongaku.abc.routeplanner.RoutePlannerDetails] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.

        Returns
        -------
        routeplanner_.RoutePlannerDetails
            The object from the payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        data = self._ensure_mapping(payload)

        _logger.log(
            TRACE_LEVEL, f"Decoding payload: {payload} into RoutePlannerDetails"
        )

        failing_addresses: list[routeplanner_.FailingAddress] = []

        for failing_address in data["failingAddresses"]:
            failing_addresses.append(
                self.build_routeplanner_failing_address(failing_address)
            )

        return routeplanner.RoutePlannerDetails(
            ip_block=self.build_routeplanner_ipblock(data["ipBlock"]),
            failing_addresses=failing_addresses,
            rotate_index=data.get("rotateIndex", None),
            ip_index=data.get("ipIndex", None),
            current_address=data.get("currentAddress", None),
            current_address_index=data.get("currentAddressIndex", None),
            block_index=data.get("blockIndex", None),
        )

    def build_routeplanner_ipblock(
        self, payload: types.PayloadMappingT, /
    ) -> routeplanner_.IPBlock:
        """Build Route Planner IP Block.

        Builds a [`IPBlock`][ongaku.abc.routeplanner.IPBlock] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.

        Returns
        -------
        routeplanner_.IPBlock
            The object from the payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into IPBlock")

        return routeplanner.IPBlock(
            type=routeplanner_.IPBlockType(data["type"]), size=data["size"]
        )

    def build_routeplanner_failing_address(
        self, payload: types.PayloadMappingT, /
    ) -> routeplanner_.FailingAddress:
        """Build Route Planner Details.

        Builds a [`RoutePlannerDetails`][ongaku.abc.routeplanner.RoutePlannerDetails] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.

        Returns
        -------
        routeplanner_.RoutePlannerDetails
            The object from the payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into FailingAddress")

        return routeplanner.FailingAddress(
            address=data["failingAddress"],
            timestamp=datetime.datetime.fromtimestamp(
                int(data["failingTimestamp"]) / 1000, datetime.timezone.utc
            ),
            time=data["failingTime"],
        )

    # session

    def build_session(self, payload: types.PayloadMappingT, /) -> session_.Session:
        """Build Session.

        Builds a [`Session`][ongaku.abc.session.Session] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.

        Returns
        -------
        session_.Session
            The object from the payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into Session")

        return session.Session(resuming=data["resuming"], timeout=data["timeout"])

    # statistics

    def build_statistics(
        self, payload: types.PayloadMappingT, /
    ) -> statistics_.Statistics:
        """Build Statistics.

        Builds a [`Statistics`][ongaku.abc.statistics.Statistics] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.

        Returns
        -------
        statistics_.Statistics
            The object from the payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into Statistics")

        return statistics.Statistics(
            players=data["players"],
            playing_players=data["playingPlayers"],
            uptime=data["uptime"],
            memory=self.build_statistics_memory(data["memory"]),
            cpu=self.build_statistics_cpu(data["cpu"]),
            frame_statistics=self.build_statistics_frame_statistics(data["frameStats"])
            if data.get("frameStats", None) is not None
            else None,
        )

    def build_statistics_memory(
        self, payload: types.PayloadMappingT, /
    ) -> statistics_.Memory:
        """Build Memory Statistics.

        Builds a [`Memory`][ongaku.abc.statistics.Memory] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.

        Returns
        -------
        statistics_.Memory
            The object from the payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into Statistics Memory")

        return statistics.Memory(
            free=data["free"],
            used=data["used"],
            allocated=data["allocated"],
            reservable=data["reservable"],
        )

    def build_statistics_cpu(
        self, payload: types.PayloadMappingT, /
    ) -> statistics_.Cpu:
        """Build Cpu Statistics.

        Builds a [`Cpu`][ongaku.abc.statistics.Cpu] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.

        Returns
        -------
        statistics_.Cpu
            The object from the payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into Statistics Cpu")

        return statistics.Cpu(
            cores=data["cores"],
            system_load=data["systemLoad"],
            lavalink_load=data["lavalinkLoad"],
        )

    def build_statistics_frame_statistics(
        self, payload: types.PayloadMappingT, /
    ) -> statistics_.FrameStatistics:
        """Build Frame Statistics.

        Builds a [`Statistics`][ongaku.abc.statistics.Statistics] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.

        Returns
        -------
        statistics_.FrameStatistics
            The object from the payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        data = self._ensure_mapping(payload)

        _logger.log(
            TRACE_LEVEL, f"Decoding payload: {payload} into Statistics FrameStatistics"
        )

        return statistics.FrameStatistics(
            sent=data["sent"], nulled=data["nulled"], deficit=data["deficit"]
        )

    # track

    def build_track(self, payload: types.PayloadMappingT, /) -> track_.Track:
        """Build Track.

        Builds a [`Track`][ongaku.abc.track.Track] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.

        Returns
        -------
        track_.Track
            The object from the payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into Track")

        return track.Track(
            encoded=data["encoded"],
            info=self.build_track_info(data["info"]),
            plugin_info=data["pluginInfo"],
            user_data=data["userData"] if data.get("userData", None) else {},
            requestor=None,
        )

    def build_track_info(self, payload: types.PayloadMappingT, /) -> track_.TrackInfo:
        """Build Track Information.

        Builds a [`TrackInformation`][ongaku.abc.track.TrackInfo] object, from a payload.

        Parameters
        ----------
        payload
            The payload you provide.

        Returns
        -------
        track_.TrackInfo
            The object from the payload.

        Raises
        ------
        TypeError
            Raised when the payload could not be turned into a mapping.
        KeyError
            Raised when a value was not found in the payload.
        """
        data = self._ensure_mapping(payload)

        _logger.log(TRACE_LEVEL, f"Decoding payload: {payload} into TrackInfo")

        return track.TrackInfo(
            identifier=data["identifier"],
            is_seekable=data["isSeekable"],
            author=data["author"],
            length=data["length"],
            is_stream=data["isStream"],
            position=data["position"],
            title=data["title"],
            source_name=data["sourceName"],
            uri=data.get("uri", None),
            artwork_url=data.get("artworkUrl", None),
            isrc=data.get("isrc", None),
        )


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
