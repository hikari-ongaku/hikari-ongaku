import datetime
import typing

import hikari
import orjson
import pytest

from ongaku.abc.errors import SeverityType
from ongaku.abc.events import TrackEndReasonType
from ongaku.abc.filters import BandType
from ongaku.abc.filters import Filters
from ongaku.abc.routeplanner import IPBlockType
from ongaku.abc.routeplanner import RoutePlannerType
from ongaku.builders import EntityBuilder
from ongaku.impl.player import Voice
from ongaku.session import Session
from tests import payloads


@pytest.fixture
def builder() -> EntityBuilder:
    return EntityBuilder()


def test_properties():
    builder = EntityBuilder(dumps=orjson.dumps, loads=orjson.loads)

    assert builder._dumps == orjson.dumps
    assert builder._loads == orjson.loads


class TestEnsureTypes:
    def test__ensure_mapping(self, builder: EntityBuilder):
        test_mapping: typing.Any = orjson.dumps({"beanos": True})

        ensure_mapping = builder._ensure_mapping(test_mapping)

        assert isinstance(ensure_mapping, typing.Mapping)
        assert ensure_mapping == orjson.loads(test_mapping)
    
    def test__ensure_mapping_invalid(self, builder: EntityBuilder):
        test_mapping: typing.Any = orjson.dumps(["beanos", "apple"])
        
        with pytest.raises(TypeError, match="Mapping is required."):
            builder._ensure_mapping(test_mapping)

    def test__ensure_sequence(self, builder: EntityBuilder):
        test_sequence: typing.Any = orjson.dumps(["beanos", "apple"])

        ensure_sequence = builder._ensure_sequence(test_sequence)

        assert isinstance(ensure_sequence, typing.Sequence)
        assert ensure_sequence == orjson.loads(test_sequence)
    
    def test__ensure_sequence_invalid(self, builder: EntityBuilder):
        test_sequence: typing.Any = orjson.dumps({"beanos": True})

        with pytest.raises(TypeError, match="Sequence is required."):
            builder._ensure_sequence(test_sequence)


