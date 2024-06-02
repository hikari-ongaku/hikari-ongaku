# Ongaku
A voice library for Hikari.

<div align="center">

[![PyPI](https://img.shields.io/pypi/v/hikari-ongaku)](https://pypi.org/project/hikari-ongaku)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)
![Pyright](https://badgen.net/badge/Pyright/strict/2A6DB2)
[![Lavalink](https://badgen.net/badge/Lavalink/V4/ff624a)](https://lavalink.dev/)

</div>

This is a library, written in asynchronous python, that is designed to take a lavalink server connection, and allow for users, to be able to play music using [hikari](https://hikari-py.dev/).


### More Information

Please check out the [docs](https://ongaku.mplaty.com/), and also checkout the [examples](https://github.com/MPlatypus/hikari-ongaku/tree/main/examples) to get started.


### Features
 - Player control
    - Playlists
    - Queuing
        - Adding songs.
        - Shuffling the queue.
        - Skipping a song or multiple.
        - Deleting via position, or a track object.
        - Clearing the queue.
    - Seeking/Reversing the tracks position.
    - Volume control
    - Setting requestors (users who requested the song.)
 - Events
    - Ready Event (when a session is online.)
    - Player Update Event (when a player gets updated.)
    - Statistics Event (about the server.)
    - Track Start Event
    - Track End Event
    - Track Exception Event
    - Track Stuck Event
    - Empty Queue Event
    - Next Queue Event
 - Sessions
    - BasicSessionHandler (Gives next available session)
 - Others
    - Traces (for debugging code.)
    - Tests (Full test coverage.)
