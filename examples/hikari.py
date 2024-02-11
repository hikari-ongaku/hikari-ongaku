# ruff: noqa: D100, D101, D102, D103

# ╔════════════════╗
# ║ Hikari example ║
# ╚════════════════╝

import logging

import hikari

import ongaku
from ongaku.ext import checker

bot = hikari.GatewayBot("...")

ongaku_client = ongaku.Client(bot, password="youshallnotpass")


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


prefix = "!"


def handle_command(content: str, name: str) -> list[str] | None:
    if content.startswith(prefix + name):
        content = content.strip(prefix + name + " ")
        return content.split(" ")


@bot.listen()
async def play_command(event: hikari.GuildMessageCreateEvent) -> None:
    if event.content is None:
        return

    args = handle_command(event.content, "play")

    if args is None:
        await bot.rest.create_message(
            event.channel_id,
            "You need to provide a song, or link.",
            reply=event.message,
        )
        return

    voice_state = bot.cache.get_voice_state(event.guild_id, event.author.id)
    if not voice_state or not voice_state.channel_id:
        await bot.rest.create_message(
            event.channel_id,
            "you are not in a voice channel.",
            reply=event.message,
        )
        return

    checked_query = await checker.check(args[0])

    if checked_query.type == checker.CheckedType.QUERY:
        result = await ongaku_client.rest.track.load(f"ytsearch:{checked_query.value}")
    else:
        result = await ongaku_client.rest.track.load(checked_query.value)

    if result is None:
        await bot.rest.create_message(
            event.channel_id,
            "Sorry, no songs were found.",
            reply=event.message,
        )
        return

    track: ongaku.Track

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
        player = await ongaku_client.player.fetch(event.guild_id)
    except ongaku.PlayerMissingException:
        player = await ongaku_client.player.create(event.guild_id)

    if player.connected is False:
        await player.connect(voice_state.channel_id)

    try:
        await player.play(track)
    except Exception as e:
        raise e

    await bot.rest.create_message(
        event.channel_id,
        embed=embed,
        reply=event.message,
    )


@bot.listen()
async def add_command(event: hikari.GuildMessageCreateEvent) -> None:
    if event.content is None:
        return

    args = handle_command(event.content, "add")

    if args is None:
        await bot.rest.create_message(
            event.channel_id,
            "You need to provide a song, or link.",
            reply=event.message,
        )
        return

    try:
        current_player = await ongaku_client.player.fetch(event.guild_id)
    except Exception:
        await bot.rest.create_message(
            event.channel_id,
            "You must have a player currently running!",
            reply=event.message,
        )
        return

    checked_query = await checker.check(args[0])

    if checked_query.type == checker.CheckedType.QUERY:
        result = await ongaku_client.rest.track.load(f"ytsearch:{checked_query.value}")
    else:
        result = await ongaku_client.rest.track.load(checked_query.value)

    if result is None:
        await bot.rest.create_message(
            event.channel_id,
            "Sorry, no songs were found.",
            reply=event.message,
        )
        return

    tracks: list[ongaku.Track] = []

    if isinstance(result, ongaku.Track):
        await current_player.add((result,))
        tracks.append(result)

    else:
        await current_player.add(result.tracks)
        tracks.extend(result.tracks)

    embed = hikari.Embed(
        title="Tracks added",
        description=f"All the tracks that have been added. (only shows top 25.)\nTotal tracks added: {len(tracks)}",
    )

    for track in tracks:
        if len(embed.fields) >= 25:
            break
        embed.add_field(track.info.title, track.info.author)

    await bot.rest.create_message(
        event.channel_id,
        embed=embed,
        reply=event.message,
    )


@bot.listen()
async def pause_command(event: hikari.GuildMessageCreateEvent) -> None:
    if event.content is None:
        return

    handle_command(event.content, "pause")

    try:
        current_player = await ongaku_client.player.fetch(event.guild_id)
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
            event.channel_id,
            "Music has been paused.",
            reply=event.message,
        )
        return

    await bot.rest.create_message(
        event.channel_id,
        "Music has been resumed.",
        reply=event.message,
    )


@bot.listen()
async def queue_command(event: hikari.GuildMessageCreateEvent) -> None:
    if event.content is None:
        return

    handle_command(event.content, "queue")

    try:
        player = await ongaku_client.player.fetch(event.guild_id)
    except Exception:
        await bot.rest.create_message(
            event.channel_id,
            "There is no player currently playing in this server.",
            reply=event.message,
        )
        return

    if len(player.queue) == 0:
        await bot.rest.create_message(
            event.channel_id,
            "There is not tracks in the queue currently.",
            reply=event.message,
        )
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

    await bot.rest.create_message(
        event.channel_id,
        embed=queue_embed,
        reply=event.message,
    )


@bot.listen()
async def volume_command(event: hikari.GuildMessageCreateEvent) -> None:
    if event.content is None:
        return

    args = handle_command(event.content, "volume")

    if args is None:
        return

    try:
        player = await ongaku_client.player.fetch(event.guild_id)
    except Exception:
        await bot.rest.create_message(
            event.channel_id,
            "There is no player currently playing in this server.",
            reply=event.message,
        )
        return

    try:
        volume = int(args[0])
    except:
        await bot.rest.create_message(
            event.channel_id,
            "Volume must be an integer.",
            reply=event.message,
        )
        return

    if volume > 100 or volume < 0:
        await bot.rest.create_message(
            event.channel_id,
            "Volume must be between 0 and 100.",
            reply=event.message,
        )
        return

    try:
        await player.set_volume(volume)
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
async def skip_command(event: hikari.GuildMessageCreateEvent) -> None:
    if event.content is None:
        return

    args = handle_command(event.content, "skip")

    if args is None:
        return

    try:
        player = await ongaku_client.player.fetch(event.guild_id)
    except Exception:
        await bot.rest.create_message(
            event.channel_id,
            "There is no player currently playing in this server.",
            reply=event.message,
        )
        return

    try:
        amount = int(args[0])
    except:
        await bot.rest.create_message(
            event.channel_id,
            "Volume must be an integer.",
            reply=event.message,
        )
        return

    if amount < 1:
        await bot.rest.create_message(
            event.channel_id,
            "Amount must be above 1.",
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
async def stop_command(event: hikari.GuildMessageCreateEvent) -> None:
    if event.content is None:
        return

    handle_command(event.content, "stop")

    try:
        player = await ongaku_client.player.fetch(event.guild_id)
    except Exception:
        await bot.rest.create_message(
            event.channel_id,
            "There is no player currently playing in this server.",
            reply=event.message,
        )
        return

    await player.disconnect()

    await bot.rest.create_message(
        event.channel_id,
        "Successfully stopped the player.",
        reply=event.message,
    )


if __name__ == "__main__":
    bot.run()
