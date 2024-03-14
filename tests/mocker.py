# ruff: noqa

from unittest.mock import AsyncMock
from unittest.mock import patch


def rest_handler_mocker():
    mock_client = AsyncMock()

    with patch("ongaku.rest.RESTClient._rest_handler") as mock_rest_handler:
        print(mock_rest_handler.call_args)
        print(mock_rest_handler.await_args)
        mock_response = "test"
        mock_rest_handler.return_value = mock_response

        with patch("aiohttp.ClientSession") as mock_session:
            mock_session.return_value.request.return_value.__aenter__.return_value.json.return_value = AsyncMock(
                return_value=mock_response
            )

    return mock_rest_handler

    mock_rest_handler.assert_called_once_with(
        "/info", mock_client._internal.headers, _HttpMethod.GET
    )
