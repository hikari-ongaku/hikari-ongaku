# Nodes

There is two options for nodes. The first one is enabled by default.

## Auto nodes

This is automatically enabled by default, and will automatically handle your nodes.

## Manual nodes

This is for people that want to do manual nodes.

!!! warning
    `client.player.create()` does not work, if manual nodes is used. You **must** fetch the node somehow, or know its name, before you create the player.

Firstly, you want to set auto_nodes to off, so that you don't have overlapping nodes.
```python
client = ongaku.Client(
    ...,
    auto_nodes=False
)
```

Then, you want to create a node, for example, you would do something like the following
```python
@bot.listen(hikari.StartedEvent)
async def started(event: hikari.StartedEvent):
    node = await client.node.create("main")
```

Then, when you need to fetch the player, you would need to use the following

```python
node = client.node.fetch("main")
```

and then from that node, you would create a player.

```python
node.player.create(guild_id)
```

And lastly, fetching, and deleting a node, can be done via the client, or the node itself.

```python
client.player.fetch(guild_id)

node.player.fetch(guild_id)
```

```python
client.player.delete(guild_id)

node.player.delete(guild_id)
```