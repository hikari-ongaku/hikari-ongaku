"""Lavalink ABC.

All of the information about the lavalink connection.
"""

from __future__ import annotations

import typing as t

import attrs

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


@attrs.define
class InfoVersion(PayloadBase[dict[str, t.Any]]):
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
    pre_release: t.Optional[str]
    """The pre-release version according to semver as a `.` separated list of identifiers"""
    build: t.Optional[str]
    """The build metadata according to semver as a `.` separated list of identifiers"""

    @classmethod
    def _from_payload(cls, payload: t.Mapping[str, t.Any]) -> InfoVersion:
        semver = payload.get("semver")
        if semver is None:
            raise ValueError("semver cannot be none.")
        if not isinstance(semver, str):
            raise TypeError("semver must be a string.")

        major = payload.get("major")
        if major is None:
            raise ValueError("major cannot be none.")
        if not isinstance(major, int):
            raise TypeError("major must be a integer.")

        minor = payload.get("minor")
        if minor is None:
            raise ValueError("minor cannot be none.")
        if not isinstance(minor, int):
            raise TypeError("minor must be a integer.")

        patch = payload.get("patch")
        if patch is None:
            raise ValueError("patch cannot be none.")
        if not isinstance(patch, int):
            raise TypeError("patch must be a integer.")

        pre_release = payload.get("preRelease")
        if pre_release is not None:
            if not isinstance(pre_release, str):
                raise TypeError("preRelease must be a string.")
        
        build = payload.get("build")
        if build is not None:
            if not isinstance(build, str):
                raise TypeError("build must be a string.")


        return cls(semver, major, minor, patch, pre_release, build)


@attrs.define
class InfoGit(PayloadBase[t.Mapping[str, t.Any]]):
    """Git information.

    All of the information about the lavalink git information.
    Find out more [here](https://lavalink.dev/api/rest.html#git-object).
    """

    branch: str
    """The branch this Lavalink server was built on."""
    commit: str
    """The commit this Lavalink server was built on."""
    commit_time: int
    """The millisecond unix timestamp for when the commit was created."""

    @classmethod
    def _from_payload(cls, payload: t.Mapping[str, t.Any]) -> InfoGit:
        branch = payload.get("branch")
        if branch is None:
            raise ValueError("branch cannot be none.")
        if not isinstance(branch, str):
            raise TypeError("branch must be a string.")
        
        commit = payload.get("commit")
        if commit is None:
            raise ValueError("commit cannot be none.")
        if not isinstance(commit, str):
            raise TypeError("commit must be a string.")
        
        commit_time = payload.get("commitTime")
        if commit_time is None:
            raise ValueError("commitTime cannot be none.")
        if not isinstance(commit_time, int):
            raise TypeError("commitTime must be a integer.")
        
        return cls(
            branch, 
            commit, 
            commit_time
        )


@attrs.define
class InfoPlugin(PayloadBase[t.Mapping[str, t.Any]]):
    """Plugin information.

    All of the Information about the currently loaded plugins.
    Find out more [here](https://lavalink.dev/api/rest.html#plugin-object).
    """

    name: str
    """The name of the plugin."""
    version: str
    """The version of the plugin."""

    @classmethod
    def _from_payload(cls, payload: t.Mapping[str, t.Any]) -> InfoPlugin:
        name = payload.get("name")
        if name is None:
            raise ValueError("name cannot be none.")
        if not isinstance(name, str):
            raise TypeError("name must be a string.")
        
        version = payload.get("version")
        if version is None:
            raise ValueError("version cannot be none.")
        if not isinstance(version, str):
            raise TypeError("version must be a string.")

        return cls(
            name, 
            version,
        )


