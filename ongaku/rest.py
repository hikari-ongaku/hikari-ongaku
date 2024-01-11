from __future__ import annotations

import typing as t

import aiohttp
import hikari

from .abc.lavalink import ExceptionError, Info
from .abc.player import Player, PlayerVoice
from .abc.session import Session
from .abc.track import Playlist, SearchResult, Track
from .enums import PlatformType
from .errors import BuildException, LavalinkException
import urllib.parse as urlparse

if t.TYPE_CHECKING:
    from .ongaku import Ongaku

    OngakuT = t.TypeVar("OngakuT", bound="Ongaku")

__all__ = ("RestApi",)


class SessionApi:
    def __init__(self, ongaku: Ongaku) -> None:
        self._ongaku = ongaku

    async def update(self, session_id: str) -> Session:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self._ongaku.internal.uri + "/sessions/" + session_id,
                headers=self._ongaku.internal.headers,
            ) as response:
                if response.status >= 400:
                    raise LavalinkException(response.status)

                try:
                    session_model = Session._from_payload(await response.json())
                except Exception as e:
                    raise BuildException(e)

                return session_model


class PlayerApi:
    """
    The Rest based actions for the player.
    """

    def __init__(self, ongaku: Ongaku) -> None:
        self._ongaku = ongaku

    async def fetch_all(self, session_id: str) -> t.Optional[list[Player]]:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self._ongaku.internal.uri + "/sessions/" + session_id + "/players",
                headers=self._ongaku.internal.headers,
            ) as response:
                if response.status >= 400:
                    raise LavalinkException(response.status)

                players = await response.json()

                player_list: list[Player] = []

                for player in players:
                    try:
                        player_model = Player._from_payload(player)
                    except Exception as e:
                        raise BuildException(e)

                    player_list.append(player_model)

        return player_list

    async def fetch(
        self, session_id: str, guild_id: hikari.Snowflake
    ) -> t.Optional[Player]:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self._ongaku.internal.uri
                + "/sessions/"
                + session_id
                + "/players/"
                + str(guild_id),
                headers=self._ongaku.internal.headers,
            ) as response:
                if response.status >= 400:
                    raise LavalinkException(response.status)

                try:
                    player_model = Player._from_payload(await response.json())
                except Exception as e:
                    raise BuildException(e)

        return player_model

    async def update(
        self,
        guild_id: hikari.Snowflake,
        session_id: str,
        *,
        track: hikari.UndefinedNoneOr[Track] = hikari.UNDEFINED,
        position: hikari.UndefinedOr[int] = hikari.UNDEFINED,
        end_time: hikari.UndefinedOr[int] = hikari.UNDEFINED,
        volume: hikari.UndefinedOr[int] = hikari.UNDEFINED,
        paused: hikari.UndefinedOr[bool] = hikari.UNDEFINED,
        voice: hikari.UndefinedOr[PlayerVoice] = hikari.UNDEFINED,
        no_replace: bool = True,
    ) -> Player:
        """
        Update a player

        Updates a player with the new parameters, or creates a new one if none exist.

        Parameters
        ----------
        guild_id : hikari.Snowflake
            The guild id that the bot is playing in.
        session_id : str
            The session_id for the lavalink server session.

        """
        patch_data: dict[str, t.Any] = {}

        if track != hikari.UNDEFINED:
            if track is None:
                patch_data.update(
                    {
                        "track": {
                            "encoded": None,
                        }
                    }
                )
            else:
                patch_data.update(
                    {
                        "track": {
                            "encoded": track.encoded,
                        }
                    }
                )

        if position != hikari.UNDEFINED:
            patch_data.update({"position": position})

        if end_time != hikari.UNDEFINED:
            patch_data.update({"endTime": end_time})

        if volume != hikari.UNDEFINED:
            patch_data.update({"volume": volume})

        if paused != hikari.UNDEFINED:
            patch_data.update({"paused": paused})

        if voice != hikari.UNDEFINED:
            patch_data.update(
                {
                    "voice": {
                        "token": voice.token,
                        "endpoint": voice.endpoint[6:],
                        "sessionId": voice.session_id,
                    }
                }
            )

        new_headers = self._ongaku.internal.headers.copy()

        new_headers.update({"Content-Type": "application/json"})

        params = {"noReplace": "false"}

        if no_replace:
            params.update({"noReplace": "true"})

        async with aiohttp.ClientSession() as session:
            try:
                async with session.patch(
                    self._ongaku.internal.uri
                    + "/sessions/"
                    + session_id
                    + "/players/"
                    + str(guild_id),
                    headers=new_headers,
                    params=params,
                    json=patch_data,
                ) as response:
                    if response.status >= 400:
                        raise LavalinkException(response.status, await response.json())

                    try:
                        player_model = Player._from_payload(await response.json())
                    except Exception as e:
                        raise BuildException(e)
            except Exception as e:
                raise e

        return player_model

    async def delete(self, session_id: str, guild_id: hikari.Snowflake) -> None:
        """
        Creates a new player for the specified guild. If one already exists, returns that instead.
        """
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                self._ongaku.internal.uri
                + "/sessions/"
                + session_id
                + "/players/"
                + str(guild_id),
                headers=self._ongaku.internal.headers,
            ) as response:
                if response.status >= 400:
                    raise LavalinkException(response.status)


