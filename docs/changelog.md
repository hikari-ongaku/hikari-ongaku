---
hide:
  - navigation
  - toc
---

# Changelogs

All the changelogs for `hikari-ongaku`.

## **v0.4.0**
 - Ongaku -> Client: `ongaku.Ongaku()` has been replaced by `ongaku.Client()`.
 - Client:
    - create, delete, and fetch player, has been renamed from `client.create_player()` -> `client.player.create()`, for all types.
 - `nodes` -> `sessions`: Nodes has been replaced with sessions, to match lavalink.
 - Sessions:
    - Websocket: It is now handled as a task, and no longer concurrently.
    - Manual: The ability to create your own sessions, by whatever methods you want.
    - Connection: The connection to the websocket lavalink provides, is now handled as a task, and not directly blocking your code. This also means it can be shutdown.
 - Player:
    - Exceptions: More cleanly handled, plus, documentation on those exceptions as well.
    - Updates: Each time a function is called, the player is actually modified (via any function) the player will be modified to reflect that.
    - volume -> set_volume: The reason for this rename, is so that the `volume` is the current volume, and `set_volume` actually sets the volume.
    - auto-play: a new feature has been added, called autoplay. (technically, it already existed) but now you can disable (and re-enable) it, and check its status via `player.set_autoplay()` and `player.autoplay`
 - Rest changes:
    - General Function: All rest actions are no longer scattered across with some containing some error exceptions, and others containing different exceptions, they all will except, in the exact same way.
    - Searching: Ongaku no longer handles your queries, with whether or not, they are a url, or a query for youtube, youtube music, or soundcloud.
    - RestApi -> RESTClient: `RestApi` has been replaced by `RESTClient` for more consistent naming. (This does not change anything outside of it.)
    - Added methods: added `decode_track`, and `decode_tracks` for more search functions.
 - Documentation:
    - Type checking: There is now type checking for the doc strings, so, they should look similar, with a lot more information packed within them.
    - Extensions: New tab added, for extensions, where extensions can be added in the future.

## **v0.3.0**
 - Filters: Added filters, for the lavalink players, so your able to change different sound effects for the players, like the EQ, Low Pass, Vibrato, and [more][ongaku.abc.filters].
 - Requestors: Added the ability to set a requestor to a specific track. When a song is added to the player, you can set a requestor as an optional argument. You can then fetch it via the [track][ongaku.abc.track.Track].
 - Auto Nodes: Automatically creates nodes, for each new shard within the hikari bot.