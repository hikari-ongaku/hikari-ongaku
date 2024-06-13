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
    equalizer = [Equalizer(BandType.HZ100, 0.95), Equalizer(BandType.HZ63, -0.1)]
    karaoke = Karaoke(1, 0.5, 4.5, 6)
    timescale = Timescale(1.2, 2.3, 4)
    tremolo = Tremolo(1.2, 4)
    vibrato = Vibrato(3, 6.8)
    rotation = Rotation(6)
    distortion = Distortion(2.1, 3, 6.9, 7.2, 9.4, 2, 4.1, 8)
    channel_mix = ChannelMix(1.2, 3, 6, 4.1)
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
        low_pass=low_pass
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

def test_filters_from_filter():
    raise Exception

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
        karaoke = Karaoke(1.0, 0.65, 4.5, 6)

        assert karaoke.level == 1
        assert karaoke.mono_level == 0.65
        assert karaoke.filter_band == 4.5
        assert karaoke.filter_width == 6

def test_timescale():
    timescale = Timescale(1.2, 2.3, 4)

    assert timescale.speed == 1.2
    assert timescale.pitch == 2.3
    assert timescale.rate == 4

def test_tremolo():
    tremolo = Tremolo(1.2, 4)

    assert tremolo.frequency == 1.2
    assert tremolo.depth == 4

def test_vibrato():
    vibrato = Vibrato(3, 6.8)

    assert vibrato.frequency == 3
    assert vibrato.depth == 6.8

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

def test_channel_mix():
    channel_mix = ChannelMix(1.2, 3, 6, 4.1)

    assert channel_mix.left_to_left == 1.2
    assert channel_mix.left_to_right == 3
    assert channel_mix.right_to_left == 6
    assert channel_mix.right_to_right == 4.1

def test_low_pass():
    low_pass = LowPass(3.8)

    assert low_pass.smoothing == 3.8