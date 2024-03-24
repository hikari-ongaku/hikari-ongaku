"""
Endpoints.

In this file, is an easy way to manage all available endpoints, and to make sure they are overridden, and handled properly.

!!! note
    Any data that is within curly brackets {} will basically become a catch-all method, meaning it doesn't matter what data is there, it will accept anything (ONLY FOR TESTING.)
"""

from __future__ import annotations

import enum
import typing as t

import attrs

from tests import payload
from ongaku.abc import Track


class _HttpMethod(enum.Enum):
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    DELETE = "DELETE"


@attrs.define
class PayloadInformation:  # noqa: D101
    path: str
    """The path to the information."""
    method: str
    """Method type: GET, POST, PATCH, DELETE"""
    return_data: t.Any | t.Sequence[t.Any]
    """The data that will be returned."""
    version: bool
    """Whether or not authentication is needed for the endpoint."""
    headers: t.Annotated[dict[str, t.Any] | None, attrs.field(kw_only=True)] = None
    """The headers (none if not needed) thats sent to the server."""
    json: t.Annotated[
        dict[str, t.Any] | list[t.Any] | None, attrs.field(kw_only=True)
    ] = None
    """The json data (none if not needed) thats sent to the server."""
    params: t.Annotated[dict[str, t.Any] | None, attrs.field(kw_only=True)] = None
    """The parameters (none if not needed) thats sent to the server."""

    @classmethod
    def build(  # noqa: D102
        cls,
        path: str,
        method: _HttpMethod,
        return_data: t.Any | t.Sequence[t.Any],
        version: bool,
        authentication: bool,
        *,
        headers: dict[str, t.Any] | None = {},
        params: dict[str, t.Any] | None = {},
        json: dict[str, t.Any] | list[t.Any] | None = {},
    ) -> PayloadInformation:
        if authentication:
            headers = {}
            headers.update({"Authorization": TEST_PASSWORD})

        return PayloadInformation(
            path, method.value, return_data, version, headers, json, params
        )


# The version to use for all tests.
TEST_VERSION = "/v4"

TEST_PASSWORD = "password"

"""WEBSOCKET = PayloadInformation.build( # Websocket does not have a method as its using ws_connect.
    "/websocket",
    _HttpMethod,
    True,
    True,
    headers={
        "User-Id":"{user_id}",
        "Client-Name":"{client_name}"
    }
)"""  # TODO: Deal with ws later.

"""LOAD_TRACKS = PayloadInformation.build( # The only special version of this.
    "/loadtracks",
    _HttpMethod.GET,
    
    True,
    True,
    params={"identifier":"{load_track}"}
)"""

DECODE_TRACK = PayloadInformation.build(
    "/decodetrack",
    _HttpMethod.GET,
    Track._from_payload(payload.convert(payload.TRACK)),
    True,
    True,
    params={"encodedTrack": "{BASE64}"},
)

DECODE_TRACKS = PayloadInformation.build(
    "/decodetracks",
    _HttpMethod.POST,
    [Track._from_payload(payload.convert(payload.TRACK))],
    True,
    True,
    json=["{encoded_track}"],
)

GET_PLAYERS = "/sessions/{session_id}/players"

GET_PLAYER = "/sessions/{session_id}/players/{guild_id}"

UPDATE_PLAYER = "/sessions/{session_id}/players/{guild_id}"

DELETE_PLAYER = "/sessions/{session_id}/players/{guild_id}"

UPDATE_SESSION = "/sessions/{sessionId}"

GET_INFO = "/info"

GET_VERSION = "/version"

GET_STATS = "/stats"

GET_ROUTEPLANNER_STATUS = "/routeplanner/status"

FREE_ROUTEPLANNER_ADDRESS = "/routeplanner/free/address"

FREE_ALL_ROUTEPLANNER_ADDRESSES = "/routeplanner/free/all"

ENDPOINTS: t.Sequence[PayloadInformation] = [
    DECODE_TRACK,
    DECODE_TRACKS,
]
