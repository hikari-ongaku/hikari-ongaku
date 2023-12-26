import abc
import typing as t


class Version(abc.ABC):
    """
    The version information of the Lavalink server.
    """

    def __init__(self, payload: dict[t.Any, t.Any]) -> None:
        self._semver = payload["semver"]
        self._major = payload["major"]
        self._minor = payload["minor"]
        self._patch = payload["patch"]
        self._pre_release = payload["preRelease"]

    _semver: str
    _major: int
    _minor: int
    _patch: int
    _pre_release: str

    @property
    def semver(self) -> str:
        return self._semver

    @property
    def major(self) -> int:
        return self._major

    @property
    def minor(self) -> int:
        return self._minor

    @property
    def patch(self) -> int:
        return self._patch

    @property
    def pre_release(self) -> str:
        return self._pre_release


class Git(abc.ABC):
    """
    The git information of the Lavalink server.
    """

    def __init__(self, payload: dict[t.Any, t.Any]) -> None:
        self._branch = payload["branch"]
        self._commit = payload["commit"]
        self._commit_time = payload["commitTime"]

    _branch: str
    _commit: str
    _commit_time: int

    @property
    def branch(self) -> str:
        return self._branch

    @property
    def commit(self) -> str:
        return self._commit

    @property
    def commit_time(self) -> int:
        return self._commit_time


class Plugin(abc.ABC):
    """
    The plugin information of the Lavalink server.
    """

    def __init__(self, payload: dict[t.Any, t.Any]) -> None:
        self._name = payload["name"]
        self._version = payload["version"]

    _name: str
    _version: int

    @property
    def name(self) -> str:
        return self._name

    @property
    def version(self) -> int:
        return self._version


class Info(abc.ABC):
    """
    The information about the lavalink server.
    """

    def __init__(self, payload: dict[t.Any, t.Any]) -> None:
        self._version = Version(payload["version"])
        self._build_time = payload["buildTime"]
        self._git = Git(payload["git"])
        self._jvm = payload["jvm"]
        self._lavaplayer = payload["lavaplayer"]
        self._source_managers = payload["sourceManager"]
        self._filters = payload["filters"]
        self._plugins = []

        payload_plugins = payload["plugins"]

        for plugin in payload_plugins:
            try:
                new_plugin = Plugin(plugin)
            except Exception as e:
                raise e

            self._plugins.append(new_plugin)

    _version: Version
    _build_time: int
    _git: Git
    _jvm: str
    _lavaplayer: str
    _source_managers: list[str]
    _filters: list[str]
    _plugins: list[Plugin]

    @property
    def version(self) -> Version:
        return self._version

    @property
    def build_time(self) -> int:
        return self._build_time

    @property
    def git(self) -> Git:
        return self._git

    @property
    def jvm(self) -> str:
        return self._jvm

    @property
    def lavaplayer(self) -> str:
        return self._lavaplayer

    @property
    def source_managers(self) -> list[str]:
        return self._source_managers

    @property
    def filters(self) -> list[str]:
        return self._filters

    @property
    def plugins(self) -> list[Plugin] | None:
        return self._plugins


class Error(abc.ABC):
    _timestamp: int
    _status: int
    _error: str
    _trace: t.Optional[str]
    _message: str
    _path: str

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @property
    def status(self) -> int:
        return self._status

    @property
    def error(self) -> str:
        return self._error

    @property
    def trace(self) -> t.Optional[str]:
        return self._trace

    @property
    def message(self) -> str:
        return self._message

    @property
    def path(self) -> str:
        return self._path
