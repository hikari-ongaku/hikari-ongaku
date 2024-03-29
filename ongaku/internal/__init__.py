"""
Internal.

All internal based functions and items.
"""

from __future__ import annotations

from ongaku.internal.about import __author__
from ongaku.internal.about import __author_email__
from ongaku.internal.about import __license__
from ongaku.internal.about import __maintainer__
from ongaku.internal.about import __url__
from ongaku.internal.about import __version__
from ongaku.internal.logger import TRACE_LEVEL
from ongaku.internal.logger import TRACE_NAME
from ongaku.internal.logger import logger
from ongaku.internal.types import RESTClientT

__all__ = (
    # ongaku.internal.about
    "__author__",
    "__author_email__",
    "__maintainer__",
    "__license__",
    "__url__",
    "__version__",
    # ongaku.internal.logger
    "TRACE_LEVEL",
    "TRACE_NAME",
    "logger",
    # ongaku.internal.types
    "RESTClientT",
)
