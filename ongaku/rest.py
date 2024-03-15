"""
Rest client.

All REST based actions, happen in here.
"""

from __future__ import annotations

import asyncio
import enum
import typing as t

import hikari
import ujson

from .abc.statistics import Statistics

from .abc.filters import Filter
from .abc.lavalink import ExceptionError
from .abc.lavalink import Info
from .abc.lavalink import RestError
from .abc.player import Player
from .abc.player import PlayerVoice
from .abc.route_planner import RoutePlannerStatus
from .abc.session import Session
from .abc.playlist import Playlist
from .abc.track import Track
from .exceptions import BuildException
from .exceptions import LavalinkException
from .internal import Trace
from .internal import logger

_logger = logger.getChild("rest")

if t.TYPE_CHECKING:
    from .client import Client

RestT = t.TypeVar(
    "RestT",
    Info,
    Player,
    PlayerVoice,
    Session,
    Playlist,
    Track,
    RoutePlannerStatus,
    Statistics,
    str,
    dict[str, t.Any]
)

__all__ = ("RESTClient",)


class _HttpMethod(enum.Enum):
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    DELETE = "DELETE"


class RESTClient:
    """
    Base REST Client.

    The base REST client, for all rest related actions.

    !!! warning
        Please do not create this on your own. Please use the rest attribute, in the base client object you created.
    """

    def __init__(self, client: Client) -> None:
        self._client = client

        self._rest_track = RESTTrack(self)
        self._rest_player = RESTPlayer(self)
        self._rest_session = RESTSession(self)
        self._rest_route_planner = RESTRoutePlanner(self)

    @property
    def track(self) -> RESTTrack:
        """The track related rest actions."""
        return self._rest_track

    @property
    def player(self) -> RESTPlayer:
        """The player related rest actions."""
        return self._rest_player

    @property
    def session(self) -> RESTSession:
        """The session related rest actions."""
        return self._rest_session

    @property
    def route_planner(self) -> RESTRoutePlanner:
        """The route planner related rest actions."""
        return self._rest_route_planner

    async def version(self) -> str:
        """
        Get Lavalink version.

        Gets the current lavalink version.

        ![Lavalink](../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#get-lavalink-version)

        Raises
        ------
        LavalinkException
            Raise when a invalid response type is received.
        ValueError
            Raised when a return type is set, and no data was received.
        BuildException
            Raised when the object could not be built.

        Returns
        -------
        str
            The version, in string format.
        """
        _logger.log(Trace.LEVEL, f"running GET /version")

        resp = await self._handle_rest(
            "/version",
            _HttpMethod.GET,
            str,
            version=False,
        )

        if resp:
            return resp

        raise TypeError("Session update requires an object to be returned.")

    async def stats(self) -> Statistics:
        """
        Get server statistics.

        Gets the current Lavalink statistics.

        ![Lavalink](../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#get-lavalink-stats)

        !!! note
            frame_statistics will always be None.

        Raises
        ------
        LavalinkException
            Raise when a invalid response type is received.
        ValueError
            Raised when a return type is set, and no data was received.
        BuildException
            Raised when the object could not be built.

        Returns
        -------
        Statistics
            The Statistics object.
        """
        _logger.log(Trace.LEVEL, f"running GET /stats")

        resp = await self._handle_rest(
            "/stats",
            _HttpMethod.GET,
            Statistics,
        )

        if resp:
            return resp

        raise TypeError("Session update requires an object to be returned.")

    async def info(self) -> Info:
        """
        Get server statistics.

        Gets the current Lavalink statistics.

        ![Lavalink](../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#get-lavalink-info)

        Raises
        ------
        LavalinkException
            Raise when a invalid response type is received.
        ValueError
            Raised when a return type is set, and no data was received.
        BuildException
            Raised when the object could not be built.

        Returns
        -------
        Info
            The Info object.
        """
        _logger.log(Trace.LEVEL, f"running GET /info")

        resp = await self._handle_rest(
            "/info",
            _HttpMethod.GET,
            Info,
        )

        if resp:
            return resp

        raise TypeError("Session update requires an object to be returned.")

    @t.overload
    async def _handle_rest(
        self,
        url: str,
        method: _HttpMethod,
        return_type: t.Type[RestT] | None,
        *,
        headers: t.Mapping[str, t.Any] = {},
        json: t.Mapping[str, t.Any] | t.Sequence[t.Any] = {},
        params: t.Mapping[str, t.Any] = {},
        sequence: t.Literal[False] = False,
        version: bool = True
    ) -> RestT: ...

    @t.overload
    async def _handle_rest(
        self,
        url: str,
        method: _HttpMethod,
        return_type: t.Type[RestT] | None,
        *,
        headers: t.Mapping[str, t.Any] = {},
        json: t.Mapping[str, t.Any] | t.Sequence[t.Any] = {},
        params: t.Mapping[str, t.Any] = {},
        sequence: t.Literal[True] = True,
        version: bool = True
    ) -> t.Sequence[RestT]: ...

    async def _handle_rest(
        self,
        url: str,
        method: _HttpMethod,
        return_type: t.Type[RestT] | None,
        *,
        headers: t.Mapping[str, t.Any] = {},
        json: t.Mapping[str, t.Any] | t.Sequence[t.Any] = {},
        params: t.Mapping[str, t.Any] = {},
        sequence: bool = False,
        version: bool = True
    ) -> RestT | t.Sequence[RestT] | None:
        """
        Handle rest.

        Raises
        ------
        LavalinkException
            Raise when a invalid response type is received.
        ValueError
            Raised when a return type is set, and no data was received.
        BuildException
            Raised when the object could not be built.
        """
        session = await self._client._get_session()

        server = await self._client._session_handler.fetch_session()

        new_headers = server.base_headers.copy()

        new_headers.update(headers)

        server_version = ""
        if version:
            server_version = server.version.value

        try:
            async with session.request(
                method.value,
                server.base_uri + server_version + url,
                headers=new_headers,
                json=json,
                params=params,
            ) as response:
                _logger.log(
                    Trace.LEVEL,
                    f"Received code: {response.status} with response {await response.text()} on url {response.url}",
                )
                if response.status >= 400:
                    try:
                        payload = await response.text()
                    except Exception:
                        raise LavalinkException(
                            f"A {response.status} error has occurred."
                        )
                    else:
                        raise LavalinkException(RestError._from_payload(payload))

                if not return_type:
                    return

                try:
                    payload = await response.text()
                except Exception:
                    raise ValueError("Payload required for this response.")

                if issubclass(return_type, str):
                    return return_type(payload)
                
                if issubclass(return_type, dict):
                    return return_type(ujson.loads(payload))

                if sequence:
                    model_seq: list[t.Any] = []
                    for item in payload:
                        try:
                            model = return_type._from_payload(item)
                        except Exception as e:
                            raise BuildException(str(e))
                        else:
                            model_seq.append(model)

                    return model_seq
                else:
                    try:
                        model = return_type._from_payload(payload)
                    except Exception as e:
                        raise BuildException(str(e))
                    else:
                        return model
        except asyncio.TimeoutError:
            server._strike_server("Timeout")

        except Exception as e:
            server._strike_server(str(e))
            raise LavalinkException(e)


