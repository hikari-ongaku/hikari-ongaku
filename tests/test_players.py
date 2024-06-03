# ruff: noqa: D100, D101, D102, D103

import datetime
import logging
import typing

import mock
import pytest
from hikari import Event
from hikari.events.voice_events import VoiceServerUpdateEvent
from hikari.events.voice_events import VoiceStateUpdateEvent
from hikari.impl import gateway_bot as gateway_bot_
from hikari.snowflakes import Snowflake

from ongaku import errors
from ongaku import events
from ongaku.abc.events import TrackEndReasonType
from ongaku.client import Client
from ongaku.impl import player
from ongaku.impl import player as player_
from ongaku.impl import playlist
from ongaku.impl.player import Voice
from ongaku.impl.track import Track
from ongaku.impl.track import TrackInfo
from ongaku.player import Player
from ongaku.session import Session


@pytest.fixture
def track(track_info: TrackInfo) -> Track:
    return Track("encoded", track_info, {}, {}, None)


async def connect_events(
    event_type: typing.Type[Event], /, timeout: typing.Union[float, int, None]
):
    if event_type == VoiceServerUpdateEvent:
        return VoiceServerUpdateEvent(
            app=mock.Mock(),
            shard=mock.Mock(),
            guild_id=Snowflake(1234567890),
            token="token",
            raw_endpoint="raw_endpoint",
        )

    if event_type == VoiceStateUpdateEvent:
        return VoiceStateUpdateEvent(
            shard=mock.Mock(),
            old_state=mock.Mock(),
            state=mock.Mock(
                session_id="session_id",
            ),
        )

    raise Exception("Invalid event requested.")


