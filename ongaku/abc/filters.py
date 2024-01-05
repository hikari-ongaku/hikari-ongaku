from __future__ import annotations

import abc
import hikari
import typing as t

if t.TYPE_CHECKING:
    BuildT = t.TypeVar("BuildT", int, float, bool, str, list[int | float | bool | str | None], dict[str, int | float | bool | str | None])

class FilterBase(abc.ABC):
    """
    Base class for all filters.
    """

    _name: str

    @abc.abstractproperty
    def name(self) -> str:
        """
        The name of the filter.

        The name of the filter. If this is a custom plugin filter, you must label it as the plugin name.
        """
        return self._name

    @abc.abstractmethod
    def build(self) -> dict[str, BuildT] | None:
        """
        Function to build the filter.

        If none, then not enough arguments were passed to fully build the command.
        """
        ...


class FilterEqualizer(FilterBase):
    """
    Equalizer filter

    Allows for building the equalizer filter to add to your filter object.
    """

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
        Set equalizers

        Set the equalizer bands. If None is specified, then sets to default, 0.

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


    is_plugin: bool = False
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

    def build(self) -> dict[str, BuildT] | None:
        return_data: list[dict[str, float | int]] = []
        for x in range(len(self._equalizers)):
            items = list(self._equalizers.values())

            current_item = items[x]

            if current_item == hikari.UNDEFINED:
                continue

            return_data.append({"band":x, "gain":current_item})

        if len(return_data) <= 0:
            return

        return {"equalizer":return_data}


class FilterKaraoke(FilterBase[BuildT]):
    """
    Karaoke filter

    Allows for building the karaoke filter to add to your filter object.
    """

    _level: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED
    _mono_level: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED
    _filter_band: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED
    _filter_width: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED

    def set(
        self,
        *,
        level: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        mono_level: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        filter_band: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
        filter_width: hikari.UndefinedNoneOr[float] = hikari.UNDEFINED,
    ) -> None:
        """
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
        self._level = level
        self._mono_level = mono_level
        self._filter_band = filter_band
        self._filter_width = filter_width

    def build(self):
        return_data: dict[str, BuildT] = {}
        if self._level != hikari.UNDEFINED:
            return_data.update({"level": 0})

class Filters:
    _filters: dict[str, hikari.UndefinedNoneOr[FilterBase[t.Any]]] = {
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

        !!! WARNING
            You can only add one of a certain type of filter. Adding more, will override already existing filters.
        """

    def remove(self, filter: FilterBase) -> None:
        """
        remove a filter

        Remove a filter from the filters. This will force disable that specific filter.
        """

    def build(self) -> dict[str, t.Any]:
        return {}
