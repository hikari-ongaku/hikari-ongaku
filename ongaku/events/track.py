import hikari
import typing as t
from .. import abc


class TrackInfo(abc.TrackInfo):
    def __init__(self, payload: dict[t.Any, t.Any]) -> None:
        self._identifier = payload["identifier"]
        self._is_seekable = payload["isSeekable"]
        self._author = payload["author"]
        self._length = payload["length"]
        self._is_stream = payload["isStream"]
        self._position = payload["position"]
        self._title = payload["title"]
        try:  # TODO: This needs to be switched to actually check if it exists first, and if it doesn't set it as none.
            self._uri = payload["uri"]
        except:
            self._uri = None
        try:
            self._artwork_url = payload["artworkUrl"]
        except:
            self._artwork_url = None
        try:
            self._isrc = payload["isrc"]
        except:
            self._isrc = None
        self._source_name = payload["sourceName"]


class Track(abc.Track):
    def __init__(self, payload: dict[t.Any, t.Any]) -> None:
        self._encoded = payload["encoded"]
        self._info = TrackInfo(payload["track"])
        self._plugin_info = payload["pluginInfo"]
        self._user_data = payload["userData"]


class TrackStartEvent(abc.TrackStart, abc.OngakuEvent):
    """
    Called when a track starts!
    """

    def __init__(self, app: hikari.RESTAware, payload: dict[t.Any, t.Any]) -> None:
        self._app = app
        self._guild_id = payload["guild_id"]
        self._track = Track(payload["track"])

    @property
    def app(self):
        return self._app

    @property
    def guild_id(self):
        return self._guild_id

    @property
    def track(self):
        return self._track


class TrackEndEvent(abc.TrackEnd, abc.OngakuEvent):
    """
    Called when a track starts!
    """

    def __init__(self, app: hikari.RESTAware, payload: dict[t.Any, t.Any]) -> None:
        self._app = app
        self._guild_id = payload["guild_id"]
        self._track = Track(payload["track"])
        self._reason = payload["reason"]

    @property
    def app(self):
        return self._app

    @property
    def guild_id(self):
        return self._guild_id

    @property
    def track(self):
        return self._track

    @property
    def reason(self):
        return self._reason


class TrackExceptionEvent(abc.TrackException, abc.OngakuEvent):
    """
    Called when a track starts!
    """

    def __init__(self, app: hikari.RESTAware, payload: dict[t.Any, t.Any]) -> None:
        self._app = app
        self._guild_id = payload["guild_id"]
        self._track = Track(payload["track"])
        self._reason = payload["reason"]

    @property
    def app(self):
        return self._app

    @property
    def guild_id(self):
        return self._guild_id

    @property
    def track(self):
        return self._track

    @property
    def reason(self):
        return self._reason


class TrackStuckEvent(abc.TrackStuck, abc.OngakuEvent):
    """
    Called when a track starts!
    """

    def __init__(self, app: hikari.RESTAware, payload: dict[t.Any, t.Any]) -> None:
        self._app = app
        self._guild_id = payload["guild_id"]
        self._track = Track(payload["track"])
        self._threshold_ms = payload["thresholdMs"]

    @property
    def app(self):
        return self._app

    @property
    def guild_id(self):
        return self._guild_id

    @property
    def track(self):
        return self._track

    @property
    def threshold_ms(self):
        return self._threshold_ms
