"""Filter ABC.

All of the filter related functions.
"""

from __future__ import annotations

import typing as t

from hikari import UNDEFINED
from hikari import UndefinedNoneOr

from ..enums import BandType

__all__ = ("Filter",)

if t.TYPE_CHECKING:
    BuildT = dict[
        str, float | t.Mapping[str, float] | t.Sequence[dict[str, float | int]]
    ]


class Filter:
    """
    create a filter object.

    The builder for your filter needs.
    """

    _volume: float | None = None
    _equalizer: dict[BandType, float] = {}
    _karaoke: dict[str, float] = {}
    _timescale: dict[str, float] = {}
    _tremolo: dict[str, float] = {}
    _vibrato: dict[str, float] = {}
    _rotation: dict[str, float] = {}
    _distortion: dict[str, float] = {}
    _channel_mix: dict[str, float] = {}
    _low_pass: dict[str, float] = {}

    def volume(self, value: float | None = None) -> None:
        """Set the volume.

        Set the volume for the player.
        """
        self._volume = value

    def set_equalizer(
        self, band: BandType, gain: UndefinedNoneOr[float] = UNDEFINED
    ) -> float | None:
        """
        Set the equalizer value.

        !!! note
            If the gain is set to `None`, then the gain band will be removed, if `UNDEFINED` is used (leaving it empty), it will return the value, if it exists.

        Parameters
        ----------
        band : BandType
            The band type.
        gain : UndefinedNoneOr[float]
            The gain of the band.


        """
        if gain == UNDEFINED:
            return self._equalizer.get(band)

        if not gain:
            try:
                self._equalizer.pop(band)
            except KeyError:
                pass
            return

        if -0.25 > gain or gain > 1:
            raise ValueError(
                f"The value {gain} ({band}) must be between -0.25, and 1.0."
            )

        self._equalizer.update({band: gain})

    def set_karaoke(
        self,
        *,
        level: UndefinedNoneOr[float] = UNDEFINED,
        mono_level: UndefinedNoneOr[float] = UNDEFINED,
        filter_band: UndefinedNoneOr[float] = UNDEFINED,
        filter_width: UndefinedNoneOr[float] = UNDEFINED,
    ) -> None:
        """
        Set the equalizer value.

        Parameters
        ----------
        level : UndefinedNoneOr[float]
            The level (0 to 1.0 where 0.0 is no effect and 1.0 is full effect)
        mono_level : UndefinedNoneOr[float]
            The mono level (0 to 1.0 where 0.0 is no effect and 1.0 is full effect)
        filter_band : UndefinedNoneOr[float]
            The filter band (in Hz)
        filter_width : UndefinedNoneOr[float]
            The filter width
        """
        if level is None:
            self._karaoke.pop("level")

        if mono_level is None:
            self._karaoke.pop("monoLevel")

        if filter_band is None:
            self._karaoke.pop("filterBand")

        if filter_width is None:
            self._karaoke.pop("filterWidth")

        if isinstance(filter_band, float):
            self._karaoke.update({"filterBand": filter_band})

        if isinstance(filter_width, float):
            self._karaoke.update({"filterWidth": filter_width})

        if isinstance(level, float):
            if 0 > level or level > 1:
                raise ValueError("Outside of value range for value level.")
            else:
                self._karaoke.update({"level": level})

        if isinstance(mono_level, float):
            if 0 > mono_level or mono_level > 1:
                raise ValueError("Outside of value range for value mono_level.")
            else:
                self._karaoke.update({"monoLevel": mono_level})

    def set_timescale(
        self,
        *,
        speed: UndefinedNoneOr[float] = UNDEFINED,
        pitch: UndefinedNoneOr[float] = UNDEFINED,
        rate: UndefinedNoneOr[float] = UNDEFINED,
    ) -> None:
        """
        Set timescale.

        Parameters
        ----------
        speed : UndefinedNoneOr[float]
            The playback speed 0.0 ≤ x
        pitch : UndefinedNoneOr[float]
            The pitch 0.0 ≤ x
        rate : UndefinedNoneOr[float]
            The rate 0.0 ≤ x
        """
        if speed is None:
            self._timescale.pop("speed")

        if isinstance(speed, float):
            self._timescale = {"speed": speed}

        if pitch is None:
            self._timescale.pop("pitch")

        if isinstance(pitch, float):
            self._timescale = {"pitch": pitch}

        if rate is None:
            self._timescale.pop("rate")

        if isinstance(rate, float):
            self._timescale = {"rate": rate}

    def set_tremolo(
        self,
        *,
        frequency: UndefinedNoneOr[float] = UNDEFINED,
        depth: UndefinedNoneOr[float] = UNDEFINED,
    ) -> None:
        """
        Set tremolo.

        Parameters
        ----------
        frequency : UndefinedNoneOr[float]
            The frequency 0.0 < x
        depth : UndefinedNoneOr[float]
            The tremolo depth 0.0 < x ≤ 1.0
        """
        if frequency is None:
            self._tremolo.pop("frequency")

        if depth is None:
            self._tremolo.pop("depth")

        if isinstance(frequency, float):
            if 0 > frequency:
                raise ValueError("Outside of value range for value level.")
            else:
                self._tremolo.update({"frequency": frequency})

        if isinstance(depth, float):
            if 0 > depth or depth > 1:
                raise ValueError("Outside of value range for value level.")
            else:
                self._tremolo.update({"depth": depth})

    def set_vibrato(
        self,
        *,
        frequency: UndefinedNoneOr[float] = UNDEFINED,
        depth: UndefinedNoneOr[float] = UNDEFINED,
    ) -> None:
        """
        Set vibrato.

        Parameters
        ----------
        frequency : UndefinedNoneOr[float]
                The frequency 0.0 < x ≤ 14.0
        depth : UndefinedNoneOr[float]
            The tremolo depth 0.0 < x ≤ 1.0
        """
        if frequency is None:
            self._vibrato.pop("frequency")

        if depth is None:
            self._vibrato.pop("depth")

        if isinstance(frequency, float):
            if 0 > frequency or frequency > 14:
                raise ValueError("Outside of value range for value level.")
            else:
                self._vibrato.update({"frequency": frequency})

        if isinstance(depth, float):
            if 0 > depth or depth > 1:
                raise ValueError("Outside of value range for value level.")
            else:
                self._vibrato.update({"depth": depth})

    def set_rotation(
        self,
        *,
        rotation_hz: UndefinedNoneOr[float] = UNDEFINED,
    ) -> None:
        """
        Set rotation.

        Parameters
        ----------
        rotation_hz : UndefinedNoneOr[float]
            The frequency of the audio rotating around the listener in Hz.
        """
        if rotation_hz is None:
            self._rotation.pop("rotationHz")

        if isinstance(rotation_hz, float):
            self._vibrato.update({"rotationHz": rotation_hz})

    def set_distortion(
        self,
        *,
        sin_offset: UndefinedNoneOr[float] = UNDEFINED,
        sin_scale: UndefinedNoneOr[float] = UNDEFINED,
        cos_offset: UndefinedNoneOr[float] = UNDEFINED,
        cos_scale: UndefinedNoneOr[float] = UNDEFINED,
        tan_offset: UndefinedNoneOr[float] = UNDEFINED,
        tan_scale: UndefinedNoneOr[float] = UNDEFINED,
        offset: UndefinedNoneOr[float] = UNDEFINED,
        scale: UndefinedNoneOr[float] = UNDEFINED,
    ) -> None:
        """
        Set distortion.

        Parameters
        ----------
        sin_offset : UndefinedNoneOr[float]
            The sin offset
        sin_scale : UndefinedNoneOr[float]
            The sin scale
        cos_offset : UndefinedNoneOr[float]
            The cos offset
        cos_scale : UndefinedNoneOr[float]
            The cos scale
        tan_offset : UndefinedNoneOr[float]
            The tan offset
        tan_scale : UndefinedNoneOr[float]
            The tan scale
        offset : UndefinedNoneOr[float]
            The offset
        scale : UndefinedNoneOr[float]
            The scale
        """
        if sin_offset is None:
            self._distortion.pop("sinOffset")

        if isinstance(sin_offset, float):
            self._distortion.update({"sinOffset": sin_offset})

        if sin_scale is None:
            self._distortion.pop("sinScale")

        if isinstance(sin_scale, float):
            self._distortion.update({"sinScale": sin_scale})

        if cos_offset is None:
            self._distortion.pop("sinOffset")

        if isinstance(cos_offset, float):
            self._distortion.update({"sinOffset": cos_offset})

        if cos_scale is None:
            self._distortion.pop("cosScale")

        if isinstance(cos_scale, float):
            self._distortion.update({"cosScale": cos_scale})

        if tan_offset is None:
            self._distortion.pop("tanOffset")

        if isinstance(tan_offset, float):
            self._distortion.update({"tanOffset": tan_offset})

        if tan_scale is None:
            self._distortion.pop("tanScale")

        if isinstance(tan_scale, float):
            self._distortion.update({"tanScale": tan_scale})

        if offset is None:
            self._distortion.pop("offset")

        if isinstance(offset, float):
            self._distortion.update({"offset": offset})

        if scale is None:
            self._distortion.pop("scale")

        if isinstance(scale, float):
            self._distortion.update({"scale": scale})

    def set_channel_mix(
        self,
        *,
        left_to_left: UndefinedNoneOr[float] = UNDEFINED,
        left_to_right: UndefinedNoneOr[float] = UNDEFINED,
        right_to_left: UndefinedNoneOr[float] = UNDEFINED,
        right_to_right: UndefinedNoneOr[float] = UNDEFINED,
    ) -> None:
        """
        Set channel mix.

        Parameters
        ----------
        left_to_left : UndefinedNoneOr[float]
            The left to left channel mix factor (0.0 ≤ x ≤ 1.0)
        left_to_right : UndefinedNoneOr[float]
            The left to right channel mix factor (0.0 ≤ x ≤ 1.0)
        right_to_left : UndefinedNoneOr[float]
            The right to left channel mix factor (0.0 ≤ x ≤ 1.0)
        right_to_right : UndefinedNoneOr[float]
            The right to right channel mix factor (0.0 ≤ x ≤ 1.0)
        """
        if left_to_left is None:
            self._channel_mix.pop("leftToLeft")

        if isinstance(left_to_left, float):
            if 0 > left_to_left or left_to_left > 1:
                raise ValueError("Outside of value range for value level.")
            else:
                self._channel_mix.update({"leftToLeft": left_to_left})

        if left_to_right is None:
            self._channel_mix.pop("leftToRight")

        if isinstance(left_to_right, float):
            if 0 > left_to_right or left_to_right > 1:
                raise ValueError("Outside of value range for value level.")
            else:
                self._channel_mix.update({"leftToRight": left_to_right})

        if right_to_left is None:
            self._channel_mix.pop("rightToLeft")

        if isinstance(right_to_left, float):
            if 0 > right_to_left or right_to_left > 1:
                raise ValueError("Outside of value range for value level.")
            else:
                self._channel_mix.update({"rightToLeft": right_to_left})

        if right_to_right is None:
            self._channel_mix.pop("rightToRight")

        if isinstance(right_to_right, float):
            if 0 > right_to_right or right_to_right > 1:
                raise ValueError("Outside of value range for value level.")
            else:
                self._channel_mix.update({"rightToRight": right_to_right})

    def set_low_pass(
        self,
        *,
        smoothing: UndefinedNoneOr[float] = UNDEFINED,
    ) -> None:
        """
        Set low pass.

        Parameters
        ----------
        smoothing : UndefinedNoneOr[float]
            The smoothing factor (1.0 < x)
        """
        if smoothing is None:
            self._low_pass.pop("left_to_left")

        if isinstance(smoothing, float):
            if 0 > smoothing:
                raise ValueError("Outside of value range for value level.")
            else:
                self._low_pass.update({"smoothing": smoothing})

    def _build(
        self,
    ) -> BuildT:
        build_dict: BuildT = {}

        if self._volume:
            build_dict.update({"volume": self._volume})

        if len(self._equalizer) > 0:
            eq_bands: list[dict[str, float | int]] = []

            for key, value in self._equalizer.items():
                eq_bands.append({"band": key.value, "gain": value})

            build_dict.update({"equalizer": eq_bands})

        if len(self._karaoke) > 0:
            build_dict.update({"karaoke": self._karaoke})

        if len(self._timescale) > 0:
            build_dict.update({"timescale": self._timescale})

        if len(self._tremolo) > 0:
            build_dict.update({"tremolo": self._tremolo})

        if len(self._vibrato) > 0:
            build_dict.update({"vibrato": self._vibrato})

        if len(self._rotation) > 0:
            build_dict.update({"rotation": self._rotation})

        if len(self._distortion) > 0:
            build_dict.update({"distortion": self._distortion})

        if len(self._channel_mix) > 0:
            build_dict.update({"channelMix": self._channel_mix})

        if len(self._low_pass) > 0:
            build_dict.update({"lowPass": self._low_pass})

        return build_dict


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
