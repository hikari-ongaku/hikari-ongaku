# ruff: noqa: D100, D101, D102

import unittest

from ongaku.abc.track import Track
from ongaku.abc.track import TrackInfo
from tests import payload


class TestTrack(unittest.TestCase):
    def test_base(self):
        track_info = TrackInfo._from_payload(payload.convert(payload.TRACK_INFO))
        track = Track(
            encoded="test_encoded",
            info=track_info,
            plugin_info={},
            user_data={},
        )

        assert track.encoded == "test_encoded"
        assert track.info == track_info
        assert track.plugin_info == {}
        assert track.user_data == {}
        assert track.requestor is None

    def test_from_payload(self):
        track_info = TrackInfo._from_payload(payload.convert(payload.TRACK_INFO))
        track = Track._from_payload(payload.convert(payload.TRACK))

        assert track.encoded == "test_encoded"
        assert track.info == track_info
        assert track.plugin_info == {}
        assert track.user_data == {}
        assert track.requestor is None

    def test_to_payload(self):
        track = Track._from_payload(payload.convert(payload.TRACK))

        assert track._to_payload == payload.TRACK


class TestTrackInfo(unittest.TestCase):
    def test_base(self):
        track_info = TrackInfo(
            identifier="test_identifier",
            is_seekable=False,
            author="test_author",
            length=1234567890,
            is_stream=False,
            position=1234567890,
            title="test_title",
            source_name="test_source_name",
            uri="https://www.youtube.com/watch?=test",
            artwork_url="https://i.ytimg.com/test.jpg",
            isrc=None,
        )

        assert track_info.identifier == "test_identifier"
        assert track_info.is_seekable is False
        assert track_info.author == "test_author"
        assert track_info.length == 1234567890
        assert track_info.is_stream == False
        assert track_info.position == 1234567890
        assert track_info.title == "test_title"
        assert track_info.source_name == "test_source_name"
        assert track_info.uri == "https://www.youtube.com/watch?=test"
        assert track_info.artwork_url == "https://i.ytimg.com/test.jpg"
        assert track_info.isrc is None

    def test_from_payload(self):
        track_info = TrackInfo._from_payload(payload.convert(payload.TRACK_INFO))

        assert track_info.identifier == "test_identifier"
        assert track_info.is_seekable is False
        assert track_info.author == "test_author"
        assert track_info.length == 1
        assert track_info.is_stream == False
        assert track_info.position == 2
        assert track_info.title == "test_title"
        assert track_info.source_name == "test_source_name"
        assert track_info.uri == "https://www.youtube.com/watch?=test"
        assert track_info.artwork_url == "https://i.ytimg.com/test.jpg"
        assert track_info.isrc is None

    def test_to_payload(self):
        track_info = TrackInfo._from_payload(payload.convert(payload.TRACK_INFO))

        assert track_info._to_payload == payload.TRACK_INFO
