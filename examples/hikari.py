# Example for base Hikari.

import hikari
import ongaku

bot = hikari.GatewayBot(token="...")

lavalink = ongaku.Ongaku(bot, password="youshallnotpass")


@bot.listen(hikari.events.StartedEvent)
async def started_event(event: hikari.events.StartedEvent):
    await lavalink.connect(
        bot.get_me().id  # type: ignore This needs to be ignored, as it should exist, however it is optional.
    )
