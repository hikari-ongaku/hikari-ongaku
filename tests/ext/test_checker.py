from __future__ import annotations

import pytest

from ongaku.ext.checker import Sites
from ongaku.ext.checker import checker

schemes = ["http://", "https://"]


@pytest.mark.parametrize(
    "query",
    ["a query.", "http://yourmom.com?banana=vegetable"],
)
def test_checker_query(query: str):
    assert checker.check(query) is False


class TestSites:
    def test_all(self):
        assert int(Sites.all()) == 2047

    def test_default(self):
        assert int(Sites.default()) == 127

    def test_has(self):
        assert (Sites.YOUTUBE | Sites.APPLE).has(Sites.YOUTUBE) is True

        assert (Sites.YOUTUBE | Sites.APPLE).has(Sites.BANDCAMP) is False

        assert (Sites.YOUTUBE | Sites.APPLE).has(Sites.APPLE | Sites.YOUTUBE) is True


@pytest.mark.parametrize(
    "path",
    ["/watch?v=abcd1234", "/watch?v=abcd1234&list=abcd1234", "/playlist?list=abcd1234"],
)
@pytest.mark.parametrize(
    "domain", ["youtube.com", "www.youtube.com", "youtu.be", "www.youtu.be"]
)
@pytest.mark.parametrize("scheme", schemes)
class TestYoutube:
    def test_working(self, scheme: str, domain: str, path: str):
        assert checker.check(scheme + domain + path, sites=Sites.YOUTUBE) is True

    def test_not_included(self, scheme: str, domain: str, path: str):
        assert (
            checker.check(scheme + domain + path, sites=Sites.all() & ~Sites.YOUTUBE)
            is False
        )


@pytest.mark.parametrize(
    "path",
    ["/watch?v=abcd1234", "/watch?v=abcd1234&list=abcd1234", "/playlist?list=abcd1234"],
)
@pytest.mark.parametrize(
    "domain",
    [
        "music.youtube.com",
    ],
)
@pytest.mark.parametrize("scheme", schemes)
class TestYoutubeMusic:
    def test_working(self, scheme: str, domain: str, path: str):
        assert checker.check(scheme + domain + path, sites=Sites.YOUTUBE_MUSIC) is True

    def test_not_included(self, scheme: str, domain: str, path: str):
        assert (
            checker.check(
                scheme + domain + path, sites=Sites.all() & ~Sites.YOUTUBE_MUSIC
            )
            is False
        )


@pytest.mark.parametrize(
    "path",
    [
        "/track/abcd1234",
        "/album/abcd1234",
        "/track/abcd1234?abcd=1234",
        "/album/abcd1234?abcd=1234",
    ],
)
@pytest.mark.parametrize(
    "domain",
    [
        "bandcamp.com",
        "www.bandcamp.com",
        "test.bandcamp.com",
    ],
)
@pytest.mark.parametrize("scheme", schemes)
class TestBandcamp:
    def test_working(self, scheme: str, domain: str, path: str):
        assert checker.check(scheme + domain + path, sites=Sites.BANDCAMP) is True

    def test_not_included(self, scheme: str, domain: str, path: str):
        assert (
            checker.check(scheme + domain + path, sites=Sites.all() & ~Sites.BANDCAMP)
            is False
        )


@pytest.mark.parametrize(
    "url",
    [
        "soundcloud.com/user1234/song1234",
        "www.soundcloud.com/band/abcd1234",
        "m.soundcloud.com/dj/super-mix?abcd=1234",
        "on.soundcloud.com/abcd1234",
        "on.soundcloud.com/abcd1234?abcd=1234",
        "soundcloud.com/user1234/song1234/s-abcd1234",
        "www.soundcloud.com/band/album1234/s-abcd1234",
        "m.soundcloud.com/dj/super-mix/s-abcd1234?abcd=1234",
        "on.soundcloud.com/abcd1234",
        "soundcloud.com/user123/likes",
        "soundcloud.com/artist/likes",
        "www.soundcloud.com/band/likes",
        "m.soundcloud.com/dj/likes?abcd=1234",
    ],
)
@pytest.mark.parametrize("scheme", schemes)
class TestSoundcloud:
    def test_working(self, scheme: str, url: str):
        assert checker.check(scheme + url, sites=Sites.SOUNDCLOUD) is True

    def test_not_included(self, scheme: str, url: str):
        assert (
            checker.check(scheme + url, sites=Sites.all() & ~Sites.SOUNDCLOUD) is False
        )


