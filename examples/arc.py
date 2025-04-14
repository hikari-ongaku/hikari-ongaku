# ruff: noqa: D100, D101, D102, D103


# ╔═════════════╗
# ║ Arc example ║
# ╚═════════════╝


import logging

import arc
import hikari

import ongaku
from ongaku.ext import checker
from ongaku.ext import injection

bot = hikari.GatewayBot("...")

client = arc.GatewayClient(bot)

ongaku_client = ongaku.Client.from_arc(client)

ongaku_client.create_session(
    "arc-session", host="127.0.0.1", password="youshallnotpass"
)


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


# ╔═══════════════╗
# ║ Error Handler ║
# ╚═══════════════╝


@client.set_error_handler()
async def error_handler(ctx: arc.GatewayContext, exc: Exception):
    if isinstance(exc, arc.GuildOnlyError):
        await ctx.respond(
            "You must be in a guild to use this command.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    elif isinstance(exc, ongaku.PlayerMissingError):
        await ctx.respond(
            "There is no player playing in this guild.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return


# ╔══════════╗
# ║ Commands ║
# ╚══════════╝


@client.include
@arc.slash_command(
    "play", "Play a song or playlist.", autodefer=arc.AutodeferMode.EPHEMERAL
)
async def play_command(
    ctx: arc.GatewayContext,
    query: arc.Option[str, arc.StrParams("The name, or link of the song to play.")],
    music: ongaku.Client = arc.inject(),
) -> None:
    if ctx.guild_id is None:
        raise arc.GuildOnlyError

    voice_state = bot.cache.get_voice_state(ctx.guild_id, ctx.author.id)
    if not voice_state or not voice_state.channel_id:
        await ctx.respond(
            "you are not in a voice channel.", flags=hikari.MessageFlag.EPHEMERAL
        )
        return

    if checker.check(query):
        result = await music.rest.load_track(query)
    else:
        result = await music.rest.load_track(f"ytsearch:{query}")

    if result is None:
        await ctx.respond(
            "Sorry, no songs were found.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

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

    player = music.create_player(ctx.guild_id)

    if player.connected is False:
        await player.connect(voice_state.channel_id)

    await player.play(track)

    await ctx.respond(
        embed=embed,
        flags=hikari.MessageFlag.EPHEMERAL,
    )


@client.include
@arc.with_hook(injection.arc_ensure_player)
@arc.slash_command(
    "add", "Add more songs or a playlist.", autodefer=arc.AutodeferMode.EPHEMERAL
)
async def add_command(
    ctx: arc.GatewayContext,
    query: arc.Option[str, arc.StrParams("The name, or link of the song to add.")],
    player: ongaku.Player = arc.inject(),
) -> None:
    if checker.check(query):
        result = await player.session.client.rest.load_track(query)
    else:
        result = await player.session.client.rest.load_track(f"ytsearch:{query}")

    if result is None:
        await ctx.respond(
            "Sorry, no songs were found.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    if isinstance(result, ongaku.Playlist):
        tracks = result.tracks

    elif isinstance(result, ongaku.Track):
        tracks = [result]

    else:
        tracks = [result[0]]

    player.add(tracks)

    embed = hikari.Embed(
        title="Tracks added",
        description=f"All the tracks that have been added. (only shows top 25.)\nTotal tracks added: {len(tracks)}",
    )

    for track in tracks:
        if len(embed.fields) >= 25:
            break
        embed.add_field(track.info.title, track.info.author)

    await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)


@client.include
@arc.with_hook(injection.arc_ensure_player)
@arc.slash_command(
    "queue", "View the current queue.", autodefer=arc.AutodeferMode.EPHEMERAL
)
async def queue_command(
    ctx: arc.GatewayContext,
    player: ongaku.Player = arc.inject(),
) -> None:
    if len(player.queue) == 0:
        await ctx.respond(
            "There is no songs in the queue.", flags=hikari.MessageFlag.EPHEMERAL
        )
        return

    embed = hikari.Embed(
        title="Queue",
        description=f"There is currently {len(player.queue)} song{'s' if len(player.queue) > 1 else ''} in the queue.",
    )

    embed.add_field(
        f"▶️ {player.queue[0].info.title}",
        f"Length: {player.queue[0].info.length / 1000}s\nArtist: {player.queue[0].info.author}",
    )

    if len(player.queue) > 1:
        for i in range(1, 24):
            if i > len(player.queue):
                break

            embed.add_field(
                player.queue[i].info.title,
                f"Length: {player.queue[i].info.length / 1000}s\nArtist: {player.queue[i].info.author}",
            )

    await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)


@client.include
@arc.with_hook(injection.arc_ensure_player)
@arc.slash_command(
    "pause", "Pause or play the current song.", autodefer=arc.AutodeferMode.EPHEMERAL
)
async def pause_command(
    ctx: arc.GatewayContext,
    player: ongaku.Player = arc.inject(),
) -> None:
    await player.pause()

    if player.is_paused:
        await ctx.respond(
            "The song has been paused.", flags=hikari.MessageFlag.EPHEMERAL
        )
    else:
        await ctx.respond(
            "The song has been unpaused.", flags=hikari.MessageFlag.EPHEMERAL
        )


@client.include
@arc.with_hook(injection.arc_ensure_player)
@arc.slash_command(
    "skip", "Skip the currently playing song.", autodefer=arc.AutodeferMode.EPHEMERAL
)
async def skip_command(
    ctx: arc.GatewayContext,
    player: ongaku.Player = arc.inject(),
) -> None:
    await player.skip()

    if len(player.queue) > 0:
        embed = hikari.Embed(
            title=player.queue[0].info.title,
            description=f"Length: {player.queue[0].info.length / 1000}s\nArtist: {player.queue[0].info.author}",
        )

        artwork_url = player.queue[0].info.artwork_url

        if artwork_url:
            embed.set_thumbnail(hikari.files.URL(artwork_url, "artwork.png"))

        await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)

    await ctx.respond("The queue is now empty!", flags=hikari.MessageFlag.EPHEMERAL)


@client.include
@arc.with_hook(injection.arc_ensure_player)
@arc.slash_command(
    "volume", "Set the volume of the player.", autodefer=arc.AutodeferMode.EPHEMERAL
)
async def volume_command(
    ctx: arc.GatewayContext,
    volume: arc.Option[int, arc.IntParams("The volume to set.", min=0, max=200)],
    player: ongaku.Player = arc.inject(),
) -> None:
    await player.set_volume(volume)

    await ctx.respond(
        f"The volume is now set to {volume}%", flags=hikari.MessageFlag.EPHEMERAL
    )


@client.include
@arc.with_hook(injection.arc_ensure_player)
@arc.slash_command(
    "loop",
    "Enable or disable the looping of the current track.",
    autodefer=arc.AutodeferMode.EPHEMERAL,
)
async def loop_command(
    ctx: arc.GatewayContext,
    player: ongaku.Player = arc.inject(),
) -> None:
    player.set_loop()

    if player.loop:
        if player.track:
            await ctx.respond(
                f"The player is now looping.\nTrack: {player.track.info.title}",
                flags=hikari.MessageFlag.EPHEMERAL,
            )
        else:
            await ctx.respond(
                "The player is now looping.", flags=hikari.MessageFlag.EPHEMERAL
            )
    else:
        await ctx.respond(
            "The player is no longer looping.", flags=hikari.MessageFlag.EPHEMERAL
        )


@client.include
@arc.with_hook(injection.arc_ensure_player)
@arc.slash_command(
    "shuffle", "Shuffle the current queue.", autodefer=arc.AutodeferMode.EPHEMERAL
)
async def shuffle_command(
    ctx: arc.GatewayContext,
    player: ongaku.Player = arc.inject(),
) -> None:
    player.shuffle()

    await ctx.respond(
        "The queue has been successfully shuffled.", flags=hikari.MessageFlag.EPHEMERAL
    )


@client.include
@arc.with_hook(injection.arc_ensure_player)
@arc.slash_command(
    "speed",
    "Increase the speed of the currently playing song.",
    autodefer=arc.AutodeferMode.EPHEMERAL,
)
async def filter_command(
    ctx: arc.GatewayContext,
    speed: arc.Option[
        float, arc.FloatParams("The speed to change the player to.", min=0, max=5)
    ] = 1,
    player: ongaku.Player = arc.inject(),
) -> None:
    if player.filters:
        filters = ongaku.Filters.from_filter(player.filters)
    else:
        filters = ongaku.Filters()

    filters.set_timescale(speed=speed)

    await player.set_filters(filters)

    await ctx.respond(
        f"The speed has now been set to {speed}", flags=hikari.MessageFlag.EPHEMERAL
    )


@client.include
@arc.with_hook(injection.arc_ensure_player)
@arc.slash_command(
    "stop", "Stop the currently playing song.", autodefer=arc.AutodeferMode.EPHEMERAL
)
async def stop_command(
    ctx: arc.GatewayContext,
    player: ongaku.Player = arc.inject(),
) -> None:
    await player.stop()

    await ctx.respond(
        "The player has been stopped.", flags=hikari.MessageFlag.EPHEMERAL
    )


@client.include
@arc.with_hook(injection.arc_ensure_player)
@arc.slash_command(
    "disconnect",
    "Stop the currently playing song and disconnect from the VC.",
    autodefer=arc.AutodeferMode.EPHEMERAL,
)
async def disconnect_command(
    ctx: arc.GatewayContext,
    player: ongaku.Player = arc.inject(),
) -> None:
    await player.disconnect()

    await ctx.respond(
        "The player has been disconnected.", flags=hikari.MessageFlag.EPHEMERAL
    )


if __name__ == "__main__":
    bot.run()
