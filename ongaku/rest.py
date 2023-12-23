from . import models, error, player
import typing as t

import hikari
import aiohttp
import logging
import json


class InternalSession:
    def __init__(self, ongaku) -> None:
        self._ongaku = ongaku

    async def update_session(self, session_id: str) -> models.Session:
        if session_id == None:
            raise error.SessionNotStartedException()

        async with aiohttp.ClientSession() as session:
            async with session.get(
                self._ongaku._default_uri + "/sessions/" + session_id,
                headers=self._ongaku._headers,
            ) as response:
                if response.status >= 400:
                    raise error.ResponseException(response.status)

                try:
                    session_model = models.Session(await response.json())
                except Exception as e:
                    raise error.BuildException(e)

                return session_model


class InternalPlayer:
    """
    The Rest based actions for the player.
    """

    def __init__(self, ongaku) -> None:
        self._ongaku = ongaku

    async def fetch_players(self, session_id: str) -> t.Optional[list[models.Player]]:
        if session_id == None:
            raise error.SessionNotStartedException()

        async with aiohttp.ClientSession() as session:
            async with session.get(
                self._ongaku._default_uri + "/sessions/" + session_id + "/players",
                headers=self._ongaku._headers,
            ) as response:
                if response.status >= 400:
                    raise error.ResponseException(response.status)

                players = await response.json()

                player_list: list[models.Player] = []

                for player in players:
                    try:
                        player_model = models.Player(player)
                    except Exception as e:
                        raise error.BuildException(e)

                    player_list.append(player_model)

        return player_list

    async def fetch_player(
        self, session_id: str, guild_id: hikari.Snowflake
    ) -> t.Optional[models.Player]:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self._ongaku._default_uri
                + "/sessions/"
                + session_id
                + "/players/"
                + str(guild_id),
                headers=self._ongaku._headers,
            ) as response:
                if response.status >= 400:
                    raise error.ResponseException(response.status)

                try:
                    player_model = models.Player(await response.json())
                except Exception as e:
                    raise error.BuildException(e)

        return player_model

    async def update_player(
        self,
        guild_id: hikari.Snowflake,
        session_id: str,
        *,
        track: hikari.UndefinedNoneOr[models.Track] = hikari.UNDEFINED,
        position: hikari.UndefinedOr[int] = hikari.UNDEFINED,
        end_time: hikari.UndefinedOr[int] = hikari.UNDEFINED,
        volume: hikari.UndefinedOr[int] = hikari.UNDEFINED,
        paused: hikari.UndefinedOr[bool] = hikari.UNDEFINED,
        voice: hikari.UndefinedOr[models.Voice] = hikari.UNDEFINED,
        no_replace: bool = True,
    ) -> models.Player:
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
        patch_data: dict = {}

        if track != hikari.UNDEFINED:
            if track == None:
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
            paused_str = "false"
            if paused:
                paused_str = "true"
            patch_data.update({"paused": paused})

        if voice != hikari.UNDEFINED:
            patch_data.update({"voice": voice.raw})

        new_headers = self._ongaku._headers.copy()

        new_headers.update({"Content-Type": "application/json"})

        params = {"noReplace": "false"}

        if no_replace:
            params.update({"noReplace": "false"})

        async with aiohttp.ClientSession() as session:
            try:
                async with session.patch(
                    self._ongaku._default_uri
                    + "/sessions/"
                    + session_id
                    + "/players/"
                    + str(guild_id),
                    headers=new_headers,
                    params=params,
                    json=patch_data,
                ) as response:
                    # if response.status >= 400:
                    #    raise error.ResponseException(response.status)

                    try:
                        player_model = models.Player(await response.json())
                    except Exception as e:
                        raise error.BuildException(e)
            except Exception as e:
                raise e

        return player_model

    async def delete_player(self, session_id: str, guild_id: hikari.Snowflake) -> None:
        """
        Creates a new player for the specified guild. If one already exists, returns that instead.
        """
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                self._ongaku._default_uri
                + "/sessions/"
                + session_id
                + "/players/"
                + str(guild_id),
                headers=self._ongaku._headers,
            ) as response:
                if response.status >= 400:
                    raise error.ResponseException(response.status)


class InternalTrack:
    """
    The rest based actions for the track.
    """

    def __init__(self, ongaku) -> None:
        from .ongaku import Ongaku  # this is probably a bad thing to do.

        self._ongaku: Ongaku = ongaku

    async def load_track(
        self, platform: models.PlatformType, query: str
    ) -> t.Optional[list[models.Track]]:
        async with aiohttp.ClientSession() as session:
            if platform == models.PlatformType.YOUTUBE:
                params = {"identifier": f'ytsearch:"{query}"'}
            elif platform == models.PlatformType.YOUTUBE_MUSIC:
                params = {"identifier": f'ytmsearch:"{query}"'}
            elif platform == models.PlatformType.SPOTIFY:
                params = {"identifier": f'scsearch:"{query}"'}
            else:
                params = {"identifier": f'scsearch:"{query}"'}

            async with session.get(
                self._ongaku._default_uri + "/loadtracks",
                headers=self._ongaku._headers,
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


class Internal:
    def __init__(self, ongaku) -> None:
        from .ongaku import Ongaku  # this is probably a bad thing to do.

        self._ongaku: Ongaku = ongaku

        self._internal_session = InternalSession(self._ongaku)

        self._internal_player = InternalPlayer(self._ongaku)

        self._internal_track = InternalTrack(self._ongaku)

    @property
    def session(self) -> InternalSession:
        return self._internal_session

    @property
    def player(self) -> InternalPlayer:
        return self._internal_player

    @property
    def track(self) -> InternalTrack:
        return self._internal_track


class RestApi:
    """
    The base rest class for all rest related things.
    """

    def __init__(self, ongaku) -> None:
        from .ongaku import Ongaku  # this is probably a bad thing to do.

        self._ongaku: Ongaku = ongaku

        self._internal = Internal(self._ongaku)

    @property
    def internal(self) -> Internal:
        return self._internal

    async def fetch_info(self) -> models.Info:
        """
        Fetch the information about the Lavalink server.

        ----
        Returns: Returns a
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self._ongaku._default_uri + "/info", headers=self._ongaku._headers
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
        return await self.internal.track.load_track(platform, query)
