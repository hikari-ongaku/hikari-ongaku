import pytest

from ongaku.abc.filters import BandType
from ongaku.impl.filters import ChannelMix
from ongaku.impl.filters import Distortion
from ongaku.impl.filters import Equalizer
from ongaku.impl.filters import Filters
from ongaku.impl.filters import Karaoke
from ongaku.impl.filters import LowPass
from ongaku.impl.filters import Rotation
from ongaku.impl.filters import Timescale
from ongaku.impl.filters import Tremolo
from ongaku.impl.filters import Vibrato


def test_filters():
    equalizer = [Equalizer(band=BandType.HZ100, gain=0.95)]
    karaoke = Karaoke(level=1, mono_level=0.5, filter_band=4.5, filter_width=6)
    timescale = Timescale(speed=1.2, pitch=2.3, rate=4)
    tremolo = Tremolo(frequency=1.2, depth=1)
    vibrato = Vibrato(frequency=3, depth=0.5)
    rotation = Rotation(rotation_hz=6)
    distortion = Distortion(
        sin_offset=2.1,
        sin_scale=3,
        cos_offset=6.9,
        cos_scale=7.2,
        tan_offset=9.4,
        tan_scale=2,
        offset=4.1,
        scale=8,
    )
    channel_mix = ChannelMix(
        left_to_left=0, left_to_right=1, right_to_left=0.5, right_to_right=0.63
    )
    low_pass = LowPass(smoothing=3.8)
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


class TestFilterFunctions:
    def test_from_filter(self, ongaku_filters: Filters):
        filters = Filters.from_filter(ongaku_filters)

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

    def test_set_volume(self):
        filters = Filters()

        filters.set_volume(10)

        assert filters.volume == 10

        with pytest.raises(ValueError):
            filters.set_volume(-0.1)

    def test_add_equalizer(self):
        filters = Filters()

        filters.add_equalizer(BandType.HZ100, 0.3)

        assert len(filters.equalizer) == 1
        assert filters.equalizer[0].band == BandType.HZ100
        assert filters.equalizer[0].gain == 0.3

    def test_remove_equalizer(self):
        filters = Filters()

        filters.add_equalizer(BandType.HZ100, 0.3)

        assert len(filters.equalizer) == 1

        filters.remove_equalizer(BandType.HZ100)

        assert len(filters.equalizer) == 0

        with pytest.raises(IndexError):
            filters.remove_equalizer(BandType.HZ100)

    def test_clear_equalizer(self):
        filters = Filters()

        filters.add_equalizer(BandType.HZ100, 0.3)

        filters.add_equalizer(BandType.HZ630, 0.5)

        assert len(filters.equalizer) == 2

        filters.clear_equalizer()

        assert len(filters.equalizer) == 0

    def test_set_karaoke(self):
        filters = Filters()

        filters.set_karaoke(level=0.1, mono_level=1.0, filter_band=0.5, filter_width=2)

        assert filters.karaoke is not None

        assert filters.karaoke.level == 0.1
        assert filters.karaoke.mono_level == 1.0
        assert filters.karaoke.filter_band == 0.5
        assert filters.karaoke.filter_width == 2

    def test_clear_karaoke(self):
        filters = Filters()

        filters.set_karaoke(level=0.1, mono_level=1.0, filter_band=0.5, filter_width=2)

        assert filters.karaoke is not None

        filters.clear_karaoke()

        assert filters.karaoke is None

    def test_set_timescale(self):
        filters = Filters()

        filters.set_timescale(speed=1, pitch=0.5, rate=0.66)

        assert filters.timescale is not None

        assert filters.timescale.speed == 1
        assert filters.timescale.pitch == 0.5
        assert filters.timescale.rate == 0.66

    def test_clear_timescale(self):
        filters = Filters()

        filters.set_timescale(speed=1, pitch=0.5, rate=0.66)

        assert filters.timescale is not None

        filters.clear_timescale()

        assert filters.timescale is None

    def test_set_tremolo(self):
        filters = Filters()

        filters.set_tremolo(frequency=8, depth=1)

        assert filters.tremolo is not None

        assert filters.tremolo.frequency == 8
        assert filters.tremolo.depth == 1

    def test_clear_tremolo(self):
        filters = Filters()

        filters.set_tremolo(frequency=8, depth=1)

        assert filters.tremolo is not None

        filters.clear_tremolo()

        assert filters.tremolo is None

    def test_set_vibrato(self):
        filters = Filters()

        filters.set_vibrato(frequency=8, depth=1)

        assert filters.vibrato is not None

        assert filters.vibrato.frequency == 8
        assert filters.vibrato.depth == 1

    def test_clear_vibrato(self):
        filters = Filters()

        filters.set_vibrato(frequency=8, depth=1)

        assert filters.vibrato is not None

        filters.clear_vibrato()

        assert filters.vibrato is None

    def test_set_rotation(self):
        filters = Filters()

        filters.set_rotation(rotation_hz=8)

        assert filters.rotation is not None

        assert filters.rotation.rotation_hz == 8

    def test_clear_rotation(self):
        filters = Filters()

        filters.set_rotation(rotation_hz=8)

        assert filters.rotation is not None

        filters.clear_rotation()

        assert filters.rotation is None

    def test_set_distortion(self):
        filters = Filters()

        filters.set_distortion(
            sin_offset=0.3,
            sin_scale=1,
            cos_offset=4,
            cos_scale=-3,
            tan_offset=4,
            tan_scale=9,
            offset=6.66,
            scale=-1.5,
        )

        assert filters.distortion is not None

        assert filters.distortion.sin_offset == 0.3
        assert filters.distortion.sin_scale == 1
        assert filters.distortion.cos_offset == 4
        assert filters.distortion.cos_scale == -3
        assert filters.distortion.tan_offset == 4
        assert filters.distortion.tan_scale == 9
        assert filters.distortion.offset == 6.66
        assert filters.distortion.scale == -1.5

    def test_clear_distortion(self):
        filters = Filters()

        filters.set_distortion(
            sin_offset=0.3,
            sin_scale=1,
            cos_offset=4,
            cos_scale=-3,
            tan_offset=4,
            tan_scale=9,
            offset=6.66,
            scale=-1.5,
        )

        assert filters.distortion is not None

        filters.clear_distortion()

        assert filters.distortion is None

    def test_set_channel_mix(self):
        filters = Filters()

        filters.set_channel_mix(
            left_to_left=0.39, left_to_right=1, right_to_left=0, right_to_right=0.8
        )

        assert filters.channel_mix is not None

        assert filters.channel_mix.left_to_left == 0.39
        assert filters.channel_mix.left_to_right == 1
        assert filters.channel_mix.right_to_left == 0
        assert filters.channel_mix.right_to_right == 0.8

    def test_clear_channel_mix(self):
        filters = Filters()

        filters.set_channel_mix(
            left_to_left=0.39, left_to_right=1, right_to_left=0, right_to_right=0.8
        )

        assert filters.channel_mix is not None

        filters.clear_channel_mix()

        assert filters.channel_mix is None

    def test_set_low_pass(self):
        filters = Filters()

        filters.set_low_pass(smoothing=8)

        assert filters.low_pass is not None

        assert filters.low_pass.smoothing == 8

    def test_clear_low_pass(self):
        filters = Filters()

        filters.set_low_pass(smoothing=8)

        assert filters.low_pass is not None

        filters.clear_low_pass()

        assert filters.low_pass is None

    def test_set_plugin_filters(self):
        filters = Filters()

        payload = {"beanos": "beanos"}

        filters.set_plugin_filters(payload)

        assert filters.plugin_filters == payload


