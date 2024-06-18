---
title: Sessions
description: Using, switching and creating session handlers
---

# sessions

## Adding a new session to the Session Handler

Something that is needed to run a session is to add a new session.
This is the lavalink server that ongaku will connect too.

```py
client.create_session(
    ssl=False,
    host="127.0.0.1",
    port=2333,
    password="youshallnotpass"
)
```

!!! tip
    You can have more than one session connected to a singular client!

    This will give your bot more servers to fallback on if one fails.


## Changing The default Session Handler

The way you change your session handler, is when you create your client.

```py
client = ongaku.Client(
    bot,
    session_handler=ongaku.BasicSessionHandler
)
```

!!! note
    There is no need to specify a session handler by default. You only need to set one, if you wish to use a different session handler.

## Session Handlers

Below is all the available session handlers.

### BasicSessionHandler

This session handler is the default session handler.

The basic session handler simply just fetches (and stores) the current session. It will only give a different session, if the current session closes, or errors out.
