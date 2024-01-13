
# Getting started

Getting Started with Ongaku.

In the following documents, you will learn how to work with ongaku, from its most basic features, to its more advanced features.

## Installation

To install Ongaku, simply run the following:

```
pip install hikari-ongaku
```

## Q's and A's
Below, will be the most common questions, and some answers to said questions.

<br>

|Question|Answer|
|--------|------|
|Why can't I use ongaku with a rest bot?|Ongaku relies on events, like the [Voice Server Update](https://docs.hikari-py.dev/en/latest/reference/hikari/events/voice_events/#hikari.events.voice_events.VoiceServerUpdateEvent) and the [Voice State Update](https://docs.hikari-py.dev/en/latest/reference/hikari/events/voice_events/#hikari.events.voice_events.VoiceStateUpdateEvent) events. Without them, the bot has no idea if its joined a voice channel, or the websocket connection, that it can stream audio to.|
|What is Ongaku compatible with?|Ongaku should be compatible with all hikari based command handlers and component handlers, however, further testing is required.|


### What is auto nodes
Auto nodes, is a simple feature, for creating new nodes (basically shards, for lavalink), without you having to do anything.

### Why auto nodes?
Auto nodes, means that for every shard your bot creates, it will create a new node. It makes sure that there isn't a heap of players on a single session.

If you would like, it is totally safe to disable this, but you need to create at least one node, so players can actually be created.