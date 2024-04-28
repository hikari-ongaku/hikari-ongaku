---
title: Changelog
description: Changelog for Ongaku
hide:
  - navigation
  - toc
---

# Changelogs

All the changelogs for `hikari-ongaku`.

## **v0.5.0**

 - About: Added about, so a few terminal commands can be used, to check the version of ongaku your using, about ongaku, and where it is installed.
 - Logging: Added logging, mainly warnings, and errors, but also, traces, for errors and debugging stuff.
 - Examples: Cleaned up examples, and made them more accurate.
 - ABC:
    - Complete reformatting: all abc files, have been reformatted, to use the new method of handling payloads, [pydantic](https://docs.pydantic.dev/)!
 - Fixes:
    - Player skip: An error occurred, when trying to skip a song, the bot would attempt to also use `autoplay` to play the next song, and keep looping, causing it to spam lavalink with update requests.
    - Player play: There was an issue, where, if the queue had songs, but you didn't provide a track, it would raise an error. This is no longer an issue.
    - Player autoplay: Fixed an issue, where it would duplicate the next track, when auto-playing tracks.
    - Player/Session Shutdown: Fixed an issue, where sessions were not shut down at all, and hikari forcefully shuts them down. This is no longer an issue, and you will not see a warning like `W 0000-00-00 00:00:00,000 hikari.bot: terminating 1 remaining tasks forcefully`
    - Player disconnect: Fixed an issue, where if you used `player.disconnect()`, it would not remove it from the node.

## **v0.4.1**
 - Extensions:
   - Added the ability to create extensions for ongaku.
   - Checker: Checks if a link, contains a video/playlist.
 - Fixes:
   - player skip: Fixed an issue where the skip function would not work.
   - player stop: Added a new function, to stop the current track, via removing it from the guilds session.

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
 - Filters: Added filters, for the lavalink players, so your able to change different sound effects for the players, like the EQ, Low Pass, Vibrato, and more.
 - Requestors: Added the ability to set a requestor to a specific track. When a song is added to the player, you can set a requestor as an optional argument. You can then fetch it via the [track][ongaku.abc.track.Track].
 - Auto Nodes: Automatically creates nodes, for each new shard within the hikari bot.