"""
Info ABC's.

The info abstract classes.
"""

from __future__ import annotations

import datetime
import typing
import attrs

__all__ = (
    "Version",
    "Git",
    "Plugin",
    "Info",
)


@attrs.define
class Version:
    """
    Version information.

    All information, about the version of lavalink that is running.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#version-object)
    """

    _semver: str = attrs.field(alias="semver")
    _major: int = attrs.field(alias="major")
    _minor: int = attrs.field(alias="minor")
    _patch: int = attrs.field(alias="patch")
    _pre_release: str = attrs.field(alias="pre_release")
    _build: str | None = attrs.field(alias="build")

    @property
    def semver(self) -> str:
        """The full version string of this Lavalink server."""
        return self._semver

    @property
    def major(self) -> int:
        """The major version of this Lavalink server."""
        return self._major

    @property
    def minor(self) -> int:
        """The minor version of this Lavalink server."""
        return self._minor

    @property
    def patch(self) -> int:
        """The patch version of this Lavalink server."""
        return self._patch

    @property
    def pre_release(self) -> str:
        """The pre-release version according to semver as a `.` separated list of identifiers."""
        return self._pre_release

    @property
    def build(self) -> str | None:
        """The build metadata according to semver as a `.` separated list of identifiers."""
        return self._build


@attrs.define
class Git:
    """
    Git information.

    All of the information about the lavalink git information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#git-object)
    """

    _branch: str = attrs.field(alias="branch")
    _commit: str = attrs.field(alias="commit")
    _commit_time: datetime.datetime = attrs.field(alias="commit_time")

    @property
    def branch(self) -> str:
        """The branch this Lavalink server was built on."""
        return self._branch

    @property
    def commit(self) -> str:
        """The commit this Lavalink server was built on."""
        return self._commit

    @property
    def commit_time(self) -> datetime.datetime:
        """The millisecond unix timestamp for when the commit was created."""
        return self._commit_time


@attrs.define
class Plugin:
    """
    Plugin information.

    All of the Information about the currently loaded plugins.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#plugin-object)
    """

    _name: str = attrs.field(alias="name")
    _version: str = attrs.field(alias="version")

    @property
    def name(self) -> str:
        """The name of the plugin."""
        return self._name

    @property
    def version(self) -> str:
        """The version of the plugin."""
        return self._version


@attrs.define
class Info:
    """
    Information.

    All of the Info Version information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#info-response)
    """

    _version: Version = attrs.field(alias="version")
    _build_time: datetime.datetime = attrs.field(alias="build_time")
    _git: Git = attrs.field(alias="git")
    _jvm: str = attrs.field(alias="jvm")
    _lavaplayer: str = attrs.field(alias="lavaplayer")
    _source_managers: typing.Sequence[str] = attrs.field(alias="source_managers")
    _filters: typing.Sequence[str] = attrs.field(alias="filters")
    _plugins: typing.Sequence[Plugin] = attrs.field(alias="plugins")

    @property
    def version(self) -> Version:
        """The version of this Lavalink server."""
        return self._version

    @property
    def build_time(self) -> datetime.datetime:
        """The millisecond unix timestamp when this Lavalink jar was built."""
        return self._build_time
    
    @property
    def git(self) -> Git:
        """The git information of this Lavalink server."""
        return self._git

    @property
    def jvm(self) -> str:
        """The JVM version this Lavalink server runs on."""
        return self._jvm
    
    @property
    def lavaplayer(self) -> str:
        """The Lavaplayer version being used by this server."""
        return self._lavaplayer

    @property
    def source_managers(self) -> typing.Sequence[str]:
        """The enabled source managers for this server."""
        return self._source_managers

    @property
    def filters(self) -> typing.Sequence[str]:
        """The enabled filters for this server."""
        return self._filters

    @property
    def plugins(self) -> typing.Sequence[Plugin]:
        """The enabled plugins for this server."""
        return self._plugins
    


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