class TestEqualizer:
    def test_valid_values(self):
        equalizer = Equalizer(band=BandType.HZ100, gain=0.95)

        assert equalizer.band == BandType.HZ100
        assert equalizer.gain == 0.95

    def test_invalid_positive_gain_value(self):
        with pytest.raises(ValueError):
            Equalizer(band=BandType.HZ100, gain=1.1)

    def test_invalid_negative_gain_value(self):
        with pytest.raises(ValueError):
            Equalizer(band=BandType.HZ100, gain=-0.26)


class TestKaraoke:
    def test_valid_values(self):
        karaoke = Karaoke(level=1, mono_level=0.5, filter_band=4.5, filter_width=6)

        assert karaoke.level == 1
        assert karaoke.mono_level == 0.5
        assert karaoke.filter_band == 4.5
        assert karaoke.filter_width == 6

    def test_invalid_negative_level_value(self):
        with pytest.raises(ValueError):
            Karaoke(level=-0.1, mono_level=0.5, filter_band=4.5, filter_width=6)

    def test_invalid_positive_level_value(self):
        with pytest.raises(ValueError):
            Karaoke(level=1.1, mono_level=0.5, filter_band=4.5, filter_width=6)

    def test_invalid_negative_mono_level_value(self):
        with pytest.raises(ValueError):
            Karaoke(level=1, mono_level=-0.1, filter_band=4.5, filter_width=6)

    def test_invalid_positive_mono_level_value(self):
        with pytest.raises(ValueError):
            Karaoke(level=1, mono_level=1.1, filter_band=4.5, filter_width=6)


