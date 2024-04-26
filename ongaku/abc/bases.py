"""
Base's ABCs.

The bases for all abstract classes.
"""

from __future__ import annotations

import typing

import hikari
import msgspec

if typing.TYPE_CHECKING:
    from typing_extensions import Self


from ongaku.internal.logger import logger

__all__ = ("PayloadBase",)

_logger = logger.getChild("abc.base")


class PayloadBase(msgspec.Struct):
    """
    Payload base.

    The base class for all lavalink functions.
    """

    @classmethod
    def _from_payload(cls, payload: str | bytes) -> Self:
        return msgspec.json.decode(
            payload, type=cls, strict=False, dec_hook=cls._decode_hook
        )

    @property
    def _to_payload(self) -> str:
        return msgspec.json.encode(self, enc_hook=self._encode_hook).decode()

    @classmethod
    def _decode_hook(cls, type: typing.Type[typing.Any], obj: typing.Any) -> typing.Any:
        if type == hikari.Snowflake:
            return hikari.Snowflake(int(obj))
        raise ValueError("Sorry, but this value does not exist.")

    @classmethod
    def _encode_hook(cls, type: typing.Type[hikari.Snowflake]) -> typing.Any:
        return str(type)


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