class TestErrors:
    def test_deserialize_rest_error(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_rest_error(payloads.REST_ERROR_PAYLOAD)

        assert parsed_result.timestamp == datetime.datetime.fromtimestamp(
            1 / 1000, datetime.timezone.utc
        )
        assert parsed_result.status == 2
        assert parsed_result.error == "error"
        assert parsed_result.message == "message"
        assert parsed_result.path == "path"
        assert parsed_result.trace == "trace"

    def test_deserialize_exception_error(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_exception_error(
            payloads.EXCEPTION_ERROR_PAYLOAD
        )

        assert parsed_result.message == "message"
        assert parsed_result.severity == SeverityType.COMMON
        assert parsed_result.cause == "cause"


class TestEvents:
    def test_deserialize_ready_event(
        self, ongaku_session: Session, builder: EntityBuilder
    ):
        parsed_result = builder.deserialize_ready_event(
            payloads.READY_PAYLOAD, session=ongaku_session
        )

        assert parsed_result.session == ongaku_session
        assert parsed_result.client == ongaku_session.client
        assert parsed_result.app == ongaku_session.app
        assert parsed_result.resumed is False
        assert parsed_result.session_id == "session_id"

    def test_deserialize_player_update_event(
        self, ongaku_session: Session, builder: EntityBuilder
    ):
        parsed_result = builder.deserialize_player_update_event(
            payloads.PLAYER_UPDATE_PAYLOAD, session=ongaku_session
        )

        assert parsed_result.session == ongaku_session
        assert parsed_result.client == ongaku_session.client
        assert parsed_result.app == ongaku_session.app
        assert isinstance(parsed_result.guild_id, hikari.Snowflake)
        assert parsed_result.guild_id == hikari.Snowflake(1234567890)
        assert parsed_result.state == builder.deserialize_player_state(
            payloads.PLAYER_STATE_PAYLOAD
        )

    def test_deserialize_statistics_event(self, ongaku_session: Session, builder: EntityBuilder):
        parsed_result = builder.deserialize_statistics_event(
            payloads.STATISTICS_PAYLOAD, session=ongaku_session
        )

        parsed_statistics = builder.deserialize_statistics(payloads.STATISTICS_PAYLOAD)

        assert parsed_result.session == ongaku_session
        assert parsed_result.client == ongaku_session.client
        assert parsed_result.app == ongaku_session.app
        assert parsed_result.players == parsed_statistics.players
        assert parsed_result.playing_players == parsed_statistics.playing_players
        assert parsed_result.uptime == parsed_statistics.uptime
        assert parsed_result.memory == parsed_statistics.memory
        assert parsed_result.cpu == parsed_statistics.cpu
        assert parsed_result.frame_stats == parsed_statistics.frame_stats

    def test_deserialize_track_start_event(
        self, ongaku_session: Session, builder: EntityBuilder
    ):
        parsed_result = builder.deserialize_track_start_event(
            payloads.TRACK_START_PAYLOAD, session=ongaku_session
        )

        assert parsed_result.session == ongaku_session
        assert parsed_result.client == ongaku_session.client
        assert parsed_result.app == ongaku_session.app
        assert isinstance(parsed_result.guild_id, hikari.Snowflake)
        assert parsed_result.guild_id == hikari.Snowflake(1234567890)
        assert parsed_result.track == builder.deserialize_track(payloads.TRACK_PAYLOAD)

    def test_deserialize_track_end_event(
        self, ongaku_session: Session, builder: EntityBuilder
    ):
        parsed_result = builder.deserialize_track_end_event(
            payloads.TRACK_END_PAYLOAD, session=ongaku_session
        )

        assert parsed_result.session == ongaku_session
        assert parsed_result.client == ongaku_session.client
        assert parsed_result.app == ongaku_session.app
        assert isinstance(parsed_result.guild_id, hikari.Snowflake)
        assert parsed_result.guild_id == hikari.Snowflake(1234567890)
        assert parsed_result.track == builder.deserialize_track(payloads.TRACK_PAYLOAD)
        assert parsed_result.reason == TrackEndReasonType.FINISHED

    def test_deserialize_track_exception(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_track_exception(
            payloads.EXCEPTION_ERROR_PAYLOAD
        )

        assert parsed_result.message == "message"
        assert parsed_result.severity == SeverityType.COMMON
        assert parsed_result.cause == "cause"

    def test_deserialize_track_exception_event(
        self, ongaku_session: Session, builder: EntityBuilder
    ):
        parsed_result = builder.deserialize_track_exception_event(
            payloads.TRACK_EXCEPTION_PAYLOAD, session=ongaku_session
        )

        assert parsed_result.session == ongaku_session
        assert parsed_result.client == ongaku_session.client
        assert parsed_result.app == ongaku_session.app
        assert isinstance(parsed_result.guild_id, hikari.Snowflake)
        assert parsed_result.guild_id == hikari.Snowflake(1234567890)
        assert parsed_result.track == builder.deserialize_track(payloads.TRACK_PAYLOAD)
        assert parsed_result.exception == builder.deserialize_exception_error(
            payloads.EXCEPTION_ERROR_PAYLOAD
        )

    def test_deserialize_track_stuck_event(
        self, ongaku_session: Session, builder: EntityBuilder
    ):
        parsed_result = builder.deserialize_track_stuck_event(
            payloads.TRACK_STUCK_PAYLOAD, session=ongaku_session
        )

        assert parsed_result.session == ongaku_session
        assert parsed_result.client == ongaku_session.client
        assert parsed_result.app == ongaku_session.app
        assert isinstance(parsed_result.guild_id, hikari.Snowflake)
        assert parsed_result.guild_id == hikari.Snowflake(1234567890)
        assert parsed_result.track == builder.deserialize_track(payloads.TRACK_PAYLOAD)
        assert parsed_result.threshold_ms == 1

    def test_deserialize_websocket_closed_event(
        self, ongaku_session: Session, builder: EntityBuilder
    ):
        parsed_result = builder.deserialize_websocket_closed_event(
            payloads.WEBSOCKET_CLOSED_PAYLOAD, session=ongaku_session
        )

        assert parsed_result.session == ongaku_session
        assert parsed_result.client == ongaku_session.client
        assert parsed_result.app == ongaku_session.app
        assert isinstance(parsed_result.guild_id, hikari.Snowflake)
        assert parsed_result.guild_id == hikari.Snowflake(1234567890)
        assert parsed_result.code == 1
        assert parsed_result.reason == "reason"
        assert parsed_result.by_remote is False


class TestFilters:
    def test_deserialize_filters(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_filters(payloads.FILTERS_PAYLOAD)

        assert parsed_result.volume == 1.2
        assert parsed_result.equalizer == [
            builder.deserialize_filters_equalizer(payloads.FILTERS_EQUALIZER_PAYLOAD)
        ]
        assert parsed_result.karaoke == builder.deserialize_filters_karaoke(
            payloads.FILTERS_KARAOKE_PAYLOAD
        )
        assert parsed_result.timescale == builder.deserialize_filters_timescale(
            payloads.FILTERS_TIMESCALE_PAYLOAD
        )
        assert parsed_result.tremolo == builder.deserialize_filters_tremolo(
            payloads.FILTERS_TREMOLO_PAYLOAD
        )
        assert parsed_result.vibrato == builder.deserialize_filters_vibrato(
            payloads.FILTERS_VIBRATO_PAYLOAD
        )
        assert parsed_result.rotation == builder.deserialize_filters_rotation(
            payloads.FILTERS_ROTATION_PAYLOAD
        )
        assert parsed_result.distortion == builder.deserialize_filters_distortion(
            payloads.FILTERS_DISTORTION_PAYLOAD
        )
        assert parsed_result.channel_mix == builder.deserialize_filters_channel_mix(
            payloads.FILTERS_CHANNEL_MIX_PAYLOAD
        )
        assert parsed_result.low_pass == builder.deserialize_filters_low_pass(
            payloads.FILTERS_LOW_PASS_PAYLOAD
        )

    def test_deserialize_filters_equalizer(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_filters_equalizer(
            payloads.FILTERS_EQUALIZER_PAYLOAD
        )

        assert parsed_result.band == BandType.HZ100
        assert parsed_result.gain == 0.95

    def test_deserialize_filters_karaoke(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_filters_karaoke(
            payloads.FILTERS_KARAOKE_PAYLOAD
        )

        assert parsed_result.level == 1
        assert parsed_result.mono_level == 0.5
        assert parsed_result.filter_band == 4.5
        assert parsed_result.filter_width == 6

    def test_deserialize_filters_timescale(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_filters_timescale(
            payloads.FILTERS_TIMESCALE_PAYLOAD
        )

        assert parsed_result.speed == 1.2
        assert parsed_result.pitch == 2.3
        assert parsed_result.rate == 4

    def test_deserialize_filters_tremolo(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_filters_tremolo(
            payloads.FILTERS_TREMOLO_PAYLOAD
        )

        assert parsed_result.frequency == 1.2
        assert parsed_result.depth == 1

    def test_deserialize_filters_vibrato(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_filters_vibrato(
            payloads.FILTERS_VIBRATO_PAYLOAD
        )

        assert parsed_result.frequency == 3
        assert parsed_result.depth == 0.5

    def test_deserialize_filters_rotation(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_filters_rotation(
            payloads.FILTERS_ROTATION_PAYLOAD
        )

        assert parsed_result.rotation_hz == 6

    def test_deserialize_filters_distortion(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_filters_distortion(
            payloads.FILTERS_DISTORTION_PAYLOAD
        )

        assert parsed_result.sin_offset == 2.1
        assert parsed_result.sin_scale == 3
        assert parsed_result.cos_offset == 6.9
        assert parsed_result.cos_scale == 7.2
        assert parsed_result.tan_offset == 9.4
        assert parsed_result.tan_scale == 2
        assert parsed_result.offset == 4.1
        assert parsed_result.scale == 8

    def test_deserialize_filters_channel_mix(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_filters_channel_mix(
            payloads.FILTERS_CHANNEL_MIX_PAYLOAD
        )

        assert parsed_result.left_to_left == 0
        assert parsed_result.left_to_right == 1
        assert parsed_result.right_to_left == 0.5
        assert parsed_result.right_to_right == 0.63

    def test_deserialize_filters_low_pass(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_filters_low_pass(
            payloads.FILTERS_LOW_PASS_PAYLOAD
        )

        assert parsed_result.smoothing == 3.8

    def test_serialize_filters(self, builder: EntityBuilder, ongaku_filters: Filters):
        parsed_result = builder.serialize_filters(ongaku_filters)

        assert parsed_result == payloads.FILTERS_PAYLOAD

    def test_serialize_filters_equalizer(
        self, builder: EntityBuilder, ongaku_filters: Filters
    ):
        assert ongaku_filters.equalizer[0] is not None

        parsed_result = builder.serialize_filters_equalizer(ongaku_filters.equalizer[0])

        assert parsed_result == payloads.FILTERS_EQUALIZER_PAYLOAD

    def test_serialize_filters_karaoke(
        self, builder: EntityBuilder, ongaku_filters: Filters
    ):
        assert ongaku_filters.karaoke is not None

        parsed_result = builder.serialize_filters_karaoke(ongaku_filters.karaoke)

        assert parsed_result == payloads.FILTERS_KARAOKE_PAYLOAD

    def test_serialize_filters_timescale(
        self, builder: EntityBuilder, ongaku_filters: Filters
    ):
        assert ongaku_filters.timescale is not None

        parsed_result = builder.serialize_filters_timescale(ongaku_filters.timescale)

        assert parsed_result == payloads.FILTERS_TIMESCALE_PAYLOAD

    def test_serialize_filters_tremolo(
        self, builder: EntityBuilder, ongaku_filters: Filters
    ):
        assert ongaku_filters.tremolo is not None

        parsed_result = builder.serialize_filters_tremolo(ongaku_filters.tremolo)

        assert parsed_result == payloads.FILTERS_TREMOLO_PAYLOAD

    def test_serialize_filters_vibrato(
        self, builder: EntityBuilder, ongaku_filters: Filters
    ):
        assert ongaku_filters.vibrato is not None

        parsed_result = builder.serialize_filters_vibrato(ongaku_filters.vibrato)

        assert parsed_result == payloads.FILTERS_VIBRATO_PAYLOAD

    def test_serialize_filters_rotation(
        self, builder: EntityBuilder, ongaku_filters: Filters
    ):
        assert ongaku_filters.rotation is not None

        parsed_result = builder.serialize_filters_rotation(ongaku_filters.rotation)

        assert parsed_result == payloads.FILTERS_ROTATION_PAYLOAD

    def test_serialize_filters_distortion(
        self, builder: EntityBuilder, ongaku_filters: Filters
    ):
        assert ongaku_filters.distortion is not None

        parsed_result = builder.serialize_filters_distortion(ongaku_filters.distortion)

        assert parsed_result == payloads.FILTERS_DISTORTION_PAYLOAD

    def test_serialize_filters_channel_mix(
        self, builder: EntityBuilder, ongaku_filters: Filters
    ):
        assert ongaku_filters.channel_mix is not None

        parsed_result = builder.serialize_filters_channel_mix(
            ongaku_filters.channel_mix
        )

        assert parsed_result == payloads.FILTERS_CHANNEL_MIX_PAYLOAD

    def test_serialize_filters_low_pass(
        self, builder: EntityBuilder, ongaku_filters: Filters
    ):
        assert ongaku_filters.low_pass is not None

        parsed_result = builder.serialize_filters_low_pass(ongaku_filters.low_pass)

        assert parsed_result == payloads.FILTERS_LOW_PASS_PAYLOAD


class TestInfo:
    def test_deserialize_info(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_info(payloads.INFO_PAYLOAD)

        assert parsed_result.version == builder.deserialize_info_version(
            payloads.INFO_VERSION_PAYLOAD
        )
        assert parsed_result.build_time == datetime.datetime.fromtimestamp(
            1 / 1000, datetime.timezone.utc
        )
        assert parsed_result.git == builder.deserialize_info_git(
            payloads.INFO_GIT_PAYLOAD
        )
        assert parsed_result.jvm == "jvm"
        assert parsed_result.lavaplayer == "lavaplayer"
        assert parsed_result.source_managers == ["source_manager_1", "source_manager_2"]
        assert parsed_result.filters == ["filter_1", "filter_2"]
        assert parsed_result.plugins == [
            builder.deserialize_info_plugin(payloads.INFO_PLUGIN_PAYLOAD)
        ]

    def test_deserialize_info_version(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_info_version(payloads.INFO_VERSION_PAYLOAD)

        assert parsed_result.semver == "semver"
        assert parsed_result.major == 1
        assert parsed_result.minor == 2
        assert parsed_result.patch == 3
        assert parsed_result.pre_release == "pre_release"
        assert parsed_result.build == "build"

    def test_deserialize_info_git(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_info_git(payloads.INFO_GIT_PAYLOAD)

        assert parsed_result.branch == "branch"
        assert parsed_result.commit == "commit"
        assert parsed_result.commit_time == datetime.datetime.fromtimestamp(
            1 / 1000, datetime.timezone.utc
        )

    def test_deserialize_info_plugin(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_info_plugin(payloads.INFO_PLUGIN_PAYLOAD)

        assert parsed_result.name == "name"
        assert parsed_result.version == "version"


class TestPlayer:
    def test_deserialize_player(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_player(payloads.PLAYER_PAYLOAD)

        assert isinstance(parsed_result.guild_id, hikari.Snowflake)
        assert parsed_result.guild_id == hikari.Snowflake(1234567890)
        assert parsed_result.track == builder.deserialize_track(payloads.TRACK_PAYLOAD)
        assert parsed_result.volume == 1
        assert parsed_result.is_paused is True
        assert parsed_result.state == builder.deserialize_player_state(
            payloads.PLAYER_STATE_PAYLOAD
        )
        assert parsed_result.voice == builder.deserialize_player_voice(
            payloads.PLAYER_VOICE_PAYLOAD
        )
        assert parsed_result.filters is None

    def test_deserialize_player_state(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_player_state(payloads.PLAYER_STATE_PAYLOAD)

        assert parsed_result.time == datetime.datetime.fromtimestamp(
            1 / 1000, datetime.timezone.utc
        )
        assert parsed_result.position == 2
        assert parsed_result.connected is True
        assert parsed_result.ping == 3

    def test_deserialize_player_voice(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_player_voice(payloads.PLAYER_VOICE_PAYLOAD)

        assert parsed_result.token == "token"
        assert parsed_result.endpoint == "endpoint"
        assert parsed_result.session_id == "session_id"

    def test_serialize_player_voice(self, builder: EntityBuilder):
        parsed_result = builder.serialize_player_voice(
            Voice(token="token", endpoint="endpoint", session_id="session_id")
        )

        assert parsed_result == payloads.PLAYER_VOICE_PAYLOAD


class TestPlaylist:
    def test_deserialize_playlist(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_playlist(payloads.PLAYLIST_PAYLOAD)

        assert parsed_result.info == builder.deserialize_playlist_info(
            payloads.PLAYLIST_INFO_PAYLOAD
        )
        assert parsed_result.plugin_info == {}
        assert isinstance(parsed_result.tracks, typing.Sequence)
        assert len(parsed_result.tracks) == 1
        assert parsed_result.tracks[0] == builder.deserialize_track(
            payloads.TRACK_PAYLOAD
        )

    def test_deserialize_playlist_info(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_playlist_info(
            payloads.PLAYLIST_INFO_PAYLOAD
        )

        assert parsed_result.name == "name"
        assert parsed_result.selected_track == 1


class TestRoutePlanner:
    def test_deserialize_routeplanner_status(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_routeplanner_status(
            payloads.ROUTEPLANNER_STATUS_PAYLOAD
        )

        assert parsed_result.cls == RoutePlannerType.ROTATING_ROUTE_PLANNER
        assert parsed_result.details == builder.deserialize_routeplanner_details(
            payloads.ROUTEPLANNER_DETAILS_PAYLOAD
        )

    def test_deserialize_routeplanner_details(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_routeplanner_details(
            payloads.ROUTEPLANNER_DETAILS_PAYLOAD
        )

        assert parsed_result.ip_block == builder.deserialize_routeplanner_ipblock(
            payloads.ROUTEPLANNER_IP_BLOCK_PAYLOAD
        )
        assert isinstance(parsed_result.failing_addresses, typing.Sequence)
        assert len(parsed_result.failing_addresses) == 1
        assert parsed_result.failing_addresses[
            0
        ] == builder.deserialize_routeplanner_failing_address(
            payloads.ROUTEPLANNER_FAILING_ADDRESS_PAYLOAD
        )
        assert parsed_result.rotate_index == "rotate_index"
        assert parsed_result.ip_index == "ip_index"
        assert parsed_result.current_address == "current_address"
        assert parsed_result.current_address_index == "current_address_index"
        assert parsed_result.block_index == "block_index"

    def test_deserialize_ip_block(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_routeplanner_ipblock(
            payloads.ROUTEPLANNER_IP_BLOCK_PAYLOAD
        )

        assert parsed_result.type == IPBlockType.INET_4_ADDRESS
        assert parsed_result.size == "size"

    def test_deserialize_routeplanner_failing_address(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_routeplanner_failing_address(
            payloads.ROUTEPLANNER_FAILING_ADDRESS_PAYLOAD
        )

        assert parsed_result.address == "failing_address"
        assert parsed_result.timestamp == datetime.datetime.fromtimestamp(
            1 / 1000, datetime.timezone.utc
        )
        assert parsed_result.time == "failing_time"


class TestSession:
    def test_deserialize_session(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_session(payloads.SESSION_PAYLOAD)

        assert parsed_result.resuming is True
        assert parsed_result.timeout == 1


class TestStatistics:
    def test_deserialize_statistics(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_statistics(payloads.STATISTICS_PAYLOAD)

        assert parsed_result.players == 1
        assert parsed_result.playing_players == 2
        assert parsed_result.uptime == 3
        assert parsed_result.memory == builder.deserialize_statistics_memory(
            payloads.STATISTICS_MEMORY_PAYLOAD
        )
        assert parsed_result.cpu == builder.deserialize_statistics_cpu(
            payloads.STATISTICS_CPU_PAYLOAD
        )
        assert (
            parsed_result.frame_stats
            == builder.deserialize_statistics_frame_statistics(
                payloads.STATISTICS_FRAME_STATS_PAYLOAD
            )
        )

    def test_deserialize_statistics_memory(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_statistics_memory(
            payloads.STATISTICS_MEMORY_PAYLOAD
        )

        assert parsed_result.free == 1
        assert parsed_result.used == 2
        assert parsed_result.allocated == 3
        assert parsed_result.reservable == 4

    def test_deserialize_statistics_cpu(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_statistics_cpu(
            payloads.STATISTICS_CPU_PAYLOAD
        )

        assert parsed_result.cores == 1
        assert parsed_result.system_load == 2.3
        assert parsed_result.lavalink_load == 4.5

    def test_deserialize_statistics_frame_statistics(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_statistics_frame_statistics(
            payloads.STATISTICS_FRAME_STATS_PAYLOAD
        )

        assert parsed_result.sent == 1
        assert parsed_result.nulled == 2
        assert parsed_result.deficit == 3


class TestTrack:
    def test_deserialize_track(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_track(payloads.TRACK_PAYLOAD)

        assert parsed_result.encoded == "encoded"
        assert parsed_result.info == builder.deserialize_track_info(
            payloads.TRACK_INFO_PAYLOAD
        )
        assert parsed_result.plugin_info == {}
        assert parsed_result.user_data == {}
        assert parsed_result.requestor is None
    
    def test_deserialize_track_with_requestor(self, builder: EntityBuilder):
        payload = dict(payloads.TRACK_PAYLOAD)

        payload["userData"] = {"ongaku_requestor": "1234"}
        parsed_result = builder.deserialize_track(payload)

        assert parsed_result.encoded == "encoded"
        assert parsed_result.info == builder.deserialize_track_info(
            payloads.TRACK_INFO_PAYLOAD
        )
        assert parsed_result.plugin_info == {}
        assert parsed_result.user_data == {}
        assert parsed_result.requestor == hikari.Snowflake(1234)
    
    def test_deserialize_track_info(self, builder: EntityBuilder):
        parsed_result = builder.deserialize_track_info(payloads.TRACK_INFO_PAYLOAD)

        assert parsed_result.identifier == "identifier"
        assert parsed_result.is_seekable is False
        assert parsed_result.author == "author"
        assert parsed_result.length == 1
        assert parsed_result.is_stream is True
        assert parsed_result.position == 2
        assert parsed_result.title == "title"
        assert parsed_result.source_name == "source_name"
        assert parsed_result.uri == "uri"
        assert parsed_result.artwork_url == "artwork_url"
        assert parsed_result.isrc == "isrc"
