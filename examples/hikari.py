# Example for base Hikari.

import hikari

import ongaku

bot = hikari.GatewayBot(token="...")

lavalink = ongaku.Ongaku(bot, password="youshallnotpass")
