import typing as t
import enum as e

class TrackSeverityType(e.Enum):
    COMMON = "common"
    SUSPICIOUS = "suspicious"
    FAULT = "fault"

class TrackEndReasonType(e.Enum):
    FINISHED = "finished"
    LOADFAILED = "loadFalied"
    STOPPED = "stopped"
    REPLACED = "replaced"
    CLEANUP = "cleanup"


class TrackInfo:
    """
    Information about related track.
    """
    def __init__(self, data: dict) -> None:
        self._identifier = data["identifier"]
        self._is_seekable = data["isSeekable"]
        self._author = data["author"]
        self._length = data["length"]
        self._is_stream = data["isStream"]
        self._position = data["position"]
        self._title = data["title"]
        self._uri = data["uri"]
        self._artwork_url = data["artworkUrl"]
        self._isrc = data["isrc"]
        self._source_name = data["sourceName"]

    @property
    def identifier(self) -> str:
        return self._identifier

    @property
    def is_seekable(self) -> bool:
        return self._is_seekable

    @property
    def author(self) -> str:
        return self._author

    @property
    def length(self) -> int:
        return self._length

    @property
    def is_stream(self) -> bool:
        return self._is_stream

    @property
    def position(self) -> int:
        return self._position

    @property
    def title(self) -> str:
        return self._title

    @property
    def uri(self) -> t.Optional[str]:
        return self._uri

    @property
    def artwork_url(self) -> t.Optional[str]:
        return self._artwork_url

    @property
    def isrc(self) -> t.Optional[str]:
        return self._isrc

    @property
    def source_name(self) -> str:
        return self._source_name

class Track:
    """
    A track Object.
    """
    def __init__(self, data: dict) -> None:
        self._encoded = data["encoded"]

        self._track = TrackInfo(data["info"])

        self._plugin_info = data["pluginInfo"]

        self._user_data = data["userData"]

    @property
    def encoded(self) -> str:
        return self._encoded

    @property
    def track(self) -> TrackInfo:
        return self._track

    @property
    def plugin_info(self) -> dict:
        return self._plugin_info

    @property
    def user_data(self) -> dict:
        return self._user_data

class TrackStart:
    def __init__(self, data: dict) -> None:
        self._track = Track(data["track"])

    @property
    def track(self) -> Track:
        return self._track

class TrackEnd:
    def __init__(self, data: dict) -> None:
        self._track = Track(data["track"])

        self._reason = TrackEndReasonType(data["reason"])

    @property
    def track(self) -> Track:
        return self._track

    @property
    def reason(self) -> TrackEndReasonType:
        return self._reason

class TrackExceptionException:
    def __init__(self, data: dict) -> None:
        self._message = data["message"]
        self._severity = TrackSeverityType(data["severity"])
        self._cause = data["cause"]

    @property
    def message(self) -> str:
        return self._message

    @property
    def severity(self) -> TrackSeverityType:
        return self._severity

    @property
    def cause(self) -> str:
        return self._cause

class TrackException:
    def __init__(self, data: dict) -> None:
        self._track = Track(data["track"])

        self._exception = TrackExceptionException(data["exception"])

    @property
    def track(self) -> Track:
        return self._track

    @property
    def exception(self) -> TrackExceptionException:
        return self._exception

class TrackStuck:
    def __init__(self, data: dict) -> None:
        self._track = Track(data["track"])

        self._threshold_ms = data["thresholdMs"]

    @property
    def track(self) -> Track:
        return self._track

    @property
    def threshold_ms(self) -> int:
        return self._threshold_ms