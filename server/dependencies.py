"""Shared objects that routes (and websocket code later?) get through Depends."""

from server.match_manager import MatchManager

match_manager = MatchManager()

def get_match_manager() -> MatchManager:
    return match_manager