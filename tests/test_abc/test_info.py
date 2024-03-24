# ruff: noqa: D100, D101, D102

import unittest

from ongaku.abc.info import InfoVersion, InfoGit, InfoPlugin, Info
from tests import payload

class TestInfoVersion(unittest.TestCase):
    def test_base(self):
        version = InfoVersion(semver="test_semver", major=1, minor=2, patch=3, pre_release="test_pre_release", build="test_build")

        assert version.semver == "test_semver"
        assert version.major == 1
        assert version.minor == 2
        assert version.patch == 3
        assert version.pre_release == "test_pre_release"
        assert version.build == "test_build"

    def test_from_payload(self):
        version = InfoVersion._from_payload(payload.convert(payload.INFO_VERSION))

        assert version.semver == "test_semver"
        assert version.major == 1
        assert version.minor == 2
        assert version.patch == 3
        assert version.pre_release == "test_pre_release"
        assert version.build == "test_build"

    def test_to_payload(self):
        version = InfoVersion._from_payload(payload.convert(payload.INFO_VERSION))

        assert version._to_payload == payload.INFO_VERSION

class TestInfoGit(unittest.TestCase):
    def test_base(self):
        git = InfoGit(branch="test_branch", commit="test_commit", commit_time=1)

        assert git.branch == "test_branch"
        assert git.commit == "test_commit"
        assert git.commit_time == 1

    def test_from_payload(self):
        git = InfoGit._from_payload(payload.convert(payload.INFO_GIT))

        assert git.branch == "test_branch"
        assert git.commit == "test_commit"
        assert git.commit_time == 1

    def test_to_payload(self):
        git = InfoGit._from_payload(payload.convert(payload.INFO_GIT))

        assert git._to_payload == payload.INFO_GIT

class TestInfoPlugin(unittest.TestCase):
    def test_base(self):
        plugin = InfoPlugin(name="test_name", version="test_version")

        assert plugin.name == "test_name"
        assert plugin.version == "test_version"

    def test_from_payload(self):
        plugin = InfoPlugin._from_payload(payload.convert(payload.INFO_PLUGIN))

        assert plugin.name == "test_name"
        assert plugin.version == "test_version"

    def test_to_payload(self):
        plugin = InfoPlugin._from_payload(payload.convert(payload.INFO_PLUGIN))

        assert plugin._to_payload == payload.INFO_PLUGIN

class TestInfo(unittest.TestCase):
    def test_base(self):
        version = InfoVersion._from_payload(payload.convert(payload.INFO_VERSION))
        git = InfoGit._from_payload(payload.convert(payload.INFO_GIT))
        plugin = InfoPlugin._from_payload(payload.convert(payload.INFO_PLUGIN))
        info = Info(
            version=version, 
            build_time=1, 
            git=git, 
            jvm="test_jvm", 
            lavaplayer="test_lavaplayer", 
            source_managers=["test_source_manager"], 
            filters=["equalizer", "karaoke", "timescale", "channelMix"], 
            plugins=[plugin]
        )

        assert info.version == version
        assert info.build_time == 1
        assert info.git == git
        assert info.jvm == "test_jvm"
        assert info.lavaplayer == "test_lavaplayer"
        assert info.source_managers == ["test_source_manager"]
        assert info.filters == ["equalizer", "karaoke", "timescale", "channelMix"]
        assert info.plugins == [plugin]

    def test_from_payload(self):
        version = InfoVersion._from_payload(payload.convert(payload.INFO_VERSION))
        git = InfoGit._from_payload(payload.convert(payload.INFO_GIT))
        plugin = InfoPlugin._from_payload(payload.convert(payload.INFO_PLUGIN))
        info = Info._from_payload(payload.convert(payload.REST_INFO))

        assert info.version == version
        assert info.build_time == 1
        assert info.git == git
        assert info.jvm == "test_jvm"
        assert info.lavaplayer == "test_lavaplayer"
        assert info.source_managers == ["test_source_manager"]
        assert info.filters == ["equalizer", "karaoke", "timescale", "channelMix"]
        assert info.plugins == [plugin]

    def test_to_payload(self):
        info = Info._from_payload(payload.convert(payload.REST_INFO))

        assert info._to_payload == payload.REST_INFO


