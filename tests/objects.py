from hikari import GatewayBot

from ongaku.client import Client
from ongaku.rest import RESTClient

test_gateway_bot = GatewayBot("...", banner=None, logs="CRITICAL")

test_ongaku_client = Client(test_gateway_bot)

test_ongaku_client.add_server()

test_rest_client = RESTClient(test_ongaku_client)
