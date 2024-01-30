# noqa: D100
from __future__ import annotations

from .abc import Checked, CheckedType
import urllib.parse as urlparse

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
            queries.update({url_query_split[0]:url_query_split[1]})

    if url.netloc in ["www.youtube.com", "youtube.com", "www.youtu.be", "youtu.be", "music.youtube.com"]:
        if url.path == "/playlist":
            return Checked(queries["list"], CheckedType.PLAYLIST)
        elif url.path == "/watch":
            return Checked(queries["v"], CheckedType.TRACK)

    return Checked(query, CheckedType.QUERY)

