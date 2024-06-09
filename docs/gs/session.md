---
title: Sessions
description: Using, switching and creating session handlers
---

# sessions

## Changing Session Handler

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
