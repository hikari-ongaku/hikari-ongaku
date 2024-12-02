from __future__ import annotations

import enum
import typing


class Filters:
    """Filters.

    The base class for filter.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#filters)
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
        """Volume.

        The volume of the player.
        """
        return self._volume

    @property
    def equalizer(self) -> typing.Sequence[Equalizer]:
        """Equalizer.

        15 bands with different gains.
        """
        return self._equalizer

    @property
    def karaoke(self) -> Karaoke | None:
        """Karaoke.

        Eliminates part of a band, usually targeting vocals.
        """
        return self._karaoke

    @property
    def timescale(self) -> Timescale | None:
        """Timescale.

        The speed, pitch, and rate.
        """
        return self._timescale

    @property
    def tremolo(self) -> Tremolo | None:
        """Tremolo.

        Creates a shuddering effect, where the volume quickly oscillates.
        """
        return self._tremolo

    @property
    def vibrato(self) -> Vibrato | None:
        """Vibrato.

        Creates a shuddering effect, where the pitch quickly oscillates.
        """
        return self._vibrato

    @property
    def rotation(self) -> Rotation | None:
        """Rotation.

        Rotates the audio around the stereo channels/user headphones (aka Audio Panning).
        """
        return self._rotation

    @property
    def distortion(self) -> Distortion | None:
        """Distortion.

        Distorts the audio.
        """
        return self._distortion

    @property
    def channel_mix(self) -> ChannelMix | None:
        """Channel Mix.

        Mixes both channels (left and right).
        """
        return self._channel_mix

    @property
    def low_pass(self) -> LowPass | None:
        """Low Pass.

        Filters higher frequencies.
        """
        return self._low_pass

    @property
    def plugin_filters(self) -> typing.Mapping[str, typing.Any]:
        """Plugin Filters.

        Filter plugin configurations.
        """
        return self._plugin_filters

    def __eq__(self, other: object) -> bool:  # noqa: C901
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

        return self.plugin_filters == other.plugin_filters


class Equalizer:
    """Equalizer.

    There are 15 bands (0-14) that can be changed.
    "gain" is the multiplier for the given band.
    The default value is 0. Valid values range from -0.25 to 1.0,
    where -0.25 means the given band is completely muted, and 0.25 means it is doubled.
    Modifying the gain could also change the volume of the output.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#equalizer)
    """

    __slots__: typing.Sequence[str] = ("_band", "_gain")

    @property
    def band(self) -> BandType:
        """The band (0 to 14)."""
        return self._band

    @property
    def gain(self) -> float:
        """The gain (-0.25 to 1.0)."""
        return self._gain

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Equalizer):
            return False

        if self.band != other.band:
            return False

        return self.gain == other.gain


class Karaoke:
    """Karaoke.

    Uses equalization to eliminate part of a band, usually targeting vocals.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#karaoke)
    """

    __slots__: typing.Sequence[str] = (
        "_level",
        "_mono_level",
        "_filter_band",
        "_filter_width",
    )

    @property
    def level(self) -> float | None:
        """The level (0 to 1.0 where 0.0 is no effect and 1.0 is full effect)."""
        return self._level

    @property
    def mono_level(self) -> float | None:
        """The mono level (0 to 1.0 where 0.0 is no effect and 1.0 is full effect)."""
        return self._mono_level

    @property
    def filter_band(self) -> float | None:
        """The filter band (in Hz)."""
        return self._filter_band

    @property
    def filter_width(self) -> float | None:
        """The filter width."""
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

        return self.filter_width == other.filter_width


class Timescale:
    """Timescale.

    Changes the speed, pitch, and rate. All default to 1.0.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#timescale)
    """

    __slots__: typing.Sequence[str] = ("_speed", "_pitch", "_rate")

    @property
    def speed(self) -> float | None:
        """The playback speed 0.0 ≤ x."""
        return self._speed

    @property
    def pitch(self) -> float | None:
        """The pitch 0.0 ≤ x."""
        return self._pitch

    @property
    def rate(self) -> float | None:
        """The rate 0.0 ≤ x."""
        return self._rate

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Timescale):
            return False

        if self.speed != other.speed:
            return False

        if self.pitch != other.pitch:
            return False

        return self.rate == other.rate


class Tremolo:
    """Tremolo.

    Uses amplification to create a shuddering effect, where the volume quickly oscillates.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#tremolo)
    """

    __slots__: typing.Sequence[str] = (
        "_frequency",
        "_depth",
    )

    @property
    def frequency(self) -> float | None:
        """The frequency 0.0 < x."""
        return self._frequency

    @property
    def depth(self) -> float | None:
        """The tremolo depth 0.0 < x ≤ 1.0."""
        return self._depth

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Tremolo):
            return False

        if self.frequency != other.frequency:
            return False

        return self.depth == other.depth


class Vibrato:
    """Vibrato.

    Similar to tremolo. While tremolo oscillates the volume, vibrato oscillates the pitch.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#vibrato)
    """

    __slots__: typing.Sequence[str] = (
        "_frequency",
        "_depth",
    )

    @property
    def frequency(self) -> float | None:
        """The frequency 0.0 < x ≤ 14.0."""
        return self._frequency

    @property
    def depth(self) -> float | None:
        """The vibrato depth 0.0 < x ≤ 1.0."""
        return self._depth

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vibrato):
            return False

        if self.frequency != other.frequency:
            return False

        return self.depth == other.depth


class Rotation:
    """Rotation.

    Rotates the sound around the stereo channels/user headphones (aka Audio Panning).

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#rotation)
    """

    __slots__: typing.Sequence[str] = "_rotation_hz"

    @property
    def rotation_hz(self) -> float | None:
        """The frequency of the audio rotating around the listener in Hz."""
        return self._rotation_hz

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Rotation):
            return False

        return self.rotation_hz == other.rotation_hz


class Distortion:
    """Distortion.

    Distortion effect. It can generate some pretty unique audio effects.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#distortion)
    """

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
        """The sin offset."""
        return self._sin_offset

    @property
    def sin_scale(self) -> float | None:
        """The sin scale."""
        return self._sin_scale

    @property
    def cos_offset(self) -> float | None:
        """The cos offset."""
        return self._cos_offset

    @property
    def cos_scale(self) -> float | None:
        """The cos scale."""
        return self._cos_scale

    @property
    def tan_offset(self) -> float | None:
        """The tan offset."""
        return self._tan_offset

    @property
    def tan_scale(self) -> float | None:
        """The tan scale."""
        return self._tan_scale

    @property
    def offset(self) -> float | None:
        """The offset."""
        return self._offset

    @property
    def scale(self) -> float | None:
        """The scale."""
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

        return self.scale == other.scale


class ChannelMix:
    """Channel Mix.

    Mixes both channels (left and right), with a configurable factor on how much each channel affects the other.
    With the defaults, both channels are kept independent of each other. Setting all factors to 0.5 means both channels get the same audio.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#channel-mix)
    """

    __slots__: typing.Sequence[str] = (
        "_left_to_left",
        "_left_to_right",
        "_right_to_left",
        "_right_to_right",
    )

    @property
    def left_to_left(self) -> float | None:
        """The left to left channel mix factor (0.0 ≤ x ≤ 1.0)."""
        return self._left_to_left

    @property
    def left_to_right(self) -> float | None:
        """The left to right channel mix factor (0.0 ≤ x ≤ 1.0)."""
        return self._left_to_right

    @property
    def right_to_left(self) -> float | None:
        """The right to left channel mix factor (0.0 ≤ x ≤ 1.0)."""
        return self._right_to_left

    @property
    def right_to_right(self) -> float | None:
        """The right to right channel mix factor (0.0 ≤ x ≤ 1.0)."""
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

        return self.right_to_right == other.right_to_right


class LowPass:
    """Low Pass.

    Higher frequencies get suppressed, while lower frequencies pass through this filter, thus the name low pass.
    Any smoothing values equal to or less than 1.0 will disable the filter.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#low-pass)
    """

    __slots__: typing.Sequence[str] = ("_smoothing",)

    @property
    def smoothing(self) -> float | None:
        """The smoothing factor (1.0 < x)."""
        return self._smoothing

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LowPass):
            return False

        return self.smoothing == other.smoothing


class BandType(enum.IntEnum):
    """Band Type.

    All the available band types.
    """

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
