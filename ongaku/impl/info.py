"""
Information Impl's.

The info implemented classes.
"""

from __future__ import annotations

import typing

from ongaku.abc import info as info_

if typing.TYPE_CHECKING:
    import datetime

__all__ = ("Info", "Version", "Git", "Plugin")


class Info(info_.Info):
    def __init__(
        self,
        version: info_.Version,
        build_time: datetime.datetime,
        git: info_.Git,
        jvm: str,
        lavaplayer: str,
        source_managers: typing.Sequence[str],
        filters: typing.Sequence[str],
        plugins: typing.Sequence[info_.Plugin],
    ) -> None:
        self._version = version
        self._build_time = build_time
        self._git = git
        self._jvm = jvm
        self._lavaplayer = lavaplayer
        self._source_managers = source_managers
        self._filters = filters
        self._plugins = plugins

    @property
    def version(self) -> info_.Version:
        return self._version

    @property
    def build_time(self) -> datetime.datetime:
        return self._build_time

    @property
    def git(self) -> info_.Git:
        return self._git

    @property
    def jvm(self) -> str:
        return self._jvm

    @property
    def lavaplayer(self) -> str:
        return self._lavaplayer

    @property
    def source_managers(self) -> typing.Sequence[str]:
        return self._source_managers

    @property
    def filters(self) -> typing.Sequence[str]:
        return self._filters

    @property
    def plugins(self) -> typing.Sequence[info_.Plugin]:
        return self._plugins


class Version(info_.Version):
    def __init__(
        self,
        semver: str,
        major: int,
        minor: int,
        patch: int,
        pre_release: str,
        build: str | None,
    ) -> None:
        self._semver = semver
        self._major = major
        self._minor = minor
        self._patch = patch
        self._pre_release = pre_release
        self._build = build

    @property
    def semver(self) -> str:
        return self._semver

    @property
    def major(self) -> int:
        return self._major

    @property
    def minor(self) -> int:
        return self._minor

    @property
    def patch(self) -> int:
        return self._patch

    @property
    def pre_release(self) -> str:
        return self._pre_release

    @property
    def build(self) -> str | None:
        return self._build


class Git(info_.Git):
    def __init__(
        self, branch: str, commit: str, commit_time: datetime.datetime
    ) -> None:
        self._branch = branch
        self._commit = commit
        self._commit_time = commit_time

    @property
    def branch(self) -> str:
        return self._branch

    @property
    def commit(self) -> str:
        return self._commit

    @property
    def commit_time(self) -> datetime.datetime:
        return self._commit_time


class Plugin(info_.Plugin):
    def __init__(self, name: str, version: str) -> None:
        self._name = name
        self._version = version

    @property
    def name(self) -> str:
        return self._name

    @property
    def version(self) -> str:
        return self._version


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
