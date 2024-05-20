"""
Statistics ABC's.

The statistic abstract classes.
"""

from __future__ import annotations

import attrs


__all__ = ("Memory", "Cpu", "FrameStatistics", "Statistics")


@attrs.define
class Memory:
    """
    Statistics Memory.

    All of the Statistics Memory information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#memory)
    """

    _free: int = attrs.field(alias="free")
    _used: int = attrs.field(alias="used")
    _allocated: int = attrs.field(alias="allocated")
    _reservable: int = attrs.field(alias="reservable")

    @property
    def free(self) -> int:
        """The amount of free memory in bytes."""
        return self._free

    @property
    def used(self) -> int:
        """The amount of used memory in bytes."""
        return self._used
    
    @property
    def allocated(self) -> int:
        """The amount of allocated memory in bytes."""
        return self._allocated
    
    @property
    def reservable(self) -> int:
        """The amount of reservable memory in bytes."""
        return self._reservable


@attrs.define
class Cpu:
    """
    Statistics CPU.

    All of the Statistics CPU information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#cpu)
    """

    _cores: int = attrs.field(alias="cores")
    _system_load: float = attrs.field(alias="system_load")
    _lavalink_load: float = attrs.field(alias="lavalink_load")

    @property
    def cores(self) -> int:
        """The amount of cores the server has."""
        return self._cores

    @property
    def system_load(self) -> float:
        """The system load of the server."""
        return self._system_load

    @property
    def lavalink_load(self) -> float:
        """The load of Lavalink on the server."""
        return self._lavalink_load


@attrs.define
class FrameStatistics:
    """
    Statistics Frame Statistics.

    All of the Statistics frame statistics information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#frame-stats)
    """

    _sent: int = attrs.field(alias="sent")
    _nulled: int = attrs.field(alias="nulled")
    _deficit: int = attrs.field(alias="deficit")

    @property
    def sent(self) -> int:
        """The amount of frames sent to Discord."""
        return self._sent

    @property
    def nulled(self) -> int:
        """The amount of frames that were nulled."""
        return self._nulled

    @property
    def deficit(self) -> int:
        """The difference between sent frames and the expected amount of frames."""
        return self._deficit
    

@attrs.define
class Statistics:
    """
    Statistics.

    All of the Statistics information.

    ![Lavalink](../../assets/lavalink_logo.png){ .twemoji } [Reference](https://lavalink.dev/api/websocket.html#stats-object)
    """

    _players: int = attrs.field(alias="players")
    _playing_players: int = attrs.field(alias="playing_players")
    _uptime: int = attrs.field(alias="uptime")
    _memory: Memory = attrs.field(alias="memory")
    _cpu: Cpu = attrs.field(alias="cpu")
    _frame_stats: FrameStatistics | None = attrs.field(alias="frame_stats")

    @property
    def players(self) -> int:
        """The amount of players connected to the session."""
        return self._players

    @property
    def playing_players(self) -> int:
        """The amount of players playing a track."""
        return self._playing_players

    @property
    def uptime(self) -> int:
        """The uptime of the session in milliseconds."""
        return self._uptime
    
    @property
    def memory(self) -> Memory:
        """The memory stats of the session."""
        return self._memory
        
    @property
    def cpu(self) -> Cpu:
        """The cpu stats of the session."""
        return self._cpu

    @property
    def frame_stats(self) -> FrameStatistics | None:
        """The frame stats of the session."""
        return self._frame_stats
    


# MIT License

# Copyright (c) 2023 MPlatypus

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
