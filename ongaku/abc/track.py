import abc
import typing as t


class TrackInfo(abc.ABC):
    """
    Information about related track.
    """

    _identifier: str
    _is_seekable: bool
    _author: str
    _length: int
    _is_stream: bool
    _position: int
    _title: str
    _uri: t.Optional[str]
    _artwork_url: t.Optional[str]
    _isrc: t.Optional[str]
    _source_name: str

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


class Track(abc.ABC):
    """
    A track Object.
    """

    _encoded: str
    _info: TrackInfo
    _plugin_info: dict[t.Any, t.Any]
    _user_data: dict[t.Any, t.Any]

    @property
    def encoded(self) -> str:
        return self._encoded

    @property
    def info(self) -> TrackInfo:
        return self._info

    @property
    def plugin_info(self) -> dict[t.Any, t.Any]:
        return self._plugin_info

    @property
    def user_data(self) -> dict[t.Any, t.Any]:
        return self._user_data
