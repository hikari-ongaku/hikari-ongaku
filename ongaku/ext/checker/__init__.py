"""
Checker.

The extension, that allows you to check if a link is a url, or a video/playlist!
"""
from __future__ import annotations

from .checker import check
from .abc import Checked, CheckedType

__all__ = (
    "check",
    "Checked",
    "CheckedType"
)