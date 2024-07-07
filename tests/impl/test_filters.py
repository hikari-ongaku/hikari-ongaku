import pytest

from ongaku.abc.filters import BandType
from ongaku.impl.filters import ChannelMix
from ongaku.impl.filters import Distortion
from ongaku.impl.filters import Equalizer
from ongaku.impl.filters import Filters
from ongaku.impl.filters import Filters as Filters_
from ongaku.impl.filters import Karaoke
from ongaku.impl.filters import LowPass
from ongaku.impl.filters import Rotation
from ongaku.impl.filters import Timescale
from ongaku.impl.filters import Tremolo
from ongaku.impl.filters import Vibrato


def test_filters():
    equalizer = [Equalizer(BandType.HZ100, 0.95), Equalizer(BandType.HZ63, -0.1)]
    karaoke = Karaoke(1, 0.5, 4.5, 6)
    timescale = Timescale(1.2, 2.3, 4)
    tremolo = Tremolo(1.2, 1)
    vibrato = Vibrato(3, 0.5)
    rotation = Rotation(6)
    distortion = Distortion(2.1, 3, 6.9, 7.2, 9.4, 2, 4.1, 8)
    channel_mix = ChannelMix(0, 1, 0.5, 0.63)
    low_pass = LowPass(3.8)
    filters = Filters(
        volume=1.2,
        equalizer=equalizer,
        karaoke=karaoke,
        timescale=timescale,
        tremolo=tremolo,
        vibrato=vibrato,
        rotation=rotation,
        distortion=distortion,
        channel_mix=channel_mix,
        low_pass=low_pass,
    )

    assert filters.volume == 1.2
    assert filters.equalizer == equalizer
    assert filters.karaoke == karaoke
    assert filters.timescale == timescale
    assert filters.tremolo == tremolo
    assert filters.vibrato == vibrato
    assert filters.rotation == rotation
    assert filters.distortion == distortion
    assert filters.channel_mix == channel_mix
    assert filters.low_pass == low_pass
    assert filters.plugin_filters == {}


def test_filters_from_filter(ongaku_filters: Filters):
    filters = Filters_.from_filter(ongaku_filters)

    assert filters.volume == 1.2
    assert filters.equalizer == ongaku_filters.equalizer
    assert filters.karaoke == ongaku_filters.karaoke
    assert filters.timescale == ongaku_filters.timescale
    assert filters.tremolo == ongaku_filters.tremolo
    assert filters.vibrato == ongaku_filters.vibrato
    assert filters.rotation == ongaku_filters.rotation
    assert filters.distortion == ongaku_filters.distortion
    assert filters.channel_mix == ongaku_filters.channel_mix
    assert filters.low_pass == ongaku_filters.low_pass
    assert filters.plugin_filters == {}


class TestEqualizer:
    def test_valid_values(self):
        equalizer = Equalizer(BandType.HZ100, 0.5)

        assert equalizer.band == BandType.HZ100
        assert equalizer.gain == 0.5

    def test_invalid_positive_gain_value(self):
        with pytest.raises(ValueError):
            Equalizer(BandType.HZ100, 1.1)

    def test_invalid_negative_gain_value(self):
        with pytest.raises(ValueError):
            Equalizer(BandType.HZ100, -0.26)


class TestKaraoke:
    def test_valid_values(self):
        karaoke = Karaoke(1, 0.65, 4.5, 6)

        assert karaoke.level == 1
        assert karaoke.mono_level == 0.65
        assert karaoke.filter_band == 4.5
        assert karaoke.filter_width == 6

    def test_invalid_negative_level_value(self):
        with pytest.raises(ValueError):
            Karaoke(-0.1, 0.65, 4.5, 6)

    def test_invalid_positive_level_value(self):
        with pytest.raises(ValueError):
            Karaoke(1.1, 0.65, 4.5, 6)

    def test_invalid_negative_mono_level_value(self):
        with pytest.raises(ValueError):
            Karaoke(1, -0.1, 4.5, 6)

    def test_invalid_positive_mono_level_value(self):
        with pytest.raises(ValueError):
            Karaoke(1, 1.1, 4.5, 6)


