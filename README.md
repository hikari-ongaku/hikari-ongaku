# Ongaku
A voice library for Hikari.

<div align="center">

[![PyPI](https://img.shields.io/pypi/v/hikari-ongaku)](https://pypi.org/project/hikari-ongaku)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)
![Pyright](https://badgen.net/badge/Pyright/strict/2A6DB2)
[![Lavalink](https://badgen.net/badge/Lavalink/v4.0.0/ff624a)](https://lavalink.dev/)
[![Docs](https://badgen.net/badge/Docs/v0.2.4/ff6b61)](https://ongaku.mplaty.com/)

</div>

This is a library, written in asynchronous python, that is designed to take a lavalink server connection, and allow for users, to be able to play music (using [hikari](https://hikari-py.dev/)) and control the players.


### More Information

Please check out the [docs](https://ongaku.mplaty.com/), and also checkout the [examples](https://github.com/MPlatypus/hikari-ongaku/tree/main/examples).


### Features
 - Player control
    - Volume
    - Playlists
    - Queuing
        - Deleting (via position, and Track)
        - Clearing
        - Adding
    - Skipping
    - Seeking/Reversing
    - Filters
    - Muting
    - Requestor [^1]
 - Events
    - Ready
    - Statistics
    - Track Start
    - Track End
    - Track Exception
    - Track Stuck
    - Empty Queue [^2]
    - Next Queue [^2]
 - Nodes
    - Automatic nodes


### Coming soon...
These features will be added in the near future.
 - [ ] Local file playing (mp3, mp4, ogg, wav, etc.)
 - [ ] Custom plugin creation.
 - [ ] Custom nodes.


[^1]: The requestor, is the user who asked for the specific song.
[^2]: The next song in the queue, or if the queue has ended.