import abc
import typing as t
import dataclasses

@dataclasses.dataclass
class TrackInfo:
    """
    Information about related track.
    """

    identifier: str
    is_seekable: bool
    author: str
    length: int
    is_stream: bool
    position: int
    title: str
    uri: t.Optional[str]
    artwork_url: t.Optional[str]
    isrc: t.Optional[str]
    source_name: str

    @classmethod
    def as_payload(cls, payload: dict[t.Any, t.Any]):
        identifier = payload["identifier"]
        is_seekable = payload["isSeekable"]
        author = payload["author"]
        length = payload["length"]
        is_stream = payload["isStream"]
        position = payload["position"]
        title = payload["title"]
        try:  # TODO: This needs to be switched to actually check if it exists first, and if it doesn't set it as none.
            uri = payload["uri"]
        except:
            uri = None
        try:
            artwork_url = payload["artworkUrl"]
        except:
            artwork_url = None
        try:
            isrc = payload["isrc"]
        except:
            isrc = None
        source_name = payload["sourceName"]

        return cls(identifier, is_seekable, author, length, is_stream, position, title, uri, artwork_url, isrc, source_name)
    
    @property
    def raw(self) -> dict[str, t.Any]:
        return dataclasses.asdict(self)

@dataclasses.dataclass
class Track(abc.ABC):
    """
    A track Object.
    """

    encoded: str
    info: TrackInfo
    plugin_info: dict[t.Any, t.Any]
    user_data: dict[t.Any, t.Any]

    @classmethod
    def as_payload(cls, payload: dict[t.Any, t.Any]):
        encoded = payload["identifier"]
        info = TrackInfo.as_payload(payload["info"])
        plugin_info = payload["pluginInfo"]
        user_data = payload["userData"]

        return cls(encoded, info, plugin_info, user_data)
    
    @property
    def raw(self) -> dict[str, t.Any]:
        return dataclasses.asdict(self)
