# Example for Lightbulb handler.

import hikari
import lightbulb
import ongaku

bot = lightbulb.BotApp(token="...", banner=None)

# You MUST setup the base Ongaku class. Everything starts from here.
lavalink = ongaku.Ongaku(bot, password="youshallnotpass")

# You then MUST connect the websocket, for events.


@bot.listen(hikari.events.StartedEvent)
async def start_event(event):
    me = bot.get_me()

    if me == None:
        print("bot is none.")
        return

    await lavalink.connect(me.id)


# Events


@bot.listen(ongaku.ReadyEvent)
async def ready_event(event: ongaku.ReadyEvent):
    print("Ready event")


@bot.listen(ongaku.StatisticsEvent)
async def stats_event(event: ongaku.StatisticsEvent):
    print("Stats event")


@bot.listen(ongaku.TrackStartEvent)
async def track_start_event(event: ongaku.TrackStartEvent):
    print("Track start event")


@bot.listen(ongaku.TrackEndEvent)
async def track_end_event(event: ongaku.TrackEndEvent):
    print("Track end event")


@bot.listen(ongaku.TrackExceptionEvent)
async def track_exception_event(event: ongaku.TrackExceptionEvent):
    print("Track exception event")


@bot.listen(ongaku.TrackStuckEvent)
async def track_event(event: ongaku.TrackStuckEvent):
    print("Track stuck event")


@bot.listen(ongaku.WebsocketClosedEvent)
async def test_stats_event(event: ongaku.WebsocketClosedEvent):
    print("Websocket closed event")


# The following, is just a bunch of example commands.


@bot.command
@lightbulb.option("query", "The song you wish to play (or a playlist link.)")
@lightbulb.command("play", "play a song")
@lightbulb.implements(lightbulb.SlashCommand)
async def play_command(ctx: lightbulb.Context) -> None:
    if ctx.guild_id == None:
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

    if query == None or not isinstance(query, str):
        await ctx.respond("A query is required.", flags=hikari.MessageFlag.EPHEMERAL)
        return

    await ctx.respond(
        hikari.ResponseType.DEFERRED_MESSAGE_CREATE, flags=hikari.MessageFlag.EPHEMERAL
    )

    musicthing = ongaku.Ongaku(ctx.bot, password="youshallnotpass")

    results = await musicthing.rest.search(ongaku.PlatformType.YOUTUBE, query)

    if results == None:
        await ctx.respond(
            hikari.ResponseType.DEFERRED_MESSAGE_UPDATE,
            "Sorry, no songs were found.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return

    embed = hikari.Embed(
        title=f"[{results[0].track.title}]({results[0].track.uri})",
        description=f"made by: {results[0].track.author}",
    )

    player = await lavalink.create_player(ctx.guild_id, ctx.channel_id)

    await player.play(results[0], ctx.author.id)

    try:
        await bot.update_voice_state(
            ctx.guild_id, voice_state.channel_id, self_deaf=True
        )
    except Exception as e:
        print(e)

    await ctx.respond(
        hikari.ResponseType.DEFERRED_MESSAGE_UPDATE,
        embed=embed,
        flags=hikari.MessageFlag.EPHEMERAL,
    )


@bot.command
@lightbulb.command("pause", "pause a song")
@lightbulb.implements(lightbulb.SlashCommand)
async def pause_command(ctx: lightbulb.Context) -> None:
    await ctx.respond("This command does not work.", flags=hikari.MessageFlag.EPHEMERAL)


@bot.command
@lightbulb.command("skip", "skip a song")
@lightbulb.implements(lightbulb.SlashCommand)
async def skip_command(ctx: lightbulb.Context) -> None:
    await ctx.respond("This command does not work.", flags=hikari.MessageFlag.EPHEMERAL)


@bot.command
@lightbulb.command("queue", "view the current queue.")
@lightbulb.implements(lightbulb.SlashCommand)
async def queue_command(ctx: lightbulb.Context) -> None:
    await ctx.respond("This command does not work.", flags=hikari.MessageFlag.EPHEMERAL)


@bot.command
@lightbulb.command("stop", "stop the current song.")
@lightbulb.implements(lightbulb.SlashCommand)
async def stop_command(ctx: lightbulb.Context) -> None:
    await ctx.respond("This command does not work.", flags=hikari.MessageFlag.EPHEMERAL)


@bot.command
@lightbulb.command("disconnect", "stop the song, and disconnect the bot.")
@lightbulb.implements(lightbulb.SlashCommand)
async def disconnect_command(ctx: lightbulb.Context) -> None:
    await ctx.respond("This command does not work.", flags=hikari.MessageFlag.EPHEMERAL)


@bot.command
@lightbulb.option(
    "value", "the value of the volume. 0-100.", type=int, min_value=0, max_value=100
)
@lightbulb.command("volume", "change the volume of the bot")
@lightbulb.implements(lightbulb.SlashCommand)
async def volume_command(ctx: lightbulb.Context) -> None:
    await ctx.respond("This command does not work.", flags=hikari.MessageFlag.EPHEMERAL)


if __name__ == "__main__":
    bot.run()
