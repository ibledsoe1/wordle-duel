"""HTTP routes for the Match resource and the Players inside a match."""

from fastapi import APIRouter, Depends, status

from server.dependencies import get_match_manager
from server.match_manager import JoinResult, MatchManager
from server.schemas import (
    CreateMatchRequest,
    JoinMatchRequest,
    PlayerResponse,
    MatchStateResponse,
    ErrorResponse,
)

router = APIRouter(prefix="/matches", tags=["Matches"])

@router.post(
    "",
    response_model=PlayerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a match",
    description="Create a match and its first player (the creator)."
)
def create_match(
    data: CreateMatchRequest,
    manager: MatchManager = Depends(get_match_manager),
) -> JoinResult:
    """Pass the validated request to the manager"""
    return manager.create_match(data) 


@router.post(
    "/{match_id}/players",
    response_model=PlayerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Join a match as a player",
    description="Add a player to an existing match.",
)
def join_match(
    # NOTE: could match_id be included in JoinMatchRequest?
    match_id: str,
    data: JoinMatchRequest,
    manager: MatchManager = Depends(get_match_manager),
) -> JoinResult:
    """Pass the match ID and validated request to the manager"""
    return manager.join_match(match_id, data)


@router.get(
    "/{match_id}",
    response_model=MatchStateResponse,
    summary="Get a match's public state",
    description="Return public state of a match.",
)
def get_match_state(
    match_id: str, 
    manager: MatchManager = Depends(get_match_manager),
) -> MatchStateResponse:
    match = manager.get_match(match_id)
    return MatchStateResponse(
        match_id=match.config.match_id,
        status=match.status,
        player_count=len(match.players),
        player_names=[player.name for player in match.players.values()],
        guess_limit=match.config.duration_seconds,
    )