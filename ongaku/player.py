import hikari
from hikari.api import VoiceConnection, VoiceComponent
import typing as t

from . import models, error


class Player(VoiceConnection):
    @classmethod
    async def initialize(
        cls,
        channel_id: hikari.Snowflake,
        endpoint: str,
        guild_id: hikari.Snowflake,
        on_close,
        owner: VoiceComponent,
        session_id: str,
        shard_id: int,
        token: str,
        user_id: hikari.Snowflake,
        *,
        bot: hikari.GatewayBot,
        ongaku,
    ):
        init_player = Player(
            bot=bot,
            ongaku=ongaku,
            channel_id=channel_id,
            endpoint=endpoint,
            guild_id=guild_id,
            on_close=on_close,
            owner=owner,
            session_id=session_id,
            shard_id=shard_id,
            token=token,
            user_id=user_id,
            
        )

        return init_player

    def __init__(
        self,
        *,
        bot: hikari.GatewayBot,
        ongaku,
        channel_id: hikari.Snowflake,
        endpoint: str,
        guild_id: hikari.Snowflake,
        on_close,
        owner: VoiceComponent,
        session_id: str,
        shard_id: int,
        token: str,
        user_id: hikari.Snowflake,
    ) -> None:
        from .ongaku import Ongaku
        self._bot = bot
        self._ongaku: Ongaku = ongaku
        self._channel_id = channel_id
        self._endpoint = endpoint
        self._guild_id = guild_id
        self._on_close = on_close
        self._owner = owner
        self._session_id = session_id
        self._shard_id = shard_id
        self._token = token
        self._user_id = user_id



    @property
    def channel_id(self) -> hikari.Snowflake:
        """ID of the voice channel this voice connection is in."""
        return self._channel_id

    @property
    def guild_id(self) -> hikari.Snowflake:
        """ID of the guild this voice connection is in."""
        return self._guild_id

    @property
    def is_alive(self) -> bool:
        """Whether the connection is alive."""
        return self._is_alive

    @property
    def shard_id(self) -> int:
        """ID of the shard that requested the connection."""
        return self._shard_id

    @property
    def owner(self) -> VoiceComponent:
        """Return the component that is managing this connection."""
        return self._owner

    async def play(self, track: models.Track) -> None:
        voice = models.Voice(
            {
                "token": self._token,
                "endpoint": self._endpoint[6:],
                "sessionId": self._session_id,
            }
        )

        if self._ongaku._session_id == None:
            raise error.SessionNotStartedException()

        await self._ongaku.rest.internal.player.update_player(
            self.guild_id, self._ongaku._session_id, track=track, voice=voice
        )

    async def disconnect(self) -> None:
        """Signal the process to shut down."""
        print("disconnected?")
        self._is_alive = False
        pass

    async def join(self) -> None:
        """Wait for the process to halt before continuing."""
        print("joined?")

    async def notify(self, event: hikari.VoiceEvent) -> None:
        """Submit an event to the voice connection to be processed."""
        pass
