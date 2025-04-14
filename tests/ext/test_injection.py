from __future__ import annotations

import typing

import arc
import hikari
import mock
import pytest

from ongaku import errors
from ongaku.client import Client
from ongaku.ext.injection import arc_ensure_player
from ongaku.player import Player

if typing.TYPE_CHECKING:
    from ongaku.session import Session


class TestArcEnsurePlayer:
    @pytest.mark.asyncio
    async def test_working(self, ongaku_client: Client, ongaku_session: Session):
        context: arc.GatewayContext = mock.Mock(guild_id=hikari.Snowflake(1234))
        with (
            mock.patch.object(
                context, "get_type_dependency", return_value=ongaku_client
            ) as patched_get_type_dependency,
            mock.patch(
                "ongaku.client.Client.fetch_player",
                return_value=Player(ongaku_session, context.guild_id),
            ) as patched_fetch_player,
        ):
            await arc_ensure_player(context)

            patched_get_type_dependency.assert_called_once_with(Client)

            patched_fetch_player.assert_called_once_with(context.guild_id)

    @pytest.mark.asyncio
    async def test_missing_guild_id(self):
        with pytest.raises(arc.GuildOnlyError):
            await arc_ensure_player(mock.Mock(guild_id=None))

    @pytest.mark.asyncio
    async def test_missing_dependency(self):
        context: arc.GatewayContext = mock.Mock(guild_id=hikari.Snowflake(1234))
        with (
            mock.patch.object(
                context, "get_type_dependency", side_effect=KeyError
            ) as patched_get_type_dependency,
            pytest.raises(errors.PlayerMissingError),
        ):
            await arc_ensure_player(context)

        patched_get_type_dependency.assert_called_once_with(Client)

    @pytest.mark.asyncio
    async def test_missing_player(self, ongaku_client: Client):
        context: arc.GatewayContext = mock.Mock(guild_id=hikari.Snowflake(1234))
        with (
            mock.patch.object(
                context, "get_type_dependency", return_value=ongaku_client
            ) as patched_get_type_dependency,
            mock.patch(
                "ongaku.client.Client.fetch_player",
                side_effect=errors.PlayerMissingError,
            ) as patched_fetch_player,
            pytest.raises(errors.PlayerMissingError),
        ):
            await arc_ensure_player(context)

        patched_get_type_dependency.assert_called_once_with(Client)

        patched_fetch_player.assert_called_once_with(context.guild_id)
