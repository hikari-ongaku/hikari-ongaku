# ruff: noqa: D100, D101, D102

import unittest

from ongaku.abc.route_planner import FailingAddress
from ongaku.abc.route_planner import IPBlock
from ongaku.abc.route_planner import RoutePlannerDetails
from ongaku.abc.route_planner import RoutePlannerStatus
from ongaku.enums import IPBlockType
from ongaku.enums import RoutePlannerType
from tests import payload


class TestIPBlock(unittest.TestCase):
    def test_base(self):
        ip_block = IPBlock(type=IPBlockType.INET_6_ADDRESS, size="test_size")

        assert ip_block.type == IPBlockType.INET_6_ADDRESS
        assert ip_block.size == "test_size"

    def test_from_payload(self):
        ip_block = IPBlock._from_payload(payload.convert(payload.ROUTEPLANNER_IP_BLOCK))

        assert ip_block.type == IPBlockType.INET_6_ADDRESS
        assert ip_block.size == "test_size"

    def test_to_payload(self):
        ip_block = IPBlock._from_payload(payload.convert(payload.ROUTEPLANNER_IP_BLOCK))

        assert ip_block._to_payload == payload.ROUTEPLANNER_IP_BLOCK


class TestFailingAddress(unittest.TestCase):
    def test_base(self):
        failing_address = FailingAddress(
            failing_address="test_failing_address",
            failing_timestamp=1,
            failing_time="test_failing_time",
        )

        assert failing_address.failing_address == "test_failing_address"
        assert failing_address.failing_timestamp == 1
        assert failing_address.failing_time == "test_failing_time"

    def test_from_payload(self):
        failing_address = FailingAddress._from_payload(
            payload.convert(payload.ROUTEPLANNER_FAILING_ADDRESS)
        )

        assert failing_address.failing_address == "test_failing_address"
        assert failing_address.failing_timestamp == 1
        assert failing_address.failing_time == "test_failing_time"

    def test_to_payload(self):
        failing_address = FailingAddress._from_payload(
            payload.convert(payload.ROUTEPLANNER_FAILING_ADDRESS)
        )

        assert failing_address._to_payload == payload.ROUTEPLANNER_FAILING_ADDRESS


class TestDetails(unittest.TestCase):
    def test_base(self):
        ip_block = IPBlock._from_payload(payload.convert(payload.ROUTEPLANNER_IP_BLOCK))
        failing_address = FailingAddress._from_payload(
            payload.convert(payload.ROUTEPLANNER_FAILING_ADDRESS)
        )
        details = RoutePlannerDetails(
            ip_block=ip_block,
            failing_addresses=[failing_address],
            rotate_index="test_rotate_index",
            ip_index="test_ip_index",
            current_address="test_current_address",
            current_address_index="test_current_address_index",
            block_index="test_block_index",
        )

        assert details.ip_block == ip_block
        assert details.failing_addresses == [failing_address]
        assert details.rotate_index == "test_rotate_index"
        assert details.ip_index == "test_ip_index"
        assert details.current_address == "test_current_address"
        assert details.current_address_index == "test_current_address_index"
        assert details.block_index == "test_block_index"

    def test_from_payload(self):
        ip_block = IPBlock._from_payload(payload.convert(payload.ROUTEPLANNER_IP_BLOCK))
        failing_address = FailingAddress._from_payload(
            payload.convert(payload.ROUTEPLANNER_FAILING_ADDRESS)
        )
        details = RoutePlannerDetails._from_payload(
            payload.convert(payload.ROUTEPLANNER_DETAILS)
        )

        assert details.ip_block == ip_block
        assert details.failing_addresses == [failing_address]
        assert details.rotate_index == "test_rotate_index"
        assert details.ip_index == "test_ip_index"
        assert details.current_address == "test_current_address"
        assert details.current_address_index == "test_current_address_index"
        assert details.block_index == "test_block_index"

    def test_to_payload(self):
        details = RoutePlannerDetails._from_payload(
            payload.convert(payload.ROUTEPLANNER_DETAILS)
        )

        assert details._to_payload == payload.ROUTEPLANNER_DETAILS


class TestStatus(unittest.TestCase):
    def test_base(self):
        details = RoutePlannerDetails._from_payload(
            payload.convert(payload.ROUTEPLANNER_DETAILS)
        )
        status = RoutePlannerStatus(
            class_type=RoutePlannerType.ROTATING_NANO_IP_ROUTE_PLANNER,
            details=details,
        )

        assert status.class_type == RoutePlannerType.ROTATING_NANO_IP_ROUTE_PLANNER
        assert status.details == details

    def test_from_payload(self):
        details = RoutePlannerDetails._from_payload(
            payload.convert(payload.ROUTEPLANNER_DETAILS)
        )
        status = RoutePlannerStatus._from_payload(
            payload.convert(payload.REST_ROUTEPLANNER_STATUS)
        )

        assert status.class_type == RoutePlannerType.ROTATING_NANO_IP_ROUTE_PLANNER
        assert status.details == details

    def test_to_payload(self):
        status = RoutePlannerStatus._from_payload(
            payload.convert(payload.REST_ROUTEPLANNER_STATUS)
        )
        assert status._to_payload == payload.REST_ROUTEPLANNER_STATUS
