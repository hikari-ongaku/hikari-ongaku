from __future__ import annotations

import attrs
import typing as t
from .base import PayloadBase

from .. import enums

__all__ = (
    "InfoVersion",
    "InfoGit",
    "InfoPlugin",
    "Info",
    "RestError",
    "ExceptionError",
)


@attrs.define
class InfoVersion(PayloadBase[dict[str, t.Any]]):
    """
    All of the Info Version information.

    Find out more [here](https://lavalink.dev/api/rest.html#version-object).

    Parameters
    ----------
    semver : str
        The full version string of this Lavalink server
    major : int
        The major version of this Lavalink server
    minor : int
        The minor version of this Lavalink server
    patch : int
        The patch version of this Lavalink server
    pre_release : str | None
        The pre-release version according to semver as a `.` separated list of identifiers
    build : str | None
        The build metadata according to semver as a `.` separated list of identifiers
    """

    semver: str
    major: int
    minor: int
    patch: int
    pre_release: t.Optional[str]
    build: t.Optional[str]

    @classmethod
    def _from_payload(cls, payload: dict[str, t.Any]) -> InfoVersion:
        semver = payload["semver"]
        major = payload["major"]
        minor = payload["minor"]
        patch = payload["patch"]
        try:
            pre_release = payload["preRelease"]
        except Exception:
            pre_release = None
        try:
            build = payload["build"]
        except Exception:
            build = None

        return cls(semver, major, minor, patch, pre_release, build)


@attrs.define
class InfoGit(PayloadBase[dict[str, t.Any]]):
    """
    All of the Info Git information.

    Find out more [here](https://lavalink.dev/api/rest.html#git-object).

    Parameters
    ----------
    branch : str
        The branch this Lavalink server was built on
    commit : str
        The commit this Lavalink server was built on
    commit_time : int
        The millisecond unix timestamp for when the commit was created
    """

    branch: str
    commit: str
    commit_time: int

    @classmethod
    def _from_payload(cls, payload: dict[str, t.Any]) -> InfoGit:
        """
        Info Git parser

        parse a payload of information, to receive a `InfoGit` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        InfoGit
            The Info Git you parsed.
        """

        branch = payload["branch"]
        commit = payload["commit"]
        commit_time = payload["commitTime"]

        return cls(branch, commit, commit_time)


@attrs.define
class InfoPlugin(PayloadBase[dict[str, t.Any]]):
    """
    All of the Info Plugin information.

    Find out more [here](https://lavalink.dev/api/rest.html#plugin-object).

    Parameters
    ----------
    name : str
        The name of the plugin
    version : int
        The version of the plugin
    """

    name: str
    version: str

    @classmethod
    def _from_payload(cls, payload: dict[str, t.Any]) -> InfoPlugin:
        """
        Info Plugin parser

        parse a payload of information, to receive a `InfoPlugin` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        InfoPlugin
            The Info Plugin you parsed.
        """

        name = payload["name"]
        version = payload["version"]

        return cls(name, version)


@attrs.define
class Info(PayloadBase[dict[str, t.Any]]):
    """
    All of the Info Version information.

    Find out more [here](https://lavalink.dev/api/rest.html#version-object).

    Parameters
    ----------
    version : InfoVersion
        The version of this Lavalink server
    build_time : int
        The millisecond unix timestamp when this Lavalink jar was built
    git : InfoGit
        The git information of this Lavalink server
    jvm : str
        The JVM version this Lavalink server runs on
    lavaplayer : str
        The Lavaplayer version being used by this server
    source_managers : list[str]
        The enabled source managers for this server
    filters : list[str]
        The enabled filters for this server
    plugins : list[InfoPlugin]
        The enabled plugins for this server
    """

    version: InfoVersion
    build_time: int
    git: InfoGit
    jvm: str
    lavaplayer: str
    source_managers: list[str]
    filters: list[str]
    plugins: list[InfoPlugin]

    @classmethod
    def _from_payload(cls, payload: dict[str, t.Any]):
        version = InfoVersion._from_payload(payload["version"])
        build_time = payload["buildTime"]
        git = InfoGit._from_payload(payload["git"])
        jvm = payload["jvm"]
        lavaplayer = payload["lavaplayer"]

        source_managers = payload["sourceManagers"]
        filters = payload["filters"]
        plugins: list[InfoPlugin] = []

        payload_plugins = payload["plugins"]

        for plugin in payload_plugins:
            try:
                new_plugin = InfoPlugin._from_payload(plugin)
            except Exception as e:
                raise e

            plugins.append(new_plugin)

        return cls(
            version, build_time, git, jvm, lavaplayer, source_managers, filters, plugins
        )


@attrs.define
class RestError(PayloadBase[dict[str, t.Any]]):
    """
    All of the Rest Error information.

    This is the error that is formed, when a call to a rest method fails.
    Find out more [here](https://lavalink.dev/api/rest.html#error-responses).

    Parameters
    ----------
    timestamp : int
        The timestamp of the error in milliseconds since the Unix epoch
    status : int
        The HTTP status code
    error : str
        The HTTP status code message
    trace : str | None
        The stack trace of the error.
    message : str
        The error message
    path : str
        The request path
    """

    timestamp: int
    status: int
    error: str
    trace: t.Optional[str]
    message: str
    path: str

    @classmethod
    def _from_payload(cls, payload: dict[str, t.Any]) -> RestError:
        """
        Rest Error parser

        parse a payload of information, to receive a `RestError` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        Error
            The Error you parsed.
        """

        timestamp = payload["timestamp"]
        status = payload["status"]
        error = payload["error"]
        try:
            trace = payload["trace"]
        except Exception:
            trace = None
        message = payload["message"]
        path = payload["path"]

        return cls(timestamp, status, error, trace, message, path)


@attrs.define
class ExceptionError(PayloadBase[dict[str, t.Any]]):
    """
    All of the Exception Error information.

    Find out more [here](https://lavalink.dev/api/websocket.html#exception-object).

    Parameters
    ----------
    message : str
        The message of the exception
    severity : enums.LavalinkSeverityType
        The severity of the exception
    cause : str
        The cause of the exception

    """

    message: str
    severity: enums.SeverityType
    cause: str

    @classmethod
    def _from_payload(cls, payload: dict[str, t.Any]) -> ExceptionError:
        """
        Exception Error parser

        parse a payload of information, to receive a `ExceptionError` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        ExceptionError
            The Error you parsed.
        """

        message = payload["message"]
        severity = payload["severity"]
        cause = payload["cause"]

        return cls(message, severity, cause)


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