@attrs.define
class Info(PayloadBase[dict[str, t.Any]]):
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
    source_managers: t.Sequence[str]
    """The enabled source managers for this server."""
    filters: t.Sequence[str]
    """The enabled filters for this server."""
    plugins: t.Sequence[InfoPlugin]
    """The enabled plugins for this server."""

    @classmethod
    def _from_payload(cls, payload: t.Mapping[str, t.Any]):
        version = payload.get("version")
        if version is None:
            raise ValueError("version cannot be none.")
        try:
            version = InfoVersion._from_payload(version)
        except TypeError:
            raise
        except ValueError:
            raise

        build_time = payload.get("buildTime")
        if build_time is None:
            raise ValueError("buildTime cannot be none.")
        if not isinstance(build_time, int):
            raise TypeError("buildTime must be a integer.")

        git = payload.get("git")
        if git is None:
            raise ValueError("git cannot be none.")
        try:
            git = InfoGit._from_payload(git)
        except TypeError:
            raise
        except ValueError:
            raise

        jvm = payload.get("jvm")
        if jvm is None:
            raise ValueError("jvm cannot be none.")
        if not isinstance(jvm, str):
            raise TypeError("jvm must be a string.")

        lavaplayer = payload.get("lavaplayer")
        if lavaplayer is None:
            raise ValueError("lavaplayer cannot be none.")
        if not isinstance(lavaplayer, str):
            raise TypeError("lavaplayer must be a string.")

        #FIXME: This needs to be changed to the new method.
        source_managers = payload.get("sourceManagers", [])
        filters = payload.get("filters", [])

        plugins: list[InfoPlugin] = []
        for plugin in payload.get("plugins", []):
            try:
                new_plugin = InfoPlugin._from_payload(plugin)
            except TypeError:
                raise
            except ValueError:
                raise

            plugins.append(new_plugin)

        return cls(
            version, 
            build_time, 
            git, 
            jvm, 
            lavaplayer, 
            source_managers, 
            filters, 
            plugins,
        )


@attrs.define
class RestError(PayloadBase[t.Mapping[str, t.Any]]):
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
    trace: str | None
    """The stack trace of the error."""
    message: str
    """The error message."""
    path: str
    """The request path."""

    @classmethod
    def _from_payload(cls, payload: t.Mapping[str, t.Any]) -> RestError:
        timestamp = payload.get("timestamp")
        if timestamp is None:
            raise ValueError("timestamp cannot be none.")
        if not isinstance(timestamp, int):
            raise TypeError("timestamp must be a integer.")

        status = payload.get("status")
        if status is None:
            raise ValueError("status cannot be none.")
        if not isinstance(status, int):
            raise TypeError("status must be a integer.")

        error = payload.get("error")
        if error is None:
            raise ValueError("error cannot be none.")
        if not isinstance(error, str):
            raise TypeError("error must be a string.")

        trace = payload.get("trace")
        if trace is not None:
            if not isinstance(trace, str):
                raise TypeError("trace must be a string.")

        message = payload.get("message")
        if message is None:
            raise ValueError("message cannot be none.")
        if not isinstance(message, str):
            raise TypeError("message must be a string.")

        path = payload.get("path")
        if path is None:
            raise ValueError("path cannot be none.")
        if not isinstance(path, str):
            raise TypeError("path must be a string.")

        return cls(
            timestamp, 
            status, 
            error, 
            trace, 
            message, 
            path
        )


@attrs.define
class ExceptionError(PayloadBase[t.Mapping[str, t.Any]]):
    """Exception error.

    The exception error lavalink returns when a track has an exception.
    """

    message: str
    """The message of the exception."""
    severity: enums.SeverityType
    """The severity of the exception."""
    cause: str
    """The cause of the exception."""

    @classmethod
    def _from_payload(cls, payload: t.Mapping[str, t.Any]) -> ExceptionError:
        message = payload.get("message")
        if message is None:
            raise ValueError("message cannot be none.")
        if not isinstance(message, str):
            raise TypeError("message must be a string.")
        
        severity = payload.get("severity")
        if severity is None:
            raise ValueError("severity cannot be none.")
        if not isinstance(severity, str):
            raise TypeError("severity must be a string.")
        
        cause = payload.get("cause")
        if cause is None:
            raise ValueError("cause cannot be none.")
        if not isinstance(cause, str):
            raise TypeError("cause must be a string.")

        return cls(
            message, 
            enums.SeverityType(severity), 
            cause
        )


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
