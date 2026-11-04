"""Messages that server pushes to be displayed to players over the websocket."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from game_engine.scoring import LetterStatus
from game_engine.scoring import WORD_LENGTH

# NOTE: Why 'type' in these classes? and not server models?
# Because it acts as a label so the client knows what kind of message/response it's receiving
# REST routes already tell client what a response is through the URL and method,
# but the websocket is one connection carrying three different message shapes, so we have to identify each message

class WsMessage(BaseModel):
    """Define the rules shared by every Websocket message."""
    model_config = ConfigDict(extra="forbid", frozen=True)

class TickMessage(WsMessage):
    """Sent every second for the client's timer countdown."""
    type: Literal["tick"] = "tick"
    phase: Literal["countdown", "active"]
    seconds_left: int = Field(ge=0)


class OpponentUpdateMessage(WsMessage):
    """Sent to a player when their oppenent submits a guess."""
    type: Literal["opponent_update"] = "opponent_update"
    colors: list[LetterStatus] = Field(min_length=WORD_LENGTH, max_length=WORD_LENGTH)
    solved_count: int = Field(ge=0)


class MatchEndMessage(WsMessage):
    """Sent to players when a match ends."""
    type: Literal["match_end"] = "match_end"
    winner: str | None