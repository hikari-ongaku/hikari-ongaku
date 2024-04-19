"""
Converters.

All internal converters for pydantic are stored.
"""

from __future__ import annotations

import typing

__all__ = ("JSONObject", "JSONArray", "default_json_dumps", "default_json_loads")

# JSON loading and dumping

JSONObject: typing.TypeAlias = typing.Mapping[str, typing.Any]
"""Type hint for a JSON-decoded object representation as a mapping."""

JSONArray: typing.TypeAlias = typing.Sequence[typing.Any]
"""Type hint for a JSON-decoded array representation as a sequence."""

JSONEncoder: typing.TypeAlias = typing.Callable[[JSONArray | JSONObject], bytes]
"""Type hint for JSON encoders."""

JSONDecoder: typing.TypeAlias = typing.Callable[[str | bytes], JSONArray | JSONObject]
"""Type hint for JSON decoder."""

default_json_dumps: JSONEncoder
"""Default json encoder to use."""

default_json_loads: JSONDecoder
"""Default json decoder to use."""

try:
    import orjson

    default_json_dumps = orjson.dumps
    default_json_loads = orjson.loads

except ModuleNotFoundError:
    import json

    _json_separators = (",", ":")

    def json_dumps(obj: JSONArray | JSONObject) -> bytes:
        """Encode a JSON object to a str."""
        return json.dumps(obj, separators=_json_separators).encode("utf-8")

    default_json_dumps = json_dumps

    default_json_loads = json.loads
