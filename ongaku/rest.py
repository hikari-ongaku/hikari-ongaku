"""
Rest client.

All REST based actions, happen in here.
"""

from __future__ import annotations

import typing

import hikari

from ongaku import errors
from ongaku.internal import routes
from ongaku.internal.logger import TRACE_LEVEL
from ongaku.internal.logger import logger

if typing.TYPE_CHECKING:
    from ongaku.abc.info import Info
    from ongaku.abc.player import Player
    from ongaku.abc.player import Voice
    from ongaku.abc.playlist import Playlist
    from ongaku.abc.routeplanner import RoutePlannerStatus
    from ongaku.abc.session import Session as ABCSession
    from ongaku.abc.statistics import Statistics
    from ongaku.abc.track import Track

_logger = logger.getChild("rest")

if typing.TYPE_CHECKING:
    from ongaku.client import Client


__all__ = ("RESTClient",)


class RESTClient:
    """
    Base REST Client.

    The base REST client, for all rest related actions.

    !!! warning
        Please do not create this on your own. Please use the rest attribute, in the base client object you created.
    """

    def __init__(self, client: Client) -> None:
        self._client = client

    async def load_track(  # noqa: C901
        self, query: str
    ) -> Playlist | typing.Sequence[Track] | Track | None:
        """
        Load tracks.

        Loads tracks, from a site, or a link to a song, to play on a player.

        ![Lavalink](../assets/lavalink_logo.png){ .twemoji }  [Reference](https://lavalink.dev/api/rest#track-loading)

        Example
        -------
        ```py
        track = await client.rest.load_track("ytsearch:ajr")

        await player.play(track)
        ```

        Parameters
        ----------
        query
            The query for the search/link.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the request required a return type, but received nothing, or a 204 response.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the track, playlist or search could not be built.
        RestRequestError
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        typing.Sequence[Track]
            A sequence of tracks (a search result)
        Playlist
            A Playlist object.
        Track
            A Track object.
        """
        route = routes.GET_LOAD_TRACKS

        _logger.log(TRACE_LEVEL, str(route))

        session = self._client.session_handler.fetch_session()

        response = await session.request(
            route.method, route.path, dict, params={"identifier": query}
        )

        if response is None:
            raise ValueError("Response is required for this request.")

        load_type: str = response["loadType"]

        if load_type == "empty":
            _logger.log(TRACE_LEVEL, "loadType is empty.")
            return

        elif load_type == "error":
            _logger.log(TRACE_LEVEL, "loadType caused an error.")

            raise errors.RestExceptionError.from_error(
                self._client.entity_builder.build_exception_error(response["data"])
            )

        elif load_type == "search":
            _logger.log(TRACE_LEVEL, "loadType was a search result.")
            tracks: typing.Sequence[Track] = []
            for track in response["data"]:
                try:
                    tracks.append(self._client.entity_builder.build_track(track))
                except Exception as e:
                    raise errors.BuildError(str(e))

            build = tracks

        elif load_type == "track":
            _logger.log(TRACE_LEVEL, "loadType was a track link.")
            try:
                build = self._client.entity_builder.build_track(response["data"])
            except Exception as e:
                raise errors.BuildError(str(e))

        elif load_type == "playlist":
            _logger.log(TRACE_LEVEL, "loadType was a playlist link.")
            try:
                build = self._client.entity_builder.build_playlist(response["data"])
            except Exception as e:
                raise errors.BuildError(str(e))

        else:
            raise errors.BuildError(f"An unknown loadType was received: {load_type}")

        return build

    async def decode_track(self, track: str) -> Track:
        """
        Decode a track.

        Decode a track from its encoded state.

        ![Lavalink](../assets/lavalink_logo.png){ .twemoji }  [Reference](https://lavalink.dev/api/rest#track-decoding)

        Example
        -------
        ```py
        track = await client.rest.decode_track("BASE64")

        await player.play(track)
        ```

        Parameters
        ----------
        track
            The BASE64 code, from a previously encoded track.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the request required a return type, but received nothing, or a 204 response.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the track could not be built
        RestRequestError
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        Track
            The Track object.
        """
        route = routes.GET_DECODE_TRACK

        _logger.log(TRACE_LEVEL, str(route))

        session = self._client.session_handler.fetch_session()

        response = await session.request(
            route.method, route.path, dict, params={"encodedTrack": track}
        )

        if response is None:
            raise ValueError("Response is required for this request.")

        return self._client.entity_builder.build_track(response)

    async def decode_tracks(self, tracks: list[str]) -> typing.Sequence[Track]:
        """
        Decode multiple tracks.

        Decode multiple tracks from their encoded state.

        ![Lavalink](../assets/lavalink_logo.png){ .twemoji }  [Reference](https://lavalink.dev/api/rest#track-decoding)

        Example
        -------
        ```py
        tracks = await client.rest.decode_many_tracks(["BASE64_1", "BASE64_2"])

        await player.add(tracks)
        ```

        Parameters
        ----------
        tracks
            The BASE64 codes, from all the previously encoded tracks.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the request required a return type, but received nothing, or a 204 response.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the tracks could not be built.
        RestRequestError
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        typing.Sequence[Track]
            The Track object.
        """
        route = routes.POST_DECODE_TRACKS

        _logger.log(TRACE_LEVEL, str(route))

        session = self._client.session_handler.fetch_session()

        response = await session.request(
            route.method,
            route.path,
            list,
            headers={"Content-Type": "application/json"},
            json=tracks,
        )

        if response is None:
            raise ValueError("Response is required for this request.")

        new_tracks: list[Track] = []

        for track in response:
            new_tracks.append(self._client.entity_builder.build_track(track))

        return new_tracks

    async def fetch_players(self, session_id: str) -> typing.Sequence[Player]:
        """
        Fetch all players.

        Fetches all players on this session.

        ![Lavalink](../assets/lavalink_logo.png){ .twemoji }  [Reference](https://lavalink.dev/api/rest#get-players)

        Example
        -------
        ```py
        players = await client.rest.fetch_players(session_id)

        for player in players:
            print(player.guild_id)
        ```

        Parameters
        ----------
        session_id
            The Session ID that the players are attached too.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the request required a return type, but received nothing, or a 204 response.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the players could not be built.
        RestRequestError
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        typing.Sequence[Player]
            The Sequence of player objects.
        """
        route = routes.GET_PLAYERS

        _logger.log(TRACE_LEVEL, str(route))

        session = self._client.session_handler.fetch_session()

        response = await session.request(
            route.method,
            route.path.format(session_id=session_id),
            list,
        )

        if response is None:
            raise ValueError("Response is required for this request.")

        players: list[Player] = []

        for player in response:
            players.append(self._client.entity_builder.build_player(player))

        return players

    async def fetch_player(
        self, session_id: str, guild: hikari.SnowflakeishOr[hikari.Guild]
    ) -> Player:
        """
        Fetch a player.

        Fetches a specific player from this session.

        ![Lavalink](../assets/lavalink_logo.png){ .twemoji }  [Reference](https://lavalink.dev/api/rest#get-player)

        Example
        -------
        ```py
        player = await client.rest.fetch_player(session_id, guild_id)

        print(player.volume)
        ```

        Parameters
        ----------
        session_id
            The Session ID that the players are attached too.
        guild
            The Guild ID that the player is attached to.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the request required a return type, but received nothing, or a 204 response.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the player could not be built.
        RestRequestError
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        Player
            The player object.
        """
        route = routes.GET_PLAYER

        _logger.log(TRACE_LEVEL, str(route))

        session = self._client.session_handler.fetch_session()

        response = await session.request(
            route.method,
            route.path.format(session_id=session_id, guild_id=hikari.Snowflake(guild)),
            dict,
        )

        if response is None:
            raise ValueError("Response is required for this request.")

        return self._client.entity_builder.build_player(response)

    async def update_player(
        self,
        session_id: str,
        guild: hikari.SnowflakeishOr[hikari.Guild],
        *,
        track: hikari.UndefinedNoneOr[Track] = hikari.UNDEFINED,
        position: hikari.UndefinedOr[int] = hikari.UNDEFINED,
        end_time: hikari.UndefinedOr[int] = hikari.UNDEFINED,
        volume: hikari.UndefinedOr[int] = hikari.UNDEFINED,
        paused: hikari.UndefinedOr[bool] = hikari.UNDEFINED,
        voice: hikari.UndefinedOr[Voice] = hikari.UNDEFINED,
        no_replace: bool = True,
    ) -> Player:
        """
        Fetch a player.

        Fetches a specific player from this session.

        ![Lavalink](../assets/lavalink_logo.png){ .twemoji }  [Reference](https://lavalink.dev/api/rest#update-player)

        !!! note
            Setting any value (except for `session_id`, or `guild_id`) to None, will set their values to None.
            To not modify them, do not set them to anything.

        !!! warning
            If you do not set any value (not including `session_id` or `guild_id` as they are required) you will receive a `ValueError`

        Example
        -------
        ```py
        await client.rest.update_player(session_id, guild_id, paused=True)
        ```

        Parameters
        ----------
        session_id
            The Session ID that the players are attached too.
        guild
            The Guild ID that the player is attached to.
        track
            The track you wish to set, or remove
        position
            The new position for the track.
        end_time
            The end time for the track.
        volume
            The volume of the player.
        paused
            Whether or not to pause the player.
        voice
            The player voice object you wish to set.
        no_replace
            Whether or not the track can be replaced.

        Raises
        ------
        ValueError
            Raised when nothing new has been set.
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the request required a return type, but received nothing, or a 204 response.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the track, playlist or search could not be built.
        RestRequestError
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        Player
            The player object.
        """
        if (
            track is hikari.UNDEFINED
            and position is hikari.UNDEFINED
            and end_time is hikari.UNDEFINED
            and volume is hikari.UNDEFINED
            and paused is hikari.UNDEFINED
            and voice is hikari.UNDEFINED
            and position is hikari.UNDEFINED
        ):
            raise ValueError("Update requires at least one change.")

        patch_data: typing.MutableMapping[str, typing.Any] = {}

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
                        "endpoint": voice.endpoint,
                        "sessionId": voice.session_id,
                    }
                }
            )

        route = routes.PATCH_PLAYER_UPDATE

        _logger.log(
            TRACE_LEVEL,
            str(route),
        )

        session = self._client.session_handler.fetch_session()
        _logger.warning(patch_data)
        response = await session.request(
            route.method,
            route.path.format(session_id=session_id, guild_id=hikari.Snowflake(guild)),
            dict,
            headers={"Content-Type": "application/json"},
            json=patch_data,
            params={"noReplace": "true" if no_replace else "false"},
        )

        if response is None:
            raise ValueError("Response is required for this request.")

        return self._client.entity_builder.build_player(response)

    async def delete_player(
        self, session_id: str, guild: hikari.SnowflakeishOr[hikari.Guild]
    ) -> None:
        """
        Delete a player.

        Deletes a specific player from this session.

        ![Lavalink](../assets/lavalink_logo.png){ .twemoji }  [Reference](https://lavalink.dev/api/rest#destroy-player)

        Example
        -------
        ```py
        await client.rest.delete_player(session_id, guild_id)
        ```

        Parameters
        ----------
        session_id
            The Session ID that the players are attached too.
        guild
            The Guild ID that the player is attached to.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the request required a return type, but received nothing, or a 204 response.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        RestRequestError
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        RestError
            Raised when an unknown error is caught.
        """
        route = routes.DELETE_PLAYER

        _logger.log(TRACE_LEVEL, str(route))

        session = self._client.session_handler.fetch_session()

        await session.request(
            route.method,
            route.path.format(session_id=session_id, guild_id=hikari.Snowflake(guild)),
            None,
        )

    async def update_session(
        self,
        session_id: str,
        *,
        resuming: bool | None = None,
        timeout: int | None = None,
    ) -> ABCSession:
        """
        Update Lavalink session.

        Updates the lavalink session.

        ![Lavalink](../assets/lavalink_logo.png){ .twemoji }  [Reference](https://lavalink.dev/api/rest#update-session)

        Example
        -------
        ```py
        await client.rest.update_session(session_id)
        ```

        Parameters
        ----------
        session_id
            The session you wish to update.
        resuming
            Whether resuming is enabled for this session or not.
        timeout
            The timeout in seconds (default is 60s).

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the request required a return type, but received nothing, or a 204 response.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the session could not be built.
        RestRequestError
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        Session
            The Session object.
        """
        route = routes.PATCH_SESSION_UPDATE

        _logger.log(TRACE_LEVEL, str(route))

        session = self._client.session_handler.fetch_session()

        data: typing.MutableMapping[str, typing.Any] = {}

        if resuming is not None:
            data.update({"resuming": resuming})

        if timeout:
            data.update({"timeout": timeout})

        response = await session.request(
            route.method,
            route.path.format(session_id=session_id),
            dict,
            headers={"Content-Type": "application/json"},
            json=data,
        )

        if response is None:
            raise ValueError("Response is required for this request.")

        return self._client.entity_builder.build_session(response)

    async def fetch_info(self) -> Info:
        """
        Get server statistics.

        Gets the current Lavalink statistics.

        ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#get-lavalink-info)

        Example
        -------
        ```py
        info = await client.rest.fetch_info()

        print(info.version.semver)
        ```

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the request required a return type, but received nothing, or a 204 response.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the information could not be built.
        RestRequestError
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        Info
            The Info object.
        """
        route = routes.GET_INFO

        _logger.log(TRACE_LEVEL, str(route))

        session = self._client.session_handler.fetch_session()

        response = await session.request(
            route.method,
            route.path,
            dict,
        )

        if response is None:
            raise ValueError("Response is required for this request.")

        return self._client.entity_builder.build_info(response)

    async def fetch_version(self) -> str:
        """
        Get Lavalink version.

        Gets the current lavalink version.

        ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#get-lavalink-version)

        Example
        -------
        ```py
        version = await client.rest.fetch_version()

        print(version)
        ```

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the request required a return type, but received nothing, or a 204 response.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        RestRequestError
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        str
            The version, in string format.
        """
        route = routes.GET_VERSION

        _logger.log(TRACE_LEVEL, str(route))

        session = self._client.session_handler.fetch_session()

        response = await session.request(route.method, route.path, str, version=False)

        if response is None:
            raise ValueError("Response is required for this request.")

        return response

    async def fetch_stats(self) -> Statistics:
        """
        Get server statistics.

        Gets the current Lavalink statistics.

        ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#get-lavalink-stats)

        !!! note
            frame_statistics will always be `None`.

        Example
        -------
        ```py
        stats = await client.rest.fetch_stats()

        print(stats.players)
        ```

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the request required a return type, but received nothing, or a 204 response.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the statistics could not be built.
        RestRequestError
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        Statistics
            The Statistics object.
        """
        route = routes.GET_STATISTICS

        _logger.log(TRACE_LEVEL, str(route))

        session = self._client.session_handler.fetch_session()

        response = await session.request(
            route.method,
            route.path,
            dict,
        )

        if response is None:
            raise ValueError("Response is required for this request.")

        return self._client.entity_builder.build_statistics(response)

    async def fetch_routeplanner_status(self) -> RoutePlannerStatus | None:
        """
        Fetch routeplanner status.

        Fetches the routeplanner status.

        ![Lavalink](../assets/lavalink_logo.png){ .twemoji }  [Reference](https://lavalink.dev/api/rest#get-routeplanner-status)

        Example
        -------
        ```py
        routeplanner_status = await client.rest.fetch_routeplanner_status()

        print(routeplanner_status.class_type.name)
        ```

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the request required a return type, but received nothing, or a 204 response.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the routeplanner status could not be built.
        RestRequestError
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        RoutePlannerStatus
            The RoutePlannerStatus object.
        None
            The Route Planner for this server is not active.
        """
        route = routes.GET_ROUTEPLANNER_STATUS

        _logger.log(TRACE_LEVEL, str(route))

        session = self._client.session_handler.fetch_session()

        try:
            response = await session.request(
                route.method,
                route.path,
                dict,
            )
        except errors.RestEmptyError:
            response = None

        if response is None:
            return

        return self._client.entity_builder.build_routeplanner_status(response)

    async def update_routeplanner_address(self, address: str) -> None:
        """
        Free routeplanner address.

        Free's the specified routeplanner address.

        ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#unmark-a-failed-address)

        Example
        -------
        ```py
        await client.rest.update_routeplanner_address(address)
        ```

        Parameters
        ----------
        address
            The address you wish to free.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the request required a return type, but received nothing, or a 204 response.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        RestRequestError
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        RestError
            Raised when an unknown error is caught.
        """
        route = routes.POST_ROUTEPLANNER_FREE_ADDRESS

        _logger.log(TRACE_LEVEL, str(route))

        session = self._client.session_handler.fetch_session()

        await session.request(
            route.method,
            route.path,
            None,
        )

    async def update_all_routeplanner_addresses(self) -> None:
        """
        Free all routeplanner addresses.

        Frees every blocked routeplanner address.

        ![Lavalink](../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#unmark-all-failed-address)

        Example
        -------
        ```py
        await client.rest.update_all_routeplanner_addresses()
        ```

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the request required a return type, but received nothing, or a 204 response.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        RestRequestError
            Raised when a 4XX or a 5XX status is received, and lavalink gives more information.
        RestError
            Raised when an unknown error is caught.
        """
        route = routes.POST_ROUTEPLANNER_FREE_ALL

        _logger.log(TRACE_LEVEL, str(route))

        session = self._client.session_handler.fetch_session()

        await session.request(
            route.method,
            route.path,
            None,
        )


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
