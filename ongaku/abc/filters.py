"""
Filter ABC's.

The filter abstract classes.
"""

from __future__ import annotations

import typing

import pydantic

from ongaku.abc.bases import PayloadBase
from ongaku.enums import BandType

__all__ = (
    "Filters",
    "FilterEqualizer",
    "FilterKaraoke",
    "FilterTimescale",
    "FilterTremolo",
    "FilterVibrato",
    "FilterRotation",
    "FilterDistortion",
    "FilterChannelMix",
    "FilterLowPass",
)


class Filters(PayloadBase):
    """
    The base filters.

    View the current filter.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#equalizer)

    !!! note
        They will only actually update, if you parse this to the player.
    """

    @classmethod
    def create(cls) -> EditableFilters:
        """
        Create a filters objectyping.

        Create an empty filters object to pass to the botyping.
        """
        return EditableFilters(
            volume=1.0,
            equalizer=[],
            karaoke=None,
            timescale=None,
            tremolo=None,
            vibrato=None,
            rotation=None,
            distortion=None,
            channel_mix=None,
            low_pass=None,
            plugin_filters={},
        )

    volume: typing.Annotated[float, pydantic.Field(default=0, ge=0.0, le=5.0)]
    """Adjusts the player volume from 0.0 to 5.0, where 1.0 is 100%. Values >1.0 may cause clipping."""
    equalizer: typing.Annotated[
        typing.MutableSequence[FilterEqualizer], pydantic.Field(default=[])
    ]
    """Adjusts 15 different bands."""
    karaoke: typing.Annotated[FilterKaraoke | None, pydantic.Field(default=None)]
    """Eliminates part of a band, usually targeting vocals."""
    timescale: typing.Annotated[FilterTimescale | None, pydantic.Field(default=None)]
    """Changes the speed, pitch, and rate."""
    tremolo: typing.Annotated[FilterTremolo | None, pydantic.Field(default=None)]
    """Creates a shuddering effect, where the volume quickly oscillates."""
    vibrato: typing.Annotated[FilterVibrato | None, pydantic.Field(default=None)]
    """Creates a shuddering effect, where the pitch quickly oscillates."""
    rotation: typing.Annotated[FilterRotation | None, pydantic.Field(default=None)]
    """Rotates the audio around the stereo channels/user headphones (aka Audio Panning)."""
    distortion: typing.Annotated[FilterDistortion | None, pydantic.Field(default=None)]
    """Distorts the audio."""
    channel_mix: typing.Annotated[
        FilterChannelMix | None, pydantic.Field(default=None, alias="channelMix")
    ]
    """Mixes both channels (left and right)."""
    low_pass: typing.Annotated[
        FilterLowPass | None, pydantic.Field(default=None, alias="lowPass")
    ]
    """Filters higher frequencies."""
    plugin_filters: typing.Annotated[
        typing.MutableMapping[str, typing.Any],
        pydantic.Field(default={}, alias="pluginFilters"),
    ]
    """Filter plugin configurations."""


class EditableFilters(Filters):
    """
    Editable Filters.

    Allows for the user to edit the filter object.
    """

    # Volume

    def set_volume(self, volume: float):
        """
        Set volume.

        Set the volume of the players filters.

        Parameters
        ----------
        volume : hikari.UndefinedNoneOr[float]
            The volume you wish to setyping.
        """
        if volume > 5.0:
            raise ValueError("Volume must be lower than 5.0")

        if volume < 0.0:
            raise ValueError("Volume must be higher than or equal to 0.")

        self.volume = volume

    # Equalizer

    def set_equalizer_band(self, band: BandType, gain: float) -> None:
        """
        Set equalizer band.

        Set, or override a new equalizer band.
        """
        if gain < -0.25:
            raise ValueError("Gain must be greater than -0.25")
        if gain > 1.0:
            raise ValueError("Gain must be less than 1.0")

        for item in self.equalizer:
            if item.band == band:
                self.equalizer.remove(item)

        self.equalizer.append(FilterEqualizer(band=band, gain=gain))

    def remove_equalizer_band(self, band: BandType) -> None:
        """
        Remove equalizer band.

        Remove, an equalizer band if it existed.
        """
        for item in self.equalizer:
            if item.band == band:
                self.equalizer.remove(item)

    def clear_equalizer_bands(self) -> None:
        """
        Clear equalizer bands.

        Clear all equalizer bands.
        """
        self.equalizer.clear()

    # Karaoke

    def set_karaoke(
        self,
        level: float,
        mono_level: float,
        filter_band: float,
        filter_width: float,
    ) -> None:
        """
        Set the karaoke levels.

        Set new karaoke levels for the current filter.

        Parameters
        ----------
        level : float
            The level (0 to 1.0 where 0.0 is no effect and 1.0 is full effect).
        mono_level : float
            The mono level (0 to 1.0 where 0.0 is no effect and 1.0 is full effect).
        filter_band : float
            The filter band (in Hz).
        filter_width : float
            The filter width.
        """
        self.karaoke = FilterKaraoke(
            level=level,
            mono_level=mono_level,
            filter_band=filter_band,
            filter_width=filter_width,
        )

    def clear_karaoke(self) -> None:
        """
        Clear karaoke.

        This will completely remove the current karaoke setup.
        """
        self.karaoke = None

    # Timescale

    def set_timescale(self, speed: float, pitch: float, rate: float) -> None:
        self.timescale = FilterTimescale(speed=speed, pitch=pitch, rate=rate)

    def clear_timescale(self) -> None:
        self.timescale = None


