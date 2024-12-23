from __future__ import annotations

import pytest

from ongaku.ext.checker import Sites
from ongaku.ext.checker import check

schemes = ["http://", "https://"]


class TestSites:
    def test_all(self):
        assert int(Sites.all()) == 2047

    def test_default(self):
        assert int(Sites.default()) == 127

    def test_has(self):
        assert (Sites.YOUTUBE | Sites.APPLE).has(Sites.YOUTUBE) is True

        assert (Sites.YOUTUBE | Sites.APPLE).has(Sites.BANDCAMP) is False

        assert (Sites.YOUTUBE | Sites.APPLE).has(Sites.APPLE | Sites.YOUTUBE) is True

    def test_bool(self):
        assert bool(Sites.YOUTUBE) is True


@pytest.mark.parametrize("query", ["a site", "https://ongaku.mplaty.com/"])
def test_checker_queries(query: str):
    assert check(query) is None


@pytest.mark.parametrize(
    "path",
    ["/watch?v=abcd1234", "/watch?v=abcd1234&list=abcd1234", "/playlist?list=abcd1234"],
)
@pytest.mark.parametrize("domain", ["youtube.com", "www.youtube.com", "youtu.be"])
@pytest.mark.parametrize("scheme", schemes)
def test_youtube(scheme: str, domain: str, path: str):
    assert check(scheme + domain + path) == Sites.YOUTUBE


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
def test_youtube_music(scheme: str, domain: str, path: str):
    assert check(scheme + domain + path) == Sites.YOUTUBE_MUSIC


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
def test_bandcamp(scheme: str, domain: str, path: str):
    assert check(scheme + domain + path) == Sites.BANDCAMP


@pytest.mark.parametrize(
    "url",
    [
        "soundcloud.com/user1234/song1234",
        "www.soundcloud.com/band/abcd1234",
        "m.soundcloud.com/dj/super-mix?abcd=1234",
        "soundcloud.com/user1234/song1234/s-abcd1234",
        "www.soundcloud.com/band/album1234/s-abcd1234",
        "m.soundcloud.com/dj/super-mix/s-abcd1234?abcd=1234",
        "soundcloud.com/user123/likes",
        "soundcloud.com/artist/likes",
        "www.soundcloud.com/band/likes",
        "m.soundcloud.com/dj/likes?abcd=1234",
    ],
)
@pytest.mark.parametrize("scheme", schemes)
def test_soundcloud(scheme: str, url: str):
    assert check(scheme + url) == Sites.SOUNDCLOUD


@pytest.mark.parametrize(
    "url", 
    [
        "https://on.soundcloud.com/abcd1234",
        "https://on.soundcloud.com/abcd1234?abcd=1234",
    ]
)
def test_soundcloud_https_only(url: str):
    assert check(url) == Sites.SOUNDCLOUD


@pytest.mark.parametrize(
    "url",
    [
        "https://twitch.tv/user1234",
        "https://www.twitch.tv/user1234",
        "https://go.twitch.tv/user1234",
        "https://m.twitch.tv/user1234",
    ],
)
def test_twitch(url: str):
    assert check(url) == Sites.TWITCH


@pytest.mark.parametrize(
    "url",
    [
        "https://vimeo.com/1234567890",
        "https://vimeo.com/1234567890?abcd=1234",
    ],
)
def test_vimeo(url: str):
    assert check(url) == Sites.VIMEO


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
def test_nico(scheme: str, domain: str, path: str):
    assert check(scheme + domain + path) == Sites.NICO


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
def test_spotify(scheme: str, domain: str, path: str):
    assert check(scheme + domain + path) == Sites.SPOTIFY


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
def test_apple(scheme: str, domain: str, path: str):
    assert check(scheme + domain + path) == Sites.APPLE


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
def test_deezer(scheme: str, domain: str, path: str):
    assert check(scheme + domain + path) == Sites.DEEZER


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
def test_yandex(scheme: str, domain: str, path: str):
    assert check(scheme + domain + path) == Sites.YANDEX
