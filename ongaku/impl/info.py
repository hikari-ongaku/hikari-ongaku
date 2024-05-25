# ruff: noqa: D101, D102

from __future__ import annotations

import datetime
import typing

from ongaku.abc import info as info_


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
