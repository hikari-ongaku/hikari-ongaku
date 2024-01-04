import dataclasses
import typing as t

from .. import enums


@dataclasses.dataclass
class InfoVersion:
    """
    All of the Info Version information.

    Find out more [here](https://lavalink.dev/api/rest.html#version-object).

    Parameters
    ----------
    semver : str
        The full version string of this Lavalink server
    major : int
        The major version of this Lavalink server
    minor : int
        The minor version of this Lavalink server
    patch : int
        The patch version of this Lavalink server
    pre_release : str | None
        The pre-release version according to semver as a `.` separated list of identifiers
    build : str | None
        The build metadata according to semver as a `.` separated list of identifiers
    """

    semver: str
    major: int
    minor: int
    patch: int
    pre_release: t.Optional[str]
    build: t.Optional[str]

    @classmethod
    def as_payload(cls, payload: dict[t.Any, t.Any]):
        """
        Info Version parser

        parse a payload of information, to receive a `InfoVersion` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        InfoVersion
            The Info Version you parsed.
        """
        semver = payload["semver"]
        major = payload["major"]
        minor = payload["minor"]
        patch = payload["patch"]
        try:
            pre_release = payload["preRelease"]
        except Exception:
            pre_release = None
        try:
            build = payload["build"]
        except Exception:
            build = None

        return cls(semver, major, minor, patch, pre_release, build)

    @property
    def raw(self) -> dict[str, t.Any]:
        return dataclasses.asdict(self)


@dataclasses.dataclass
class InfoGit:
    """
    All of the Info Git information.

    Find out more [here](https://lavalink.dev/api/rest.html#git-object).

    Parameters
    ----------
    branch : str
        The branch this Lavalink server was built on
    commit : str
        The commit this Lavalink server was built on
    commit_time : int
        The millisecond unix timestamp for when the commit was created
    """

    branch: str
    commit: str
    commit_time: int

    @classmethod
    def as_payload(cls, payload: dict[t.Any, t.Any]):
        """
        Info Git parser

        parse a payload of information, to receive a `InfoGit` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        InfoGit
            The Info Git you parsed.
        """
        branch = payload["branch"]
        commit = payload["commit"]
        commit_time = payload["commitTime"]

        return cls(branch, commit, commit_time)

    @property
    def raw(self) -> dict[str, t.Any]:
        return dataclasses.asdict(self)


@dataclasses.dataclass
class InfoPlugin:
    """
    All of the Info Plugin information.

    Find out more [here](https://lavalink.dev/api/rest.html#plugin-object).

    Parameters
    ----------
    name : str
        The name of the plugin
    version : int
        The version of the plugin
    """

    name: str
    version: int

    @classmethod
    def as_payload(cls, payload: dict[t.Any, t.Any]):
        """
        Info Plugin parser

        parse a payload of information, to receive a `InfoPlugin` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        InfoPlugin
            The Info Plugin you parsed.
        """
        name = payload["name"]
        version = payload["version"]

        return cls(name, version)

    @property
    def raw(self) -> dict[str, t.Any]:
        return dataclasses.asdict(self)


@dataclasses.dataclass
class Info:
    """
    All of the Info Version information.

    Find out more [here](https://lavalink.dev/api/rest.html#version-object).

    Parameters
    ----------
    version : InfoVersion
        The version of this Lavalink server
    build_time : int
        The millisecond unix timestamp when this Lavalink jar was built
    git : InfoGit
        The git information of this Lavalink server
    jvm : str
        The JVM version this Lavalink server runs on
    lavaplayer : str
        The Lavaplayer version being used by this server
    source_managers : list[str]
        The enabled source managers for this server
    filters : list[str]
        The enabled filters for this server
    plugins : list[InfoPlugin]
        The enabled plugins for this server
    """

    version: InfoVersion
    build_time: int
    git: InfoGit
    jvm: str
    lavaplayer: str
    source_managers: list[str]
    filters: list[str]
    plugins: list[InfoPlugin]

    @classmethod
    def as_payload(cls, payload: dict[t.Any, t.Any]):
        """
        Info parser

        parse a payload of information, to receive a `Info` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        Info
            The Info you parsed.
        """
        version = InfoVersion.as_payload(payload["version"])
        build_time = payload["buildTime"]
        git = InfoGit.as_payload(payload["git"])
        jvm = payload["jvm"]
        lavaplayer = payload["lavaplayer"]
        source_managers = payload["sourceManager"]
        filters = payload["filters"]
        plugins: list[InfoPlugin] = []

        payload_plugins = payload["plugins"]

        for plugin in payload_plugins:
            try:
                new_plugin = InfoPlugin.as_payload(plugin)
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
class RestError:
    """
    All of the Rest Error information.

    This is the error that is formed, when a call to a rest method fails.
    Find out more [here](https://lavalink.dev/api/rest.html#error-responses).

    Parameters
    ----------
    timestamp : int
        The timestamp of the error in milliseconds since the Unix epoch
    status : int
        The HTTP status code
    error : str
        The HTTP status code message
    trace : str | None
        The stack trace of the error.
    message : str
        The error message
    path : str
        The request path
    """

    timestamp: int
    status: int
    error: str
    trace: t.Optional[str]
    message: str
    path: str

    @classmethod
    def as_payload(cls, payload: dict[t.Any, t.Any]):
        """
        Rest Error parser

        parse a payload of information, to receive a `RestError` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        Error
            The Error you parsed.
        """
        timestamp = payload["timestamp"]
        status = payload["status"]
        error = payload["error"]
        try:
            trace = payload["trace"]
        except Exception:
            trace = None
        message = payload["message"]
        path = payload["path"]

        return cls(timestamp, status, error, trace, message, path)

    @property
    def raw(self) -> dict[str, t.Any]:
        return dataclasses.asdict(self)


@dataclasses.dataclass
class ExceptionError:
    """
    All of the Exception Error information.

    Find out more [here](https://lavalink.dev/api/websocket.html#exception-object).

    Parameters
    ----------
    message : str
        The message of the exception
    severity : enums.LavalinkSeverityType
        The severity of the exception
    cause : str
        The cause of the exception

    """

    message: str
    severity: enums.SeverityType
    cause: str

    @classmethod
    def as_payload(cls, payload: dict[t.Any, t.Any]):
        """
        Exception Error parser

        parse a payload of information, to receive a `ExceptionError` dataclass.

        Parameters
        ----------
        payload : dict[Any, Any]
            The payload you wish to pass.

        Returns
        -------
        ExceptionError
            The Error you parsed.
        """
        message = payload["message"]
        severity = payload["severity"]
        cause = payload["cause"]

        return cls(message, severity, cause)
