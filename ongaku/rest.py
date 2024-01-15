from __future__ import annotations

import typing as t

import aiohttp
import hikari

from .abc.lavalink import ExceptionError, Info
from .abc.player import Player, PlayerVoice
from .abc.session import Session
from .abc.track import Playlist, SearchResult, Track
from .abc.filters import Filter
from .enums import PlatformType
from .errors import BuildException, LavalinkException
import urllib.parse as urlparse

if t.TYPE_CHECKING:
    from .ongaku import Ongaku

__all__ = ("Rest",)


class Rest:
    """
    Base rest class

    The base rest class, for all rest related actions.

    !!! WARNING
        Please do not create this on your own. Please use the rest attribute, in the base ongaku object you created.
    """

    def __init__(self, ongaku: Ongaku) -> None:
        self._ongaku: Ongaku = ongaku

        self._rest_track = RestTrack(ongaku)
        self._rest_player = RestPlayer(ongaku)
        self._rest_session = RestSession(ongaku)

    @property
    def track(self) -> RestTrack:
        """The track related rest actions"""
        return self._rest_track

    @property
    def player(self) -> RestPlayer:
        """The player related rest actions"""
        return self._rest_player

    @property
    def session(self) -> RestSession:
        """The session related rest actions"""
        return self._rest_session

    async def fetch_info(self) -> Info:
        """
        Fetch info

        Fetch the information about the Lavalink server.

        Raises
        ------
        LavalinkException
            Response was a 400 or 500 error.
        BuildException
            Failure to build `abc.Info`

        Returns
        -------
        Info
            Returns an information object.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self._ongaku._internal.base_uri + "/info",
                headers=self._ongaku._internal.headers,
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


class RestSession:
    """
    !!! WARNING
        Please do not create this on your own. Please use the rest attribute, in the base ongaku object you created.
    """

    def __init__(self, ongaku: Ongaku) -> None:
        self._ongaku = ongaku

    async def update(self, session_id: str) -> Session:
        """
        Session Update

        Update the current session.

        Parameters
        ----------
        session_id : str
            The Session ID connected to the update.

        Raises
        ------
        LavalinkException
            If an error code of 4XX or 5XX is received.
        BuildException
            Failure to build the session object.

        Returns
        -------
        Session
            The session object information.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self._ongaku._internal.base_uri + "/sessions/" + session_id,
                headers=self._ongaku._internal.headers,
            ) as response:
                if response.status >= 400:
                    raise LavalinkException(response.status)

                try:
                    session_model = Session._from_payload(await response.json())
                except Exception as e:
                    raise BuildException(e)

                return session_model


