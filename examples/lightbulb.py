# ruff: noqa: D100, D101, D102, D103


# ╔═══════════════════╗
# ║ Lightbulb example ║
# ╚═══════════════════╝


import logging

import hikari
import lightbulb

import ongaku
from ongaku.ext import checker

bot = lightbulb.BotApp("...")

ongaku_client = ongaku.Client(bot, password="youshallnotpass")

bot.d.ongaku_client = ongaku_client


# ╔════════╗
# ║ Events ║
# ╚════════╝


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


# ╔══════════╗
# ║ Commands ║
# ╚══════════╝


@bot.command
@lightbulb.option("query", "The song you wish to play.", str, required=True)
@lightbulb.command("play", "Play a song.")
@lightbulb.implements(lightbulb.SlashCommand)
async def play_command(
    ctx: lightbulb.Context,
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

    checked_query = await checker.check(ctx.options.query)

    if checked_query.type == checker.CheckedType.QUERY:
        result = await ctx.bot.d.ongaku_client.rest.track.load(
            f"ytsearch:{checked_query.value}"
        )
    else:
        result = await ctx.bot.d.ongaku_client.rest.track.load(checked_query.value)

    if result is None:
        await ctx.respond(
            "Sorry, no songs were found.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    track: ongaku.Track

    if isinstance(result, ongaku.Playlist):
        track = result.tracks[0]

    elif isinstance(result, ongaku.Track):
        track = result

    else:
        track = result[0]

    embed = hikari.Embed(
        title=f"[{track.info.title}]({track.info.uri})",
        description=f"made by: {track.info.author}",
    )

    try:
        player = await ongaku_client.player.fetch(ctx.guild_id)
    except ongaku.PlayerMissingException:
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


@bot.command
@lightbulb.option("query", "The song you wish to play.", str, required=True)
@lightbulb.command("add", "Add a song (or songs!)")
@lightbulb.implements(lightbulb.SlashCommand)
async def add_command(
    ctx: lightbulb.Context,
) -> None:
    if ctx.guild_id is None:
        await ctx.respond(
            "This command must be ran in a guild.", flags=hikari.MessageFlag.EPHEMERAL
        )
        return

    try:
        current_player = await ctx.bot.d.ongaku_client.player.fetch(ctx.guild_id)
    except Exception:
        await ctx.respond(
            "You must have a player currently running!",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    checked_query = await checker.check(ctx.options.query)

    if checked_query.type == checker.CheckedType.QUERY:
        result = await ctx.bot.d.ongaku_client.rest.track.load(
            f"ytsearch:{checked_query.value}"
        )
    else:
        result = await ctx.bot.d.ongaku_client.rest.track.load(checked_query.value)

    if result is None:
        await ctx.respond(
            "Sorry, no songs were found.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    tracks: list[ongaku.Track] = []

    if isinstance(result, ongaku.Playlist):
        tracks.extend(result.tracks)

    elif isinstance(result, ongaku.Track):
        tracks.append(result)

    else:
        tracks.extend(result)

    await current_player.add(tracks)

    embed = hikari.Embed(
        title="Tracks added",
        description=f"All the tracks that have been added. (only shows top 25.)\nTotal tracks added: {len(tracks)}",
    )

    for track in tracks:
        if len(embed.fields) >= 25:
            break
        embed.add_field(track.info.title, track.info.author)

    await ctx.respond(embed=embed)


@bot.command
@lightbulb.command("pause", "pause or unpause the currently playing song.")
@lightbulb.implements(lightbulb.SlashCommand)
async def pause_command(
    ctx: lightbulb.Context,
) -> None:
    if ctx.guild_id is None:
        await ctx.respond(
            "This command must be ran in a guild.", flags=hikari.MessageFlag.EPHEMERAL
        )
        return
    try:
        current_player = await ctx.bot.d.ongaku_client.player.fetch(ctx.guild_id)
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


@bot.command
@lightbulb.command("queue", "View the queue of the player.")
@lightbulb.implements(lightbulb.SlashCommand)
async def queue_command(
    ctx: lightbulb.Context,
) -> None:
    if ctx.guild_id is None:
        await ctx.respond(
            "Guild ID is none! You must be in a guild to run this command.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    try:
        player = await ctx.bot.d.ongaku_client.player.fetch(ctx.guild_id)
    except Exception:
        await ctx.respond(
            "There is no player currently playing in this server.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    if len(player.queue) == 0:
        await ctx.respond("There is not tracks in the queue currently.")
        return

    queue_embed = hikari.Embed(
        title="Queue",
        description=f"The queue for this server.\nCurrent song: {player.queue[0].info.title}",
    )

    for x in range(len(player.queue)):
        if x == 0:
            continue

        if x >= 25:
            break

        track = player.queue[x]

        queue_embed.add_field(track.info.title, track.info.author)

    await ctx.respond(embed=queue_embed)


@bot.command
@lightbulb.option(
    "volume",
    "The volume number you wish to set.",
    int,
    required=True,
    min_value=0,
    max_value=100,
)
@lightbulb.command("volume", "change the volume of the player.")
@lightbulb.implements(lightbulb.SlashCommand)
async def volume_command(
    ctx: lightbulb.Context,
) -> None:
    if ctx.guild_id is None:
        await ctx.respond(
            "Guild ID is none! You must be in a guild to run this command.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    try:
        player = await ctx.bot.d.ongaku_client.player.fetch(ctx.guild_id)
    except Exception:
        await ctx.respond(
            "There is no player currently playing in this server.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    try:
        await player.set_volume(ctx.options.volume)
    except ValueError:
        await ctx.respond("Sorry, but you have entered an invalid number.")
        return

    await ctx.respond(
        f"the volume has successfully been set to {ctx.options.volume}/100"
    )


@bot.command
@lightbulb.option(
    "amount",
    "The amount of songs you wish to skip. default is 1.",
    int,
    required=True,
    min_value=0,
    default=1,
)
@lightbulb.command("skip", "skip a song, or multiple")
@lightbulb.implements(lightbulb.SlashCommand)
async def skip_command(
    ctx: lightbulb.Context,
) -> None:
    if ctx.guild_id is None:
        await ctx.respond(
            "Guild ID is none! You must be in a guild to run this command.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    try:
        player = await ctx.bot.d.ongaku_client.player.fetch(ctx.guild_id)
    except Exception:
        await ctx.respond(
            "There is no player currently playing in this server.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    try:
        await player.skip(ctx.options.amount)
    except ongaku.PlayerQueueException:
        await ctx.respond(
            "It looks like the queue is empty, so no new songs will be played."
        )
        return

    await ctx.respond(f"{ctx.options.amount} song(s) were successfully skipped.")


@bot.command
@lightbulb.command("stop", "Stops the player, and disconnects it from the server.")
@lightbulb.implements(lightbulb.SlashCommand)
async def stop_command(
    ctx: lightbulb.Context,
) -> None:
    if ctx.guild_id is None:
        await ctx.respond(
            "Guild ID is none! You must be in a guild to run this command.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return
    try:
        player = await ctx.bot.d.ongaku_client.player.fetch(ctx.guild_id)
    except Exception:
        await ctx.respond(
            "There is no player currently playing in this server.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    await player.disconnect()

    await ctx.respond("Successfully stopped the player.")


if __name__ == "__main__":
    bot.run()
