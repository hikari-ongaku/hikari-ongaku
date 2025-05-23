from __future__ import annotations

import pytest


class TestBasicHandler:
    def test_properties(self):
        raise NotImplementedError

    @pytest.mark.asyncio
    async def test_start(self):
        raise NotImplementedError

    @pytest.mark.asyncio
    async def test_stop(self):
        raise NotImplementedError

    def test_add_session(self):
        raise NotImplementedError

    @pytest.mark.asyncio
    async def test_add_session_with_started_client(self):
        raise NotImplementedError

    def test_get_session(self):
        raise NotImplementedError

    def test_get_session_with_name(self):
        raise NotImplementedError

    def test_get_session_without_current_session(self):
        raise NotImplementedError

    def test_get_session_with_no_sessions(self):
        raise NotImplementedError

    @pytest.mark.asyncio
    async def test_delete_session(self):
        raise NotImplementedError

    @pytest.mark.asyncio
    async def test_delete_session_with_missing(self):
        raise NotImplementedError

    def test_add_player(self):
        raise NotImplementedError

    def test_add_player_without_missing(self):
        raise NotImplementedError

    def test_get_player(self):
        raise NotImplementedError

    def test_get_player_with_missing(self):
        raise NotImplementedError

    @pytest.mark.asyncio
    async def test_delete_player(self):
        raise NotImplementedError

    @pytest.mark.asyncio
    async def test_delete_player_with_missing(self):
        raise NotImplementedError
