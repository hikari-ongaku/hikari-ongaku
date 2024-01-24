import logging

import arc
import hikari

import ongaku

bot = hikari.GatewayBot("...")

client = arc.GatewayClient(bot)

ongaku_client = ongaku.Client(bot, password="youshallnotpass")

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


@bot.listen(ongaku.QueueNextEvent)
async def queue_next_event(event: ongaku.QueueNextEvent):
    logging.info(
        f"guild: {event.guild_id}'s track: {event.old_track.info.title} has finished! Now playing: {event.track.info.title}"
    )


@bot.listen(ongaku.QueueEmptyEvent)
async def queue_empty_event(event: ongaku.QueueEmptyEvent):
    logging.info(f"Queue is empty in guild: {event.guild_id}")


# Commands


@client.include
@arc.slash_command("play", "Play a song. (must be a name, not a url.)")
async def play_command(
    ctx: arc.GatewayContext,
    query: arc.Option[str, arc.StrParams("The song you wish to play.")],
) -> None:
    if ctx.guild_id is None:
        await ctx.respond(
            "This command must be ran in a guild.", flags=hikari.MessageFlag.EPHEMERAL
        )
        return

    voice_state = bot.cache.get_voice_state(ctx.guild_id, ctx.author.id)
    if not voice_state or not voice_state.channel_id:
        await ctx.respond(
            "you are not in a voice channel.", flags=hikari.MessageFlag.EPHEMERAL
        )
        return

    result = await ongaku_client.rest.track.load(query)

    if result is None:
        await ctx.respond(
            "Sorry, no songs were found.",
            flags=hikari.MessageFlag.EPHEMERAL,
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
        player = await ongaku_client.player.fetch(ctx.guild_id)
    except Exception:
        player = await ongaku_client.player.create(ctx.guild_id)

    if player.connected is False:
        await player.connect(voice_state.channel_id)

    try:
        await player.play(track)
    except Exception as e:
        raise e

    await ctx.respond(
        embed=embed,
        flags=hikari.MessageFlag.EPHEMERAL,
    )


@client.include
@arc.slash_command("add", "Add a song. (must be a name, not a url.)")
async def add_command(
    ctx: arc.GatewayContext,
    query: arc.Option[str, arc.StrParams("The song you wish to add.")],
) -> None:
    if ctx.guild_id is None:
        await ctx.respond(
            "This command must be ran in a guild.", flags=hikari.MessageFlag.EPHEMERAL
        )
        return
    try:
        current_player = await ongaku_client.player.fetch(ctx.guild_id)
    except Exception:
        await ctx.respond(
            "You must have a player currently running!",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    result = await ongaku_client.rest.track.load(query)

    if result is None:
        await ctx.respond(
            "Sorry, no songs were found.",
            flags=hikari.MessageFlag.EPHEMERAL,
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

    await ctx.respond(f"Added {track_count} track(s) to the player.")


@client.include
@arc.slash_command("pause", "pause or unpause the currently playing song.")
async def pause_command(ctx: arc.GatewayContext) -> None:
    if ctx.guild_id is None:
        await ctx.respond(
            "This command must be ran in a guild.", flags=hikari.MessageFlag.EPHEMERAL
        )
        return
    try:
        current_player = await ongaku_client.player.fetch(ctx.guild_id)
    except Exception:
        await ctx.respond(
            "You must have a player currently running!",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    await current_player.pause()

    if current_player.is_paused:
        await ctx.respond("Music has been paused.", flags=hikari.MessageFlag.EPHEMERAL)
    else:
        await ctx.respond("Music has been resumed.", flags=hikari.MessageFlag.EPHEMERAL)


@client.include
@arc.slash_command("queue", "View the queue of the player.")
async def queue_command(ctx: arc.GatewayContext) -> None:
    if ctx.guild_id is None:
        await ctx.respond(
            "Guild ID is none! You must be in a guild to run this command.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    try:
        player = await ongaku_client.player.fetch(ctx.guild_id)
    except Exception:
        await ctx.respond(
            "There is no player currently playing in this server.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    if len(player.queue) == 0:
        await ctx.respond("There is not tracks in the queue currently.")

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

    await ctx.respond(embed=queue_embed)


@client.include
@arc.slash_command("volume", "change the volume of the player.")
async def volume_command(
    ctx: arc.GatewayContext,
    volume: arc.Option[
        int, arc.IntParams("The volume number you wish to set.", min=0, max=100)
    ],
) -> None:
    if ctx.guild_id is None:
        await ctx.respond(
            "Guild ID is none! You must be in a guild to run this command.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    try:
        player = await ongaku_client.player.fetch(ctx.guild_id)
    except Exception:
        await ctx.respond(
            "There is no player currently playing in this server.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    try:
        await player.set_volume(volume * 10)
    except ValueError:
        await ctx.respond("Sorry, but you have entered an invalid number.")
        return

    await ctx.respond(f"the volume has successfully been set to {volume}/100")


@client.include
@arc.slash_command("skip", "skip a song, or multiple")
async def skip_command(
    ctx: arc.GatewayContext,
    amount: arc.Option[
        int, arc.IntParams("The amount of songs you wish to skip. default is 1.", min=1)
    ] = 1,
) -> None:
    if ctx.guild_id is None:
        await ctx.respond(
            "Guild ID is none! You must be in a guild to run this command.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    try:
        player = await ongaku_client.player.fetch(ctx.guild_id)
    except Exception:
        await ctx.respond(
            "There is no player currently playing in this server.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    try:
        await player.skip(amount)
    except ongaku.PlayerQueueException:
        await ctx.respond(
            "It looks like the queue is empty, so no new songs will be played."
        )
        return

    await ctx.respond(f"{amount} song(s) were successfully skipped.")


@client.include
@arc.slash_command("stop", "Stops the player, and disconnects it from the server.")
async def stop_command(ctx: arc.GatewayContext) -> None:
    if ctx.guild_id is None:
        await ctx.respond(
            "Guild ID is none! You must be in a guild to run this command.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    try:
        await ongaku_client.player.delete(ctx.guild_id)
    except Exception:
        await ctx.respond(
            "There is no player currently playing in this server.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    await ctx.respond("Successfully stopped the player.")


if __name__ == "__main__":
    bot.run()
