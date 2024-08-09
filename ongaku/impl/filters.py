from __future__ import annotations

import typing

import hikari

from ongaku.abc import filters as filters_


class Filters(filters_.Filters):
    """Filters.

    An empty filter object.

    Parameters
    ----------
    volume
        Volume of the player.
    equalizer
        A sequence of equalizer objects.
    karaoke
        A karaoke object.
    timescale
        A timescale object.
    tremolo
        A tremolo object.
    vibrato
        A vibrato object.
    rotation
        A rotation object.
    distortion
        A distortion object.
    channel_mix
        A channel mix object.
    low_pass
        A low pass object.
    plugin_filters
        A dict of plugin filters.

    """

    def __init__(
        self,
        *,
        volume: float | None = None,
        equalizer: typing.Sequence[filters_.Equalizer] = [],
        karaoke: filters_.Karaoke | None = None,
        timescale: filters_.Timescale | None = None,
        tremolo: filters_.Tremolo | None = None,
        vibrato: filters_.Vibrato | None = None,
        rotation: filters_.Rotation | None = None,
        distortion: filters_.Distortion | None = None,
        channel_mix: filters_.ChannelMix | None = None,
        low_pass: filters_.LowPass | None = None,
        plugin_filters: typing.Mapping[str, typing.Any] = {},
    ) -> None:
        self._volume = volume
        self._equalizer: typing.MutableSequence[filters_.Equalizer] = list(equalizer)
        self._karaoke = karaoke
        self._timescale = timescale
        self._tremolo = tremolo
        self._vibrato = vibrato
        self._rotation = rotation
        self._distortion = distortion
        self._channel_mix = channel_mix
        self._low_pass = low_pass
        self._plugin_filters = plugin_filters

    @classmethod
    def from_filter(cls, filters: filters_.Filters) -> Filters:
        """From Filter.

        Convert a immutable filter, into a mutable filter.

        !!! note
            The purpose of this is so that you can modify a players filter object, without directly modifying it.

        Parameters
        ----------
        filters
            The filter to pull data from.
        """
        return cls(
            volume=filters.volume,
            equalizer=filters.equalizer,
            karaoke=filters.karaoke,
            timescale=filters.timescale,
            tremolo=filters.tremolo,
            vibrato=filters.vibrato,
            rotation=filters.rotation,
            distortion=filters.distortion,
            channel_mix=filters.channel_mix,
            low_pass=filters.low_pass,
        )

    def set_volume(self, volume: float) -> Filters:
        """Set Volume.

        Set the volume of the filter.

        Parameters
        ----------
        volume
            The volume of the player. (Must be greater than 0.)
        """
        if volume <= 0:
            raise ValueError("Volume must be at or above 0.")
        self._volume = volume

        return self

    # Equalizer

    def add_equalizer(
        self,
        band: filters_.BandType,
        gain: float,
    ) -> Filters:
        """Add Equalizer.

        Add a new equalizer band, with appropriate gain.

        Parameters
        ----------
        band
            The [BandType][ongaku.abc.filters.BandType].
        gain
            The gain of the band. (-0.25 to 1.0)
        """
        self._equalizer.append(Equalizer(band, gain))

        return self

    def remove_equalizer(self, band: filters_.BandType) -> Filters:
        """Remove Equalizer.

        Remove a equalizer via its band.

        Parameters
        ----------
        band
            The [BandType][ongaku.abc.filters.BandType].
        """
        for equalizer in self.equalizer:
            if equalizer.band == band:
                self._equalizer.remove(equalizer)
                return self

        raise IndexError("No values found.")

    def clear_equalizer(self) -> Filters:
        """Clear Equalizer.

        Clear all equalizer bands from the filter.
        """
        self._equalizer.clear()

        return self

    # Karaoke

    def set_karaoke(
        self,
        *,
        level: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        mono_level: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        filter_band: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        filter_width: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
    ) -> Filters:
        """Set Karaoke.

        Set karaoke values.

        Parameters
        ----------
        level
            The level (0 to 1.0 where 0.0 is no effect and 1.0 is full effect).
        mono_level
            The mono level (0 to 1.0 where 0.0 is no effect and 1.0 is full effect).
        filter_band
            The filter band (in Hz).
        filter_width
            The filter width.
        """
        if self._karaoke is None:
            self._karaoke = Karaoke(None, None, None, None)

        self._karaoke = Karaoke(
            self._karaoke.level if level == hikari.UNDEFINED else level,
            self._karaoke.mono_level if mono_level == hikari.UNDEFINED else mono_level,
            self._karaoke.filter_band
            if filter_band == hikari.UNDEFINED
            else filter_band,
            self._karaoke.filter_width
            if filter_width == hikari.UNDEFINED
            else filter_width,
        )

        return self

    def clear_karaoke(self) -> Filters:
        """Clear Karaoke.

        Clear all karaoke values from the filter.
        """
        self._karaoke = None
        return self

    # Timescale

    def set_timescale(
        self,
        *,
        speed: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        pitch: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        rate: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
    ) -> Filters:
        """Set Timescale.

        Set timescale values.

        Parameters
        ----------
        speed
            The playback speed 0.0 ≤ x.
        pitch
            The pitch 0.0 ≤ x.
        rate
            The rate 0.0 ≤ x.
        """
        if self._timescale is None:
            self._timescale = Timescale(None, None, None)

        self._timescale = Timescale(
            self._timescale.speed if speed == hikari.UNDEFINED else speed,
            self._timescale.pitch if pitch == hikari.UNDEFINED else pitch,
            self._timescale.rate if rate == hikari.UNDEFINED else rate,
        )

        return self

    def clear_timescale(self) -> Filters:
        """Clear Timescale.

        Clear all timescale values from the filter.
        """
        self._timescale = None
        return self

    # Tremolo

    def set_tremolo(
        self,
        *,
        frequency: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        depth: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
    ) -> Filters:
        """Set Tremolo.

        Set tremolo values.

        Parameters
        ----------
        frequency
            The frequency 0.0 < x.
        depth
            The tremolo depth 0.0 < x ≤ 1.0.
        """
        if self._tremolo is None:
            self._tremolo = Tremolo(None, None)

        self._tremolo = Tremolo(
            self._tremolo.frequency if frequency == hikari.UNDEFINED else frequency,
            self._tremolo.depth if depth == hikari.UNDEFINED else depth,
        )

        return self

    def clear_tremolo(self) -> Filters:
        """Clear Tremolo.

        Clear all tremolo values from the filter.
        """
        self._tremolo = None
        return self

    # Vibrato

    def set_vibrato(
        self,
        *,
        frequency: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        depth: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
    ) -> Filters:
        """Set Vibrato.

        Set vibrato values.

        Parameters
        ----------
        frequency
            The frequency 0.0 < x ≤ 14.0.
        depth
            The vibrato depth 0.0 < x ≤ 1.0.

        """
        if self._vibrato is None:
            self._vibrato = Vibrato(None, None)

        self._vibrato = Vibrato(
            self._vibrato.frequency if frequency == hikari.UNDEFINED else frequency,
            self._vibrato.depth if depth == hikari.UNDEFINED else depth,
        )

        return self

    def clear_vibrato(self) -> Filters:
        """Clear Vibrato.

        Clear all vibrato values from the filter.
        """
        self._vibrato = None
        return self

    # Rotation

    def set_rotation(
        self,
        *,
        rotation_hz: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
    ) -> Filters:
        """Set Rotation.

        Set rotation values.

        Parameters
        ----------
        rotation_hz
            The frequency of the audio rotating around the listener in Hz.
        """
        if self._rotation is None:
            self._rotation = Rotation(None)

        self._rotation = Rotation(
            self._rotation.rotation_hz
            if rotation_hz == hikari.UNDEFINED
            else rotation_hz,
        )

        return self

    def clear_rotation(self) -> Filters:
        """Clear Rotation.

        Clear all rotation values from the filter.
        """
        self._rotation = None
        return self

    # Distortion

    def set_distortion(
        self,
        *,
        sin_offset: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        sin_scale: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        cos_offset: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        cos_scale: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        tan_offset: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        tan_scale: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        offset: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        scale: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
    ) -> Filters:
        """Set Distortion.

        Set distortion values.

        Parameters
        ----------
        sin_offset
            The sin offset.
        sin_scale
            The sin scale.
        cos_offset
            The cos offset.
        cos_scale
            The cos scale.
        tan_offset
            The tan offset.
        tan_scale
            The tan scale.
        offset
            The offset.
        scale
            The scale.
        """
        if self._distortion is None:
            self._distortion = Distortion(
                None, None, None, None, None, None, None, None
            )

        self._distortion = Distortion(
            self._distortion.sin_offset
            if sin_offset == hikari.UNDEFINED
            else sin_offset,
            self._distortion.sin_scale if sin_scale == hikari.UNDEFINED else sin_scale,
            self._distortion.cos_offset
            if cos_offset == hikari.UNDEFINED
            else cos_offset,
            self._distortion.cos_scale if cos_scale == hikari.UNDEFINED else cos_scale,
            self._distortion.tan_offset
            if tan_offset == hikari.UNDEFINED
            else tan_offset,
            self._distortion.tan_scale if tan_scale == hikari.UNDEFINED else tan_scale,
            self._distortion.offset if offset == hikari.UNDEFINED else offset,
            self._distortion.scale if scale == hikari.UNDEFINED else scale,
        )

        return self

    def clear_distortion(self) -> Filters:
        """Clear Distortion.

        Clear all distortion values from the filter.
        """
        self._distortion = None
        return self

    # Channel Mix

    def set_channel_mix(
        self,
        *,
        left_to_left: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        left_to_right: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        right_to_left: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        right_to_right: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
    ) -> Filters:
        """Set Channel Mix.

        Set tremolo values.

        Parameters
        ----------
        left_to_left
            The left to left channel mix factor (0.0 ≤ x ≤ 1.0).
        left_to_right
            The left to right channel mix factor (0.0 ≤ x ≤ 1.0).
        right_to_left
            The right to left channel mix factor (0.0 ≤ x ≤ 1.0).
        right_to_right
            The right to right channel mix factor (0.0 ≤ x ≤ 1.0).

        """
        if self._channel_mix is None:
            self._channel_mix = ChannelMix(None, None, None, None)

        self._channel_mix = ChannelMix(
            self._channel_mix.left_to_left
            if left_to_left == hikari.UNDEFINED
            else left_to_left,
            self._channel_mix.left_to_right
            if left_to_right == hikari.UNDEFINED
            else left_to_right,
            self._channel_mix.right_to_left
            if right_to_left == hikari.UNDEFINED
            else right_to_left,
            self._channel_mix.right_to_right
            if right_to_right == hikari.UNDEFINED
            else right_to_right,
        )

        return self

    def clear_channel_mix(self) -> Filters:
        """Clear Channel Mix.

        Clear all channel mix values from the filter.
        """
        self._channel_mix = None
        return self

    # Low Pass

    def set_low_pass(
        self,
        *,
        smoothing: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
    ) -> Filters:
        """Set Low Pass.

        Set low pass values.

        Parameters
        ----------
        smoothing
            The smoothing factor (1.0 < x).
        """
        if self._low_pass is None:
            self._low_pass = LowPass(None)

        self._low_pass = LowPass(
            self._low_pass.smoothing if smoothing == hikari.UNDEFINED else smoothing,
        )

        return self

    def clear_low_pass(self) -> Filters:
        """Clear Low Pass.

        Clear all low pass values from the filter.
        """
        self._low_pass = None
        return self

    # Plugin filters

    def set_plugin_filters(
        self, plugin_filters: typing.Mapping[str, typing.Any] = {}
    ) -> Filters:
        """Set Plugin Filters.

        Set the filters for plugins.

        Parameters
        ----------
        plugin_filters
            The plugin filters you wish to set.
        """
        self._plugin_filters = plugin_filters
        return self


