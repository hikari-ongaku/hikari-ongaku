# ruff: noqa: D101, D102

from __future__ import annotations

import datetime
import typing

from ongaku.abc import routeplanner as routeplanner_
from ongaku.enums import IPBlockType
from ongaku.enums import RoutePlannerType


class RoutePlannerStatus(routeplanner_.RoutePlannerStatus):
    def __init__(
        self, cls: RoutePlannerType, details: routeplanner_.RoutePlannerDetails
    ) -> None:
        self._cls = cls
        self._details = details

    @property
    def cls(self) -> RoutePlannerType:
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
    def __init__(self, type: IPBlockType, size: str) -> None:
        self._type = type
        self._size = size

    @property
    def type(self) -> IPBlockType:
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
