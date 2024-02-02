"""Lavalink ABC.

All of the information about the lavalink connection.
"""

from __future__ import annotations

import typing as t
import pydantic

from .. import enums
from .base import PayloadBase

__all__ = (
    "InfoVersion",
    "InfoGit",
    "InfoPlugin",
    "Info",
    "RestError",
    "ExceptionError",
)



class InfoVersion(PayloadBase):
    """Version information.

    All information, about the version of lavalink that is running.
    Find out more [here](https://lavalink.dev/api/rest.html#version-object).
    """

    semver: str
    """The full version string of this Lavalink server."""
    major: int
    """The major version of this Lavalink server."""
    minor: int
    """The minor version of this Lavalink server"""
    patch: int
    """The patch version of this Lavalink server"""
    pre_release:  t.Annotated[str, pydantic.Field(alias="preRelease")]
    """The pre-release version according to semver as a `.` separated list of identifiers"""
    build: t.Annotated[str | None, pydantic.Field(default=None)]
    """The build metadata according to semver as a `.` separated list of identifiers"""


class InfoGit(PayloadBase):
    """Git information.

    All of the information about the lavalink git information.
    Find out more [here](https://lavalink.dev/api/rest.html#git-object).
    """

    branch: str
    """The branch this Lavalink server was built on."""
    commit: str
    """The commit this Lavalink server was built on."""
    commit_time: t.Annotated[int, pydantic.Field(alias="commitTime")]
    """The millisecond unix timestamp for when the commit was created."""


class InfoPlugin(PayloadBase):
    """Plugin information.

    All of the Information about the currently loaded plugins.
    Find out more [here](https://lavalink.dev/api/rest.html#plugin-object).
    """

    name: str
    """The name of the plugin."""
    version: str
    """The version of the plugin."""


class Info(PayloadBase):
    """
    All of the Info Version information.

    Find out more [here](https://lavalink.dev/api/rest.html#info-response).
    """

    version: InfoVersion
    """The version of this Lavalink server."""
    build_time: int
    """The millisecond unix timestamp when this Lavalink jar was built."""
    git: InfoGit
    """The git information of this Lavalink server."""
    jvm: str
    """The JVM version this Lavalink server runs on."""
    lavaplayer: str
    """The Lavaplayer version being used by this server."""
    source_managers:  t.Annotated[t.Sequence[str], pydantic.Field(alias="sourceManagers")]
    """The enabled source managers for this server."""
    filters: t.Sequence[str]
    """The enabled filters for this server."""
    plugins: t.Sequence[InfoPlugin]
    """The enabled plugins for this server."""


class RestError(PayloadBase):
    """Rest error information.

    This is the error that is formed, when a call to a rest method fails.
    Find out more [here](https://lavalink.dev/api/rest.html#error-responses).
    """

    timestamp: int
    """The timestamp of the error in milliseconds since the Unix epoch."""
    status: int
    """The HTTP status code."""
    error: str
    """The HTTP status code message."""
    trace: t.Annotated[str | None, pydantic.Field(default=None)]
    """The stack trace of the error."""
    message: str
    """The error message."""
    path: str
    """The request path."""



class ExceptionError(PayloadBase):
    """Exception error.

    The exception error lavalink returns when a track has an exception.
    """

    message: str
    """The message of the exception."""
    severity: enums.SeverityType
    """The severity of the exception."""
    cause: str
    """The cause of the exception."""



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
