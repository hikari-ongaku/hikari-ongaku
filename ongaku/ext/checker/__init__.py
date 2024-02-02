"""
Checker.

The extension, that allows you to check if a link is a url, or a video/playlist!
"""
from __future__ import annotations

from .abc import Checked
from .abc import CheckedType
from .checker import check

__all__ = ("check", "Checked", "CheckedType")
