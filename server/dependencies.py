"""Shared objects that routes (and websocket code later?) get through Depends."""

from server.match_manager import MatchManager
from server.connection_manager import ConnectionManager
from server.match_runner import MatchRunner

match_manager = MatchManager()
connection_manager = ConnectionManager()
match_runner = MatchRunner(match_manager, connection_manager)

def get_match_manager() -> MatchManager:
    return match_manager

def get_connection_manager() -> ConnectionManager:
    return connection_manager

def get_match_runner() -> MatchRunner:
    return match_runner