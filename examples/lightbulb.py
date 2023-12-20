# Example for Lightbulb handler.

import hikari, lightbulb, os, dotenv

import ongaku

dotenv.load_dotenv("secrets.env")

token = os.getenv("TOKEN", "")

bot = lightbulb.BotApp(
    token=os.getenv("TOKEN", ""),
    banner=None
)

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



@bot.command
@lightbulb.option("query", "The song you wish to play (or a playlist link.)")
@lightbulb.command("play", "play a song")
@lightbulb.implements(lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context) -> None:
    if ctx.guild_id == None:
        await ctx.respond("This command must be ran in a guild.")
        return
    
    voice_state = bot.cache.get_voice_state(ctx.guild_id, ctx.author.id)
    if not voice_state or not voice_state.channel_id:
        await ctx.respond("you are not in a voice channel.")
        return
    
    query = ctx.options.query

    if query == None or not isinstance(query, str):
        await ctx.respond(
            "A query is required."
        )
        return
    
    await ctx.respond(
        hikari.ResponseType.DEFERRED_MESSAGE_CREATE
    )

    musicthing = ongaku.Ongaku(ctx.bot, password="youshallnotpass")

    results = await musicthing.rest.search(ongaku.PlatformType.YOUTUBE, query)

    if results == None:
        await ctx.respond(
            hikari.ResponseType.DEFERRED_MESSAGE_UPDATE,
            "Sorry, no songs were found."
        )
        return
    
        
    embed = hikari.Embed(
        title=f"[{results[0].track.title}]({results[0].track.uri})",
        description=f"made by: {results[0].track.author}"
    )

    player = await lavalink.create_player(ctx.guild_id, ctx.channel_id)

    await player.play(results[0], ctx.author.id)

    try:
        await bot.update_voice_state(ctx.guild_id, voice_state.channel_id, self_deaf=True)
    except Exception as e:
        print(e)

    await ctx.respond(
        hikari.ResponseType.DEFERRED_MESSAGE_UPDATE,
        embed=embed
    )

lavalink = ongaku.Ongaku(bot, password="youshallnotpass")

@bot.listen(hikari.events.StartedEvent)
async def start_event(event):
    me = bot.get_me()

    if me == None:
        print("bot is none.")
        return
    
    await lavalink.connect(me.id)

if __name__ == "__main__":
    bot.run()