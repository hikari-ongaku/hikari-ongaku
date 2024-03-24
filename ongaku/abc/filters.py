"""
Filter ABC's.

The filter abstract classes.
"""

from __future__ import annotations

import typing as t

from pydantic import Field

from ..enums import BandType
from .bases import PayloadBase

__all__ = (
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

if t.TYPE_CHECKING:
    BuildT = dict[
        str, float | t.Mapping[str, float] | t.Sequence[dict[str, float | int]]
    ]


class Filters(PayloadBase):
    """
    The base filters.

    Build a new filter, or view the current filter.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#equalizer)

    !!! note
        They will only actually update, if you parse this to the player.
    """

    @classmethod
    def build(cls) -> Filters:
        """
        build a filters object.

        Build an empty filters object to pass to the bot.
        """
        return Filters(
            volume=None,
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

    volume: t.Annotated[float | None, Field(default=None, ge=0.0, le=5.0)]
    """Adjusts the player volume from 0.0 to 5.0, where 1.0 is 100%. Values >1.0 may cause clipping."""
    equalizer: t.Annotated[t.MutableSequence[FilterEqualizer], Field(default=[])]
    """Adjusts 15 different bands."""
    karaoke: t.Annotated[FilterKaraoke | None, Field(default=None)]
    """Eliminates part of a band, usually targeting vocals."""
    timescale: t.Annotated[FilterTimescale | None, Field(default=None)]
    """Changes the speed, pitch, and rate."""
    tremolo: t.Annotated[FilterTremolo | None, Field(default=None)]
    """Creates a shuddering effect, where the volume quickly oscillates."""
    vibrato: t.Annotated[FilterVibrato | None, Field(default=None)]
    """Creates a shuddering effect, where the pitch quickly oscillates."""
    rotation: t.Annotated[FilterRotation | None, Field(default=None)]
    """Rotates the audio around the stereo channels/user headphones (aka Audio Panning)."""
    distortion: t.Annotated[FilterDistortion | None, Field(default=None)]
    """Distorts the audio."""
    channel_mix: t.Annotated[
        FilterChannelMix | None, Field(default=None, alias="channelMix")
    ]
    """Mixes both channels (left and right)."""
    low_pass: t.Annotated[FilterLowPass | None, Field(default=None, alias="lowPass")]
    """Filters higher frequencies."""
    plugin_filters: t.Annotated[
        t.MutableMapping[str, t.Any], Field(default={}, alias="pluginFilters")
    ]
    """Filter plugin configurations."""


class FilterEqualizer(PayloadBase):
    """
    Filter Equalizer.

    The filter equilizer, that allows you to set different values for different gains.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#equalizer)
    """

    band: BandType
    """The band (HZ25 to HZ16000)."""
    value: t.Annotated[float | None, Field(default=None, ge=-0.25, le=1.0)]
    """The gain (-0.25 to 1.0)."""


class FilterKaraoke(PayloadBase):
    """
    Filter Karaoke.

    The karaoke portion of the filter.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#karaoke)
    """

    level: t.Annotated[float | None, Field(default=None, ge=0.0, le=1.0)]
    """The level (0 to 1.0 where 0.0 is no effect and 1.0 is full effect)."""
    mono_level: t.Annotated[
        float | None, Field(default=None, alias="monoLevel", ge=0.0, le=1.0)
    ]
    """The mono level (0 to 1.0 where 0.0 is no effect and 1.0 is full effect)."""
    filter_band: t.Annotated[
        float | None, Field(default=None, alias="filterBand", ge=0)
    ]
    """The filter band (in Hz)."""
    filter_width: t.Annotated[float | None, Field(default=None, alias="filterWidth")]
    """The filter width."""


class FilterTimescale(PayloadBase):
    """
    Filter Timescale.

    The timescale portion of the filter.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#timescale)
    """

    speed: t.Annotated[float | None, Field(default=None, ge=0.0)]
    """The playback speed 0.0 ≤ x."""
    pitch: t.Annotated[float | None, Field(default=None, ge=0.0)]
    """The pitch 0.0 ≤ x."""
    rate: t.Annotated[float | None, Field(default=None, ge=0.0)]
    """The rate 0.0 ≤ x."""


class FilterTremolo(PayloadBase):
    """
    Filter Tremolo.

    The tremolo portion of the filter.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#tremolo)
    """

    frequency: t.Annotated[float | None, Field(default=None, ge=0.0)]
    """The frequency 0.0 < x."""
    depth: t.Annotated[float | None, Field(default=None, ge=0.0)]
    """The tremolo depth 0.0 < x ≤ 1.0."""


class FilterVibrato(PayloadBase):
    """
    Filter Vibrato.

    The vibrato portion of the filter.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#vibrato)
    """

    frequency: t.Annotated[float | None, Field(default=None, ge=0.0)]
    """The frequency 0.0 < x ≤ 14.0"""
    depth: t.Annotated[float | None, Field(default=None, ge=0.0)]
    """The tremolo depth 0.0 < x ≤ 1.0."""


class FilterRotation(PayloadBase):
    """
    Filter Rotation.

    The rotation portion of the filter.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#rotation)
    """

    rotation_hz: t.Annotated[
        float | None, Field(default=None, alias="rotationHz", ge=0.0)
    ]
    """The frequency of the audio rotating around the listener in Hz. 0.2 is similar to the example video above."""


class FilterDistortion(PayloadBase):
    """
    Filter Distortion.

    The distortion portion of the filter.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#distortion)
    """

    sin_offset: t.Annotated[float | None, Field(default=None, alias="sinOffset")]
    """The sin offset."""
    sin_scale: t.Annotated[float | None, Field(default=None, alias="sinScale")]
    """The sin scale."""
    cos_offset: t.Annotated[float | None, Field(default=None, alias="cosOffset")]
    """The cos offset."""
    cos_scale: t.Annotated[float | None, Field(default=None, alias="cosScale")]
    """The cos scale."""
    tan_offset: t.Annotated[float | None, Field(default=None, alias="tanOffset")]
    """The tan offset."""
    tan_scale: t.Annotated[float | None, Field(default=None, alias="tanScale")]
    """The tan scale."""
    offset: t.Annotated[float | None, Field(default=None)]
    """The offset."""
    scale: t.Annotated[float | None, Field(default=None)]
    """The scale."""


class FilterChannelMix(PayloadBase):
    """
    Filter Channel Mix.

    The channel mix portion of the filter.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#channel-mix)
    """

    left_to_left: t.Annotated[
        float | None, Field(default=None, alias="leftToLeft", ge=0.0, le=1.0)
    ]
    """The left to left channel mix factor (0.0 ≤ x ≤ 1.0)."""
    left_to_right: t.Annotated[
        float | None, Field(default=None, alias="leftToRight", ge=0.0, le=1.0)
    ]
    """The left to right channel mix factor (0.0 ≤ x ≤ 1.0)."""
    right_to_left: t.Annotated[
        float | None, Field(default=None, alias="rightToLeft", ge=0.0, le=1.0)
    ]
    """The right to left channel mix factor (0.0 ≤ x ≤ 1.0)."""
    right_to_right: t.Annotated[
        float | None, Field(default=None, alias="rightToRight", ge=0.0, le=1.0)
    ]
    """The right to right channel mix factor (0.0 ≤ x ≤ 1.0)."""


class FilterLowPass(PayloadBase):
    """
    Filter Low Pass.

    The low pass portion of the filter.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#low-pass)
    """

    smoothing: t.Annotated[float | None, Field(default=None)]
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
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
