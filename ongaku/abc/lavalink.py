import abc
import dataclasses
import typing as t


@dataclasses.dataclass
class Version:
    """
    The version information of the Lavalink server.
    """

    semver: str
    major: int
    minor: int
    patch: int
    pre_release: str

    @classmethod
    def as_payload(cls, payload: dict[t.Any, t.Any]):
        semver = payload["semver"]
        major = payload["major"]
        minor = payload["minor"]
        patch = payload["patch"]
        pre_release = payload["preRelease"]

        return cls(semver, major, minor, patch, pre_release)

    @property
    def raw(self) -> dict[str, t.Any]:
        return dataclasses.asdict(self)


@dataclasses.dataclass
class Git:
    """
    The git information of the Lavalink server.
    """

    branch: str
    commit: str
    commit_time: int

    @classmethod
    def as_payload(cls, payload: dict[t.Any, t.Any]):
        branch = payload["branch"]
        commit = payload["commit"]
        commit_time = payload["commitTime"]

        return cls(branch, commit, commit_time)

    @property
    def raw(self) -> dict[str, t.Any]:
        return dataclasses.asdict(self)


@dataclasses.dataclass
class Plugin:
    """
    The plugin information of the Lavalink server.
    """

    name: str
    version: int

    @classmethod
    def as_payload(cls, payload: dict[t.Any, t.Any]):
        name = payload["name"]
        version = payload["version"]

        return cls(name, version)

    @property
    def raw(self) -> dict[str, t.Any]:
        return dataclasses.asdict(self)


@dataclasses.dataclass
class Info(abc.ABC):
    """
    The information about the lavalink server.
    """

    version: Version
    build_time: int
    git: Git
    jvm: str
    lavaplayer: str
    source_managers: list[str]
    filters: list[str]
    plugins: list[Plugin]

    @classmethod
    def as_payload(cls, payload: dict[t.Any, t.Any]):
        version = Version.as_payload(payload["version"])
        build_time = payload["buildTime"]
        git = Git.as_payload(payload["git"])
        jvm = payload["jvm"]
        lavaplayer = payload["lavaplayer"]
        source_managers = payload["sourceManager"]
        filters = payload["filters"]
        plugins: list[Plugin] = []

        payload_plugins = payload["plugins"]

        for plugin in payload_plugins:
            try:
                new_plugin = Plugin.as_payload(plugin)
            except Exception as e:
                raise e

            plugins.append(new_plugin)

        return cls(
            version, build_time, git, jvm, lavaplayer, source_managers, filters, plugins
        )

    @property
    def raw(self) -> dict[str, t.Any]:
        return dataclasses.asdict(self)


@dataclasses.dataclass
class Error(abc.ABC):
    timestamp: int
    status: int
    error: str
    trace: t.Optional[str]
    message: str
    path: str

    @classmethod
    def as_payload(cls, payload: dict[t.Any, t.Any]):
        timestamp = payload["timestamp"]
        status = payload["status"]
        error = payload["error"]
        try:
            trace = payload["trace"]
        except:
            trace = None
        message = payload["message"]
        path = payload["path"]

        return cls(timestamp, status, error, trace, message, path)

    @property
    def raw(self) -> dict[str, t.Any]:
        return dataclasses.asdict(self)
