# ruff: noqa: D100

from hikari import GatewayBot

from ongaku.client import Client
from ongaku.enums import VersionType
from ongaku.rest import RESTClient
from ongaku.session import Session

test_gateway_bot = GatewayBot("...", banner=None, logs="CRITICAL")

test_ongaku_client = Client(test_gateway_bot)

test_ongaku_client.add_server(host="127.0.0.1", password="youshallnotpass")

test_rest_client = RESTClient(test_ongaku_client)

test_session = Session(
    test_ongaku_client, False, "127.0.0.1", 2333, "youshallnotpass", VersionType.V4, 3
)
