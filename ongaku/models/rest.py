from .. import error
import enum as e

class PlatformType(e.Enum):
    YOUTUBE = 0
    YOUTUBE_MUSIC = 1
    SPOTIFY = 2

class Version:
    """
    The version information of the Lavalink server.
    """
    def __init__(self, data: dict) -> None:
        self._semver = data["semver"]
        self._major = data["major"]
        self._minor = data["minor"]
        self._patch = data["patch"]
        self._pre_release = data["preRelease"]

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

class Git:
    """
    The git information of the Lavalink server.
    """
    def __init__(self, data: dict) -> None:
        self._branch = data["branch"]
        self._commit = data["commit"]
        self._commit_time = data["commitTime"]

    @property
    def branch(self) -> str:
        return self._branch
    
    @property
    def commit(self) -> str:
        return self._commit
    
    @property
    def commit_time(self) -> int:
        return self._commit_time

class Plugin:
    """
    The plugin information of the Lavalink server.
    """
    def __init__(self, data: dict) -> None:
        self._name = data["name"]
        self._version = data["version"]
    
    @property
    def name(self) -> int:
        return self._name
    
    @property
    def version(self) -> int:
        return self._version

class Info:
    """
    The information about the lavalink server.
    """

    def __init__(self, data: dict) -> None:
        self._version = Version(data["version"])
        self._build_time = int(data["buildTime"])
        self._git = Git(data["git"])
        self._jvm = str(data["jvm"])
        self._lavaplayer = str(data["lavaplayer"])
        self._source_managers: list[str] = data["sourceManagers"]
        self._filters: list[str] = data["filters"]

        plugins: list[dict] = data["plugins"]

        if plugins == None:
            self._plugins = None

        else:
            self._plugins = []
            for plugin in plugins:
                new_plugin = Plugin(plugin)

                self._plugins.append(new_plugin)
        

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
