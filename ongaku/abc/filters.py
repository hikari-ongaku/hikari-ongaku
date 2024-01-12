from __future__ import annotations

import abc
import hikari
import typing as t


class FilterBase(abc.ABC):
    """
    Base class for all filters.
    """

    _name: str

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """
        The name of the filter.

        The name of the filter. If this is a custom plugin filter, you must label it as the plugin name.
        """
        return self._name

    @abc.abstractmethod
    def _build(self) -> t.Mapping[str, t.Any] | None:
        """
        Function to build the filter.

        If none, then not enough arguments were passed to fully build the command.
        """
        ...


class FilterEqualizer(FilterBase):
    def __init__(
        self,
        *,
        hz25: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        hz40: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        hz63: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        hz100: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        hz160: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        hz250: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        hz400: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        hz630: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        hz1000: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        hz1600: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        hz2500: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        hz4000: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        hz6300: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        hz10000: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        hz16000: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
    ) -> None:
        """
        Equalizer filter

        Set the equalizer filter bands. If None is specified, then sets to default, 0.

        Parameters
        ----------
        hz25 : UndefinedNoneOr[float]
            The band for 25hz.
        hz40 : UndefinedNoneOr[float]
            The band for 40hz.
        hz63 : UndefinedNoneOr[float]
            The band for 63hz.
        hz100 : UndefinedNoneOr[float]
            The band for 100hz.
        hz160 : UndefinedNoneOr[float]
            The band for 160hz.
        hz250 : UndefinedNoneOr[float]
            The band for 250hz.
        hz400 : UndefinedNoneOr[float]
            The band for 400hz.
        hz630 : UndefinedNoneOr[float]
            The band for 630hz.
        hz1000 : UndefinedNoneOr[float]
            The band for 1000hz.
        hz1600 : UndefinedNoneOr[float]
            The band for 1600hz.
        hz2500 : UndefinedNoneOr[float]
            The band for 2500hz.
        hz4000 : UndefinedNoneOr[float]
            The band for 4000hz.
        hz4000 : UndefinedNoneOr[float]
            The band for 4000hz.
        hz6300 : UndefinedNoneOr[float]
            The band for 6300hz.
        hz10000 : UndefinedNoneOr[float]
            The band for 10000hz.
        hz16000 : UndefinedNoneOr[float]
            The band for 16000hz.


        Raises
        ------
        ValueError
            Raised because one or more of the values, are either below -0.25, or above 1.
        """

        for band, gain in zip(
            [
                "hz25",
                "hz40",
                "hz63",
                "hz100",
                "hz160",
                "hz250",
                "hz400",
                "hz630",
                "hz1000",
                "hz1600",
                "hz2500",
                "hz4000",
                "hz6300",
                "hz10000",
                "hz16000",
            ],
            [
                hz25,
                hz40,
                hz63,
                hz100,
                hz160,
                hz250,
                hz400,
                hz630,
                hz1000,
                hz1600,
                hz2500,
                hz4000,
                hz6300,
                hz10000,
                hz16000,
            ],
        ):
            if gain == hikari.UNDEFINED:
                continue

            if gain is None:
                self._equalizers.update({band: hikari.UNDEFINED})
                continue

            if not (-0.25 >= gain <= 1.0):
                raise ValueError(
                    f"The value {gain} ({band}) must be between -0.25, and 1.0."
                )

            self._equalizers.update({band: gain})

    _is_plugin: bool = False
    """Internal use only."""

    _name = "equalizer"

    _equalizers: dict[str, hikari.UndefinedOr[float]] = {
        "hz25": hikari.UNDEFINED,
        "hz40": hikari.UNDEFINED,
        "hz63": hikari.UNDEFINED,
        "hz100": hikari.UNDEFINED,
        "hz160": hikari.UNDEFINED,
        "hz250": hikari.UNDEFINED,
        "hz400": hikari.UNDEFINED,
        "hz630": hikari.UNDEFINED,
        "hz1000": hikari.UNDEFINED,
        "hz1600": hikari.UNDEFINED,
        "hz2500": hikari.UNDEFINED,
        "hz4000": hikari.UNDEFINED,
        "hz6300": hikari.UNDEFINED,
        "hz10000": hikari.UNDEFINED,
        "hz16000": hikari.UNDEFINED,
    }

    def _build(self):
        return_data: list[dict[str, float | int]] = []
        for x in range(len(self._equalizers)):
            items = list(self._equalizers.values())

            current_item = items[x]

            if current_item == hikari.UNDEFINED:
                continue

            return_data.append({"band": x, "gain": current_item})

        if len(return_data) <= 0:
            return

        return {"equalizer": return_data}


