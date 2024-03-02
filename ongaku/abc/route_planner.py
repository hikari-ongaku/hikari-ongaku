"""Route Planner ABC's.

Route planner abstract classes. find more [here](https://lavalink.dev/api/rest#routeplanner-api)
"""

from __future__ import annotations

import typing as t

from ..enums import IPBlockType
from ..enums import RoutePlannerType
from .base import PayloadBase

__all__ = (
    "FailingAddress",
    "RoutePlannerDetails",
    "RoutePlannerStatus",
)


class FailingAddress(PayloadBase[t.Mapping[str, t.Any]]):
    """Failing address.

    more [here](https://lavalink.dev/api/rest#failing-address-object)
    """

    failing_address: str
    """The failing address"""
    failing_timestamp: int
    """The timestamp when the address failed"""
    failing_time: str
    """The timestamp when the address failed as a pretty string"""


class RoutePlannerDetails(PayloadBase[t.Mapping[str, t.Any]]):
    """Route Planner details.

    more [here](https://lavalink.dev/api/rest#details-object)
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


class RoutePlannerStatus(PayloadBase[t.Mapping[str, t.Any]]):
    """Route Planner Status Object.

    The status of the route-planner.
    """

    class_type: RoutePlannerType | None
    details: RoutePlannerDetails | None
