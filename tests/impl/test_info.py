# ruff: noqa: D100, D101, D102, D103

import datetime

from ongaku.impl.info import Git
from ongaku.impl.info import Info
from ongaku.impl.info import Plugin
from ongaku.impl.info import Version


def test_info():
    time = datetime.datetime.now()
    version = Version(
        semver="semver",
        major=1,
        minor=2,
        patch=3,
        pre_release="pre_release",
        build="build",
    )
    git = Git(branch="branch", commit="commit", commit_time=time)
    source_managers = ["source_manager_1", "source_manager_2"]
    filters = ["filter_1", "filter_2"]
    plugins = [
        Plugin(name="name_1", version="version_1"),
        Plugin(name="name_2", version="version_2"),
    ]
    info = Info(
        version=version,
        build_time=time,
        git=git,
        jvm="jvm",
        lavaplayer="lavaplayer",
        source_managers=source_managers,
        filters=filters,
        plugins=plugins,
    )

    assert info.version == version
    assert info.build_time == time
    assert info.git == git
    assert info.jvm == "jvm"
    assert info.lavaplayer == "lavaplayer"
    assert info.source_managers == source_managers
    assert info.filters == filters
    assert info.plugins == plugins


def test_info_version():
    info_version = Version(
        semver="semver",
        major=1,
        minor=2,
        patch=3,
        pre_release="pre_release",
        build="build",
    )

    assert info_version.semver == "semver"
    assert info_version.major == 1
    assert info_version.minor == 2
    assert info_version.patch == 3
    assert info_version.pre_release == "pre_release"
    assert info_version.build == "build"


def test_info_git():
    time = datetime.datetime.now()
    info_git = Git(branch="branch", commit="commit", commit_time=time)

    assert info_git.branch == "branch"
    assert info_git.commit == "commit"
    assert info_git.commit_time == time


def test_info_plugin():
    info_plugin = Plugin(name="name", version="version")

    assert info_plugin.name == "name"
    assert info_plugin.version == "version"