class FilterKaraoke(FilterBase):
    _is_plugin: bool = False
    """Internal use only."""

    _name = "karaoke"

    _level: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED
    _mono_level: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED
    _filter_band: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED
    _filter_width: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED

    def __init__(
        self,
        *,
        level: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        mono_level: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        filter_band: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        filter_width: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
    ) -> None:
        """
        Karaoke filter

        Allows for building the karaoke filter to add to your filter object.

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
        if isinstance(level, float):
            if 0 > level or level > 1:
                raise ValueError("Outside of value range for value level.")

        if isinstance(mono_level, float):
            if 0 > mono_level or mono_level > 1:
                raise ValueError("Outside of value range for value mono_level.")

        self._level = level
        self._mono_level = mono_level
        self._filter_band = filter_band
        self._filter_width = filter_width

    def build(self):
        return_data: dict[str, t.Any] = {}
        if self._level != hikari.UNDEFINED:
            return_data.update({"level": 0})

        return return_data


class FilterTimeScale(FilterBase):
    _is_plugin: bool = False
    """Internal use only."""

    _name = "equalizer"

    _speed: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED
    _pitch: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED
    _rate: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED

    def __init__(
        self,
        speed: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
    ) -> None:
        self._speed = speed


class FilterTremolo(FilterBase):
    _is_plugin: bool = False
    """Internal use only."""

    _name = "tremolo"

    _frequency: hikari.UndefinedOr[float] = hikari.UNDEFINED
    _depth: hikari.UndefinedOr[float] = hikari.UNDEFINED


class FilterVibrato(FilterBase):
    _is_plugin: bool = False
    """Internal use only."""

    _name = "vibrato"

    _frequency: hikari.UndefinedOr[float] = hikari.UNDEFINED
    _depth: hikari.UndefinedOr[float] = hikari.UNDEFINED


class FilterRotation(FilterBase):
    _is_plugin: bool = False
    """Internal use only."""

    _name = "rotation"

    _rotation_hz: hikari.UndefinedOr[float] = hikari.UNDEFINED


class FilterDistortion(FilterBase):
    _is_plugin: bool = False
    """Internal use only."""

    _name = "distortion"

    _sin_offset: hikari.UndefinedOr[float] = hikari.UNDEFINED
    _sin_scale: hikari.UndefinedOr[float] = hikari.UNDEFINED
    _cos_offset: hikari.UndefinedOr[float] = hikari.UNDEFINED
    _cos_scale: hikari.UndefinedOr[float] = hikari.UNDEFINED
    _tan_offset: hikari.UndefinedOr[float] = hikari.UNDEFINED
    _tan_scale: hikari.UndefinedOr[float] = hikari.UNDEFINED
    _offset: hikari.UndefinedOr[float] = hikari.UNDEFINED
    _scale: hikari.UndefinedOr[float] = hikari.UNDEFINED


class FilterChannelMix(FilterBase):
    _is_plugin: bool = False
    """Internal use only."""

    _name = "channel_mix"

    _left_to_left: hikari.UndefinedOr[float] = hikari.UNDEFINED
    _left_to_right: hikari.UndefinedOr[float] = hikari.UNDEFINED
    _right_to_left: hikari.UndefinedOr[float] = hikari.UNDEFINED
    _right_to_right: hikari.UndefinedOr[float] = hikari.UNDEFINED


class FilterLowPass(FilterBase):
    _is_plugin: bool = False
    """Internal use only."""

    _name = "low_pass"

    _smoothing: hikari.UndefinedOr[float] = hikari.UNDEFINED


class FilterBuilder:
    _filters: dict[str, hikari.UndefinedNoneOr[FilterBase]] = {
        "equalizer": hikari.UNDEFINED,
        "karaoke": hikari.UNDEFINED,
        "timescale": hikari.UNDEFINED,
        "tremolo": hikari.UNDEFINED,
        "vibrato": hikari.UNDEFINED,
        "rotation": hikari.UNDEFINED,
        "distortion": hikari.UNDEFINED,
        "channel_mix": hikari.UNDEFINED,
        "low_pass": hikari.UNDEFINED,
        "plugin_filters": hikari.UNDEFINED,
    }
    _volume: int | None = None

    def volume(self, value: int | None = None):
        """
        Set the volume

        Set the volume for the player.
        """
        self._volume = value

    def add(
        self, filters: FilterBase | list[FilterBase], override: bool = False
    ) -> None:
        """
        add a filter

        Add a filter to this filter object.

        Parameters
        ----------
        filters : FilterBase | list[Filter]
            anything that incorporates the [FilterBase][ongaku.abc.filters.FilterBase] can be added here.
        override : bool
            whether to override the existing value or not.

        !!! NOTE
            If override is True, then all values that you pass, will be overridden, otherwise, the value will be ignored.
        """

    def remove(self, filter: FilterBase) -> None:
        """
        remove a filter

        Remove a filter from the filters. This will force disable that specific filter.
        """

    def build(self) -> dict[str, t.Any]:
        return {}


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
