"""
Routes.

All the routes for lavalink.
"""

from __future__ import annotations

import typing

GET: typing.Final[str] = "GET"
POST: typing.Final[str] = "POST"
PATCH: typing.Final[str] = "PATCH"
DELETE: typing.Final[str] = "DELETE"


class Route:
    """
    Route.

    The route object that has mostly been built.
    """

    def __init__(self, built_path: str, route: BaseRoute) -> None:
        self._built_path = built_path
        self._route = route

    @property
    def path(self) -> str:
        """The path with all variables set."""
        return self._built_path

    @property
    def route(self) -> BaseRoute:
        """The original route made."""
        return self._route

    def build_url(self, uri: str) -> str:
        """Build the full url."""
        return uri + self.path

    def __str__(self) -> str:
        """."""
        return f"{self.route.method} {self.route.path}"


class BaseRoute:
    """
    The base route.

    No arguments have been added to the path.
    """

    def __init__(self, method: str, path: str, *, include_version: bool = True) -> None:
        self._method = method
        self._path = path
        self._include_version = include_version

    @property
    def method(self) -> str:
        """The method of this request."""
        return self._method

    @property
    def path(self) -> str:
        """The path for this method."""
        return self._path

    @property
    def include_version(self) -> bool:
        """Whether or not to include the version in the request."""
        return self._include_version

    def build(self, args: typing.Mapping[str, typing.Any] | None = None) -> Route:
        """Build the route object from the route."""
        if args:
            return Route(
                f"/{'v4' if self.include_version else ''}{self.path.format_map(args)}",
                self,
            )

        return Route(f"/{'v4' if self.include_version else ''}{self.path}", self)

    def __str__(self) -> str:
        """."""
        return f"{self._method} {self._path}"


# Info

GET_INFO: typing.Final[BaseRoute] = BaseRoute(GET, "/info")

GET_VERSION: typing.Final[BaseRoute] = BaseRoute(GET, "/version", include_version=False)

GET_STATISTICS: typing.Final[BaseRoute] = BaseRoute(GET, "/stats")

# Session

PATCH_SESSION_UPDATE: typing.Final[BaseRoute] = BaseRoute(
    PATCH, "/sessions/{session_id}"
)

# Player

GET_PLAYERS: typing.Final[BaseRoute] = BaseRoute(GET, "/sessions/{session_id}/players")

GET_PLAYER: typing.Final[BaseRoute] = BaseRoute(
    GET, "/sessions/{session_id}/players/{guild_id}"
)

PATCH_PLAYER_UPDATE: typing.Final[BaseRoute] = BaseRoute(
    PATCH, "/sessions/{session_id}/players/{guild_id}"
)

DELETE_PLAYER: typing.Final[BaseRoute] = BaseRoute(
    DELETE, "/sessions/{session_id}/players/{guild_id}"
)

# Tracks

GET_LOAD_TRACKS: typing.Final[BaseRoute] = BaseRoute(GET, "/loadtracks")

GET_DECODE_TRACK: typing.Final[BaseRoute] = BaseRoute(GET, "/decodetrack")

GET_DECODE_TRACKS: typing.Final[BaseRoute] = BaseRoute(GET, "/decodetracks")

# Route Planner

GET_ROUTEPLANNER_STATUS: typing.Final[BaseRoute] = BaseRoute(
    GET, "/routeplanner/status"
)

POST_ROUTEPLANNER_FREE_ADDRESS: typing.Final[BaseRoute] = BaseRoute(
    POST, "/routeplanner/free/address"
)

POST_ROUTEPLANNER_FREE_ALL: typing.Final[BaseRoute] = BaseRoute(
    POST, "/routeplanner/free/all"
)

# MIT License

# Copyright (c) 2023 MPlatypus

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
