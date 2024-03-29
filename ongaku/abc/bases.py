"""
Base's ABCs.

The bases for all abstract classes.
"""

from __future__ import annotations

import typing

import hikari
import pydantic

if typing.TYPE_CHECKING:
    from ongaku.abc.track import Track
    from ongaku.client import Client
    from ongaku.internal.types import GuildIdT
    from ongaku.session import Session

from ongaku.internal import TRACE_LEVEL
from ongaku.internal import logger

__all__ = (
    "_string_to_snowflake",
    "_snowflake_to_string",
    "PayloadBase",
    "OngakuEvent",
    "PayloadBaseApp",
)

_logger = logger.getChild("abc.base")


def _string_to_snowflake(
    guild_id: str,
    handler: pydantic.ValidatorFunctionWrapHandler,
    info: pydantic.ValidationInfo,
) -> hikari.Snowflake:
    try:
        return hikari.Snowflake(int(guild_id))
    except:
        raise


def _snowflake_to_string(
    guild_id: hikari.Snowflake,
    handler: pydantic.SerializerFunctionWrapHandler,
    info: pydantic.SerializationInfo,
) -> str:
    return str(guild_id)


class PayloadBase(pydantic.BaseModel):
    """
    Payload base.

    The payload base, that allows for converting back into payloads to transfer.
    """

    model_config = pydantic.ConfigDict(
        arbitrary_types_allowed=True, populate_by_name=True
    )

    @classmethod
    def _from_payload(cls, payload: str) -> typing.Self:
        """
        From payload.

        Converts the payload, into the current objectyping.

        Raises
        ------
        ValueError
            Raised when it is not valid data.
        """
        name = cls.__qualname__

        _logger.log(TRACE_LEVEL, f"Validating payload: {payload} to {name}")

        cls = cls.model_validate_json(payload, strict=True)

        _logger.log(
            TRACE_LEVEL,
            f"Payload validation to {name} completed successfully.",
        )

        return cls

    @property
    def _to_payload(self) -> typing.Mapping[str, typing.Any]:
        """
        To payload.

        Converts your object, to a payload.
        """
        return self.model_dump(by_alias=True, mode="json")


class OngakuEvent(hikari.Event):
    """
    Ongaku Eventyping.

    The base event, that all other Ongaku events are attached too.
    """


class PayloadBaseApp(PayloadBase, OngakuEvent):
    """
    Payload base application.

    The payload base, that supports an application/botyping.
    """

    _client: Client
    _session: Session
    _app: hikari.RESTAware

    @property
    def client(self) -> Client:
        """The client that this event is attached too."""
        return self._client

    @client.setter
    def _set_client(self, client: Client):
        self._client = client

    @property
    def session(self) -> Session:
        """The session that this event is attached too."""
        return self._session

    @session.setter
    def _set_session(self, session: Session):
        self._session = session

    @property
    def app(self) -> hikari.RESTAware:
        """The application the event is attached too."""
        return self._app

    @app.setter
    def _set_app(self, value: hikari.RESTAware):
        self._app = value

    @classmethod
    def _build(
        cls, payload: str, session: Session, app: hikari.RESTAware
    ) -> typing.Self:
        """
        Build.

        Build this PayloadBaseApp.
        """
        cls = cls._from_payload(payload)

        cls._set_client = session.client
        cls._set_session = session
        cls._set_app = app

        return cls


class TrackBase(PayloadBaseApp):
    """
    Base track class.

    The class that all Track based events, inherit.
    """

    guild_id: GuildIdT
    """The guild the track is playing in."""
    track: Track
    """The track that the event is attached too."""


class PlayerBase(PayloadBaseApp):
    """
    Player base.

    This is the base player object for all Ongaku player events.

    !!! note
        All player based events, are ongaku related. Not lavalink related.
    """

    guild_id: GuildIdT
    """The guild id of the player."""


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
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENtyping. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
