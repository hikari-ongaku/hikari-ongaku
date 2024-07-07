from __future__ import annotations

import enum
import typing

# FIXME: Docs need to be done for everything.


class Filters:
    """Filters.

    The base class for controlling filters.
    """

    __slots__: typing.Sequence[str] = (
        "_volume",
        "_equalizer",
        "_karaoke",
        "_timescale",
        "_tremolo",
        "_vibrato",
        "_rotation",
        "_distortion",
        "_channel_mix",
        "_low_pass",
        "_plugin_filters",
    )

    @property
    def volume(self) -> float | None:
        return self._volume

    @property
    def equalizer(self) -> typing.Sequence[Equalizer]:
        return self._equalizer

    @property
    def karaoke(self) -> Karaoke | None:
        return self._karaoke

    @property
    def timescale(self) -> Timescale | None:
        return self._timescale

    @property
    def tremolo(self) -> Tremolo | None:
        return self._tremolo

    @property
    def vibrato(self) -> Vibrato | None:
        return self._vibrato

    @property
    def rotation(self) -> Rotation | None:
        return self._rotation

    @property
    def distortion(self) -> Distortion | None:
        return self._distortion

    @property
    def channel_mix(self) -> ChannelMix | None:
        return self._channel_mix

    @property
    def low_pass(self) -> LowPass | None:
        return self._low_pass

    @property
    def plugin_filters(self) -> typing.Mapping[str, typing.Any]:
        return self._plugin_filters

    def __eq__(self, other: object) -> bool: # noqa: C901
        if not isinstance(other, Filters):
            return False

        if self.volume != other.volume:
            return False

        if self.equalizer != other.equalizer:
            return False

        if self.karaoke != other.karaoke:
            return False

        if self.timescale != other.timescale:
            return False

        if self.tremolo != other.tremolo:
            return False

        if self.vibrato != other.vibrato:
            return False

        if self.rotation != other.rotation:
            return False

        if self.distortion != other.distortion:
            return False

        if self.channel_mix != other.channel_mix:
            return False

        if self.low_pass != other.low_pass:
            return False

        if self.plugin_filters != other.plugin_filters:
            return False

        return True


class Equalizer:
    __slots__: typing.Sequence[str] = ("_band", "_gain")

    @property
    def band(self) -> BandType:
        return self._band

    @property
    def gain(self) -> float:
        return self._gain

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Equalizer):
            return False

        if self.band != other.band:
            return False

        if self.gain != other.gain:
            return False

        return True


class Karaoke:
    __slots__: typing.Sequence[str] = (
        "_level",
        "_mono_level",
        "_filter_band",
        "_filter_width",
    )

    @property
    def level(self) -> float | None:
        return self._level

    @property
    def mono_level(self) -> float | None:
        return self._mono_level

    @property
    def filter_band(self) -> float | None:
        return self._filter_band

    @property
    def filter_width(self) -> float | None:
        return self._filter_width

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Karaoke):
            return False

        if self.level != other.level:
            return False

        if self.mono_level != other.mono_level:
            return False

        if self.filter_band != other.filter_band:
            return False

        if self.filter_width != other.filter_width:
            return False

        return True


class Timescale:
    __slots__: typing.Sequence[str] = ("_speed", "_pitch", "_rate")

    @property
    def speed(self) -> float | None:
        return self._speed

    @property
    def pitch(self) -> float | None:
        return self._pitch

    @property
    def rate(self) -> float | None:
        return self._rate

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Timescale):
            return False

        if self.speed != other.speed:
            return False

        if self.pitch != other.pitch:
            return False

        if self.rate != other.rate:
            return False

        return True


class Tremolo:
    __slots__: typing.Sequence[str] = (
        "_frequency",
        "_depth",
    )

    @property
    def frequency(self) -> float | None:
        return self._frequency

    @property
    def depth(self) -> float | None:
        return self._depth

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tremolo):
            return False

        if self.frequency != other.frequency:
            return False

        if self.depth != other.depth:
            return False

        return True


