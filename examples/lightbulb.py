# Example for Lightbulb handler.
import hikari
import lightbulb
import ongaku
import logging

import dotenv
import os

dotenv.load_dotenv(dotenv_path=".env")

bot = lightbulb.BotApp(token=os.getenv("TOKEN", ""), banner=None)

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
        f"Websocket Close Event, guild: {event.guild_id}, Reason: {event.reason}, Code: {event.code}"
    )


# The following, is just a bunch of example commands.


@bot.command
@lightbulb.option("query", "The song you wish to play (or a playlist link.)")
@lightbulb.command("play", "play a song")
@lightbulb.implements(lightbulb.SlashCommand)
async def play_command(ctx: lightbulb.Context) -> None:
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

    query = ctx.options.query

    if query is None or not isinstance(query, str):
        await ctx.respond("A query is required.", flags=hikari.MessageFlag.EPHEMERAL)
        return

    await ctx.respond(
        hikari.ResponseType.DEFERRED_MESSAGE_CREATE, flags=hikari.MessageFlag.EPHEMERAL
    )

    result = await lavalink.rest.track.load(query)

    if result is None:
        await ctx.respond(
            hikari.ResponseType.DEFERRED_MESSAGE_UPDATE,
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
        player = await lavalink.fetch_player(ctx.guild_id)
    except Exception:
        player = await lavalink.create_player(ctx.guild_id)

    await player.play(track)

    await ctx.respond(
        hikari.ResponseType.DEFERRED_MESSAGE_UPDATE,
        embed=embed,
        flags=hikari.MessageFlag.EPHEMERAL,
    )


@bot.command
@lightbulb.command("pause", "pause the currently playing song.")
@lightbulb.implements(lightbulb.SlashCommand)
async def pause_command(ctx: lightbulb.Context) -> None:
    if ctx.guild_id is None:
        await ctx.respond(
            "This command must be ran in a guild.", flags=hikari.MessageFlag.EPHEMERAL
        )
        return
    try:
        current_player = await lavalink.fetch_player(ctx.guild_id)
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


if __name__ == "__main__":
    bot.run()
