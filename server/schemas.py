from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

from game_engine.models import MatchStatus

# NOTE: Ask Claude -> Why are playername and duration seconds in this schemas file?
# shouldn't they be in models.py?

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
    duration_seconds: int | None = Field(
        default=None, # None means use the server's default (from MatchConfig)
        gt=0,
        description="Match length in seconds: 60, 120, 180, 240, 300",
        examples=[180],
    )
    word_count: int | None = Field(
        default=10,
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


class CreateMatchResponse(BaseModel):
    """Describe the result of creating a match"""

    model_config = ConfigDict(frozen=True)

    match_id: str = Field(description="Server-generated match identifier.")
    player_id: str = Field(description="Server-generated match specific player identifier")
    status: MatchStatus = Field(description="Current match status.")

# NOTE: Ask if CreateMatchResponse and PlayerResponse are redundant
# could I just use player response for both? or combine them into one with a new name?

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
    # NOTE: Ask what 'safe to branch on' and 'may be reworded; do not branch on it' mean
    # from descriptions that claude generated
    message: str = Field(
        description="Human readable explanation.",
        examples=["This match is already full."]
    )