class Vibrato:
    __slots__: typing.Sequence[str] = (
        "_frequency",
        "_depth",
    )

    @property
    def frequency(self) -> float | None:
        return self._frequency

    @property
    def depth(self) -> float | None:
        return self._depth

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vibrato):
            return False

        if self.frequency != other.frequency:
            return False

        if self.depth != other.depth:
            return False

        return True


class Rotation:
    __slots__: typing.Sequence[str] = "_rotation_hz"

    @property
    def rotation_hz(self) -> float | None:
        return self._rotation_hz

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Rotation):
            return False

        if self.rotation_hz != other.rotation_hz:
            return False

        return True


class Distortion:
    __slots__: typing.Sequence[str] = (
        "_sin_offset",
        "_sin_scale",
        "_cos_offset",
        "_cos_scale",
        "_tan_offset",
        "_tan_scale",
        "_offset",
        "_scale",
    )

    @property
    def sin_offset(self) -> float | None:
        return self._sin_offset

    @property
    def sin_scale(self) -> float | None:
        return self._sin_scale

    @property
    def cos_offset(self) -> float | None:
        return self._cos_offset

    @property
    def cos_scale(self) -> float | None:
        return self._cos_scale

    @property
    def tan_offset(self) -> float | None:
        return self._tan_offset

    @property
    def tan_scale(self) -> float | None:
        return self._tan_scale

    @property
    def offset(self) -> float | None:
        return self._offset

    @property
    def scale(self) -> float | None:
        return self._scale

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Distortion):
            return False

        if self.sin_offset != other.sin_offset:
            return False

        if self.sin_scale != other.sin_scale:
            return False

        if self.cos_offset != other.cos_offset:
            return False

        if self.cos_scale != other.cos_scale:
            return False

        if self.tan_offset != other.tan_offset:
            return False

        if self.tan_scale != other.tan_scale:
            return False

        if self.offset != other.offset:
            return False

        if self.scale != other.scale:
            return False

        return True


class ChannelMix:
    __slots__: typing.Sequence[str] = (
        "_left_to_left",
        "_left_to_right",
        "_right_to_left",
        "_right_to_right",
    )

    @property
    def left_to_left(self) -> float | None:
        return self._left_to_left

    @property
    def left_to_right(self) -> float | None:
        return self._left_to_right

    @property
    def right_to_left(self) -> float | None:
        return self._right_to_left

    @property
    def right_to_right(self) -> float | None:
        return self._right_to_right

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ChannelMix):
            return False

        if self.left_to_left != other.left_to_left:
            return False

        if self.left_to_right != other.left_to_right:
            return False

        if self.right_to_left != other.right_to_left:
            return False

        if self.right_to_right != other.right_to_right:
            return False

        return True


class LowPass:
    __slots__: typing.Sequence[str] = ("_smoothing",)

    @property
    def smoothing(self) -> float | None:
        return self._smoothing

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LowPass):
            return False

        if self.smoothing != other.smoothing:
            return False

        return True


class BandType(enum.IntEnum):
    HZ25 = 0
    """25 Hz"""
    HZ40 = 1
    """40 Hz"""
    HZ63 = 2
    """63 Hz"""
    HZ100 = 3
    """100 Hz"""
    HZ160 = 4
    """160 Hz"""
    HZ250 = 5
    """250 Hz"""
    HZ400 = 6
    """400 Hz"""
    HZ630 = 7
    """630 Hz"""
    HZ1000 = 8
    """1000 Hz"""
    HZ1600 = 9
    """1600 Hz"""
    HZ2500 = 10
    """2500 Hz"""
    HZ4000 = 11
    """4000 Hz"""
    HZ6300 = 12
    """6300 Hz"""
    HZ10000 = 13
    """10000 Hz"""
    HZ16000 = 14
    """16000 Hz"""


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
