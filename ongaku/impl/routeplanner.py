"""
RoutePlanner Impl's.

The routeplanner implemented classes.
"""

from __future__ import annotations

import typing

from ongaku.abc import routeplanner as routeplanner_

if typing.TYPE_CHECKING:
    import datetime

__all__ = ("RoutePlannerStatus", "RoutePlannerDetails", "IPBlock", "FailingAddress")


class RoutePlannerStatus(routeplanner_.RoutePlannerStatus):
    def __init__(
        self,
        cls: routeplanner_.RoutePlannerType,
        details: routeplanner_.RoutePlannerDetails,
    ) -> None:
        self._cls = cls
        self._details = details

    @property
    def cls(self) -> routeplanner_.RoutePlannerType:
        return self._cls

    @property
    def details(self) -> routeplanner_.RoutePlannerDetails:
        return self._details


class RoutePlannerDetails(routeplanner_.RoutePlannerDetails):
    def __init__(
        self,
        ip_block: routeplanner_.IPBlock,
        failing_addresses: typing.Sequence[routeplanner_.FailingAddress],
        rotate_index: str | None,
        ip_index: str | None,
        current_address: str | None,
        current_address_index: str | None,
        block_index: str | None,
    ) -> None:
        self._ip_block = ip_block
        self._failing_addresses = failing_addresses
        self._rotate_index = rotate_index
        self._ip_index = ip_index
        self._current_address = current_address
        self._current_address_index = current_address_index
        self._block_index = block_index

    @property
    def ip_block(self) -> routeplanner_.IPBlock:
        return self._ip_block

    @property
    def failing_addresses(self) -> typing.Sequence[routeplanner_.FailingAddress]:
        return self._failing_addresses

    @property
    def rotate_index(self) -> str | None:
        return self._rotate_index

    @property
    def ip_index(self) -> str | None:
        return self._ip_index

    @property
    def current_address(self) -> str | None:
        return self._current_address

    @property
    def current_address_index(self) -> str | None:
        return self._current_address_index

    @property
    def block_index(self) -> str | None:
        return self._block_index


class IPBlock(routeplanner_.IPBlock):
    def __init__(self, type: routeplanner_.IPBlockType, size: str) -> None:
        self._type = type
        self._size = size

    @property
    def type(self) -> routeplanner_.IPBlockType:
        return self._type

    @property
    def size(self) -> str:
        return self._size


class FailingAddress(routeplanner_.FailingAddress):
    def __init__(self, address: str, timestamp: datetime.datetime, time: str) -> None:
        self._address = address
        self._timestamp = timestamp
        self._time = time

    @property
    def address(self) -> str:
        return self._address

    @property
    def timestamp(self) -> datetime.datetime:
        return self._timestamp

    @property
    def time(self) -> str:
        return self._time


# MIT License

# Copyright (c) 2023-present MPlatypus

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
