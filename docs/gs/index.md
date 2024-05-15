---
title: Getting Started
description: Home for getting started
---

# Getting started

Getting Started with Ongaku.

In the following documents, you will learn how to work with ongaku, from its most basic features, to its more advanced features.

## Installation

To install Ongaku, simply run the following:

```
pip install hikari-ongaku
```

## Where to next?

<div class="grid cards" markdown>

 -  Client as State

    ---

    How to set client as state in all different libraries.

    [:material-arrow-right: Learn more](./client.md)

 -  Player control

    ---

    All the functions of a player and its features.

    [:material-arrow-right: Learn more](./player.md)

 -  Sessions

    ---

    How to change to a different session handler, and what all session handlers do.

    [:material-arrow-right: Learn more](./session.md)

 -  Filters

    ---

    All the filter options, and how to use them.

    [:material-arrow-right: Learn more](./filter.md)

 -  Injection

    ---

    Shows how to use the injection for arc, and tanjun.

    [:material-arrow-right: Learn more](./injection.md)


</div>

## Q's and A's
Below, will be the most common questions, and some answers to said questions.

<br>

|Question|Answer|
|--------|------|
|Why can't I use ongaku with a rest bot?|Ongaku relies on events, like the [Voice Server Update](https://docs.hikari-py.dev/en/latest/reference/hikari/events/voice_events/#hikari.events.voice_events.VoiceServerUpdateEvent) and the [Voice State Update](https://docs.hikari-py.dev/en/latest/reference/hikari/events/voice_events/#hikari.events.voice_events.VoiceStateUpdateEvent) events. Without them, the bot has no idea if its joined a voice channel, or the websocket connection, that it can stream audio to.|
|What is Ongaku compatible with?|Ongaku should be compatible with all hikari based command handlers and component handlers, however, further testing is required.|

Got another question that should be added? contact me via [contact@mplaty.com](mailto:contact@mplaty.com)