@pytest.mark.parametrize(
    "url",
    [
        "https://twitch.tv/user1234",
        "https://www.twitch.tv/user1234",
        "https://go.twitch.tv/user1234",
        "https://m.twitch.tv/user1234",
    ],
)
class TestTwitch:
    def test_working(self, url: str):
        assert checker.check(url, sites=Sites.TWITCH) is True

    def test_not_included(self, url: str):
        assert checker.check(url, sites=Sites.all() & ~Sites.TWITCH) is False


@pytest.mark.parametrize(
    "url",
    [
        "https://vimeo.com/1234567890",
        "https://vimeo.com/1234567890?abcd=1234",
    ],
)
class TestVimeo:
    def test_working(self, url: str):
        assert checker.check(url, sites=Sites.VIMEO) is True

    def test_not_included(self, url: str):
        assert checker.check(url, sites=Sites.all() & ~Sites.VIMEO) is False


@pytest.mark.parametrize(
    "path",
    [
        "/watch/sm1234",
        "/watch/sm1234?abcd=1234",
    ],
)
@pytest.mark.parametrize(
    "domain",
    [
        "nicovideo.jp",
        "www.nicovideo.jp",
    ],
)
@pytest.mark.parametrize("scheme", schemes)
class TestNico:
    def test_working(self, scheme: str, domain: str, path: str):
        assert checker.check(scheme + domain + path, sites=Sites.NICO) is True

    def test_not_included(self, scheme: str, domain: str, path: str):
        assert (
            checker.check(scheme + domain + path, sites=Sites.all() & ~Sites.NICO)
            is False
        )


@pytest.mark.parametrize(
    "path",
    [
        "/track/abcd1234",
        "/playlist/abcd1234",
        "/album/abcd1234",
        "/user/spotify/playlist/abcd1234",
        "/artist/abcd1234",
        "/us/user/spotify/track/abcd1234",
    ],
)
@pytest.mark.parametrize(
    "domain",
    [
        "www.open.spotify.com",
        "open.spotify.com",
    ],
)
@pytest.mark.parametrize("scheme", schemes)
class TestSpotify:
    def test_working(self, scheme: str, domain: str, path: str):
        assert checker.check(scheme + domain + path, sites=Sites.SPOTIFY) is True

    def test_not_included(self, scheme: str, domain: str, path: str):
        assert (
            checker.check(scheme + domain + path, sites=Sites.all() & ~Sites.SPOTIFY)
            is False
        )


@pytest.mark.parametrize(
    "path",
    [
        "/song/1234",
        "/playlist/1234",
        "/artist/1234",
        "/album/1234",
        "/us/album/1234",
        "/artist/1234?i=1234",
        "/song/1234?i=1234",
    ],
)
@pytest.mark.parametrize(
    "domain",
    [
        "www.music.apple.com",
        "music.apple.com",
    ],
)
@pytest.mark.parametrize("scheme", schemes)
class TestApple:
    def test_working(self, scheme: str, domain: str, path: str):
        assert checker.check(scheme + domain + path, sites=Sites.APPLE) is True

    def test_not_included(self, scheme: str, domain: str, path: str):
        assert (
            checker.check(scheme + domain + path, sites=Sites.all() & ~Sites.APPLE)
            is False
        )


@pytest.mark.parametrize(
    "path",
    ["/track/1234", "/album/1234", "/playlist/1234", "/artist/1234", "/us/track/1234"],
)
@pytest.mark.parametrize(
    "domain",
    [
        "www.deezer.com",
        "deezer.com",
    ],
)
@pytest.mark.parametrize("scheme", schemes)
class TestDeezer:
    def test_working(self, scheme: str, domain: str, path: str):
        assert checker.check(scheme + domain + path, sites=Sites.DEEZER) is True

    def test_not_included(self, scheme: str, domain: str, path: str):
        assert (
            checker.check(scheme + domain + path, sites=Sites.all() & ~Sites.DEEZER)
            is False
        )


@pytest.mark.parametrize(
    "path",
    [
        "/artist/1234",
        "/album/1234",
        "/track/1234",
        "/track/1234/track/1234",
        "/artist/1234/track/1234",
    ],
)
@pytest.mark.parametrize(
    "domain",
    [
        "music.yandex.ru",
        "music.yandex.com",
        "music.yandex.kz",
        "music.yandex.by",
    ],
)
@pytest.mark.parametrize("scheme", schemes)
class TestYandex:
    def test_working(self, scheme: str, domain: str, path: str):
        assert checker.check(scheme + domain + path, sites=Sites.YANDEX) is True

    def test_not_included(self, scheme: str, domain: str, path: str):
        assert (
            checker.check(scheme + domain + path, sites=Sites.all() & ~Sites.YANDEX)
            is False
        )
