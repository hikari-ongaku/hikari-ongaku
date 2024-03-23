from hikari import GatewayBot

from ongaku.abc import Track, TrackInfo
from ongaku.client import Client
from ongaku.rest import RESTClient

from tests import payload

test_gateway_bot = GatewayBot("...", banner=None, logs="CRITICAL")

test_ongaku_client = Client(test_gateway_bot)

test_ongaku_client.add_server()

test_rest_client = RESTClient(test_ongaku_client)


test_track = Track._from_payload(payload.convert(payload.TRACK))
test_track_info = TrackInfo._from_payload(payload.convert(payload.TRACK_INFO))
