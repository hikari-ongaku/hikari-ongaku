import enum


class TrackSeverityType(str, enum.Enum):
    COMMON = "common"
    SUSPICIOUS = "suspicious"
    FAULT = "fault"


class TrackEndReasonType(str, enum.Enum):
    FINISHED = "finished"
    LOADFAILED = "loadFailed"
    STOPPED = "stopped"
    REPLACED = "replaced"
    CLEANUP = "cleanup"


class PlatformType(int, enum.Enum):
    YOUTUBE = 0
    YOUTUBE_MUSIC = 1
    SPOTIFY = 2


class VersionType(enum.Enum):
    V3 = "v3"
    V4 = "v4"

class ConnectionStatus(enum.Enum):
    FAILURE = 0
    """The bot has failed to connect to the lavalink server."""
    LOADING = 1
    """The bot has not yet attempted to connect to the server."""
    CONNECTED = 2
    """The bot has successfully connected to the lavalink server"""
