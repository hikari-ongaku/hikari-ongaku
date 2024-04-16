---
title: Filters
description: Basics of creating and using filters.
---

# Filters

Filters are a feature, that allows for modifying the audio effects

For more information on filters, check out [here](https://lavalink.dev/api/rest.html#filters)

## Basics

To use filters, you need to make a filter.

```python
import ongaku

player_filter = ongaku.Filter()
```

Then, from that filter, you can then change, any of the filter types (which can be found above.)

```python
player_filter.set_equalizer(BandType.HZ400, 0.64)
player_filter.set_karaoke(mono_level=1)
```

or remove said filters

```python
player_filter.set_equalizer(BandType.HZ400, None)
player_filter.set_karaoke(mono_level=None)
```

And finally, you want to set that filter, to the player.

```python
player = client.fetch_player(guild_id)

player.filter(player_filter)
```

!!! WARNING
    If the filter object fails to build, you will receive an error.