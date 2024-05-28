"""
Route Planner ABC's.

Route planner abstract classes.
"""

from __future__ import annotations

import abc
import enum
import typing

if typing.TYPE_CHECKING:
    import datetime

__all__ = (
    "RoutePlannerStatus",
    "RoutePlannerDetails",
    "IPBlock",
    "FailingAddress",
    "RoutePlannerType",
    "IPBlockType",
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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RoutePlannerStatus):
            return False

        if self.cls != other.cls:
            return False

        if self.details != other.details:
            return False

        return True


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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, RoutePlannerDetails):
            return False

        if self.ip_block != other.ip_block:
            return False

        if self.failing_addresses != other.failing_addresses:
            return False

        if self.rotate_index != other.rotate_index:
            return False

        if self.ip_index != other.ip_index:
            return False

        if self.current_address != other.current_address:
            return False

        if self.current_address_index != other.current_address_index:
            return False

        if self.block_index != other.block_index:
            return False

        return True


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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, IPBlock):
            return False

        if self.type != other.type:
            return False

        if self.size != other.size:
            return False

        return True


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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FailingAddress):
            return False

        if self.address != other.address:
            return False

        if self.timestamp != other.timestamp:
            return False

        if self.time != other.time:
            return False

        return True


class RoutePlannerType(str, enum.Enum):
    """
    Route Planner Type.

    The type of routeplanner that the server is currently using.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#route-planner-types)
    """

    ROTATING_ROUTE_PLANNER = "RotatingIpRoutePlanner"
    """IP address used is switched on ban. Recommended for IPv4 blocks or IPv6 blocks smaller than a /64."""
    NANO_IP_ROUTE_PLANNER = "NanoIpRoutePlanner"
    """IP address used is switched on clock update. Use with at least 1 /64 IPv6 block."""
    ROTATING_NANO_IP_ROUTE_PLANNER = "RotatingNanoIpRoutePlanner"
    """IP address used is switched on clock update, rotates to a different /64 block on ban. Use with at least 2x /64 IPv6 blocks."""
    BALANCING_IP_ROUTE_PLANNER = "BalancingIpRoutePlanner"
    """IP address used is selected at random per request. Recommended for larger IP blocks."""


class IPBlockType(str, enum.Enum):
    """
    IP Block Type.

    The IP Block type, 4, or 6.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#ip-block-type)
    """

    INET_4_ADDRESS = "Inet4Address"
    """The ipv4 block type"""
    INET_6_ADDRESS = "Inet6Address"
    """The ipv6 block type"""


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
