from . import models, error, player
import typing as t

import hikari
import aiohttp
import logging

class InternalPlayer:
    """
    The Rest based actions for the player.
    """
    def __init__(self, link) -> None:
        from .ongaku import Ongaku  # this is probably a bad thing to do.

        self._link: Ongaku = link

    async def play_track(self, guild_id: hikari.Snowflake, track: models.Track) -> None:
        """
        internally plays a track.
        """


class Internal:
    def __init__(self, link) -> None:
        from .ongaku import Ongaku  # this is probably a bad thing to do.

        self._link: Ongaku = link

        self._internal_player = InternalPlayer(self._link)

    @property
    def player(self) -> InternalPlayer:
        return self._internal_player

class Rest:
    """
    The base rest class for all rest related things.
    """

    def __init__(self, link) -> None:
        from .ongaku import Ongaku  # this is probably a bad thing to do.

        self._link: Ongaku = link

        self._internal = Internal(self._link)

    async def fetch_info(self) -> models.Info:
        """
        Fetch the information about the lavalink server.

        ----
        Returns: Returns a
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self._link._standard_uri + "/info", headers=self._link._headers
            ) as response:
                if response.status >= 400:
                    raise error.ResponseException(response.status)

                try:
                    info_resp = models.Info(await response.json())
                except Exception as e:
                    raise error.BuildException(e)

        return info_resp

    async def search(
        self, platform: models.PlatformType, query: str
    ) -> t.Optional[list[models.Track]]:
        async with aiohttp.ClientSession() as session:
            if platform == models.PlatformType.YOUTUBE:
                params = {"identifier": f'ytsearch:"{query}"'}
            elif platform == models.PlatformType.YOUTUBE_MUSIC:
                params = {"identifier": f'ytmsearch:"{query}"'}
            else:
                params = {"identifier": f'scsearch:"{query}"'}

            async with session.get(
                self._link._standard_uri + "/loadtracks",
                headers=self._link._headers,
                params=params,
            ) as response:
                if response.status >= 400:
                    raise error.ResponseException(response.status)

                data = await response.json()

                load_type = data["loadType"]

                if load_type == "search":
                    tracks = []

                    for t in data["data"]:
                        try:
                            track = models.Track(t)
                        except Exception as e:
                            logging.error("Failed to build track: " + str(e))
                            continue

                        tracks.append(track)

                    if len(tracks) <= 0:
                        return

                    else:
                        return tracks

    async def load_track(self, track: models.Track, guild_id: int) -> None:
        async with aiohttp.ClientSession() as session:
            params = {"identifier": track.encoded}
            async with session.get(
                self._link._standard_uri, headers=self._link._headers, params=params
            ) as response:
                if response.status >= 400:
                    raise error.ResponseException(response.status)

                data = await response.json()

    async def skip_track(self, track: models.Track, guild_id: int) -> None:
        """
        Skip the current track.
        """

    @property
    def internal(self) -> Internal:
        return self._internal