class RestPlayer:
    """
    !!! WARNING
        Please do not create this on your own. Please use the rest attribute, in the base ongaku object you created.
    """

    def __init__(self, ongaku: Ongaku) -> None:
        self._ongaku = ongaku

    async def fetch_all(self, session_id: str) -> t.Sequence[Player] | None:
        """
        Fetch all players

        Fetch all of the players in the current session.

        Parameters
        ----------
        session_id : str
            The Session ID that the players are attached too.

        Raises
        ------
        LavalinkException
            If an error code of 4XX or 5XX is received.
        BuildException
            Failure to build the player object.

        Returns
        -------
        typing.Sequence[Player]
            The players that are attached to the session.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self._ongaku._internal.base_uri
                + "/sessions/"
                + session_id
                + "/players",
                headers=self._ongaku._internal.headers,
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

    async def fetch(self, session_id: str, guild_id: hikari.Snowflake) -> Player | None:
        """
        Fetch a player.

        Fetch a specific player, for the specified Guild ID.

        Parameters
        ----------
        session_id : str
            The Session ID that the players are attached too.
        guild_id : hikari.Snowflake
            The Guild ID that the player is attached to.

        Raises
        ------
        LavalinkException
            If an error code of 4XX or 5XX is received.
        BuildException
            Failure to build the player object.

        Returns
        -------
        Player
            The player that was found for the specified guild.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self._ongaku._internal.base_uri
                + "/sessions/"
                + session_id
                + "/players/"
                + str(guild_id),
                headers=self._ongaku._internal.headers,
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
        filter: hikari.UndefinedNoneOr[Filter] = hikari.UNDEFINED,
        voice: hikari.UndefinedOr[PlayerVoice] = hikari.UNDEFINED,
        no_replace: bool = True,
    ) -> Player:
        """
        Update a player.

        Update a specific player, for the specified Guild ID.

        Parameters
        ----------
        session_id : str
            The Session ID that the players are attached too.
        guild_id : hikari.Snowflake
            The Guild ID that the player is attached to.
        track : hikari.UndefinedNoneOr[Track]
            The track you wish to set.
        position : hikari.UndefinedNoneOr[int]
            The new position for the track.
        end_time : hikari.UndefinedNoneOr[int]
            The end time for the track.
        volume : hikari.UndefinedNoneOr[int]
            The volume of the player.
        paused : hikari.UndefinedNoneOr[bool]
            Whether or not to pause the player.
        filter : hikari.UndefinedNoneOr[Filter]
            The filter you wish to set, or remove.
        voice : hikari.UndefinedNoneOr[PlayerVoice]
            The player voice object you wish to set.
        no_replace : bool
            Whether or not the track can be replaced.

        !!! INFO
            If no_replace is true, then setting a track to the track option, will not do anything.

        Raises
        ------
        LavalinkException
            If an error code of 4XX or 5XX is received.
        BuildException
            Failure to build the player object.

        Returns
        -------
        Player
            The player that was found for the specified guild.
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

        if filter != hikari.UNDEFINED:
            if filter is None:
                patch_data.update({"filters": None})
            else:
                patch_data.update({"filters": filter._build()})

        new_headers = self._ongaku._internal.headers.copy()

        new_headers.update({"Content-Type": "application/json"})

        params = {"noReplace": "false"}

        if no_replace:
            params.update({"noReplace": "true"})

        async with aiohttp.ClientSession() as session:
            try:
                async with session.patch(
                    self._ongaku._internal.base_uri
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
        Delete player

        Delete a specific player, from the specified guild.

        Parameters
        ----------
        session_id : str
            The Session ID that the players are attached too.
        guild_id : hikari.Snowflake
            The Guild ID that the player is attached to.

        Raises
        ------
        LavalinkException
            If an error code of 4XX or 5XX is received.
        """
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                self._ongaku._internal.base_uri
                + "/sessions/"
                + session_id
                + "/players/"
                + str(guild_id),
                headers=self._ongaku._internal.headers,
            ) as response:
                if response.status >= 400:
                    raise LavalinkException(response.status)


class RestTrack:
    """
    !!! WARNING
        Please do not create this on your own. Please use the rest attribute, in the base ongaku object you created.
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
        """
        Load tracks

        Load tracks to be able to play on a player.

        Parameters
        ----------
        query : str
            The query for a track/url
        platform : PlatformType
            The platform type for the query

        !!! INFO
            If the query is a url, it will use that to search. If not, it will use the [PlatformType][ongaku.enums.PlatformType] you set in the platform parameter.

        Raises
        ------
        LavalinkException
            If an error code of 4XX or 5XX is received.
        BuildException
            If it fails to build the [SearchResult][ongaku.abc.track.SearchResult], [Playlist][ongaku.abc.track.Playlist] or [Track][ongaku.abc.track.Track]

        Returns
        -------
        SearchResult
            If it was not a url, you will always receive this.
        Playlist
            If a playlist url is sent, you will receive this option.
        Track
            If a song/track url is sent, you will receive this option.
        """
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
                self._ongaku._internal.base_uri + "/loadtracks",
                headers=self._ongaku._internal.headers,
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
                        raise BuildException(e)

                    return search_result

                if load_type == "track":
                    try:
                        track = Track._from_payload(data["data"])
                    except Exception as e:
                        raise BuildException(e)

                    return track

                if load_type == "playlist":
                    try:
                        playlist = Playlist._from_payload(data["data"])
                    except Exception as e:
                        raise BuildException(e)

                    return playlist


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