class TestPlayer:
    @pytest.mark.asyncio
    async def test_properties(
        self, gateway_bot: gateway_bot_.GatewayBot, ongaku_session: Session
    ):
        player = Player(ongaku_session, 1234567890)

        assert player.session == ongaku_session

        assert player.app == gateway_bot

        assert player.guild_id == Snowflake(1234567890)

        assert player.channel_id is None

        assert player.is_alive is False

        assert player.position == 0

        assert player.volume == -1

        assert player.is_paused is True

        assert player.autoplay is True

        assert player.connected is False

        assert isinstance(player.queue, typing.Sequence)
        assert player.queue == []

        assert player.voice is None

        assert player.state is None

        assert isinstance(player.filters, typing.Mapping)
        assert player.filters == {}

    @pytest.mark.asyncio
    async def test_connect(self, ongaku_session: Session, ongaku_player: Player):
        # Test Working

        voice = Voice("token", "raw_endpoint", "session_id")

        with (
            mock.patch.object(
                ongaku_session, "_get_session_id", return_value="session_id"
            ),
            mock.patch.object(
                ongaku_session.client.app,
                "update_voice_state",
                new_callable=mock.AsyncMock,
            ) as patched_voice_state,
            mock.patch.object(
                ongaku_player.app.event_manager, "wait_for", connect_events
            ),
            mock.patch.object(
                ongaku_session.client.rest,
                "update_player",
                new_callable=mock.AsyncMock,
                return_value=player_.Player(
                    Snowflake(1234567890), None, 1, False, mock.Mock(), voice, {}
                ),
            ) as patched_update,
        ):
            await ongaku_player.connect(987654321)

            patched_voice_state.assert_called_once_with(
                Snowflake(1234567890),
                Snowflake(987654321),
                self_mute=False,
                self_deaf=True,
            )

            patched_update.assert_called_once_with(
                ongaku_session._get_session_id(),
                Snowflake(1234567890),
                voice=voice,
                no_replace=False,
            )

            assert ongaku_player.voice is not None

            assert ongaku_player.voice.endpoint == voice.endpoint
            assert ongaku_player.voice.token == voice.token
            assert ongaku_player.voice.session_id == voice.session_id

            assert ongaku_player.is_alive is True

        # Events were received, but raw endpoint was empty.

        with (
            mock.patch.object(
                ongaku_session, "_get_session_id", return_value="session_id"
            ),
            mock.patch.object(
                ongaku_session.client.app,
                "update_voice_state",
                new_callable=mock.AsyncMock,
            ) as patched_voice_state,
            mock.patch.object(
                ongaku_player.app.event_manager,
                "wait_for",
                new_callable=mock.AsyncMock,
                return_value=mock.Mock(raw_endpoint=None),
            ),
            pytest.raises(errors.PlayerConnectError),
        ):
            await ongaku_player.connect(987654321)

    @pytest.mark.asyncio
    async def test_disconnect(self, ongaku_session: Session, ongaku_player: Player):
        with (
            mock.patch.object(
                ongaku_session, "_get_session_id", return_value="session_id"
            ),
            mock.patch.object(
                ongaku_session.client.app,
                "update_voice_state",
                new_callable=mock.AsyncMock,
            ) as patched_voice_state,
            mock.patch.object(
                ongaku_player.app.event_manager, "wait_for", connect_events
            ),
            mock.patch.object(
                ongaku_session.client.rest, "update_player"
            ) as patched_update,
            mock.patch.object(
                ongaku_session.client.rest, "delete_player"
            ) as patched_delete,
            mock.patch.object(ongaku_player, "clear") as patched_clear,
        ):
            await ongaku_player.connect(987654321)

            patched_voice_state.assert_called_once_with(
                Snowflake(1234567890),
                Snowflake(987654321),
                self_mute=False,
                self_deaf=True,
            )

            patched_update.assert_called_once_with(
                ongaku_session._get_session_id(),
                Snowflake(1234567890),
                voice=Voice("token", "raw_endpoint", "session_id"),
                no_replace=False,
            )

            await ongaku_player.disconnect()

            patched_clear.assert_called_once()

            patched_delete.assert_called_once_with(
                ongaku_session._get_session_id(), Snowflake(1234567890)
            )

            assert ongaku_player.is_alive is False

            patched_voice_state.assert_called_with(Snowflake(1234567890), None)

    @pytest.mark.asyncio
    async def test_play(
        self, ongaku_session: Session, track: Track, ongaku_player: Player
    ):
        # Test working

        with (
            mock.patch.object(
                ongaku_session, "_get_session_id", return_value="session_id"
            ),
            mock.patch.object(
                ongaku_player, "_channel_id", return_value=Snowflake(987654321)
            ),
            mock.patch.object(
                ongaku_session.client.rest,
                "update_player",
                return_value=player.Player(
                    Snowflake(1234567890),
                    track,
                    3,
                    False,
                    mock.Mock(),
                    mock.Mock(),
                    {},
                ),
            ) as patched_request,
        ):
            await ongaku_player.play(track, Snowflake(123454321))

            patched_request.assert_called_once_with(
                ongaku_session._get_session_id(),
                Snowflake(1234567890),
                track=track,
                no_replace=False,
            )

            assert ongaku_player.is_paused is False

            assert len(ongaku_player.queue) == 1

            assert ongaku_player.queue[0].requestor == Snowflake(123454321)

        # No session_id

        with pytest.raises(errors.SessionStartError):
            await ongaku_player.play(track, 123454321)

        # No channel.

        with (
            mock.patch.object(
                ongaku_session, "_get_session_id", return_value="session_id"
            ),
            pytest.raises(errors.PlayerConnectError),
        ):
            await ongaku_player.play(track, 123454321)

        # No track in queue.

        with (
            mock.patch.object(
                ongaku_session, "_get_session_id", return_value="session_id"
            ),
            mock.patch.object(
                ongaku_player, "_channel_id", return_value=Snowflake(987654321)
            ),
            pytest.raises(errors.PlayerQueueError),
        ):
            ongaku_player.remove(0)

            await ongaku_player.play()

    @pytest.mark.asyncio
    async def test_add(
        self,
        ongaku_session: Session,
        track_info: TrackInfo,
        track: Track,
        ongaku_player: Player,
    ):
        # Add singular track

        assert len(ongaku_player.queue) == 0

        ongaku_player.add(Track("encoded_1", track_info, {}, {}, None), Snowflake(1))

        assert len(ongaku_player.queue) == 1

        # Add two tracks.

        tracks: list[Track] = [
            Track("encoded_2", track_info, {}, {}, None),
            Track("encoded_3", track_info, {}, {}, None),
        ]

        ongaku_player.add(tracks, Snowflake(22))

        assert len(ongaku_player.queue) == 3

        # Add a playlist
        info = playlist.PlaylistInfo("beans", -1)
        playlist_tracks: list[Track] = [
            Track("encoded_4", track_info, {}, {}, None),
            Track("encoded_5", track_info, {}, {}, None),
        ]
        new_playlist = playlist.Playlist(info, playlist_tracks, {})

        ongaku_player.add(new_playlist, Snowflake(333))

        assert len(ongaku_player.queue) == 5

        # Check correct requestor got set, and make sure none is supported.

        ongaku_player.add(track)

        assert len(ongaku_player.queue) == 6
        logging.warning(ongaku_player.queue[0].requestor)
        assert ongaku_player.queue[0].requestor == Snowflake(1)
        assert ongaku_player.queue[1].requestor == Snowflake(22)
        assert ongaku_player.queue[2].requestor == Snowflake(22)
        assert ongaku_player.queue[3].requestor == Snowflake(333)
        assert ongaku_player.queue[4].requestor == Snowflake(333)
        assert ongaku_player.queue[5].requestor is None

    @pytest.mark.asyncio
    async def test_pause(
        self, ongaku_session: Session, track: Track, ongaku_player: Player
    ):
        with (
            mock.patch.object(
                ongaku_session, "_get_session_id", return_value="session_id"
            ),
            mock.patch.object(
                ongaku_player, "_channel_id", return_value=Snowflake(987654321)
            ),
            mock.patch.object(
                ongaku_session.client.rest,
                "update_player",
                return_value=player.Player(
                    Snowflake(1234567890),
                    track,
                    3,
                    False,
                    mock.Mock(),
                    mock.Mock(),
                    {},
                ),
            ) as patched_request,
        ):
            await ongaku_player.pause(True)

            patched_request.assert_called_once_with(
                ongaku_session._get_session_id(), Snowflake(1234567890), paused=True
            )

    @pytest.mark.asyncio
    async def test_stop(self, ongaku_session: Session, ongaku_player: Player):
        with (
            mock.patch.object(
                ongaku_session, "_get_session_id", return_value="session_id"
            ),
            mock.patch.object(
                ongaku_player, "_channel_id", return_value=Snowflake(987654321)
            ),
            mock.patch.object(
                ongaku_session.client.rest,
                "update_player",
                return_value=player.Player(
                    Snowflake(1234567890),
                    None,
                    3,
                    False,
                    mock.Mock(),
                    mock.Mock(),
                    {},
                ),
            ) as patched_request,
        ):
            await ongaku_player.stop()

            patched_request.assert_called_once_with(
                ongaku_session._get_session_id(),
                Snowflake(1234567890),
                track=None,
                no_replace=False,
            )

    @pytest.mark.asyncio
    async def test_shuffle(
        self, ongaku_session: Session, track: Track, ongaku_player: Player
    ):
        tracks: list[Track] = [  # So many tracks are placed here, to ensure
            mock.Mock(encoded="test_track_1"),
            mock.Mock(encoded="test_track_2"),
            mock.Mock(encoded="test_track_3"),
            mock.Mock(encoded="test_track_4"),
            mock.Mock(encoded="test_track_5"),
            mock.Mock(encoded="test_track_6"),
            mock.Mock(encoded="test_track_7"),
            mock.Mock(encoded="test_track_8"),
            mock.Mock(encoded="test_track_9"),
        ]

        ongaku_player.add(tracks)

        assert ongaku_player.queue == tracks

        ongaku_player.shuffle()

        assert ongaku_player.queue[0].encoded == tracks[0].encoded
        assert ongaku_player.queue != tracks

        # Queue has 1 track

        ongaku_player._queue = []

        ongaku_player.add(track)

        with pytest.raises(errors.PlayerQueueError):
            ongaku_player.shuffle()

        # Queue has 2 tracks

        ongaku_player._queue = []

        ongaku_player.add([mock.Mock(), mock.Mock()])

        with pytest.raises(errors.PlayerQueueError):
            ongaku_player.shuffle()

    @pytest.mark.asyncio
    async def test_skip(self, ongaku_session: Session, ongaku_player: Player):
        with (
            mock.patch.object(
                ongaku_session, "_get_session_id", return_value="session_id"
            ),
            mock.patch.object(
                ongaku_player, "_channel_id", return_value=Snowflake(987654321)
            ),
            mock.patch.object(
                ongaku_session.client.rest,
                "update_player",
                return_value=player.Player(
                    Snowflake(1234567890),
                    None,
                    3,
                    False,
                    mock.Mock(),
                    mock.Mock(),
                    {},
                ),
            ) as patched_request,
        ):
            tracks: list[Track] = [
                mock.Mock(encoded="test_track_1"),
                mock.Mock(encoded="test_track_2"),
            ]

            ongaku_player.add(tracks)

            # Skip to new song.

            await ongaku_player.skip()

            patched_request.assert_called_with(
                ongaku_session._get_session_id(),
                Snowflake(1234567890),
                track=tracks[1],
                no_replace=False,
            )

            assert len(ongaku_player.queue) == 1

            # Skip to no song.

            await ongaku_player.skip()

            patched_request.assert_called_with(
                ongaku_session._get_session_id(),
                Snowflake(1234567890),
                track=None,
                no_replace=False,
            )

            assert len(ongaku_player.queue) == 0

    @pytest.mark.asyncio
    async def test_remove(self, track: Track, ongaku_player: Player):
        tracks: list[Track] = [
            mock.Mock(encoded="test_encoded_1"),
            mock.Mock(encoded="test_encoded_2"),
            track,
            mock.Mock(encoded="test_encoded_3"),
        ]

        ongaku_player.add(tracks)

        assert len(ongaku_player.queue) == 4

        # Remove particular track

        ongaku_player.remove(track)

        assert len(ongaku_player.queue) == 3
        assert ongaku_player.queue == [tracks[0], tracks[1], tracks[3]]

        # Remove track based on position

        ongaku_player.remove(1)

        assert len(ongaku_player.queue) == 2
        assert ongaku_player.queue == [tracks[0], tracks[3]]

        # Test empty queue

        ongaku_player._queue = []

        with pytest.raises(errors.PlayerQueueError):
            ongaku_player.remove(0)

        tracks.pop(2)

        ongaku_player.add(tracks)

        with pytest.raises(errors.PlayerQueueError):
            ongaku_player.remove(300)

        with pytest.raises(errors.PlayerQueueError):
            ongaku_player.remove(track)

    @pytest.mark.asyncio
    async def test_clear(self, ongaku_session: Session, ongaku_player: Player):
        with (
            mock.patch.object(
                ongaku_session, "_get_session_id", return_value="session_id"
            ),
            mock.patch.object(
                ongaku_player, "_channel_id", return_value=Snowflake(987654321)
            ),
            mock.patch.object(
                ongaku_session.client.rest,
                "update_player",
                return_value=player.Player(
                    Snowflake(1234567890),
                    None,
                    3,
                    False,
                    mock.Mock(),
                    mock.Mock(),
                    {},
                ),
            ) as patched_request,
        ):
            tracks: list[Track] = [track, mock.Mock(encoded="test_track_2")]

            ongaku_player.add(tracks)

            assert len(ongaku_player.queue) == 2

            await ongaku_player.clear()

            patched_request.assert_called_once_with(
                ongaku_session._get_session_id(),
                Snowflake(1234567890),
                track=None,
                no_replace=False,
            )

            assert len(ongaku_player.queue) == 0

    @pytest.mark.asyncio
    async def test_set_autoplay(self, ongaku_player: Player):
        assert ongaku_player.autoplay is True

        ongaku_player.set_autoplay()

        assert ongaku_player.autoplay is False

        ongaku_player.set_autoplay(True)

        assert ongaku_player.autoplay is True

        ongaku_player.set_autoplay(False)

        assert ongaku_player.autoplay is False

    @pytest.mark.asyncio
    async def test_set_volume(self, ongaku_session: Session, ongaku_player: Player):
        with (
            mock.patch.object(
                ongaku_session, "_get_session_id", return_value="session_id"
            ),
            mock.patch.object(
                ongaku_session.client.rest,
                "update_player",
                return_value=player.Player(
                    Snowflake(1234567890),
                    None,
                    3,
                    False,
                    mock.Mock(),
                    mock.Mock(),
                    {},
                ),
            ) as patched_request,
        ):
            # set volume to a value

            await ongaku_player.set_volume(250)

            patched_request.assert_called_with(
                ongaku_session._get_session_id(),
                Snowflake(1234567890),
                volume=250,
                no_replace=False,
            )

            # Reset volume

            await ongaku_player.set_volume()

            patched_request.assert_called_with(
                ongaku_session._get_session_id(),
                Snowflake(1234567890),
                volume=100,
                no_replace=False,
            )

        # Give negative number

        with (
            mock.patch.object(
                ongaku_session, "_get_session_id", return_value="session_id"
            ),
            pytest.raises(ValueError),
        ):
            await ongaku_player.set_volume(-100)

        # Give a number greater than 1000

        with (
            mock.patch.object(
                ongaku_session, "_get_session_id", return_value="session_id"
            ),
            pytest.raises(ValueError),
        ):
            await ongaku_player.set_volume(9001)

    @pytest.mark.asyncio
    async def test_set_position(
        self, ongaku_session: Session, track: Track, ongaku_player: Player
    ):
        with (
            mock.patch.object(
                ongaku_session, "_get_session_id", return_value="session_id"
            ),
            mock.patch.object(
                ongaku_session.client.rest,
                "update_player",
                return_value=player.Player(
                    Snowflake(1234567890),
                    None,
                    3,
                    False,
                    mock.Mock(),
                    mock.Mock(),
                    {},
                ),
            ) as patched_request,
        ):
            ongaku_player.add(track)

            assert len(ongaku_player.queue) == 1

            await ongaku_player.set_position(10)

            patched_request.assert_called_once_with(
                ongaku_session._get_session_id(),
                Snowflake(1234567890),
                position=10,
                no_replace=False,
            )

        # Negative number provided

        with (
            mock.patch.object(
                ongaku_session, "_get_session_id", return_value="session_id"
            ),
            pytest.raises(ValueError),
        ):
            await ongaku_player.set_position(-10)

        # Queue is empty

        ongaku_player._queue = []

        with (
            mock.patch.object(
                ongaku_session, "_get_session_id", return_value="session_id"
            ),
            pytest.raises(errors.PlayerQueueError),
        ):
            await ongaku_player.set_position(10)

        # Queue is empty

        ongaku_player.add(track)

        with (
            mock.patch.object(
                ongaku_session, "_get_session_id", return_value="session_id"
            ),
            pytest.raises(ValueError),
        ):
            await ongaku_player.set_position(1000000000000000000000000)

    @pytest.mark.asyncio
    async def test_transfer(
        self,
        ongaku_client: Client,
        ongaku_session: Session,
        track: Track,
        ongaku_player: Player,
    ):
        new_session = Session(
            ongaku_client, "session", False, "127.0.0.1", 2333, "youshallnotpass", 3
        )

        # Test not connected

        tracks: list[Track] = [
            track,
            mock.Mock(encoded="encoded_1"),
            mock.Mock(encoded="encoded_2"),
            mock.Mock(encoded="encoded_3"),
        ]

        ongaku_player.add(tracks)

        ongaku_player = await ongaku_player.transfer(new_session)

        assert ongaku_player.queue == ongaku_player.queue

        # Test connected.

        with (
            mock.patch.object(
                ongaku_session, "_get_session_id", return_value="session_id"
            ),
            mock.patch.object(
                new_session, "_get_session_id", return_value="session_id"
            ),
            mock.patch.object(
                new_session.client.app,
                "update_voice_state",
                new_callable=mock.AsyncMock,
            ),
            mock.patch.object(
                new_session.app.event_manager, "wait_for", connect_events
            ),
            mock.patch.object(
                ongaku_session.client.rest, "update_player"
            ) as patched_update,
            mock.patch.object(
                ongaku_player,
                "_connected",
                new_callable=mock.PropertyMock(return_value=True),
            ),
            mock.patch.object(
                ongaku_player,
                "_is_paused",
                new_callable=mock.PropertyMock(return_value=False),
            ),
            mock.patch.object(
                ongaku_player,
                "_position",
                new_callable=mock.PropertyMock(return_value=30),
            ),
            mock.patch.object(
                ongaku_player, "_channel_id", return_value=Snowflake(987654321)
            ),
            mock.patch.object(ongaku_player, "disconnect") as patch_disconnect,
        ):
            ongaku_player = await ongaku_player.transfer(new_session)

            patch_disconnect.assert_called_once()

            # Check .connect() method of the new player was called.
            patched_update.assert_any_call(
                ongaku_session._get_session_id(),
                Snowflake(1234567890),
                voice=Voice("token", "raw_endpoint", "session_id"),
                no_replace=False,
            )

            # Check .play() method of the new player was called.
            patched_update.assert_any_call(
                ongaku_session._get_session_id(),
                Snowflake(1234567890),
                track=tracks[0],
                no_replace=False,
            )

            # Check .set_position() method of the new player was called.
            patched_update.assert_any_call(
                ongaku_session._get_session_id(),
                Snowflake(1234567890),
                position=30,
                no_replace=False,
            )

    @pytest.mark.asyncio
    async def test_update(self, ongaku_player: Player):
        assert ongaku_player.volume == -1
        assert ongaku_player.is_paused is True
        assert ongaku_player.state is None
        assert ongaku_player.voice is None
        assert ongaku_player.filters == {}

        state = player_.State(datetime.datetime.now(), 1, True, 2)
        voice = player_.Voice("token", "endpoint", "session_id")
        filters: typing.Mapping[str, typing.Any] = {"filter": {}}
        replacement_player = player_.Player(
            Snowflake(1234567890), None, 10, False, state, voice, filters
        )

        ongaku_player._update(replacement_player)

        assert ongaku_player.volume == 10
        assert ongaku_player.is_paused is False
        assert ongaku_player.state == state
        assert ongaku_player.voice == voice
        assert ongaku_player.filters == filters

    @pytest.mark.asyncio
    async def test_track_end_event(
        self, ongaku_session: Session, track: Track, ongaku_player: Player
    ):
        track_finished_event = (
            events.TrackEndEvent.from_session(  # This should play the new song.
                ongaku_session,
                Snowflake(1234567890),
                track=mock.Mock(encoded="encoded"),
                reason=TrackEndReasonType.FINISHED,
            )
        )

        track_load_failed_event = (
            events.TrackEndEvent.from_session(  # This should play the new song
                ongaku_session,
                Snowflake(1234567890),
                track=mock.Mock(encoded="encoded"),
                reason=TrackEndReasonType.LOADFAILED,
            )
        )

        track_stopped_event = (
            events.TrackEndEvent.from_session(  # This should not play the new song
                ongaku_session,
                Snowflake(1234567890),
                track=mock.Mock(encoded="encoded"),
                reason=TrackEndReasonType.STOPPED,
            )
        )

        track_wrong_guild_event = (
            events.TrackEndEvent.from_session(  # This should not play the new song.
                ongaku_session,
                Snowflake(987654321),
                track=mock.Mock(encoded="encoded"),
                reason=TrackEndReasonType.FINISHED,
            )
        )

        with (
            mock.patch.object(
                ongaku_session, "_get_session_id", return_value="session_id"
            ),
            mock.patch.object(
                ongaku_session.client.app.event_manager,
                "dispatch",
                new_callable=mock.AsyncMock,
            ) as patched_dispatch,
            mock.patch.object(
                ongaku_player, "play", new_callable=mock.AsyncMock
            ) as patched_play,
            mock.patch.object(
                ongaku_player.session.client.rest,
                "update_player",
                return_value=player_.Player(
                    Snowflake(1234567890),
                    None,
                    100,
                    False,
                    mock.Mock(),
                    mock.Mock(),
                    {},
                ),
            ),
        ):
            # Test autoplay

            ongaku_player.set_autoplay(False)

            await ongaku_player._track_end_event(track_finished_event)

            patched_dispatch.assert_not_called()

            ongaku_player.set_autoplay(True)

            # Test not allowed track end reason type.

            await ongaku_player._track_end_event(track_stopped_event)

            patched_dispatch.assert_not_called()

            # Test allowed track type, but wrong guild ID.

            await ongaku_player._track_end_event(track_wrong_guild_event)

            patched_dispatch.assert_not_called()

            # Test empty queue

            await ongaku_player._track_end_event(track_finished_event)

            patched_dispatch.assert_not_called()

            # Test one track (finished end reason)

            assert len(ongaku_player.queue) == 0

            ongaku_player.add(track)

            assert len(ongaku_player.queue) == 1
            assert ongaku_player.queue[0] == track

            await ongaku_player._track_end_event(track_finished_event)

            patched_dispatch.assert_called_with(
                events.QueueEmptyEvent.from_session(
                    ongaku_session, Snowflake(1234567890), track
                )
            )

            assert len(ongaku_player.queue) == 0

            await ongaku_player.clear()

            # Test two tracks (finished end reason)

            assert len(ongaku_player.queue) == 0

            tracks: list[Track] = [
                mock.Mock(encoded="encoded_1"),
                mock.Mock(encoded="encoded_2"),
            ]

            ongaku_player.add(tracks)

            assert len(ongaku_player.queue) == 2

            await ongaku_player._track_end_event(track_finished_event)

            patched_dispatch.assert_called_with(
                events.QueueEmptyEvent.from_session(
                    ongaku_session, Snowflake(1234567890), tracks[0]
                )
            )

            patched_play.assert_called_with()

            assert len(ongaku_player.queue) == 1

            assert ongaku_player.queue[0].encoded == "encoded_2"

            await ongaku_player.clear()

            # Test one track (load failed end reason)

            assert len(ongaku_player.queue) == 0

            ongaku_player.add(track)

            assert len(ongaku_player.queue) == 1
            assert ongaku_player.queue[0] == track

            await ongaku_player._track_end_event(track_load_failed_event)

            patched_dispatch.assert_called_with(
                events.QueueEmptyEvent.from_session(
                    ongaku_session, Snowflake(1234567890), track
                )
            )

            assert len(ongaku_player.queue) == 0

            await ongaku_player.clear()

            # Test two tracks (load failed end reason)

            assert len(ongaku_player.queue) == 0

            tracks: list[Track] = [
                mock.Mock(encoded="encoded_1"),
                mock.Mock(encoded="encoded_2"),
            ]

            ongaku_player.add(tracks)

            assert len(ongaku_player.queue) == 2

            await ongaku_player._track_end_event(track_load_failed_event)

            patched_dispatch.assert_called_with(
                events.QueueEmptyEvent.from_session(
                    ongaku_session, Snowflake(1234567890), tracks[0]
                )
            )

            patched_play.assert_called_with()

            assert len(ongaku_player.queue) == 1

            assert ongaku_player.queue[0].encoded == "encoded_2"

    @pytest.mark.asyncio
    async def test_player_update_event(
        self, ongaku_session: Session, ongaku_player: Player
    ):
        assert ongaku_player.state is None

        state = player_.State(datetime.datetime.now(), 1, True, 2)
        event = events.PlayerUpdateEvent.from_session(
            ongaku_session, Snowflake(1234567890), state
        )

        await ongaku_player._player_update_event(event)

        assert ongaku_player.state == state
