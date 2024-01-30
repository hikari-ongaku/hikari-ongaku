"""The local server."""
from __future__ import annotations

import typing as t
import asyncio
import os
import json
from aiohttp.web_request import BaseRequest
from aiohttp import web


class URL(str):
    """URL of the track."""

    def __init__(self, url: str) -> None:
        self._url = url
        super().__init__()

    @property
    def url(self) -> str:
        """The url of the local file."""
        return self._url

class Server:
    """Local server.

    Parameters
    ----------
    host : str
        The host of the local audio server.
    port : int
        The port of the local audio server.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 5959):
        self._files: dict[str, URL] = {}

        self._task: asyncio.Task[t.Any] | None = None
        
        self._base_uri: str = f"http://{host}:{port}"

        self._host = host
        self._port = port

    async def _handler(self, request: BaseRequest):
        path = request.path.lstrip("/")
        track = self._files.get(path)

        if not track:
            return web.Response(
                status=404,
                content_type="application/json", 
                body=json.dumps({"response":"Track was not found."})
            )
        
        # Somehow feed lavalink the track.
        return web.FileResponse(path)

    async def start(self):
        """Start local server.
        
        Allows for starting the local server. (must be ran before the bot is started.)
        """
        server = web.Server(self._handler)
        runner = web.ServerRunner(server)
        await runner.setup()
        site = web.TCPSite(runner, self._host, self._port)
        self._task = asyncio.create_task(site.start())

    async def stop(self):
        """Stop the local server.
        
        Allow for deleting the local server.
        """
        if self._task:
            self._task.cancel()

    async def create(self, location: str) -> URL:
        """Create a file.
        
        Create a new track, with optional track information.

        !!! warning
            If a location is not added, then the server will not be able to receive the track. This is for privacy reasons.

        Parameters
        ----------
        location : str
            The location of the track. Must be the path, starting from the current location.
        
        Raises
        ------
        ValueError
            Raised when your location is not a valid track location.
        """
        track = self._files.get(location)

        if track:
            return track
        
        if not os.path.isfile(location):
            raise ValueError("Not a valid track to store.")

        url = URL(self._base_uri + "/" + location.replace(" ", "%20"))

        self._files.update({location:url})
        
        return url
    
    async def delete(self, location: str) -> None:
        """Create a file.
        
        Create a new track, with optional track information.

        !!! warning
            If a location is not added, then the server will not be able to receive the track. This is for privacy reasons.

        Parameters
        ----------
        location : str
            The location of the track. Must be the path, starting from the current location.
        """
        self._files.pop(location)

