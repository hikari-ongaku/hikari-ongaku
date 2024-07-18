from __future__ import annotations

import pytest

from ongaku.ext.checker import checker


@pytest.mark.parametrize(
    "query",
    [
        "a query.",
    ],
)
def test_checker_query(query: str):
    assert checker.check(query) is False


@pytest.mark.parametrize(
    "url",
    [
        # youtube video links
        "https://www.youtube.com/watch?v=test_video",
        "https://youtube.com/watch?v=test_video",
        "https://www.youtu.be/watch?v=test_video",
        "https://youtu.be/watch?v=test_video",
        "https://music.youtube.com/watch?v=test_video",
        # youtube playlist links
        "https://www.youtube.com/playlist?list=test_playlist",
        "https://youtube.com/playlist?list=test_playlist",
        "https://www.youtu.be/playlist?list=test_playlist",
        "https://youtu.be/playlist?list=test_playlist",
        "https://music.youtube.com/playlist?list=test_playlist",
    ],
)
def test_checker_links(url: str):
    assert checker.check(url) is True
