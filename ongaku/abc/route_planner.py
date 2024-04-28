"""
Route Planner ABC's.

Route planner abstract classes.
"""

from __future__ import annotations

import typing

import msgspec

from ongaku.abc.bases import PayloadBase
from ongaku.enums import IPBlockType
from ongaku.enums import RoutePlannerType

__all__ = (
    "FailingAddress",
    "RoutePlannerDetails",
    "RoutePlannerStatus",
)


class FailingAddress(PayloadBase):
    """
    Failing address.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#failing-address-object)
    """

    failing_address: str = msgspec.field(name="failingAddress")
    """The failing address."""
    failing_timestamp: int = msgspec.field(name="failingTimestamp")
    """The timestamp when the address failed."""
    failing_time: str = msgspec.field(name="failingTime")
    """The timestamp when the address failed as a pretty string."""


class IPBlock(PayloadBase):
    """
    Route Planner IP Block.

    All of the information about the IP Block.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest.html#ip-block-object)
    """

    type: IPBlockType
    """The type of the ip block."""
    size: str
    """The size of the ip block."""


class RoutePlannerDetails(PayloadBase):
    """
    Route Planner details.

    All of the information about the failing addresses.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#details-object)
    """

    ip_block: IPBlock = msgspec.field(name="ipBlock")
    """The ip block being used."""
    failing_addresses: typing.Sequence[FailingAddress] = msgspec.field(
        name="failingAddresses"
    )
    """The failing addresses."""
    rotate_index: str | None = msgspec.field(default=None, name="rotateIndex")
    """The number of rotations."""
    ip_index: str | None = msgspec.field(default=None, name="ipIndex")
    """The current offset in the block."""
    current_address: str | None = msgspec.field(default=None, name="currentAddress")
    """The current address being used."""
    current_address_index: str | None = msgspec.field(
        default=None, name="currentAddressIndex"
    )
    """The current offset in the ip block."""
    block_index: str | None = msgspec.field(default=None, name="blockIndex")
    """The current offset in the ip block."""


class RoutePlannerStatus(PayloadBase):
    """
    Route Planner Status Object.

    The status of the route-planner.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest.html#get-routeplanner-status)
    """

    class_type: RoutePlannerType | None = msgspec.field(default=None, name="class")
    """The name of the RoutePlanner implementation being used by this server."""
    details: RoutePlannerDetails | None = msgspec.field(default=None)
    """The status details of the RoutePlanner."""


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