class FilterEqualizer(PayloadBase):
    """
    Filter Equalizer.

    The filter equilizer, that allows you to set different values for different gains.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#equalizer)
    """

    band: BandType
    """The band (HZ25 to HZ16000)."""
    gain: typing.Annotated[float | None, pydantic.Field(default=None, ge=-0.25, le=1.0)]
    """The gain (-0.25 to 1.0)."""


class FilterKaraoke(PayloadBase):
    """
    Filter Karaoke.

    The karaoke portion of the filter.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#karaoke)
    """

    level: typing.Annotated[float | None, pydantic.Field(default=None, ge=0.0, le=1.0)]
    """The level (0 to 1.0 where 0.0 is no effect and 1.0 is full effect)."""
    mono_level: typing.Annotated[
        float | None, pydantic.Field(default=None, alias="monoLevel", ge=0.0, le=1.0)
    ]
    """The mono level (0 to 1.0 where 0.0 is no effect and 1.0 is full effect)."""
    filter_band: typing.Annotated[
        float | None, pydantic.Field(default=None, alias="filterBand", ge=0)
    ]
    """The filter band (in Hz)."""
    filter_width: typing.Annotated[
        float | None, pydantic.Field(default=None, alias="filterWidth")
    ]
    """The filter width."""


class FilterTimescale(PayloadBase):
    """
    Filter Timescale.

    The timescale portion of the filter.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#timescale)
    """

    speed: typing.Annotated[float | None, pydantic.Field(default=None, ge=0.0)]
    """The playback speed 0.0 ≤ x."""
    pitch: typing.Annotated[float | None, pydantic.Field(default=None, ge=0.0)]
    """The pitch 0.0 ≤ x."""
    rate: typing.Annotated[float | None, pydantic.Field(default=None, ge=0.0)]
    """The rate 0.0 ≤ x."""


class FilterTremolo(PayloadBase):
    """
    Filter Tremolo.

    The tremolo portion of the filter.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#tremolo)
    """

    frequency: typing.Annotated[float | None, pydantic.Field(default=None, ge=0.0)]
    """The frequency 0.0 < x."""
    depth: typing.Annotated[float | None, pydantic.Field(default=None, ge=0.0)]
    """The tremolo depth 0.0 < x ≤ 1.0."""


class FilterVibrato(PayloadBase):
    """
    Filter Vibrato.

    The vibrato portion of the filter.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#vibrato)
    """

    frequency: typing.Annotated[float | None, pydantic.Field(default=None, ge=0.0)]
    """The frequency 0.0 < x ≤ 14.0"""
    depth: typing.Annotated[float | None, pydantic.Field(default=None, ge=0.0)]
    """The tremolo depth 0.0 < x ≤ 1.0."""


class FilterRotation(PayloadBase):
    """
    Filter Rotation.

    The rotation portion of the filter.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#rotation)
    """

    rotation_hz: typing.Annotated[
        float | None, pydantic.Field(default=None, alias="rotationHz", ge=0.0)
    ]
    """The frequency of the audio rotating around the listener in Hz. 0.2 is similar to the example video above."""


class FilterDistortion(PayloadBase):
    """
    Filter Distortion.

    The distortion portion of the filter.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#distortion)
    """

    sin_offset: typing.Annotated[
        float | None, pydantic.Field(default=None, alias="sinOffset")
    ]
    """The sin offsetyping."""
    sin_scale: typing.Annotated[
        float | None, pydantic.Field(default=None, alias="sinScale")
    ]
    """The sin scale."""
    cos_offset: typing.Annotated[
        float | None, pydantic.Field(default=None, alias="cosOffset")
    ]
    """The cos offsetyping."""
    cos_scale: typing.Annotated[
        float | None, pydantic.Field(default=None, alias="cosScale")
    ]
    """The cos scale."""
    tan_offset: typing.Annotated[
        float | None, pydantic.Field(default=None, alias="tanOffset")
    ]
    """The tan offsetyping."""
    tan_scale: typing.Annotated[
        float | None, pydantic.Field(default=None, alias="tanScale")
    ]
    """The tan scale."""
    offset: typing.Annotated[float | None, pydantic.Field(default=None)]
    """The offsetyping."""
    scale: typing.Annotated[float | None, pydantic.Field(default=None)]
    """The scale."""


class FilterChannelMix(PayloadBase):
    """
    Filter Channel Mix.

    The channel mix portion of the filter.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#channel-mix)
    """

    left_to_left: typing.Annotated[
        float | None, pydantic.Field(default=None, alias="leftToLeft", ge=0.0, le=1.0)
    ]
    """The left to left channel mix factor (0.0 ≤ x ≤ 1.0)."""
    left_to_right: typing.Annotated[
        float | None, pydantic.Field(default=None, alias="leftToRight", ge=0.0, le=1.0)
    ]
    """The left to right channel mix factor (0.0 ≤ x ≤ 1.0)."""
    right_to_left: typing.Annotated[
        float | None, pydantic.Field(default=None, alias="rightToLeft", ge=0.0, le=1.0)
    ]
    """The right to left channel mix factor (0.0 ≤ x ≤ 1.0)."""
    right_to_right: typing.Annotated[
        float | None, pydantic.Field(default=None, alias="rightToRight", ge=0.0, le=1.0)
    ]
    """The right to right channel mix factor (0.0 ≤ x ≤ 1.0)."""


class FilterLowPass(PayloadBase):
    """
    Filter Low Pass.

    The low pass portion of the filter.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#low-pass)
    """

    smoothing: typing.Annotated[float | None, pydantic.Field(default=None)]
    """The smoothing factor (1.0 < x)."""


# MIT License

# Copyright (c) 2023 MPlatypus

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
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENtyping. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
