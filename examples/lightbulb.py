# ╔═══════════╗
# ║ Lightbulb ║
# ╚═══════════╝

import logging
import hikari
import lightbulb

import ongaku

bot = hikari.GatewayBot("...")

client = lightbulb.GatewayEnabledClient(bot)

ongaku_client = ongaku.Client.from_lightbulb(client)

ongaku_client.create_session(
    name="lightbulb-session",
    host="127.0.0.1",
    password="youshallnotpass"
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
        f"Websocket Close Event, guild: {event.guild_id}, Reason: {event.reason}, Code: {event.code}"
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

@client.register()
class Play(
    lightbulb.SlashCommand,
    name="play",
    description="play a song."
):
    query = lightbulb.string("query", "The song you wish to add.")

    @lightbulb.invoke
    async def command(self, ctx: lightbulb.Context) -> None:
        if ctx.guild_id is None or ctx.member is None:
            await ctx.respond(
                "This command must be ran in a guild.", flags=hikari.MessageFlag.EPHEMERAL
            )
            return

        voice_state = bot.cache.get_voice_state(ctx.guild_id, ctx.member.id)
        if not voice_state or not voice_state.channel_id:
            await ctx.respond(
                "you are not in a voice channel.", flags=hikari.MessageFlag.EPHEMERAL
            )
            return

        await ctx.respond(
            hikari.ResponseType.DEFERRED_MESSAGE_CREATE, flags=hikari.MessageFlag.EPHEMERAL
        )

        result = await ongaku_client.rest.load_track(self.query)

        if result is None:
            await ctx.respond(
                "Sorry, no songs were found.",
                flags=hikari.MessageFlag.EPHEMERAL,
            )
            return

        track: ongaku.Track | None = None

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
            player = ongaku_client.fetch_player(ctx.guild_id)
        except Exception:
            player = ongaku_client.create_player(ctx.guild_id)

        await player.play(track)

        await ctx.respond(
            hikari.ResponseType.DEFERRED_MESSAGE_UPDATE,
            embed=embed,
            flags=hikari.MessageFlag.EPHEMERAL,
        )

@client.register()
class Add(
    lightbulb.SlashCommand,
    name="add",
    description="Add a song. (must be a name, not a url.)"
):
    query = lightbulb.string("query", "The song you wish to add.")

    @lightbulb.invoke
    async def command(
        self, ctx: lightbulb.Context,
    ) -> None:
        if ctx.guild_id is None:
            await ctx.respond(
                "This command must be ran in a guild.", flags=hikari.MessageFlag.EPHEMERAL
            )
            return
        try:
            current_player = ongaku_client.fetch_player(ctx.guild_id)
        except Exception:
            await ctx.respond(
                "You must have a player currently running!",
                flags=hikari.MessageFlag.EPHEMERAL,
            )
            return

        result = await ongaku_client.rest.load_track(self.query)

        if result is None:
            await ctx.respond(
                "Sorry, no songs were found.",
                flags=hikari.MessageFlag.EPHEMERAL,
            )
            return

        track_count: int = 0

        if isinstance(result, ongaku.Playlist):
            current_player.add((result.tracks[0],))
            track_count = 1

        elif isinstance(result, ongaku.Track):
            current_player.add((result,))
            track_count = 1

        else:
            current_player.add(result)
            track_count = len(result)

        await ctx.respond(f"Added {track_count} track(s) to the player.")


@client.register()
class Pause(
    lightbulb.SlashCommand,
    name="pause",
    description="Add a song. (must be a name, not a url.)"
):
    @lightbulb.invoke
    async def command(self, ctx: lightbulb.Context) -> None:
        if ctx.guild_id is None:
            await ctx.respond(
                "This command must be ran in a guild.", flags=hikari.MessageFlag.EPHEMERAL
            )
            return
        try:
            current_player = ongaku_client.fetch_player(ctx.guild_id)
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


@client.register()
class Queue(
    lightbulb.SlashCommand,
    name="queue",
    description="View the queue of the player."
):
    @lightbulb.invoke
    async def command(self, ctx: lightbulb.Context) -> None:
        if ctx.guild_id is None:
            await ctx.respond(
                "Guild ID is none! You must be in a guild to run this command.",
                flags=hikari.MessageFlag.EPHEMERAL,
            )
            return

        try:
            player = ongaku_client.fetch_player(ctx.guild_id)
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

@client.register()
class Volume(
    lightbulb.SlashCommand,
    name="volume",
    description="Change the volume of the player."
):
    volume = lightbulb.integer("volume", "The volume you wish to set.", min_value=0, max_value=200)

    @lightbulb.invoke
    async def command(
        self, ctx: lightbulb.Context,
    ) -> None:
        if ctx.guild_id is None:
            await ctx.respond(
                "Guild ID is none! You must be in a guild to run this command.",
                flags=hikari.MessageFlag.EPHEMERAL,
            )
            return

        try:
            player = ongaku_client.fetch_player(ctx.guild_id)
        except Exception:
            await ctx.respond(
                "There is no player currently playing in this server.",
                flags=hikari.MessageFlag.EPHEMERAL,
            )
            return

        try:
            await player.set_volume(self.volume)
        except ValueError:
            await ctx.respond("Sorry, but you have entered an invalid number.")
            return

        await ctx.respond(f"the volume has successfully been set to {self.volume}%")


@client.register()
class Skip(
    lightbulb.SlashCommand,
    name="skip",
    description="Skip a song, or multiple."
):
    amount = lightbulb.integer("amount", "the amount of songs to skip.", min_value=1)

    @lightbulb.invoke
    async def skip_command(
        self, ctx: lightbulb.Context,
    ) -> None:
        if ctx.guild_id is None:
            await ctx.respond(
                "Guild ID is none! You must be in a guild to run this command.",
                flags=hikari.MessageFlag.EPHEMERAL,
            )
            return

        try:
            player = ongaku_client.fetch_player(ctx.guild_id)
        except Exception:
            await ctx.respond(
                "There is no player currently playing in this server.",
                flags=hikari.MessageFlag.EPHEMERAL,
            )
            return

        try:
            await player.skip(self.amount)
        except ongaku.PlayerQueueError:
            await ctx.respond(
                "It looks like the queue is empty, so no new songs will be played."
            )
            return

        await ctx.respond(f"{self.amount} song(s) were successfully skipped.")


@client.register()
class Stop(
    lightbulb.SlashCommand,
    name="stop",
    description="Stops the player, and disconnects it from the server."
):
    @lightbulb.invoke
    async def stop_command(self, ctx: lightbulb.Context) -> None:
        if ctx.guild_id is None:
            await ctx.respond(
                "Guild ID is none! You must be in a guild to run this command.",
                flags=hikari.MessageFlag.EPHEMERAL,
            )
            return

        try:
            await ongaku_client.delete_player(ctx.guild_id)
        except Exception:
            await ctx.respond(
                "There is no player currently playing in this server.",
                flags=hikari.MessageFlag.EPHEMERAL,
            )
            return

        await ctx.respond("Successfully stopped the player.")


if __name__ == "__main__":
    bot.run()