class TestTimescale:
    def test_valid_values(self):
        timescale = Timescale(1.2, 2.3, 4)

        assert timescale.speed == 1.2
        assert timescale.pitch == 2.3
        assert timescale.rate == 4

    def test_invalid_negative_speed_value(self):
        with pytest.raises(ValueError):
            Timescale(-0.1, 2.3, 4)

    def test_invalid_negative_pitch_value(self):
        with pytest.raises(ValueError):
            Timescale(1.2, -0.1, 4)

    def test_invalid_negative_rate_value(self):
        with pytest.raises(ValueError):
            Timescale(1.2, 2.3, -0.1)


class TestTremolo:
    def test_valid_values(self):
        tremolo = Tremolo(1.2, 1)

        assert tremolo.frequency == 1.2
        assert tremolo.depth == 1

    def test_invalid_negative_frequency_value(self):
        with pytest.raises(ValueError):
            Vibrato(-0.1, 1)

    def test_invalid_negative_depth_value(self):
        with pytest.raises(ValueError):
            Tremolo(1.2, -0.1)

    def test_invalid_positive_depth_value(self):
        with pytest.raises(ValueError):
            Tremolo(1.2, 1.1)


class TestVibrato:
    def test_valid_values(self):
        vibrato = Vibrato(3, 0.5)

        assert vibrato.frequency == 3
        assert vibrato.depth == 0.5

    def test_invalid_negative_frequency_value(self):
        with pytest.raises(ValueError):
            Vibrato(-0.1, 0.5)

    def test_invalid_positive_frequency_value(self):
        with pytest.raises(ValueError):
            Vibrato(14.1, 1.1)

    def test_invalid_negative_depth_value(self):
        with pytest.raises(ValueError):
            Vibrato(3, -0.1)

    def test_invalid_positive_depth_value(self):
        with pytest.raises(ValueError):
            Vibrato(3, 1.1)


def test_rotation():
    rotation = Rotation(6)

    assert rotation.rotation_hz == 6


def test_distortion():
    distortion = Distortion(2.1, 3, 6.9, 7.2, 9.4, 2, 4.1, 8)

    assert distortion.sin_offset == 2.1
    assert distortion.sin_scale == 3
    assert distortion.cos_offset == 6.9
    assert distortion.cos_scale == 7.2
    assert distortion.tan_offset == 9.4
    assert distortion.tan_scale == 2
    assert distortion.offset == 4.1
    assert distortion.scale == 8


class TestChannelMix:
    def test_valid_values(self):
        channel_mix = ChannelMix(0, 1, 0.5, 0.63)

        assert channel_mix.left_to_left == 0
        assert channel_mix.left_to_right == 1
        assert channel_mix.right_to_left == 0.5
        assert channel_mix.right_to_right == 0.63

    def test_invalid_negative_left_to_left_value(self):
        with pytest.raises(ValueError):
            ChannelMix(-0.1, 1, 0.5, 0.63)

    def test_invalid_positive_left_to_left_value(self):
        with pytest.raises(ValueError):
            ChannelMix(1.1, 1, 0.5, 0.63)

    def test_invalid_negative_left_to_right_value(self):
        with pytest.raises(ValueError):
            ChannelMix(0, -0.1, 0.5, 0.63)

    def test_invalid_positive_left_to_right_value(self):
        with pytest.raises(ValueError):
            ChannelMix(0, 1.1, 0.5, 0.63)

    def test_invalid_negative_right_to_left_value(self):
        with pytest.raises(ValueError):
            ChannelMix(0, 1, -0.1, 0.63)

    def test_invalid_positive_right_to_left_value(self):
        with pytest.raises(ValueError):
            ChannelMix(0, 1, 1.1, 0.63)

    def test_invalid_negative_right_to_right_value(self):
        with pytest.raises(ValueError):
            ChannelMix(0, 1, 0.5, -0.1)

    def test_invalid_positive_right_to_right_value(self):
        with pytest.raises(ValueError):
            ChannelMix(0, 1, 0.5, 1.1)


class TestLowPass:
    def test_valid_values(self):
        low_pass = LowPass(3.8)

        assert low_pass.smoothing == 3.8

    def test_invalid_negative_smoothing_value(self):
        with pytest.raises(ValueError):
            LowPass(0.9)
