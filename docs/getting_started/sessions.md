# sessions

There is two options for sessions. The first one is enabled by default.

## Auto session

This is automatically enabled by default, and will automatically handle your session.

## Manual session

This is for people that want to do manual sessions.

!!! warning
    `client.player.create()` does not work, if manual sessions is used. You **must** fetch the session somehow, or know its name, before you create the player.

Firstly, you want to set auto_sessions to off, so that you don't have overlapping sessions.
```python
client = ongaku.Client(
    ...,
    auto_sessions=False
)
```

Then, you want to create a session, for example, you would do something like the following
```python
@bot.listen(hikari.StartedEvent)
async def started(event: hikari.StartedEvent):
    session = await client.session.create("main")
```

Then, when you need to fetch the player, you would need to use the following

```python
session = client.session.fetch("main")
```

and then from that session, you would create a player.

```python
session.player.create(guild_id)
```

And lastly, fetching, and deleting a session, can be done via the client, or the session itself.

```python
client.player.fetch(guild_id)

session.player.fetch(guild_id)
```

```python
client.player.delete(guild_id)

session.player.delete(guild_id)
```