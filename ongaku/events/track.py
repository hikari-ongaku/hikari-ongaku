import hikari
import typing as t
from .. import abc

class TrackStartEvent(abc.TrackStart, abc.OngakuEvent):
    """
    Called when a track starts!
    """

    def __init__(self, app: hikari.RESTAware, payload: dict[t.Any, t.Any]) -> None:
        self._app = app
        self._guild_id = payload["guild_id"]
        self._track = abc.Track.as_payload(payload["track"])

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
        self._track = abc.Track.as_payload(payload["track"])
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
        self._track = abc.Track.as_payload(payload["track"])
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
        self._track = abc.Track.as_payload(payload["track"])
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