class Equalizer(filters_.Equalizer):
    def __init__(
        self,
        band: filters_.BandType,
        gain: float,
    ) -> None:
        if gain > 1:
            raise ValueError("Gain must be at or below 1.")
        if gain < -0.25:
            raise ValueError("Gain must be at or above -0.25.")

        self._band = band
        self._gain = gain


class Karaoke(filters_.Karaoke):
    def __init__(
        self,
        level: float | None,
        mono_level: float | None,
        filter_band: float | None,
        filter_width: float | None,
    ) -> None:
        if level is not None:
            if level > 1:
                raise ValueError("Level must be at or below 1.")
            if level < 0:
                raise ValueError("Level must be at or above 0.")

        if mono_level is not None:
            if mono_level > 1:
                raise ValueError("MonoLevel must be at or below 1.")
            if mono_level < 0:
                raise ValueError("MonoLevel must be at or above 0.")

        self._level = level
        self._mono_level = mono_level
        self._filter_band = filter_band
        self._filter_width = filter_width


class Timescale(filters_.Timescale):
    def __init__(
        self, speed: float | None, pitch: float | None, rate: float | None
    ) -> None:
        if speed is not None and speed < 0:
            raise ValueError("Speed must be at or above 0.")
        if pitch is not None and pitch < 0:
            raise ValueError("Pitch must be at or above 0.")
        if rate is not None and rate < 0:
            raise ValueError("Rate must be at or above 0.")

        self._speed = speed
        self._pitch = pitch
        self._rate = rate


