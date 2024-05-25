"""
Route Planner ABC's.

Route planner abstract classes.
"""

from __future__ import annotations

import abc
import datetime
import typing

from ongaku.enums import IPBlockType
from ongaku.enums import RoutePlannerType

__all__ = (
    "RoutePlannerStatus",
    "RoutePlannerDetails",
    "IPBlock",
    "FailingAddress",
)


class RoutePlannerStatus(abc.ABC):
    """
    Route Planner Status Object.

    The status of the route-planner.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#get-routeplanner-status)
    """

    @property
    @abc.abstractmethod
    def cls(self) -> RoutePlannerType:
        """The name of the RoutePlanner implementation being used by this server."""
        ...

    @property
    @abc.abstractmethod
    def details(self) -> RoutePlannerDetails:
        """The status details of the RoutePlanner."""
        ...


class RoutePlannerDetails(abc.ABC):
    """
    Route Planner details.

    All of the information about the failing addresses.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#details-object)
    """

    @property
    @abc.abstractmethod
    def ip_block(self) -> IPBlock:
        """The ip block being used."""
        ...

    @property
    @abc.abstractmethod
    def failing_addresses(self) -> typing.Sequence[FailingAddress]:
        """The failing addresses."""
        ...

    @property
    @abc.abstractmethod
    def rotate_index(self) -> str | None:
        """The number of rotations."""
        ...

    @property
    @abc.abstractmethod
    def ip_index(self) -> str | None:
        """The current offset in the block."""
        ...

    @property
    @abc.abstractmethod
    def current_address(self) -> str | None:
        """The current address being used."""
        ...

    @property
    @abc.abstractmethod
    def current_address_index(self) -> str | None:
        """The current offset in the ip block."""
        ...

    @property
    @abc.abstractmethod
    def block_index(self) -> str | None:
        """The current offset in the ip block."""
        ...


class IPBlock(abc.ABC):
    """
    Route Planner IP Block.

    All of the information about the IP Block.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#ip-block-object)
    """

    @property
    @abc.abstractmethod
    def type(self) -> IPBlockType:
        """The type of the ip block."""
        ...

    @property
    @abc.abstractmethod
    def size(self) -> str:
        """The size of the ip block."""
        ...


class FailingAddress(abc.ABC):
    """
    Failing address.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#failing-address-object)
    """

    @property
    @abc.abstractmethod
    def address(self) -> str:
        """The failing address."""
        ...

    @property
    @abc.abstractmethod
    def timestamp(self) -> datetime.datetime:
        """The timestamp when the address failed."""
        ...

    @property
    @abc.abstractmethod
    def time(self) -> str:
        """The timestamp when the address failed as a pretty string."""
        ...


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