class TestTimescale:
    def test_valid_values(self):
        timescale = Timescale(speed=1.2, pitch=2.3, rate=4)

        assert timescale.speed == 1.2
        assert timescale.pitch == 2.3
        assert timescale.rate == 4

    def test_invalid_negative_speed_value(self):
        with pytest.raises(ValueError):
            Timescale(speed=-0.1, pitch=2.3, rate=4)

    def test_invalid_negative_pitch_value(self):
        with pytest.raises(ValueError):
            Timescale(speed=1.2, pitch=-0.1, rate=4)

    def test_invalid_negative_rate_value(self):
        with pytest.raises(ValueError):
            Timescale(speed=1.2, pitch=2.3, rate=-0.1)


class TestTremolo:
    def test_valid_values(self):
        tremolo = Tremolo(frequency=1.2, depth=1)

        assert tremolo.frequency == 1.2
        assert tremolo.depth == 1

    def test_invalid_negative_frequency_value(self):
        with pytest.raises(ValueError):
            Tremolo(frequency=-0.1, depth=1)

    def test_invalid_negative_depth_value(self):
        with pytest.raises(ValueError):
            Tremolo(frequency=1.2, depth=-0.1)

    def test_invalid_positive_depth_value(self):
        with pytest.raises(ValueError):
            Tremolo(frequency=1.2, depth=1.1)


class TestVibrato:
    def test_valid_values(self):
        vibrato = Vibrato(frequency=3, depth=0.5)

        assert vibrato.frequency == 3
        assert vibrato.depth == 0.5

    def test_invalid_negative_frequency_value(self):
        with pytest.raises(ValueError):
            Vibrato(frequency=-0.1, depth=0.5)

    def test_invalid_positive_frequency_value(self):
        with pytest.raises(ValueError):
            Vibrato(frequency=14.1, depth=0.5)

    def test_invalid_negative_depth_value(self):
        with pytest.raises(ValueError):
            Vibrato(frequency=3, depth=-0.1)

    def test_invalid_positive_depth_value(self):
        with pytest.raises(ValueError):
            Vibrato(frequency=3, depth=1.1)


def test_rotation():
    rotation = Rotation(rotation_hz=6)

    assert rotation.rotation_hz == 6


def test_distortion():
    distortion = Distortion(
        sin_offset=2.1,
        sin_scale=3,
        cos_offset=6.9,
        cos_scale=7.2,
        tan_offset=9.4,
        tan_scale=2,
        offset=4.1,
        scale=8,
    )

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
        channel_mix = ChannelMix(
            left_to_left=0, left_to_right=1, right_to_left=0.5, right_to_right=0.63
        )

        assert channel_mix.left_to_left == 0
        assert channel_mix.left_to_right == 1
        assert channel_mix.right_to_left == 0.5
        assert channel_mix.right_to_right == 0.63

    def test_invalid_negative_left_to_left_value(self):
        with pytest.raises(ValueError):
            ChannelMix(
                left_to_left=-0.1,
                left_to_right=1,
                right_to_left=0.5,
                right_to_right=0.63,
            )

    def test_invalid_positive_left_to_left_value(self):
        with pytest.raises(ValueError):
            ChannelMix(
                left_to_left=1.1,
                left_to_right=1,
                right_to_left=0.5,
                right_to_right=0.63,
            )

    def test_invalid_negative_left_to_right_value(self):
        with pytest.raises(ValueError):
            ChannelMix(
                left_to_left=0,
                left_to_right=-0.1,
                right_to_left=0.5,
                right_to_right=0.63,
            )

    def test_invalid_positive_left_to_right_value(self):
        with pytest.raises(ValueError):
            ChannelMix(
                left_to_left=0,
                left_to_right=1.1,
                right_to_left=0.5,
                right_to_right=0.63,
            )

    def test_invalid_negative_right_to_left_value(self):
        with pytest.raises(ValueError):
            ChannelMix(
                left_to_left=0, left_to_right=1, right_to_left=-0.1, right_to_right=0.63
            )

    def test_invalid_positive_right_to_left_value(self):
        with pytest.raises(ValueError):
            ChannelMix(
                left_to_left=0, left_to_right=1, right_to_left=1.1, right_to_right=0.63
            )

    def test_invalid_negative_right_to_right_value(self):
        with pytest.raises(ValueError):
            ChannelMix(
                left_to_left=0, left_to_right=1, right_to_left=0.5, right_to_right=-0.1
            )

    def test_invalid_positive_right_to_right_value(self):
        with pytest.raises(ValueError):
            ChannelMix(
                left_to_left=0, left_to_right=1, right_to_left=0.5, right_to_right=1.1
            )


class TestLowPass:
    def test_valid_values(self):
        low_pass = LowPass(smoothing=3.8)

        assert low_pass.smoothing == 3.8

    def test_invalid_negative_smoothing_value(self):
        with pytest.raises(ValueError):
            LowPass(smoothing=0.9)
