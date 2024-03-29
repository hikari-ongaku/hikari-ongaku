# ruff: noqa: D100, D101, D102
import unittest
from unittest.mock import AsyncMock
from unittest.mock import patch

import hikari

import ongaku

test_bot = hikari.GatewayBot("", banner=None)

test_client = ongaku.Client(test_bot)

test_client.add_server(host="localhost", password="youshallnotpass")


class NewRestSessionTest(unittest.IsolatedAsyncioTestCase):
    @patch("ongaku.rest.RESTClient._handle_rest", new_callable=AsyncMock)
    async def handle_rest(
        self,
        mock_rest: AsyncMock,
    ) -> None:
        print(mock_rest.call_args)
        mock_rest.return_value

    async def test_session_update(self):
        await test_client.rest.session.update("test_session")

        # assert result == objects.test_track
