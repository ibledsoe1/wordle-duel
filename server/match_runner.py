"""Runs the match timeline: countdown, match clock, and the match end"""

import asyncio

from game_engine.models import MatchStatus
from server.connection_manager import ConnectionManager
from server.match_manager import MatchManager
from server.ws_messages import MatchEndMessage, TickMessage

COUNTDOWN_SECONDS = 5

class MatchRunner:
    def __init__(
        self,
        manager: MatchManager,
        connections: ConnectionManager,
        countdown_seconds: int = COUNTDOWN_SECONDS,
        tick_interval: float = 1.0,
    ) -> None:
        self._manager = manager
        self._connections = connections
        self._countdown_seconds = countdown_seconds
        self._tick_interval = tick_interval
        # Keep references to each running task so it's not garbage-collected
        self._tasks: dict[str, asyncio.Task] = {}

    def start(self, code: str) -> None:
        match = self._manager.get_match(code)
        code = match.config.match_id
        if match.status != MatchStatus.COUNTDOWN or code in self._tasks:
            return
        self._tasks[code] = asyncio.create_task(self._run(code))

    async def _run(self, code: str) -> None:
        try:
            await self._tick_down(code, "countdown", self._countdown_seconds)
            self._manager.finish_match(code)

            # Placeholder winnner=None for now
            # TODO: real winner and tiebreaker logic next sprint
            await self._connections.broadcast(code, MatchEndMessage(winner=None))
        finally:
            self._tasks.pop(code, None)

    async def _tick_down(self, code: str, phase: str, seconds: int) -> None:
        for seconds_left in range(seconds, 0, -1):
            await self._connections.broadcast(
                code, TickMessage(phase=phase, seconds_left=seconds_left)
            )
            await asyncio.sleep(self._tick_interval)
