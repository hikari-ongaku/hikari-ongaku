# Creating simple commands. #

## First, you need to fetch the player for the guild, no matter what.

for example

```py
player = await lavalink.fetch_player(ctx.guild_id)
```

!!! WARNING
    This will look for a player. It will not create a player, and will raise an error if it fails to find it.

## You then can run any of the following functions

Play a song:
```py
await player.play(track)
```

!!! INFO
    Play requires a track, which will be explained, how to [search](#how-to-search) for those, later.

Pause or unpause the currently playing song:
```py
await player.pause()
```

Skip the currently playing song:
```py
await player.skip()
```

Change the current track position:
```py
await player.position()
```

Add song(s) to the queue:
```py
await player.add(track)
```

Remove a track via the track itself, or the position of the track in the queue.
```py
await player.remove(track)
```

Clear the queue of songs, and stop the currently playing song:
```py
await player.clear()
```

Change the volume of the player:
```py
await player.volume(500)
```

## How to search #

now, for the functions that require a track, you will need to search for a track.
To search for a track, you must use rest. for example:

```py
tracks =  await lavalink.rest.search(ongaku.PlatformType.YOUTUBE, "AJR")
```

The first argument parsed, is the [platform type](../api_reference/enums.md#ongaku.enums.PlatformType).
The second argument parsed, is the query, or the song/link you wish to search.