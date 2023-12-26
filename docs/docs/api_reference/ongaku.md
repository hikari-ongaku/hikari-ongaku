# Ongaku

## Ongaku #

```python
Ongaku(
    bot: hikari.RESTAware,
    *,
    host: str = "localhost",
    port: int = 2333,
    password: str | None = None,
    version: enums.VersionType = enums.VersionType.V4,
    max_retries: int = 3
)
```

The base class for your Ongaku handler

|Parameter|Type|Description|Default|
|:--------|:---|:----------|:------|
|bot|hikari.RESTAware|The bot that Ongaku will attach too.|None|
|host*|string|The IP/host of the lavalink server you wish to connect to.|"localhost"|
|port*|int|The port of the lavalink server you wish to connect to.|2333|
|password*|str, None|The password to the lavalink server you wish to connect to.|None|
|version*|VersionType|The version of the lavalink server you wish to connect to.|VersionType.V4|
|max_retries*|int|The maximum amount of retries the server will attempt when the [connect()](#connect)|3|

!!! info
    `*` means it is an optional marker, and will have a default

### connect #

```python
connect(
    user_id: hikari.Snowflake
)
```

Allows for the bot to actually connect to the lavalink server.

|Parameter|Type|Description|Default|
|:--------|:---|:----------|:------|
|user_id|hikari.Snowflake|The User ID for the discord bot.|None|