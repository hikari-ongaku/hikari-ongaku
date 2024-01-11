from __future__ import annotations

import abc
import attrs
import hikari
import typing as t

__all__ = ("PayloadT", "PayloadBase", "PayloadBaseApp")

PayloadT = t.TypeVar("PayloadT", list[t.Any], dict[str, t.Any])


class Payload(abc.ABC, t.Generic[PayloadT]):
    """
    Main payload

    The main payload, that all payload types are inherited from.
    """


class PayloadBase(Payload[PayloadT], abc.ABC):
    """
    Payload Base

    The payload base, that allows for converting back into payloads to transfer.
    """

    @classmethod
    def from_payload(cls, payload: PayloadT) -> PayloadBase[PayloadT]:
        ...

    @property
    def to_payload(self) -> dict[str, t.Any]:
        new_data: dict[str, t.Any] = {}
        for key, value in attrs.asdict(self).items():
            if key.count("_") > 0:
                split = key.split("_")
                new_name_list: list[str] = []
                for x in range(len(split)):
                    if x == 0:
                        new_name_list.append(split[x])
                    else:
                        new_name_list.append(split[x].capitalize())

                key = "".join(new_name_list)

            new_data.update({key: value})

        return new_data


class PayloadBaseApp(Payload[PayloadT], abc.ABC):
    """
    Payload base app

    The payload base, that supports an application/bot.

    !!! WARNING
        This cannot be converted into a dict.
    """

    @classmethod
    def from_payload(
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
