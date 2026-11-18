from dataclasses import dataclass

@dataclass
class Player:
    name: str = ""
    player_id: str | None = None
    match_id: str | None = None