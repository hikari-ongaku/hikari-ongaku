import hikari
import tanjun
import ongaku
import logging

bot = hikari.GatewayBot("...")

client = tanjun.Client.from_gateway_bot(bot)

lavalink = ongaku.Ongaku(bot, password="youshallnotpass")


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


component = tanjun.Component()


@component.with_slash_command
@tanjun.with_str_slash_option("query", "query to search")
@tanjun.as_slash_command("play", "Play a song, or a playlist.")
async def play_command(ctx: tanjun.abc.SlashContext, query: str) -> None:
    if ctx.guild_id is None:
        await ctx.create_initial_response(
            "This command must be ran in a guild.", flags=hikari.MessageFlag.EPHEMERAL
        )
        return

    voice_state = bot.cache.get_voice_state(ctx.guild_id, ctx.author.id)
    if not voice_state or not voice_state.channel_id:
        await ctx.create_initial_response(
            "you are not in a voice channel.", flags=hikari.MessageFlag.EPHEMERAL
        )
        return

    result = await lavalink.rest.track.load(query)

    if result is None:
        await ctx.create_initial_response(
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
        title=track.info.title,
        description=f"made by: {track.info.author}",
    )

    embed.set_image(track.info.artwork_url)

    try:
        player = await lavalink.fetch_player(ctx.guild_id)
    except Exception:
        player = await lavalink.create_player(ctx.guild_id)

    if player.connected is False:
        await player.connect(voice_state.channel_id)

    try:
        await player.play(track)
    except Exception as e:
        raise e

    await ctx.create_initial_response(
        embed=embed,
        flags=hikari.MessageFlag.EPHEMERAL,
    )


@component.with_slash_command
@tanjun.with_str_slash_option("query", "query to search")
@tanjun.as_slash_command("add", "add a song to the queue")
async def add_command(
    ctx: tanjun.abc.SlashContext,
    query: str,
) -> None:
    if ctx.guild_id is None:
        await ctx.create_initial_response(
            "This command must be ran in a guild.", flags=hikari.MessageFlag.EPHEMERAL
        )
        return
    try:
        current_player = await lavalink.fetch_player(ctx.guild_id)
    except Exception:
        await ctx.create_initial_response(
            "You must have a player currently running!",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    result = await lavalink.rest.track.load(query)

    if result is None:
        await ctx.create_initial_response(
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

    await ctx.create_initial_response(f"Added {track_count} track(s) to the player.")


@component.with_slash_command
@tanjun.as_slash_command("pause", "pause or unpause the currently playing song.")
async def pause_command(ctx: tanjun.abc.SlashContext) -> None:
    if ctx.guild_id is None:
        await ctx.create_initial_response(
            "This command must be ran in a guild.", flags=hikari.MessageFlag.EPHEMERAL
        )
        return
    try:
        current_player = await lavalink.fetch_player(ctx.guild_id)
    except Exception:
        await ctx.create_initial_response(
            "You must have a player currently running!",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    await current_player.pause()

    if current_player.is_paused:
        await ctx.create_initial_response(
            "Music has been paused.", flags=hikari.MessageFlag.EPHEMERAL
        )
    else:
        await ctx.create_initial_response(
            "Music has been resumed.", flags=hikari.MessageFlag.EPHEMERAL
        )


@component.with_slash_command
@tanjun.as_slash_command("queue", "View the queue of the player.")
async def queue_command(ctx: tanjun.abc.SlashContext) -> None:
    if ctx.guild_id is None:
        await ctx.create_initial_response(
            "Guild ID is none! You must be in a guild to run this command.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    try:
        player = await lavalink.fetch_player(ctx.guild_id)
    except Exception:
        await ctx.create_initial_response(
            "There is no player currently playing in this server.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    if len(player.queue) == 0:
        await ctx.create_initial_response("There is not tracks in the queue currently.")

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

    await ctx.create_initial_response(embed=queue_embed)


@component.with_slash_command
@tanjun.with_int_slash_option(
    "volume", "The volume of the player.", min_value=0, max_value=100
)
@tanjun.as_slash_command("volume", "change the volume of the player.")
async def volume_command(
    ctx: tanjun.abc.SlashContext,
    volume: int,
) -> None:
    if ctx.guild_id is None:
        await ctx.create_initial_response(
            "Guild ID is none! You must be in a guild to run this command.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    try:
        player = await lavalink.fetch_player(ctx.guild_id)
    except Exception:
        await ctx.create_initial_response(
            "There is no player currently playing in this server.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    try:
        await player.volume(volume * 10)
    except ongaku.PlayerSettingException:
        await ctx.create_initial_response(
            "Sorry, but you have entered an invalid number."
        )
        return

    await ctx.create_initial_response(
        f"the volume has successfully been set to {volume}/100"
    )


@component.with_slash_command
@tanjun.with_int_slash_option(
    "amount", "The amount of songs to skip.", min_value=1, default=1
)
@tanjun.as_slash_command("skip", "skip a song, or multiple")
async def skip_command(
    ctx: tanjun.abc.SlashContext,
    amount: int,
) -> None:
    if ctx.guild_id is None:
        await ctx.create_initial_response(
            "Guild ID is none! You must be in a guild to run this command.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    try:
        player = await lavalink.fetch_player(ctx.guild_id)
    except Exception:
        await ctx.create_initial_response(
            "There is no player currently playing in this server.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    try:
        await player.skip(amount)
    except ongaku.PlayerQueueException:
        await ctx.create_initial_response(
            "It looks like the queue is empty, so no new songs will be played."
        )
        return

    await ctx.create_initial_response(f"{amount} song(s) were successfully skipped.")


@component.with_slash_command
@tanjun.as_slash_command(
    "stop", "Stops the player, and disconnects it from the server."
)
async def stop_command(ctx: tanjun.abc.SlashContext) -> None:
    if ctx.guild_id is None:
        await ctx.create_initial_response(
            "Guild ID is none! You must be in a guild to run this command.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    try:
        await lavalink.delete_player(ctx.guild_id)
    except Exception:
        await ctx.create_initial_response(
            "There is no player currently playing in this server.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    await ctx.create_initial_response("Successfully stopped the player.")


if __name__ == "__main__":
    client.add_component(component)
    bot.run()