class RESTSession:
    """
    REST Session.

    !!! WARNING
        Please do not create this on your own. Please use the rest attribute, in the base client object you created.
    """

    def __init__(self, rest: RESTClient) -> None:
        self._rest = rest

    async def update(self, session_id: str) -> Session:
        """
        Update Lavalink session.

        Updates the lavalink session.

        ![Lavalink](../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#update-session)

        Raises
        ------
        LavalinkException
            Raise when a invalid response type is received.
        ValueError
            Raised when a return type is set, and no data was received.
        BuildException
            Raised when the object could not be built.

        Returns
        -------
        Session
            The Session object.
        """
        _logger.log(Trace.LEVEL, f"running PATCH /sessions/{session_id}")

        resp = await self._rest._handle_rest(
            "/sessions/" + session_id,
            _HttpMethod.PATCH,
            Session,
        )

        if resp:
            return resp

        raise TypeError("Session update requires an object to be returned.")


class RESTPlayer:
    """
    REST Player.

    !!! WARNING
        Please do not create this on your own. Please use the rest attribute, in the base client object you created.
    """

    def __init__(self, rest: RESTClient) -> None:
        self._rest = rest

    async def fetch_all(self, session_id: str) -> t.Sequence[Player] | None:
        """
        Fetch all players.

        Fetches all players on this session.

        ![Lavalink](../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#get-players)
        
        Parameters
        ----------
        session_id : str
            The Session ID that the players are attached too.
        
        Raises
        ------
        LavalinkException
            Raise when a invalid response type is received.
        ValueError
            Raised when a return type is set, and no data was received.
        BuildException
            Raised when the object could not be built.

        Returns
        -------
        typing.Sequence[Player]
            The Sequence of player objects.
        """
        _logger.log(Trace.LEVEL, f"running GET /sessions/{session_id}/players")

        resp = await self._rest._handle_rest(
            "/sessions/" + session_id + "/players",
            _HttpMethod.GET,
            Player,
            sequence=True,
        )

        if resp:
            return resp

        raise TypeError("fetch_all requires an object to be returned.")

    async def fetch(self, session_id: str, guild_id: hikari.Snowflake) -> Player | None:
        """
        Fetch a player.

        Fetches a specific player from this session.

        ![Lavalink](../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#get-player)
        
        Parameters
        ----------
        session_id : str
            The Session ID that the players are attached too.
        guild_id : hikari.Snowflake
            The Guild ID that the player is attached to.
        
        Raises
        ------
        LavalinkException
            Raise when a invalid response type is received.
        ValueError
            Raised when a return type is set, and no data was received.
        BuildException
            Raised when the object could not be built.

        Returns
        -------
        Player
            The player object.
        """
        _logger.log(
            Trace.LEVEL,
            f"running GET /sessions/{session_id}/players/{guild_id}",
        )

        resp = await self._rest._handle_rest(
            "/sessions/" + session_id,
            _HttpMethod.GET,
            Player,
        )

        if resp:
            return resp

        raise TypeError("fetch update requires an object to be returned.")

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
        Fetch a player.

        Fetches a specific player from this session.

        ![Lavalink](../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#update-player)
        
        !!! note
            Setting any value (except for `session_id`, or `guild_id`) to None, will set their values to None. To not modify them, do not set them to anything.

        Parameters
        ----------
        session_id : str
            The Session ID that the players are attached too.
        guild_id : hikari.Snowflake
            The Guild ID that the player is attached to.
        track : hikari.UndefinedNoneOr[Track]
            The track you wish to set, or remove
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
        
        Raises
        ------
        LavalinkException
            Raise when a invalid response type is received.
        ValueError
            Raised when a return type is set, and no data was received.
        ValueError
            Raised when nothing new has been set.
        BuildException
            Raised when the object could not be built.

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
            and filter is hikari.UNDEFINED
            and voice is hikari.UNDEFINED
            and position is hikari.UNDEFINED
        ):
            raise ValueError("Update requires at least one change.")

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

        params = {"noReplace": "false"}

        if no_replace:
            params.update({"noReplace": "true"})

        _logger.log(
            Trace.LEVEL,
            f"running PATCH /sessions/{session_id}/players/{guild_id} with params: {params} and json: {patch_data}",
        )

        resp = await self._rest._handle_rest(
            "/sessions/" + session_id + "/players/" + str(guild_id),
            _HttpMethod.PATCH,
            Player,
            headers={"Content-Type": "application/json"},
            json=patch_data,
            params=params,
        )

        if resp:
            return resp

        raise TypeError("fetch update requires an object to be returned.")

    async def delete(self, session_id: str, guild_id: hikari.Snowflake) -> None:
        """
        Delete a player.

        Deletes a specific player from this session.

        ![Lavalink](../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#destroy-player)
        
        Parameters
        ----------
        session_id : str
            The Session ID that the players are attached too.
        guild_id : hikari.Snowflake
            The Guild ID that the player is attached to.
        
        Raises
        ------
        LavalinkException
            Raise when a invalid response type is received.
        """
        _logger.log(
            Trace.LEVEL,
            f"running DELETE /sessions/{session_id}/players/{guild_id}",
        )

        await self._rest._handle_rest(
            "/sessions/" + session_id + "/players/" + str(guild_id),
            _HttpMethod.DELETE,
            None,
        )


