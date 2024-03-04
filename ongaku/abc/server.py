"""Server.

All server relation functions and classes.
"""

from __future__ import annotations

import typing as t

import attrs

from ..enums import ConnectionType
from ..enums import VersionType

__all__ = ("Server",)


@attrs.define
class Server:
    """Server.

    A server object.
    """

    ssl: t.Final[bool]
    host: t.Final[str]
    port: t.Final[int]
    password: t.Final[str] | None
    version: t.Final[VersionType]
    remaining_attempts: int

    base_uri: t.Final[str]
    default_headers: dict[str, t.Any]
    status: ConnectionType = ConnectionType.NOT_CONNECTED

    @classmethod
    def build(
        cls,
        ssl: bool,
        host: str,
        port: int,
        password: str | None,
        version: VersionType,
        attempts: int,
    ) -> Server:
        """Build Server.

        Build a new server object.
        """
        return Server(
            ssl,
            host,
            port,
            password,
            version,
            attempts,
            f"http{'s' if ssl else ''}://{host}:{port}",
            {"Authorization": password} if password else {},
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