class Tremolo(filters_.Tremolo):
    def __init__(self, frequency: float | None, depth: float | None) -> None:
        if frequency is not None and frequency < 0:
            raise ValueError("Frequency must be at or above 0.")

        if depth is not None:
            if depth > 1:
                raise ValueError("Depth must be at or below 1.")
            if depth < 0:
                raise ValueError("Depth must be at or above 0.")

        self._frequency = frequency
        self._depth = depth


class Vibrato(filters_.Vibrato):
    def __init__(self, frequency: float | None, depth: float | None) -> None:
        if frequency is not None:
            if frequency > 14:
                raise ValueError("Frequency must be at or below 1.")
            if frequency < 0:
                raise ValueError("Frequency must be at or above 0.")

        if depth is not None:
            if depth > 1:
                raise ValueError("Depth must be at or below 1.")
            if depth < 0:
                raise ValueError("Depth must be at or above 0.")

        self._frequency = frequency
        self._depth = depth


class Rotation(filters_.Rotation):
    def __init__(self, rotation_hz: float | None) -> None:
        self._rotation_hz = rotation_hz


class Distortion(filters_.Distortion):
    def __init__(
        self,
        sin_offset: float | None,
        sin_scale: float | None,
        cos_offset: float | None,
        cos_scale: float | None,
        tan_offset: float | None,
        tan_scale: float | None,
        offset: float | None,
        scale: float | None,
    ) -> None:
        self._sin_offset = sin_offset
        self._sin_scale = sin_scale
        self._cos_offset = cos_offset
        self._cos_scale = cos_scale
        self._tan_offset = tan_offset
        self._tan_scale = tan_scale
        self._offset = offset
        self._scale = scale


