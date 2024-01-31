"""Payload bases.

All of the payload base related objects.
"""

from __future__ import annotations

import abc
import typing as t

import attrs
import hikari

__all__ = ("PayloadT", "PayloadBase", "PayloadBaseApp")

PayloadT = t.TypeVar("PayloadT", t.Sequence[t.Any], t.Mapping[str, t.Any])


class Payload(abc.ABC, t.Generic[PayloadT]):
    """
    Main payload.

    The main payload, that all payload types are inherited from.
    """

def _to_payload(payload: t.Mapping[str, t.Any]) -> dict[str, t.Any]:
    fixed_data: dict[str, t.Any] = {}
    for key, value in payload.items():
        if key.count("_") > 0:
            split = key.split("_")
            new_name_list: list[str] = []
            for x in range(len(split)):
                if x == 0:
                    new_name_list.append(split[x])
                else:
                    new_name_list.append(split[x].capitalize())
            key = "".join(new_name_list)
        
        if isinstance(value, t.Mapping):
            fixed_data.update({key:_to_payload(value)}) #type: ignore
        
        else:
            fixed_data.update({key:value})
    
    return fixed_data

class PayloadBase(Payload[PayloadT], abc.ABC):
    """
    Payload base.

    The payload base, that allows for converting back into payloads to transfer.
    """

    @classmethod
    def _from_payload(cls, payload: PayloadT) -> PayloadBase[PayloadT]:
        """From payload.
        
        Converts the payload, into the current object.

        Raises
        ------
        TypeError
            When the type the value wanted, is incorrect.
        ValueError
            When the value is none.
        """
        ...

    @property
    def to_payload(self) -> dict[str, t.Any]:
        """To payload.
        
        Converts your object, to a payload.
        """
        return _to_payload(attrs.asdict(self))


class PayloadBaseApp(Payload[PayloadT], abc.ABC):
    """
    Payload base application.

    The payload base, that supports an application/bot.

    !!! WARNING
        This cannot be converted into a dict.
    """

    @classmethod
    def _from_payload(
        cls, payload: PayloadT, *, app: hikari.RESTAware
    ) -> PayloadBaseApp[PayloadT]:
        ...


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
