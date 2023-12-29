from __future__ import annotations

from .errors import *
from .events import *
from .ongaku import *
from .enums import *
from .player import *
from .rest import *


from .abc.track import Track, Playlist, SearchResult

__all__ = (
    "Track", 
    "Playlist", 
    "SearchResult"
)
