# schemas: defined shapes for data to follow, constraints
# these are for request and response data for creating and joining matches,
# creating players, returning match state, and error responses
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from game_engine.models import MatchStatus
from game_engine.scoring import LetterStatus
from game_engine.word_list import WORD_LENGTH

PlayerName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=20)
]

DurationSeconds = Literal[60, 120, 180, 240, 300]

MAX_WORD_COUNT = 40


class CreateMatchRequest(BaseModel):
    """Validate the creator's name and optional settings for a new match"""

    # Reject unknown JSON fields, strip whitespace
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, frozen=True)

    name: PlayerName = Field(
        description="Display name for the creator (1 to 20 characters).",
        examples=["Izzy"],
    )
    duration_seconds: DurationSeconds | None = Field(
        default=None, # None means use the server's default (from MatchConfig)
        description="Match length in seconds: 60, 120, 180, 240, 300",
        examples=[180],
    )
    word_count: int | None = Field(
        default=None, 
        gt=0,
        le=MAX_WORD_COUNT,
        description="Number of words in the match. Omit to use server default (10).",
        examples=[5],
    )


class JoinMatchRequest(BaseModel):
    """Validate the name a second player sends when joining a match."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, frozen=True)

    name: PlayerName = Field(
        description="Display name for the creator (1 to 20 characters).",
        examples=["Izzy"],
    )

class GuessRequest(BaseModel): 
    """Validate the word a player submits as a guess."""
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, frozen=True)

    guess: str = Field(
        min_length=1,
        max_length=WORD_LENGTH,
        description="The guessed word.",
        examples=["CRANE"],
    )

class GuessResponse(BaseModel):
    """Describe the scored result of a guess"""
 
    model_config = ConfigDict(frozen=True)
 
    colors: list[LetterStatus] = Field(description="One color per letter of the guess.")
    puzzle_ended: bool = Field(description="True if this guess finished the word.")
    solved: bool = Field(description="True if the word was guessed correctly.")


# NOTE: merged with CreateMatchResponse because it was redundant,
# I don't really see them doing different things in the long run so I merged them
class PlayerResponse(BaseModel):
    """Describe a newly added player to a match"""

    model_config = ConfigDict(frozen=True)

    match_id: str = Field(description="Server-generated match identifier.")
    player_id: str = Field(description="Server-generated match specific player identifier")
    status: MatchStatus = Field(description="Current match status.")


class MatchStateResponse(BaseModel):
    """Describe the public, read-only state of a match"""

    model_config = ConfigDict(frozen=True)

    match_id: str = Field(description="Match identifier.")
    status: MatchStatus = Field(description="Current match status.")
    player_count: int = Field(ge=0, description="Number of players who have joined.")
    player_names: list[str] = Field(
        description="Display names of the player, in order they joined.",
        examples=[["Sam", "Alex"]],
    )
    guess_limit: int = Field(gt=0, description="Maximum guesses per word.")
    duration_seconds: int = Field(gt=0, description="Match length in seconds.")


class ErrorResponse(BaseModel):
    """Describe the body of every error response"""

    model_config = ConfigDict(frozen=True)

    error_name: str = Field(
        description="Name describing the specific error.",
        examples=["match_full"],
    )

    message: str = Field(
        description="Human readable explanation.",
        examples=["This match is already full."]
    )