class ChannelMix(filters_.ChannelMix):
    def __init__(  # noqa: C901
        self,
        left_to_left: float | None,
        left_to_right: float | None,
        right_to_left: float | None,
        right_to_right: float | None,
    ) -> None:
        if left_to_left is not None:
            if left_to_left > 1:
                raise ValueError("Left to Left must be at or below 1.")
            if left_to_left < 0:
                raise ValueError("Left to Left must be at or above 0.")

        if left_to_right is not None:
            if left_to_right > 1:
                raise ValueError("Left to Right must be at or below 1.")
            if left_to_right < 0:
                raise ValueError("Left to Right must be at or above 0.")

        if right_to_left is not None:
            if right_to_left > 1:
                raise ValueError("Right to Left must be at or below 1.")
            if right_to_left < 0:
                raise ValueError("Right to Left must be at or above 0.")

        if right_to_right is not None:
            if right_to_right > 1:
                raise ValueError("Right to Left must be at or below 1.")
            if right_to_right < 0:
                raise ValueError("Right to Left must be at or above 0.")

        self._left_to_left = left_to_left
        self._left_to_right = left_to_right
        self._right_to_left = right_to_left
        self._right_to_right = right_to_right


class LowPass(filters_.LowPass):
    def __init__(
        self,
        smoothing: float | None,
    ) -> None:
        if smoothing is not None and smoothing < 1:
            raise ValueError("Frequency must be at or above 1.")

        self._smoothing = smoothing


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
