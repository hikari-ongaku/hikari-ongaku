"""
Route Planner ABC's.

Route planner abstract classes.
"""

from __future__ import annotations

import typing
import attrs
import datetime

from ongaku.enums import IPBlockType
from ongaku.enums import RoutePlannerType

__all__ = (
    "FailingAddress",
    "RoutePlannerDetails",
    "RoutePlannerStatus",
)


@attrs.define
class FailingAddress:
    """
    Failing address.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#failing-address-object)
    """

    _address: str = attrs.field(alias="address")
    _timestamp: datetime.datetime = attrs.field(alias="timestamp")
    _time: str = attrs.field(alias="time")

    @property
    def address(self) -> str:
        """The failing address."""
        return self._address

    @property
    def timestamp(self) -> datetime.datetime:
        """The timestamp when the address failed."""
        return self._timestamp

    @property
    def time(self) -> str:
        """The timestamp when the address failed as a pretty string."""
        return self._time


@attrs.define
class IPBlock:
    """
    Route Planner IP Block.

    All of the information about the IP Block.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#ip-block-object)
    """

    _type: IPBlockType = attrs.field(alias="type")
    _size: str = attrs.field(alias="size") 

    @property
    def type(self) -> IPBlockType:
        """The type of the ip block."""
        return self._type

    @property
    def size(self) -> str:
        """The size of the ip block."""
        return self._size


@attrs.define
class RoutePlannerDetails:
    """
    Route Planner details.

    All of the information about the failing addresses.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#details-object)
    """

    _ip_block: IPBlock = attrs.field(alias="ip_block")
    _failing_address: typing.Sequence[FailingAddress] = attrs.field(alias="failing_addresses")
    _rotate_index: str | None = attrs.field(alias="rotate_index")
    _ip_index: str | None = attrs.field(alias="ip_index")
    _current_address: str | None = attrs.field(alias="current_address")
    _current_address_index: str | None = attrs.field(alias="current_address_index")
    _block_index: str | None = attrs.field(alias="block_index")


    @property
    def ip_block(self) -> IPBlock:
        """The ip block being used."""
        return self._ip_block

    @property
    def failing_addresses(self) -> typing.Sequence[FailingAddress]:
        """The failing addresses."""
        return self._failing_address
    
    @property
    def rotate_index(self) -> str | None:
        """The number of rotations."""
        return self._rotate_index
    
    @property
    def ip_index(self) -> str | None:
        """The current offset in the block."""
        return self._ip_index
    
    @property
    def current_address(self) -> str | None:
        """The current address being used."""
        return self._current_address
    
    @property
    def current_address_index(self) -> str | None:
        """The current offset in the ip block."""
        return self._current_address_index
    
    @property
    def block_index(self) -> str | None:
        """The current offset in the ip block."""
        return self._block_index

@attrs.define
class RoutePlannerStatus:
    """
    Route Planner Status Object.

    The status of the route-planner.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#get-routeplanner-status)
    """

    _cls: RoutePlannerType = attrs.field(alias="cls")
    _details: RoutePlannerDetails = attrs.field(alias="details")

    @property
    def cls(self) -> RoutePlannerType:
        """The name of the RoutePlanner implementation being used by this server."""
        return self._cls

    @property
    def details(self) -> RoutePlannerDetails:
        """The status details of the RoutePlanner."""
        return self._details
    


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
