from __future__ import annotations

import attrs
import typing as t
from .base import PayloadBase

__all__ = ("Session",)


@attrs.define
class Session(PayloadBase[dict[str, t.Any]]):
    """
    Session

    All of the Session information.

    Find out more [here](https://lavalink.dev/api/rest.html#update-session).

    Parameters
    ----------
    resuming : bool
        Whether resuming is enabled for this session or not
    timeout : int
        The timeout in seconds (default is 60s)
    """

    resuming: bool
    timeout: int

    @classmethod
    def _from_payload(cls, payload: dict[str, t.Any]) -> Session:
        resuming = payload["resuming"]
        timeout = payload["timeout"]

        return cls(resuming, timeout)


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
