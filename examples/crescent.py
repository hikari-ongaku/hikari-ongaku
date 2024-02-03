import logging

import crescent
import hikari

import ongaku

bot = hikari.GatewayBot("...")

client = crescent.Client(bot)

ongaku_client = ongaku.Client(bot, password="youshallnotpass")


# Events


@client.include
@crescent.event(ongaku.ReadyEvent)
async def ready_event(event: ongaku.ReadyEvent):
    logging.info(
        f"Ready Event, Resumed: {event.resumed}, session id: {event.session_id}"
    )


@client.include
@crescent.event(ongaku.TrackStartEvent)
async def track_start_event(event: ongaku.TrackStartEvent):
    logging.info(
        f"Track Started Event, guild: {event.guild_id}, Track Title: {event.track.info.title}"
    )


@client.include
@crescent.event(ongaku.TrackEndEvent)
async def track_end_event(event: ongaku.TrackEndEvent):
    logging.info(
        f"Track Ended Event, guild: {event.guild_id}, Track Title: {event.track.info.title}, Reason: {event.reason.name}"
    )


@client.include
@crescent.event(ongaku.TrackExceptionEvent)
async def track_exception_event(event: ongaku.TrackExceptionEvent):
    logging.info(
        f"Track Exception Event, guild: {event.guild_id}, Track Title: {event.track.info.title}, Exception message: {event.exception.message}"
    )


@client.include
@crescent.event(ongaku.TrackStuckEvent)
async def track_stuck_event(event: ongaku.TrackStuckEvent):
    logging.info(
        f"Track Stuck Event, guild: {event.guild_id}, Track Title: {event.track.info.title}, Threshold ms: {event.threshold_ms}"
    )


@client.include
@crescent.event(ongaku.WebsocketClosedEvent)
async def websocket_close_event(event: ongaku.WebsocketClosedEvent):
    logging.info(
        f"Websocket Close Event, guild: {event.guild_id}, Reason: {event.reason}, Code: {event.code}, By Remote: {event.by_remote}"
    )


@client.include
@crescent.event(ongaku.QueueNextEvent)
async def queue_next_event(event: ongaku.QueueNextEvent):
    logging.info(
        f"guild: {event.guild_id}'s track: {event.old_track.info.title} has finished! Now playing: {event.track.info.title}"
    )


@client.include
@crescent.event(ongaku.QueueEmptyEvent)
async def queue_empty_event(event: ongaku.QueueEmptyEvent):
    logging.info(f"Queue is empty in guild: {event.guild_id}")


# Commands


@client.include
@crescent.command(name="play", description="Play a song in a voice channel.")
class Play:
    query = crescent.option(str, "The song you wish to play.")

    async def callback(self, ctx: crescent.Context):
        if ctx.guild_id is None:
            await ctx.respond(
                "This command must be ran in a guild.",
                flags=hikari.MessageFlag.EPHEMERAL,
            )
            return

        voice_state = bot.cache.get_voice_state(ctx.guild_id, ctx.user.id)
        if not voice_state or not voice_state.channel_id:
            await ctx.respond(
                "you are not in a voice channel.", flags=hikari.MessageFlag.EPHEMERAL
            )
            return

        result = await ongaku_client.rest.track.load(self.query)

        if result is None:
            await ctx.respond(
                "Sorry, no songs were found.", flags=hikari.MessageFlag.EPHEMERAL
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

        await ctx.respond(embed=embed, flags=hikari.MessageFlag.EPHEMERAL)


@client.include
@crescent.command(name="add", description="add a song to the queue")
class Add:
    query = crescent.option(str, "The song you wish to play.")

    async def callback(self, ctx: crescent.Context):
        if ctx.guild_id is None:
            await ctx.respond(
                "This command must be ran in a guild.",
                flags=hikari.MessageFlag.EPHEMERAL,
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

        result = await ongaku_client.rest.track.load(self.query)

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
@crescent.command(
    name="pause", description="pause or unpause the currently playing song."
)
class Pause:
    async def callback(self, ctx: crescent.Context):
        if ctx.guild_id is None:
            await ctx.respond(
                "This command must be ran in a guild.",
                flags=hikari.MessageFlag.EPHEMERAL,
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
            await ctx.respond(
                "Music has been paused.", flags=hikari.MessageFlag.EPHEMERAL
            )
        else:
            await ctx.respond(
                "Music has been resumed.", flags=hikari.MessageFlag.EPHEMERAL
            )


@client.include
@crescent.command(name="queue", description="View the queue of the player.")
class Queue:
    async def callback(self, ctx: crescent.Context):
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
@crescent.command(name="volume", description="change the volume of the player.")
class Volume:
    volume = crescent.option(
        int, "The volume you wish to set.", min_value=0, max_value=100
    )

    async def callback(self, ctx: crescent.Context):
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
            await player.set_volume(self.volume * 10)
        except ValueError:
            await ctx.respond("Sorry, but you have entered an invalid number.")
            return

        await ctx.respond(f"the volume has successfully been set to {self.volume}/100")


@client.include
@crescent.command(name="skip", description="skip a song, or multiple")
class Skip:
    amount = crescent.option(
        int, "The amount of songs you wish to skip.", min_value=1, default=1
    )

    async def callback(self, ctx: crescent.Context):
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
            await player.skip(self.amount)
        except ongaku.PlayerQueueException:
            await ctx.respond(
                "It looks like the queue is empty, so no new songs will be played."
            )
            return

        await ctx.respond(f"{self.amount} song(s) were successfully skipped.")


@client.include
@crescent.command(
    name="stop", description="Stops the player, and disconnects it from the server."
)
class Stop:
    async def callback(self, ctx: crescent.Context):
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
