"""
Converters.

All internal converters.
"""

from __future__ import annotations

import typing

__all__ = ("json_dumps", "json_loads")

json_dumps: typing.Callable[
    [typing.Sequence[typing.Any] | typing.Mapping[str, typing.Any]], bytes
]

json_loads: typing.Callable[
    [str | bytes], typing.Sequence[typing.Any] | typing.Mapping[str, typing.Any]
]

try:
    import orjson

    json_dumps = orjson.dumps
    json_loads = orjson.loads

except ModuleNotFoundError:
    import json

    def basic_json_dumps(
        obj: typing.Sequence[typing.Any] | typing.Mapping[str, typing.Any],
    ) -> bytes:
        """Encode a JSON object to a str."""
        return json.dumps(obj).encode("utf-8")

    json_dumps = basic_json_dumps

    json_loads = json.loads

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
