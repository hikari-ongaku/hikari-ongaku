# The basics

## Installation #

To install Ongaku, simply run the following:

```
pip install hikari-ongaku
```

## Basic setup #


All bots that use Ongaku, require the following basics. 

 - Gateway Bot
 - Ongaku

### Gateway Bot #

you must have a gateway bot, like any other hikari discord bot. This library is compatible with all hikari command handlers.

```python
import hikari

bot = hikari.GatewayBot(
    token="..."
)

bot.run()
```

### Ongaku #

You now must make the ongaku class, and attach it to hikari.

```python
import ongaku

1

int

# comment

def function()

lavalink = ongaku.Ongaku(
    bot,
    password="youshallnotpass"
)
```

## Thats it!

After doing all of that, you can now officially start the bot, and have a connection to your lavalink server.
For actually playing audio, check out the [commands](commands.md) for more information.