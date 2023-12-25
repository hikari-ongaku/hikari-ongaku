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
