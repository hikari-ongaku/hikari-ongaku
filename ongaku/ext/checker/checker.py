"""
Checker.

The extension, that allows you to check if a link is a url, or a video/playlist!
"""

from __future__ import annotations

import urllib.parse as urlparse

from .abc import Checked
from .abc import CheckedType


async def check(query: str) -> Checked:
    """
    Check a string.

    Allows for the user to check a current string, and see what type it is.

    Parameters
    ----------
    query : str
        The query you wish to check.
    """
    url = urlparse.urlparse(query)

    queries: dict[str, str] = {}

    if url.query.strip() != "":
        url_queries = url.query.split("&")

        for url_query in url_queries:
            url_query_split = url_query.split("=")
            queries.update({url_query_split[0]: url_query_split[1]})

    if url.netloc in [
        "www.youtube.com",
        "youtube.com",
        "www.youtu.be",
        "youtu.be",
        "music.youtube.com",
    ]:
        if url.path == "/playlist":
            return Checked(queries["list"], CheckedType.PLAYLIST)
        elif url.path == "/watch":
            return Checked(queries["v"], CheckedType.TRACK)

    return Checked(query, CheckedType.QUERY)


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