class RESTTrack:
    """
    REST Track.

    !!! WARNING
        Please do not create this on your own. Please use the rest attribute, in the base client object you created.
    """

    def __init__(self, rest: RESTClient) -> None:
        self._rest = rest

    async def load(self, query: str) -> Playlist | t.Sequence[Track] | Track | None:
        """
        Load tracks.

        Loads tracks, from a site, or a link to a song, to play on a player.

        ![Lavalink](../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#track-loading)

        Parameters
        ----------
        query : str
            The query for the search/link.
        
        Raises
        ------
        LavalinkException
            Raise when a invalid response type is received.
        ValueError
            Raised when a return type is set, and no data was received.
        BuildException
            Raised when the object could not be built.

        Returns
        -------
        typing.Sequence[Track]
            A sequence of tracks (a search result)
        Playlist
            A Playlist object.
        Track
            A Track object.
        """
        params = {"identifier": query}

        _logger.log(Trace.LEVEL, f"running GET /loadtracks with params: {params}")

        resp = await self._rest._handle_rest(
            "/loadtracks",
            _HttpMethod.GET,
            dict,
            params=params
        )

        load_type: str = resp["loadType"]

        if load_type == "empty":
            _logger.log(Trace.LEVEL, f"loadType is empty.")
            return

        elif load_type == "error":
            _logger.log(Trace.LEVEL, f"loadType caused an error.")
            raise LavalinkException(
                ExceptionError._from_payload(ujson.dumps(resp["data"]))
            )

        elif load_type == "search":
            _logger.log(Trace.LEVEL, f"loadType was a search result.")
            tracks: t.Sequence[Track] = []
            for trk in resp["data"]:
                try:
                    track = Track._from_payload(ujson.dumps(trk))
                except Exception as e:
                    raise BuildException(str(e))
                else:
                    tracks.append(track)

            build = tracks

        elif load_type == "track":
            _logger.log(Trace.LEVEL, f"loadType was a track link.")
            build = Track._from_payload(ujson.dumps(resp["data"]))

        elif load_type == "playlist":
            _logger.log(Trace.LEVEL, f"loadType was a playlist link.")
            build = Playlist._from_payload(ujson.dumps(resp["data"]))

        else:
            raise Exception(f"An unknown loadType was received: {load_type}")

        return build

    async def decode(self, code: str) -> Track:
        """
        Decode a track.

        Decode a track from its encoded state.

        ![Lavalink](../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#track-decoding)
        
        Parameters
        ----------
        code : str
            The BASE64 code, from a previously encoded track.

        Raises
        ------
        LavalinkException
            Raise when a invalid response type is received.
        ValueError
            Raised when a return type is set, and no data was received.
        BuildException
            Raised when the object could not be built.

        Returns
        -------
        Track
            The Track object.
        """
        params = {"encodedTrack": code}

        _logger.log(Trace.LEVEL, f"running GET /decodetrack with params: {params}")

        resp = await self._rest._handle_rest(
            "/decodetrack",
            _HttpMethod.GET,
            Track,
        )

        return resp

    async def decode_many(self, codes: t.Sequence[str]) -> t.Sequence[Track]:
        """
        Decode multiple tracks.

        Decode multiple tracks from their encoded state.

        ![Lavalink](../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#track-decoding)
        
        Parameters
        ----------
        codes : typing.Sequence[str]
            The BASE64 codes, from all the previously encoded tracks.

        Raises
        ------
        LavalinkException
            Raise when a invalid response type is received.
        ValueError
            Raised when a return type is set, and no data was received.
        BuildException
            Raised when the object could not be built.

        Returns
        -------
        typing.Sequence[Track]
            The Track object.
        """
        _logger.log(Trace.LEVEL, f"running GET /decodetracks with json: {[*codes]}")

        resp = await self._rest._handle_rest(
            "/decodetracks",
            _HttpMethod.GET,
            Track,
            json=[*codes],
            sequence=True,
        )

        if resp:
            return resp

        raise TypeError("decode_many requires an object to be returned.")


