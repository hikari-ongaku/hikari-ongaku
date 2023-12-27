import typing as t
import dataclasses


@dataclasses.dataclass
class TrackInfo:
    """
    Track information

    All of the track information.

    Find out more [here](https://lavalink.dev/api/rest.html#track-info).

    Parameters
    ----------
    identifier : str
        The track identifier
    is_seekable : bool
        Whether the track is seekable
    author : str
        The track author
    length : int
        The track length in milliseconds
    is_stream : bool
        Whether the track is a stream
    title : str
        The track position in milliseconds
    source_name : str
        The track source name
    uri : str | None
        The track uri
    artwork_url : str | None
        The track artwork url
    isrc : str | None
        The track ISRC
    """

    identifier: str
    is_seekable: bool
    author: str
    length: int
    is_stream: bool
    position: int
    title: str
    source_name: str
    uri: t.Optional[str] = None
    artwork_url: t.Optional[str] = None
    isrc: t.Optional[str] = None
    

    @classmethod
    def as_payload(cls, payload: dict[t.Any, t.Any]):
        """
        Track info parser

        parse a payload of information, to receive a `TrackInfo` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        TrackInfo
            The Track Info you parsed.
        """
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

        return cls(
            identifier,
            is_seekable,
            author,
            length,
            is_stream,
            position,
            title,
            source_name,
            uri,
            artwork_url,
            isrc,
        )

    @property
    def raw(self) -> dict[str, t.Any]:
        return dataclasses.asdict(self)


@dataclasses.dataclass
class Track:
    """
    Track

    The base track object.

    Find out more [here](https://lavalink.dev/api/rest.html#track).

    Parameters
    ----------
    encoded : str
        The base64 encoded track data
    info : TrackInfo
        Information about the track
    plugin_info : dict[Any, Any]
        Additional track info provided by plugins
    user_data : dict[Any, Any]
        Additional track data.
    """

    encoded: str
    info: TrackInfo
    plugin_info: dict[t.Any, t.Any]
    user_data: dict[t.Any, t.Any]

    @classmethod
    def as_payload(cls, payload: dict[t.Any, t.Any]):
        """
        Track parser

        parse a payload of information, to receive a `Track` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        Track
            The Track you parsed.
        """
        encoded = payload["encoded"]
        info = TrackInfo.as_payload(payload["info"])
        plugin_info = payload["pluginInfo"]
        user_data = payload["userData"]

        return cls(encoded, info, plugin_info, user_data)

    @property
    def raw(self) -> dict[str, t.Any]:
        return dataclasses.asdict(self)
