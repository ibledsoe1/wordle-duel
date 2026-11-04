"""WebSocket Connection manager, keeps track of open connections, grouped by match."""

from fastapi import WebSocket, WebSocketDisconnect

from server.ws_messages import WsMessage

class ConnectionManager:
    def __init__(self) -> None:
        self._connections: dict[str, dict[str, WebSocket]] = {}

    async def connect(self, code: str, player_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self._connections.setdefault(code, {})[player_id] = websocket

    def disconnect(self, code: str, player_id: str) -> None:
        players = self._connections.get(code)
        if players is None:
            return
        players.pop(player_id, None)
        if not players:
            del self._connections[code]

    def connected_count(self, code: str) -> int:
        return len(self._connections.get(code, {}))

    async def send_to(self, code: str, player_id: str, message: WsMessage) -> None:
        """Send message to one player."""
        websocket = self._connections.get(code, {}).get(player_id)
        if websocket is None:
            return
        try:
            await websocket.send_json(message.model_dump(mode="json"))
        except (WebSocketDisconnect, RuntimeError):
            self.disconnect(code, player_id)

    async def send_to_others(self, code: str, sender_id: str, message: WsMessage) -> None:
        """Send message to other players that aren't the sender."""
        for player_id in list(self._connections.get(code, {})):
            if player_id != sender_id:
                await self.send_to(code, player_id, message)

    async def broadcast(self, code: str, message: WsMessage) -> None:
        """Send message to all players."""
        for player_id in list(self._connections.get(code, {})):
            await self.send_to(code, player_id, message)