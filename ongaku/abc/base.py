"""Payload bases.

All of the payload base related objects.
"""

from __future__ import annotations

import abc
import typing as t

import pydantic
import hikari

__all__ = ("PayloadBase", "PayloadBaseApp")

if t.TYPE_CHECKING:
    BaseT = t.Mapping[str, t.Any] | t.Sequence[t.Any]

# FIXME: handle hikari.Snowflake type somehow.

class Payload(abc.ABC, pydantic.BaseModel):
    """
    Main payload.

    The main payload, that all payload types are inherited from.
    """



class PayloadBase(Payload, abc.ABC):
    """
    Payload base.

    The payload base, that allows for converting back into payloads to transfer.
    """

    @classmethod
    def _from_payload(cls, payload: BaseT):
        """From payload.

        Converts the payload, into the current object.

        Raises
        ------
        TypeError
            When the type the value wanted, is incorrect.
        ValueError
            When the value is none.
        """
        return cls.model_validate(payload, strict=True)

    @property
    def _to_payload(self) -> BaseT:
        """To payload.

        Converts your object, to a payload.
        """
        return self.model_dump_json(by_alias=True)


class PayloadBaseApp(Payload, abc.ABC):
    """
    Payload base application.

    The payload base, that supports an application/bot.
    """

    model_config = pydantic.ConfigDict(ignored_types=(hikari.RESTAware,))

    _app: hikari.RESTAware

    @property
    def app(self) -> hikari.RESTAware:
        """The application the event is attached too."""
        return self._app

    @classmethod
    def _from_payload(cls, payload: BaseT, app: hikari.RESTAware):
        """From payload.

        Converts the payload, into the current object.

        Raises
        ------
        TypeError
            When the type the value wanted, is incorrect.
        ValueError
            When the value is none.
        """
        cls._app = app
        return cls.model_validate(payload, strict=True)

    @property
    def _to_payload(self) -> BaseT:
        """To payload.

        Converts your object, to a payload.
        """
        return self.model_dump(by_alias=True)


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
