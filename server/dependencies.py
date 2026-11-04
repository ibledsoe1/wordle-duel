"""Shared objects that routes (and websocket code later?) get through Depends."""

from server.match_manager import MatchManager
from server.connection_manager import ConnectionManager

match_manager = MatchManager()
connection_manager = ConnectionManager()

def get_match_manager() -> MatchManager:
    return match_manager

def get_connection_manager() -> ConnectionManager:
    return connection_manager