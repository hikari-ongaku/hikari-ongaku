import logging

import hikari

import ongaku

bot = hikari.GatewayBot(token="...", intents=hikari.Intents.ALL)

lavalink = ongaku.Client(bot, password="youshallnotpass")


# Events


@bot.listen(ongaku.ReadyEvent)
async def ready_event(event: ongaku.ReadyEvent):
    logging.info(
        f"Ready Event, Resumed: {event.resumed}, session id: {event.session_id}"
    )


@bot.listen(ongaku.TrackStartEvent)
async def track_start_event(event: ongaku.TrackStartEvent):
    logging.info(
        f"Track Started Event, guild: {event.guild_id}, Track Title: {event.track.info.title}"
    )


@bot.listen(ongaku.TrackEndEvent)
async def track_end_event(event: ongaku.TrackEndEvent):
    logging.info(
        f"Track Ended Event, guild: {event.guild_id}, Track Title: {event.track.info.title}, Reason: {event.reason.name}"
    )


@bot.listen(ongaku.TrackExceptionEvent)
async def track_exception_event(event: ongaku.TrackExceptionEvent):
    logging.info(
        f"Track Exception Event, guild: {event.guild_id}, Track Title: {event.track.info.title}, Exception message: {event.exception.message}"
    )


@bot.listen(ongaku.TrackStuckEvent)
async def track_stuck_event(event: ongaku.TrackStuckEvent):
    logging.info(
        f"Track Stuck Event, guild: {event.guild_id}, Track Title: {event.track.info.title}, Threshold ms: {event.threshold_ms}"
    )


@bot.listen(ongaku.WebsocketClosedEvent)
async def websocket_close_event(event: ongaku.WebsocketClosedEvent):
    logging.info(
        f"Websocket Close Event, guild: {event.guild_id}, Reason: {event.reason}, Code: {event.code}, By Remote: {event.by_remote}"
    )


# Commands

prefix = "!"


@bot.listen()
async def play_event(event: hikari.MessageCreateEvent):
    if event.content is None:
        logging.error(
            "The content is None. Please make sure you have the correct intents!"
        )
        return

    if not event.content.startswith(prefix + "play"):
        return

    split_content = event.content.split(" ")

    if len(split_content) <= 1:
        await bot.rest.create_message(
            event.channel_id, "Sorry, but no query was provided.", reply=event.message
        )
        return

    if event.message.guild_id is None:
        await bot.rest.create_message(
            event.channel_id,
            "Sorry, but this command must be ran in a guild.",
            reply=event.message,
        )
        return

    query = split_content[1]

    voice_state = bot.cache.get_voice_state(event.message.guild_id, event.author.id)
    if not voice_state or not voice_state.channel_id:
        await bot.rest.create_message(
            event.channel_id,
            "Sorry, but you must be in a vc to run this command.",
            reply=event.message,
        )
        return

    result = await lavalink.rest.track.load(query)

    if result is None:
        await bot.rest.create_message(
            event.channel_id, "Your query returned no results D:", reply=event.message
        )
        return

    track: ongaku.Track | None = None

    if isinstance(result, ongaku.SearchResult):
        track = result.tracks[0]

    elif isinstance(result, ongaku.Track):
        track = result

    else:
        track = result.tracks[0]

    embed = hikari.Embed(
        title=f"[{track.info.title}]({track.info.uri})",
        description=f"made by: {track.info.author}",
    )

    try:
        player = await lavalink.fetch_player(event.message.guild_id)
    except Exception:
        player = await lavalink.create_player(event.message.guild_id)

    if player.connected is False:
        await player.connect(voice_state.channel_id)

    try:
        await player.play(track)
    except Exception as e:
        raise e

    await bot.rest.create_message(event.channel_id, embed=embed, reply=event.message)


@bot.listen()
async def add_event(event: hikari.MessageCreateEvent):
    if event.content is None:
        logging.error(
            "The content is None. Please make sure you have the correct intents!"
        )
        return

    if not event.content.startswith(prefix + "add"):
        return

    split_content = event.content.split(" ")

    if len(split_content) <= 1:
        await bot.rest.create_message(
            event.channel_id, "Sorry, but no query was provided.", reply=event.message
        )
        return

    if event.message.guild_id is None:
        await bot.rest.create_message(
            event.channel_id,
            "Sorry, but this command must be ran in a guild.",
            reply=event.message,
        )
        return

    query = split_content[1]

    try:
        current_player = await lavalink.fetch_player(event.message.guild_id)
    except Exception:
        await bot.rest.create_message(
            event.channel_id,
            "You must have a player currently running!",
            reply=event.message,
        )
        return

    result = await lavalink.rest.track.load(query)

    if result is None:
        await bot.rest.create_message(
            event.channel_id, "Sorry, no songs were found.", reply=event.message
        )
        return

    track_count: int = 0

    if isinstance(result, ongaku.SearchResult):
        await current_player.add((result.tracks[0],))
        track_count = 1

    elif isinstance(result, ongaku.Track):
        await current_player.add((result,))
        track_count = 1

    else:
        await current_player.add(result.tracks)
        track_count = len(result.tracks)

    await bot.rest.create_message(
        event.channel_id,
        f"Added {track_count} track(s) to the player.",
        reply=event.message,
    )


