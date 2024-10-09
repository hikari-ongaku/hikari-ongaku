import mock
import pytest

from ongaku import Client
from ongaku import Session
from ongaku.ext import youtube as yt
from ongaku.rest import RESTClient


@pytest.mark.asyncio
async def test_fetch_youtube(ongaku_client: Client, ongaku_session: Session):
    rest = RESTClient(ongaku_client)

    with (
        mock.patch.object(rest._client, "_session_handler"),
        mock.patch.object(
            ongaku_session,
            "request",
            new_callable=mock.AsyncMock,
            return_value="refresh_token",
        ) as patched_request,
    ):
        assert await yt.fetch_youtube(ongaku_session) == "refresh_token"

        patched_request.assert_called_once_with(
            "GET",
            "/youtube",
            str,
        )


@pytest.mark.asyncio
async def test_update_youtube(ongaku_client: Client, ongaku_session: Session):
    rest = RESTClient(ongaku_client)

    # Test with payload
    with (
        mock.patch.object(rest._client, "_session_handler"),
        mock.patch.object(
            ongaku_session,
            "request",
            new_callable=mock.AsyncMock,
            return_value=None,
        ) as patched_request,
    ):
        await yt.update_youtube(
            ongaku_session,
            refresh_token="refresh_token",
            skip_initialization=False,
            po_token="po_token",
            visitor_data="visitor_data",
        )

        patched_request.assert_called_once_with(
            "POST",
            "/youtube",
            None,
            json={
                "refreshToken": "refresh_token",
                "skipInitialization": False,
                "poToken": "po_token",
                "visitorData": "visitor_data",
            },
        )