class TrackApi:
    """
    The rest based actions for the track.
    """

    def __init__(self, ongaku: Ongaku) -> None:
        self._ongaku: Ongaku = ongaku

    async def _url_handler(self, possible_url: str) -> t.Optional[str]:
        try:
            url = urlparse.parse_qs(possible_url.split("?")[1], strict_parsing=True)
        except Exception:
            return

        try:
            code = url["list"]
        except Exception:
            pass
        else:
            return code[0]

        try:
            code = url["v"]
        except Exception:
            pass
        else:
            return code[0]

    async def load(
        self, query: str, platform: PlatformType = PlatformType.YOUTUBE
    ) -> SearchResult | Playlist | Track | None:
        async with aiohttp.ClientSession() as session:
            query_sanitize = await self._url_handler(query)

            if query_sanitize is not None:
                params = {"identifier": query_sanitize}
            else:
                if platform == PlatformType.YOUTUBE:
                    params = {"identifier": f"ytsearch:{query}"}
                elif platform == PlatformType.YOUTUBE_MUSIC:
                    params = {"identifier": f"ytmsearch:{query}"}
                elif platform == PlatformType.SOUNDCLOUD:
                    params = {"identifier": f"scsearch:{query}"}
                else:
                    params = {"identifier": f"ytsearch:{query}"}

            async with session.get(
                self._ongaku.internal.uri + "/loadtracks",
                headers=self._ongaku.internal.headers,
                params=params,
            ) as response:
                if response.status >= 400:
                    raise LavalinkException(
                        f"status: {response.status} message: {response.text()}"
                    )

                data = await response.json()

                load_type = data["loadType"]

                if load_type == "empty":
                    return

                if load_type == "error":
                    raise LavalinkException(ExceptionError._from_payload(data["data"]))

                if load_type == "search":
                    try:
                        search_result = SearchResult._from_payload(data["data"])
                    except Exception as e:
                        raise e

                    return search_result

                if load_type == "track":
                    try:
                        track = Track._from_payload(data["data"])
                    except Exception as e:
                        raise e

                    return track

                if load_type == "playlist":
                    try:
                        playlist = Playlist._from_payload(data["data"])
                    except Exception as e:
                        raise e

                    return playlist


class RestApi:
    """
    Base rest class

    The base rest class, for all rest related actions.
    """

    def __init__(self, ongaku: Ongaku) -> None:
        self._ongaku: Ongaku = ongaku

        self._track_api = TrackApi(ongaku)
        self._player_api = PlayerApi(ongaku)
        self._session_api = SessionApi(ongaku)

    @property
    def track(self) -> TrackApi:
        return self._track_api

    @property
    def player(self) -> PlayerApi:
        return self._player_api

    @property
    def session(self) -> SessionApi:
        return self._session_api

    async def fetch_info(self) -> Info:
        """
        Fetch info

        Fetch the information about the Lavalink server.

        Returns
        -------
        abc.Info
            Returns an information object.

        Raises
        ------
        LavalinkException
            Response was a 400 or 500 error.
        BuildException
            Failure to build `abc.Info`
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self._ongaku.internal.uri + "/info",
                headers=self._ongaku.internal.headers,
            ) as response:
                if response.status >= 400:
                    raise LavalinkException(
                        f"status: {response.status} message: {response.text()}"
                    )

                try:
                    info_resp = Info._from_payload(await response.json())
                except Exception as e:
                    raise BuildException(e)

        return info_resp


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