class RESTRoutePlanner:
    """
    REST RoutePlanner.

    !!! WARNING
        Please do not create this on your own. Please use the rest attribute, in the base client object you created.
    """

    def __init__(self, rest: RESTClient) -> None:
        self._rest = rest

    async def status(self) -> RoutePlannerStatus:
        """
        Fetch routeplanner status.

        Fetches the routeplanner status.

        ![Lavalink](../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#get-routeplanner-status)
        
        Raises
        ------
        LavalinkException
            Raise when a invalid response type is received.
        ValueError
            Raised when a return type is set, and no data was received.
        BuildException
            Raised when the object could not be built.

        Returns
        -------
        RoutePlannerStatus
            The RoutePlannerStatus object.
        """
        _logger.log(Trace.LEVEL, f"running GET /routeplanner/status")

        resp = await self._rest._handle_rest(
            "/loadtracks",
            _HttpMethod.GET,
            RoutePlannerStatus,
        )

        return resp

    async def free(self, address: str) -> None:
        """
        Free routeplanner address.

        Free's the specified routeplanner address.

        ![Lavalink](../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#unmark-a-failed-address)
        
        Parameters
        ----------
        address : str
            The address you wish to free.
        
        Raises
        ------
        LavalinkException
            Raise when a invalid response type is received.
        """
        _logger.log(Trace.LEVEL, f"running POST /routeplanner/free/{address}")

        await self._rest._handle_rest(
            "/routeplanner/free/" + address,
            _HttpMethod.POST,
            None,
        )

    async def free_all(self) -> None:
        """
        Free all routeplanner addresses.

        Frees every blocked routeplanner address.

        ![Lavalink](../assets/lavalink_logo.png){ height="18" width="18"} [Reference](https://lavalink.dev/api/rest#unmark-all-failed-address)
        
        Raises
        ------
        LavalinkException
            Raise when a invalid response type is received.
        """
        _logger.log(Trace.LEVEL, f"running POST /routeplanner/free/all")

        await self._rest._handle_rest(
            "/routeplanner/free/all",
            _HttpMethod.POST,
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
