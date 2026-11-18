"""
Network client wrapper.

This is for players to be able to create and join matches,
and it translates any failures into predictable errors
"""

import httpx
from client.config import SERVER_URL, REQUEST_TIMEOUT


# only carries error name because it's the fixed error identifier
# message gets decided from the error name
class NetworkError(Exception):
    def __init__(self, error_name: str):
        super().__init__(error_name)
        self.error_name = error_name

def _post(path: str, body: dict) -> dict:
    try:
        response = httpx.post(f"{SERVER_URL}{path}", json=body, timeout=REQUEST_TIMEOUT)
    except httpx.RequestError:
        raise NetworkError("server_unreachable")
    if response.is_success:
        return response.json()
    
    try:
        error_name = response.json().get("error_name")
    except (ValueError, AttributeError):
        error_name = None
    raise NetworkError(error_name or "unknown_error")

def create_match(name: str, duration_seconds: int) -> dict:
    return _post("/matches", {"name": name, "duration_seconds": duration_seconds})

def join_match(match_id: str, name: str) -> dict:
    return _post(f"/matches/{match_id.strip()}/players", {"name": name})