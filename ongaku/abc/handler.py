"""
Handler ABC's.

The handler abstract classes.
"""

import abc
import typing

if typing.TYPE_CHECKING:
    import hikari
    from ongaku.client import Client
    from ongaku.session import Session
    from ongaku.player import Player

class SessionHandler(abc.ABC):
    """
    Session handler base.

    The base session handler object.

    !!! note
        All custom session handlers **must** subclass this.

    Parameters
    ----------
    client
        The base ongaku client.
    """

    @abc.abstractmethod
    def __init__(self, client: Client): ...

    @property
    @abc.abstractmethod
    def sessions(self) -> typing.Sequence[Session]:
        """The sessions attached to this handler."""
        ...

    @property
    @abc.abstractmethod
    def players(self) -> typing.Sequence[Player]:
        """The players attached to this handler."""
        ...

    @property
    @abc.abstractmethod
    def is_alive(self) -> bool:
        """Whether the handler is alive or not."""
        ...

    @abc.abstractmethod
    async def start(self) -> None:
        """Start the session handler."""
        ...

    @abc.abstractmethod
    async def stop(self) -> None:
        """Stop the session handler."""
        ...

    @abc.abstractmethod
    def add_session(
        self, ssl: bool, host: str, port: int, password: str, attempts: int
    ) -> None:
        """Add a session."""
        ...

    @abc.abstractmethod
    def fetch_session(self) -> Session:
        """Return a valid session."""
        ...

    @abc.abstractmethod
    async def create_player(self, guild: hikari.SnowflakeishOr[hikari.Guild]) -> Player:
        """
        Create a player.

        Create a new player for this session.

        Parameters
        ----------
        guild
            The guild, or guild id you wish to delete the player from.
        """
        ...

    @abc.abstractmethod
    async def fetch_player(self, guild: hikari.SnowflakeishOr[hikari.Guild]) -> Player:
        """
        Fetch a player.

        Fetches an existing player.

        Parameters
        ----------
        guild
            The guild, or guild id you wish to delete the player from.

        Raises
        ------
        PlayerMissingException
            Raised when the player for the guild, does not exist.
        """
        ...

    @abc.abstractmethod
    async def delete_player(self, guild: hikari.SnowflakeishOr[hikari.Guild]) -> None:
        """
        Delete a player.

        Delete a pre-existing player.

        Parameters
        ----------
        guild
            The guild, or guild id you wish to delete the player from.

        Raises
        ------
        PlayerMissingException
            Raised when the player for the guild, does not exist.
        """
        ...