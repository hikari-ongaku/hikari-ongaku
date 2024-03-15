"""
Route Planner ABC's.

Route planner abstract classes. 
"""

from __future__ import annotations

import typing as t

from ..enums import IPBlockType
from ..enums import RoutePlannerType
from .bases import PayloadBase

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

    failing_address: str
    """The failing address"""
    failing_timestamp: int
    """The timestamp when the address failed"""
    failing_time: str
    """The timestamp when the address failed as a pretty string"""


class RoutePlannerDetails(PayloadBase):
    """
    Route Planner details.

    All of the information about the failing addresses.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#details-object)
    """

    ip_block: IPBlockType
    """The ip block being used"""
    failing_addresses: t.Sequence[FailingAddress]
    """The failing addresses"""
    rotate_index: str
    """The number of rotations"""
    ip_index: str
    """The current offset in the block"""
    current_address: str
    """The current address being used"""
    current_address_index: str
    """The current offset in the ip block"""
    block_index: str
    """The current offset in the ip block"""


class RoutePlannerStatus(PayloadBase):
    """
    Route Planner Status Object.

    The status of the route-planner.

    ![Lavalink](../../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest.html#get-routeplanner-status)
    """

    class_type: RoutePlannerType | None
    """The name of the RoutePlanner implementation being used by this server."""
    details: RoutePlannerDetails | None
    """The status details of the RoutePlanner"""