@bot.listen()
async def pause_event(event: hikari.MessageCreateEvent):
    if event.content is None:
        logging.error(
            "The content is None. Please make sure you have the correct intents!"
        )
        return

    if not event.content.startswith(prefix + "pause"):
        return

    if event.message.guild_id is None:
        await bot.rest.create_message(
            event.channel_id,
            "Sorry, but this command must be ran in a guild.",
            reply=event.message,
        )
        return

    try:
        current_player = await lavalink.fetch_player(event.message.guild_id)
    except Exception:
        await bot.rest.create_message(
            event.channel_id,
            "You must have a player currently running!",
            reply=event.message,
        )
        return

    await current_player.pause()

    if current_player.is_paused:
        await bot.rest.create_message(
            event.channel_id, "Music has been paused.", reply=event.message
        )
    else:
        await bot.rest.create_message(
            event.channel_id, "Music has been resumed.", reply=event.message
        )


@bot.listen()
async def queue_event(event: hikari.MessageCreateEvent):
    if event.content is None:
        logging.error(
            "The content is None. Please make sure you have the correct intents!"
        )
        return

    if not event.content.startswith(prefix + "queue"):
        return

    if event.message.guild_id is None:
        await bot.rest.create_message(
            event.channel_id,
            "Sorry, but this command must be ran in a guild.",
            reply=event.message,
        )
        return

    try:
        player = await lavalink.fetch_player(event.message.guild_id)
    except Exception:
        await bot.rest.create_message(
            event.channel_id,
            "There is no player currently playing in this server.",
            reply=event.message,
        )
        return

    if len(player.queue) == 0:
        await bot.rest.create_message(
            event.channel_id, "Sorry, but the queue is empty.", reply=event.message
        )
        return

    queue_embed = hikari.Embed(
        title="Queue",
        description=f"The current queue for this server.\nCurrent song: {player.queue[0].info.title}",
    )

    for x in range(len(player.queue)):
        if x == 0:
            continue

        if x >= 25:
            break

        track = player.queue[x]

        queue_embed.add_field(track.info.title, track.info.author)

    await bot.rest.create_message(
        event.channel_id, embed=queue_embed, reply=event.message
    )


@bot.listen()
async def volume_event(event: hikari.MessageCreateEvent):
    if event.content is None:
        logging.error(
            "The content is None. Please make sure you have the correct intents!"
        )
        return

    if not event.content.startswith(prefix + "volume"):
        return

    split_content = event.content.split(" ")

    if len(split_content) <= 1:
        await bot.rest.create_message(
            event.channel_id, "Sorry, but no query was provided.", reply=event.message
        )
        return

    if event.message.guild_id is None:
        await bot.rest.create_message(
            event.channel_id,
            "Sorry, but this command must be ran in a guild.",
            reply=event.message,
        )
        return

    volume = split_content[1]

    try:
        volume = int(volume)
    except Exception:
        await bot.rest.create_message(
            event.channel_id, "Volume must be an integer!", reply=event.message
        )
        return

    if volume > 100 or volume < 0:
        await bot.rest.create_message(
            event.channel_id, "Volume must be between 0, and 100.", reply=event.message
        )
        return

    try:
        player = await lavalink.fetch_player(event.message.guild_id)
    except Exception:
        await bot.rest.create_message(
            event.channel_id,
            "There is no player currently playing in this server.",
            reply=event.message,
        )
        return

    try:
        await player.volume(volume * 10)
    except ValueError:
        await bot.rest.create_message(
            event.channel_id,
            "Sorry, but you have entered an invalid number.",
            reply=event.message,
        )
        return

    await bot.rest.create_message(
        event.channel_id,
        f"the volume has successfully been set to {volume}/100",
        reply=event.message,
    )


@bot.listen()
async def skip_event(event: hikari.MessageCreateEvent):
    if event.content is None:
        logging.error(
            "The content is None. Please make sure you have the correct intents!"
        )
        return

    if not event.content.startswith(prefix + "skip"):
        return

    split_content = event.content.split(" ")

    if len(split_content) <= 1:
        await bot.rest.create_message(
            event.channel_id, "Sorry, but no query was provided.", reply=event.message
        )
        return

    if event.message.guild_id is None:
        await bot.rest.create_message(
            event.channel_id,
            "Sorry, but this command must be ran in a guild.",
            reply=event.message,
        )
        return

    amount = split_content[1]

    try:
        amount = int(amount)
    except Exception:
        await bot.rest.create_message(
            event.channel_id, "Amount must be an integer!", reply=event.message
        )
        return

    if amount < 0:
        await bot.rest.create_message(
            event.channel_id, "Amount must be 1 or above.", reply=event.message
        )
        return

    try:
        player = await lavalink.fetch_player(event.message.guild_id)
    except Exception:
        await bot.rest.create_message(
            event.channel_id,
            "There is no player currently playing in this server.",
            reply=event.message,
        )
        return

    try:
        await player.skip(amount)
    except ongaku.PlayerQueueException:
        await bot.rest.create_message(
            event.channel_id,
            "It looks like the queue is empty, so no new songs will be played.",
            reply=event.message,
        )
        return

    await bot.rest.create_message(
        event.channel_id,
        f"{amount} song(s) were successfully skipped.",
        reply=event.message,
    )


@bot.listen()
async def stop_event(event: hikari.MessageCreateEvent):
    if event.content is None:
        logging.error(
            "The content is None. Please make sure you have the correct intents!"
        )
        return

    if not event.content.startswith(prefix + "stop"):
        return

    if event.message.guild_id is None:
        await bot.rest.create_message(
            event.channel_id,
            "Sorry, but this command must be ran in a guild.",
            reply=event.message,
        )
        return

    try:
        await lavalink.delete_player(event.message.guild_id)
    except Exception:
        await bot.rest.create_message(
            event.channel_id,
            "There is no player currently playing in this server.",
            reply=event.message,
        )
        return

    await bot.rest.create_message(
        event.channel_id, "Successfully stopped the player.", reply=event.message
    )


if __name__ == "__main__":
    bot.run()
