from __future__ import annotations

import abc
import attrs
import hikari
import typing as t

class Payload(abc.ABC): # the base payload?
    pass

class PayloadBase(Payload, abc.ABC):

    @classmethod
    def from_payload(cls, payload: dict[str, t.Any]) -> PayloadBase:
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

class PayloadBaseApp(Payload, abc.ABC):

    @classmethod
    def from_payload(cls, payload: dict[str, t.Any], *, app: hikari.RESTAware) -> PayloadBaseApp:
        ...
