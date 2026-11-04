"""WebSocket route for the server to push match update messages to connected players."""

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from server.connection_manager import ConnectionManager
from server.dependencies import get_connection_manager, get_match_manager
from server.exceptions import AppError
from server.match_manager import MatchManager

router = APIRouter(tags=["WebSocket"])

# Code 1008 is a "policy violation", standard code for failed auth
WS_POLICY_VIOLATION = 1008

def get_ws_token(websocket: WebSocket) -> str | None:
    scheme, _, token = websocket.headers.get("authorization", "").partition(" ")
    if scheme.lower() != "bearer":
        return None
    return token.strip() or None

@router.websocket("/ws/matches/{match_id}")
async def match_socket(
    websocket: WebSocket,
    match_id: str,
    manager: MatchManager = Depends(get_match_manager),
    connections: ConnectionManager = Depends(get_connection_manager),
) -> None:
    """Hold a player's connection open for the lifespan of the match."""

    try:
        match = manager.get_match(match_id)
        player = manager.authenticate_player(match, get_ws_token(websocket))
    except AppError:
        await websocket.close(code=WS_POLICY_VIOLATION)
        return

    code = match.config.match_id
    await connections.connect(code, player.player_id, websocket)

    try:
        # TODO: countdown task to start match
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally: 
        connections.disconnect(code, player.player_id)
