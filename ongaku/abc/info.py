"""
Info ABC's.

The info abstract classes.
"""

from __future__ import annotations

import abc
import typing

if typing.TYPE_CHECKING:
    import datetime

__all__ = (
    "Version",
    "Git",
    "Plugin",
    "Info",
)


class Info(abc.ABC):
    """
    Information.

    All of the Info Version information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#info-response)
    """

    __slots__: typing.Sequence[str] = (
        "_version",
        "_build_time",
        "_git",
        "_jvm",
        "_lavaplayer",
        "_source_managers",
        "_filters",
        "_plugins",
    )

    @property
    def version(self) -> Version:
        """The version of this Lavalink server."""
        return self._version

    @property
    def build_time(self) -> datetime.datetime:
        """The datetime object of when this Lavalink jar was built."""
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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Info):
            return False

        if self.version != other.version:
            return False

        if self.build_time != other.build_time:
            return False

        if self.git != other.git:
            return False

        if self.jvm != other.jvm:
            return False

        if self.lavaplayer != other.lavaplayer:
            return False

        if self.source_managers != other.source_managers:
            return False

        if self.filters != other.filters:
            return False

        return self.plugins == other.plugins


class Version(abc.ABC):
    """
    Version information.

    All information, about the version of lavalink that is running.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#version-object)
    """

    __slots__: typing.Sequence[str] = (
        "_semver",
        "_major",
        "_minor",
        "_patch",
        "_pre_release",
        "_build",
    )

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

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return False

        if self.semver != other.semver:
            return False

        if self.major != other.major:
            return False

        if self.minor != other.minor:
            return False

        if self.patch != other.patch:
            return False

        if self.pre_release != other.pre_release:
            return False

        return self.build == other.build


class Git(abc.ABC):
    """
    Git information.

    All of the information about the lavalink git information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#git-object)
    """

    __slots__: typing.Sequence[str] = (
        "_branch",
        "_commit",
        "_commit_time",
    )

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
        """The datetime object of when the commit was created."""
        return self._commit_time

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Git):
            return False

        if self.branch != other.branch:
            return False

        if self.commit != other.commit:
            return False

        return self.commit_time == other.commit_time


class Plugin(abc.ABC):
    """
    Plugin information.

    All of the Information about the currently loaded plugins.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest.html#plugin-object)
    """

    __slots__: typing.Sequence[str] = ("_name", "_version")

    @property
    def name(self) -> str:
        """The name of the plugin."""
        return self._name

    @property
    def version(self) -> str:
        """The version of the plugin."""
        return self._version

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Plugin):
            return False

        if self.name != other.name:
            return False

        return self.version == other.version


# MIT License

# Copyright (c) 2023-present MPlatypus

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
