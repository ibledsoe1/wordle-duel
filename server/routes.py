"""HTTP routes for the Match resource and the Players inside a match."""
# TODO: Add responses in the decorators

from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from server.dependencies import get_match_manager
from server.match_manager import JoinResult, MatchManager
from server.schemas import (
    CreateMatchRequest,
    JoinMatchRequest,
    PlayerResponse,
    MatchStateResponse,
    GuessRequest,
    GuessResponse,
    ErrorResponse,
)

router = APIRouter(prefix="/matches", tags=["Matches"])

bearer_scheme = HTTPBearer(
    auto_error=False, # Give None instead of FastAPIs own error
    description="Send player_id as: Authorization: Bearer <player_id>"
)

def get_player_token(
        credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)
) -> str | None:
    """The bearer token(player_id), or None if header is absent."""
    return credentials.credentials if credentials else None


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


@router.post(
    "/{match_id}/guesses",
    response_model=GuessRequest,
    summary="Submit a guess",
    description="Score a submitted guess for the authenticated player."
)
def submit_guess(
    match_id: str, 
    data: GuessRequest,
    token: str | None = Depends(get_match_manager),
    manager: MatchManager = Depends(get_match_manager),
) -> GuessResponse:
    """Pass match ID, bearer token, and guess to manager."""
    return manager.submit_guess(match_id, token, data.guess)