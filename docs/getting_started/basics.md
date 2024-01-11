# The basics

This will show you how to get started with creating your first music bot.

## Basic setup

you must have a gateway bot, like any other hikari discord bot. 
Ongaku is incompatible with RESTBots. [read more](/getting_started/#qs-and-as)

First step, is setting up a discord bot. This is the minimum requirement.
```python
import hikari

bot = hikari.GatewayBot(
    token="..."
)
```

You then must create an ongaku class, that attaches to that bot.

```python
import ongaku

lavalink = ongaku.Ongaku(
    bot,
    password="youshallnotpass"
)
```

then, you have to run the bot:

```python
bot.run()
```

## Searching for tracks

```py
tracks =  await lavalink.rest.search(
    ongaku.PlatformType.YOUTUBE,
    "AJR"
)
```

The first argument parsed, is the [platform type](../api_reference/enums.md#ongaku.enums.PlatformType).
The second argument parsed, is the query, or the song/link you wish to search.

The method, will then return one of the following:

 * `Playlist` - This is a list of songs, that originated from a playlist on the platform.

 * `Track` - This is a singular track, because a url to a video/song was originally sent.

 * `SearchResult` - This is a list of songs, that are usually going to be very similar to each other.

 * `None` - Your result returned absolutely nothing!


## Creating a player

Then, with the track above, you want to create a player, for the guild that you wish to play music from.

```py
player = await lavalink.create_player(guild_id)
```

This will return an existing player, or, will create a new player if no player exists.

## Getting the player to join a channel

With the player you have just created, you will then need to get it to join a channel.

```python
await player.join(channel_id)
```

This will attempt to get the player to join the current channel you have given the player. If it cannot join the channel, it will raise an error.

## Changing things for the player

The following functions, will allow for you to modify things about the player. This includes playing, pausing, and skipping songs.

#### Play a song, or the queue
```py
await player.play(track)
```
this will start playing the track you have fed to it. This must be a valid [track](/api_reference/abc/track/#ongaku.abc.track.Track)

#### Pausing or unpausing the player
```py
await player.pause()
```
this will pause, or unpause the currently playing track.

#### Skipping songs
```py
await player.skip(1)
```
This will allow for the user to skip a song, or you can skip multiple, by adding a number.

#### Change the tracks position
```py
await player.position()
```
This will allow for the user, to change the tracks current playing position.

#### Add songs to the queue
```py
await player.add(track)
```
This allows for the user to add a list of songs, a singular track, or a [Playlist](/api_reference/abc/track/#ongaku.abc.track.Playlist) to the queue.

#### Remove a track from the queue
```py
await player.remove(track)
```
This will allow the user to remove a track from the queue, or a song via it's position.

#### Clear the entire queue
```py
await player.clear()
```
This will clear the entire queue, including the currently playing song, and also will stop the songs from playing.

#### Change the volume
```py
await player.volume(500)
```
This will allow you to change the volume of the player.
