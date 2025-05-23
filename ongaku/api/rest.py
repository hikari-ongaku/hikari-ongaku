# MIT License

# Copyright (c) 2023-present MPlatypus

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
"""Rest client for rest endpoint handling."""

from __future__ import annotations

import logging
import typing

import hikari

from ongaku import errors
from ongaku.internal import routes

if typing.TYPE_CHECKING:
    from ongaku import information
    from ongaku import player
    from ongaku import routeplanner
    from ongaku import session
    from ongaku import statistics
    from ongaku.api import builders
    from ongaku.client import Client
    from ongaku.playlist import Playlist
    from ongaku.track import Track

__all__: typing.Sequence[str] = ("RESTClient",)

_logger: typing.Final[logging.Logger] = logging.getLogger("ongaku.rest")


class RESTClient:
    """REST Client.

    The REST client, for all rest related actions.

    !!! warning
        Please do not create this on your own.
        Please use the rest attribute, in the base client object you created.
    """

    __slots__: typing.Sequence[str] = ("_client",)

    def __init__(self, client: Client) -> None:
        self._client = client

    async def load_track(
        self,
        query: str,
        *,
        session: session.ControllableSession | None = None,
    ) -> Playlist | typing.Sequence[Track] | Track | None:
        """Load track.

        Loads tracks, playlists or search from a site, for playing on a player.

        ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#track-loading)

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
        session
            If provided, the session to use for this request.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the response is 204, or 404.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the track, playlist or search could not be built.
        RestRequestError
            Raised when a request fails, but Lavalink has more information.
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
        None
            No result was returned.
        """
        route = routes.GET_LOAD_TRACKS.build()

        if not session:
            session = self._client.handler.get_session()

        response = await session.request(
            route,
            params={"identifier": query},
        )

        if not isinstance(response, typing.Mapping):
            raise TypeError(
                "Unexpected response type.",
            )  # FIXME: I am not sure I like this error.  # noqa: TD001, TD002, TD003

        load_type: str = response["loadType"]

        if load_type == "empty":
            return None

        if load_type == "error":
            raise self._client.builder.deserialize_exception_error(response["data"])

        if load_type == "search":
            return [
                self._client.builder.deserialize_track(track)
                for track in response["data"]
            ]

        if load_type == "track":
            return self._client.builder.deserialize_track(response["data"])

        if load_type == "playlist":
            return self._client.builder.deserialize_playlist(
                response["data"],
            )

        raise errors.BuildError(
            f"Unknown load type: `{load_type}`.",
        ) from None

    async def decode_track(
        self,
        track: str,
        /,
        *,
        session: session.ControllableSession | None = None,
    ) -> Track:
        """Decode track.

        Decode a track from its encoded state.

        ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#track-decoding)

        Example
        -------
        ```py
        track = await client.rest.decode_track(BASE64)

        await player.play(track)
        ```

        Parameters
        ----------
        track
            The BASE64 code, from a previously encoded track.
        session
            If provided, the session to use for this request.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the response is 204, or 404.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the track could not be built
        RestRequestError
            Raised when a request fails, but Lavalink has more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        Track
            The Track object.
        """
        route = routes.GET_DECODE_TRACK.build()

        if not session:
            session = self._client.handler.get_session()

        response = await session.request(
            route,
            params={"encodedTrack": track},
        )

        if not isinstance(response, typing.Mapping):
            raise TypeError("Unexpected response type.")

        return self._client.builder.deserialize_track(response)

    async def decode_tracks(
        self,
        tracks: typing.Sequence[str],
        *,
        session: session.ControllableSession | None = None,
    ) -> typing.Sequence[Track]:
        """Decode tracks.

        Decode multiple tracks from their encoded state.

        ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#track-decoding)

        Example
        -------
        ```py
        tracks = await client.rest.decode_tracks([BASE64_1, BASE64_2])

        await player.add(tracks)
        ```

        Parameters
        ----------
        tracks
            The BASE64 codes, from all the previously encoded tracks.
        session
            If provided, the session to use for this request.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the response is 204, or 404.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the tracks could not be built.
        RestRequestError
            Raised when a request fails, but Lavalink has more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        typing.Sequence[Track]
            The Track object.
        """
        route = routes.POST_DECODE_TRACKS.build()

        if not session:
            session = self._client.handler.get_session()

        response = await session.request(
            route,
            headers={"Content-Type": "application/json"},
            body=tracks,
        )

        if not isinstance(response, typing.Sequence):
            raise TypeError("Unexpected response type.")

        return [self._client.builder.deserialize_track(track) for track in response]

    async def fetch_player(
        self,
        session_id: str,
        guild: hikari.SnowflakeishOr[hikari.Guild],
        *,
        session: session.ControllableSession | None = None,
    ) -> player.Player:
        """Fetch player.

        Fetches a specific player from the specified session.

        ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#get-player)

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
            The `guild` or `guild id` that the player is attached to.
        session
            If provided, the session to use for this request.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the response is 204, or 404.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the player could not be built.
        RestRequestError
            Raised when a request fails, but Lavalink has more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        Player
            The player object.
        """
        route = routes.GET_PLAYER.build(
            session_id=session_id,
            guild_id=hikari.Snowflake(guild),
        )

        if not session:
            session = self._client.handler.get_session()

        response = await session.request(
            route,
        )

        if not isinstance(response, typing.Mapping):
            raise TypeError("Unexpected response type.")

        return self._client.builder.deserialize_player(response)

    async def fetch_players(
        self,
        session_id: str,
        *,
        session: session.ControllableSession | None = None,
    ) -> typing.Sequence[player.Player]:
        """Fetch players.

        Fetches all players from the specified session.

        ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#get-players)

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
        session
            If provided, the session to use for this request.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the response is 204, or 404.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the players could not be built.
        RestRequestError
            Raised when a request fails, but Lavalink has more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        typing.Sequence[Player]
            The Sequence of player objects.
        """
        route = routes.GET_PLAYERS.build(session_id=session_id)

        if not session:
            session = self._client.handler.get_session()

        response = await session.request(
            route,
        )

        if not isinstance(response, typing.Sequence):
            raise TypeError("Unexpected response type.")

        return [self._client.builder.deserialize_player(player) for player in response]

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
        filters: hikari.UndefinedNoneOr[builders.FiltersBuilder] = hikari.UNDEFINED,
        voice: hikari.UndefinedOr[player.Voice] = hikari.UNDEFINED,
        no_replace: bool = True,
        session: session.ControllableSession | None = None,
    ) -> player.Player:
        """Update player.

        Update a specific player from the specified session.

        ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#update-player)

        !!! tip
            Setting any value (except for `session_id`, or `guild_id`) to None,
            will set their values to None.
            To not modify them, do not set them to anything.

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
            The `guild` or `guild id` that the player is attached to.
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
        filters
            The filters to apply to the player.
        voice
            The player voice object you wish to set.
        no_replace
            Whether or not the track can be replaced.
        session
            If provided, the session to use for this request.

        Raises
        ------
        ValueError
            Raised when nothing new has been set,
            or when `session_id` or `guild_id` is missing.
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the response is 204, or 404.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the track, playlist or search could not be built.
        RestRequestError
            Raised when a request fails, but Lavalink has more information.
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
            and filters is hikari.UNDEFINED
            and voice is hikari.UNDEFINED
        ):
            raise ValueError("One or more of the undefined values must be set.")

        patch_data: typing.MutableMapping[str, typing.Any] = {}

        if track != hikari.UNDEFINED:
            if track is None:
                patch_data["track"] = {"encoded": None}
            else:
                track_data: dict[str, typing.Any] = {
                    "encoded": track.encoded,
                }

                user_data = dict(track.user_data)

                if track.requestor:
                    user_data["ongaku_requestor"] = str(track.requestor)

                track_data["userData"] = user_data

                patch_data["track"] = track_data

        if position != hikari.UNDEFINED:
            patch_data["position"] = position

        if end_time != hikari.UNDEFINED:
            patch_data["endTime"] = end_time

        if volume != hikari.UNDEFINED:
            patch_data["volume"] = volume

        if paused != hikari.UNDEFINED:
            patch_data["paused"] = paused

        if filters != hikari.UNDEFINED:
            if filters is None:
                patch_data["filters"] = None
            else:
                patch_data["filters"] = filters.build()

        if voice != hikari.UNDEFINED:
            patch_data["voice"] = self._client.builder.serialize_voice(voice)

        route = routes.PATCH_PLAYER_UPDATE.build(
            session_id=session_id,
            guild_id=hikari.Snowflake(guild),
        )

        if not session:
            session = self._client.handler.get_session()

        response = await session.request(
            route,
            headers={"Content-Type": "application/json"},
            body=patch_data,
            params={"noReplace": "true" if no_replace else "false"},
        )

        if not isinstance(response, typing.Mapping):
            raise TypeError("Unexpected response type.")

        return self._client.builder.deserialize_player(response)

    async def delete_player(
        self,
        session_id: str,
        guild: hikari.SnowflakeishOr[hikari.Guild],
        *,
        session: session.ControllableSession | None = None,
    ) -> None:
        """Delete player.

        Deletes a specific player from the specified session.

        ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#destroy-player)

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
            The `guild` or `guild id` that the player is attached to.
        session
            If provided, the session to use for this request.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the response is 204, or 404.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        RestRequestError
            Raised when a request fails, but Lavalink has more information.
        RestError
            Raised when an unknown error is caught.
        """
        route = routes.DELETE_PLAYER.build(
            session_id=session_id,
            guild_id=hikari.Snowflake(guild),
        )

        if not session:
            session = self._client.handler.get_session()

        await session.request(
            route,
        )

    async def update_session(
        self,
        session_id: str,
        *,
        resuming: bool | None = None,
        timeout: int | None = None,
        session: session.ControllableSession | None = None,
    ) -> session.Session:
        """Update Session.

        Update the lavalink session.

        ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#update-session)

        Example
        -------
        ```py
        await client.rest.update_session(session_id, False)
        ```

        Parameters
        ----------
        session_id
            The session you wish to update.
        resuming
            Whether resuming is enabled for this session or not.
        timeout
            The timeout in seconds (default is 60s)
        session
            If provided, the session to use for this request.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the response is 204, or 404.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the session could not be built.
        RestRequestError
            Raised when a request fails, but Lavalink has more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        Session
            The Session object.
        """
        route = routes.PATCH_SESSION_UPDATE.build(session_id=session_id)

        if not session:
            session = self._client.handler.get_session()

        data: typing.MutableMapping[str, typing.Any] = {}

        if resuming is not None:
            data.update({"resuming": resuming})

        if timeout:
            data.update({"timeout": timeout})

        response = await session.request(
            route,
            headers={"Content-Type": "application/json"},
            body=data,
        )

        if not isinstance(response, typing.Mapping):
            raise TypeError("Unexpected response type.")

        return self._client.builder.deserialize_session(response)

    async def fetch_info(
        self,
        *,
        session: session.ControllableSession | None = None,
    ) -> information.Information:
        """Fetch information.

        Fetches the current sessions information.

        ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#get-lavalink-info)

        Example
        -------
        ```py
        info = await client.rest.fetch_info()

        print(info.version.semver)
        ```

        Parameters
        ----------
        session
            If provided, the session to use for this request.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the response is 204, or 404.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the information could not be built.
        RestRequestError
            Raised when a request fails, but Lavalink has more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        Info
            The Info object.
        """
        route = routes.GET_INFO.build()

        if not session:
            session = self._client.handler.get_session()

        response = await session.request(route)

        if not isinstance(response, typing.Mapping):
            raise TypeError("Unexpected response type.")

        return self._client.builder.deserialize_information(response)

    async def fetch_version(
        self,
        *,
        session: session.ControllableSession | None = None,
    ) -> str:
        """Fetch version.

        Fetches the current Lavalink version.

        ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#get-lavalink-version)

        Example
        -------
        ```py
        version = await client.rest.fetch_version()

        print(version)
        ```

        Parameters
        ----------
        session
            If provided, the session to use for this request.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the response is 204, or 404.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        RestRequestError
            Raised when a request fails, but Lavalink has more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        str
            The version, in string format.
        """
        route = routes.GET_VERSION.build()

        if not session:
            session = self._client.handler.get_session()

        response = await session.request(route)

        if not isinstance(response, str):
            raise TypeError("Unexpected response type.")

        return response

    async def fetch_statistics(
        self,
        *,
        session: session.ControllableSession | None = None,
    ) -> statistics.Statistics:
        """Fetch statistics.

        Fetches the current Lavalink statistics.

        ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#get-lavalink-stats)

        !!! note
            frame_statistics will always be `None`.

        Example
        -------
        ```py
        stats = await client.rest.fetch_stats()

        print(stats.players)
        ```

        Parameters
        ----------
        session
            If provided, the session to use for this request.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the response is 204, or 404.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the statistics could not be built.
        RestRequestError
            Raised when a request fails, but Lavalink has more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        Statistics
            The Statistics object.
        """
        route = routes.GET_STATISTICS.build()

        if not session:
            session = self._client.handler.get_session()

        response = await session.request(route)

        if not isinstance(response, typing.Mapping):
            raise TypeError("Unexpected response type.")

        return self._client.builder.deserialize_statistics(response)

    async def fetch_routeplanner_status(
        self,
        *,
        session: session.ControllableSession | None = None,
    ) -> routeplanner.RoutePlannerStatus | None:
        """Fetch routeplanner status.

        Fetches the routeplanner status of the current session.

        ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#get-routeplanner-status)

        Example
        -------
        ```py
        routeplanner_status = await client.rest.fetch_routeplanner_status()

        if routeplanner_status:
            print(routeplanner_status.class_type.name)
        ```

        Parameters
        ----------
        session
            If provided, the session to use for this request.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the response is 204, or 404.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        BuildError
            Raised when the routeplanner status could not be built.
        RestRequestError
            Raised when a request fails, but Lavalink has more information.
        RestError
            Raised when an unknown error is caught.

        Returns
        -------
        RoutePlannerStatus
            The RoutePlannerStatus object.
        None
            The Route Planner for this server is not active.
        """
        route = routes.GET_ROUTEPLANNER_STATUS.build()

        if not session:
            session = self._client.handler.get_session()

        try:
            response = await session.request(route)
        except errors.RestEmptyError:
            return None

        if not isinstance(response, typing.Mapping):
            raise TypeError("Unexpected response type.")

        return self._client.builder.deserialize_routeplanner_status(response)

    async def update_routeplanner_address(
        self,
        address: str,
        *,
        session: session.ControllableSession | None = None,
    ) -> None:
        """Free routeplanner address.

        Free's the specified routeplanner address.

        ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#unmark-a-failed-address)

        Example
        -------
        ```py
        await client.rest.update_routeplanner_address(address)
        ```

        Parameters
        ----------
        address
            The address you wish to free.
        session
            If provided, the session to use for this request.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the response is 204, or 404.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        RestRequestError
            Raised when a request fails, but Lavalink has more information.
        RestError
            Raised when an unknown error is caught.
        """
        route = routes.POST_ROUTEPLANNER_FREE_ADDRESS.build()

        if not session:
            session = self._client.handler.get_session()

        await session.request(route, body={"address": address})

    async def update_all_routeplanner_addresses(
        self,
        *,
        session: session.ControllableSession | None = None,
    ) -> None:
        """Free all routeplanner addresses.

        Frees every blocked routeplanner address.

        ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/rest#unmark-all-failed-address)

        Example
        -------
        ```py
        await client.rest.update_all_routeplanner_addresses()
        ```

        Parameters
        ----------
        session
            If provided, the session to use for this request.

        Raises
        ------
        NoSessionsError
            Raised when there is no available sessions for this request to take place.
        TimeoutError
            Raised when the request takes too long to respond.
        RestEmptyError
            Raised when the response is 204, or 404.
        RestStatusError
            Raised when a 4XX or a 5XX status is received.
        RestRequestError
            Raised when a request fails, but Lavalink has more information.
        RestError
            Raised when an unknown error is caught.
        """
        route = routes.POST_ROUTEPLANNER_FREE_ALL.build()

        if not session:
            session = self._client.handler.get_session()

        await session.request(
            route,
        )
