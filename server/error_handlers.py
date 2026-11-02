"""Turn application's expected errors in HTTP responses."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from game_engine.exceptions import PlayerFinishedAllPuzzlesError

from server.exceptions import AppError
from server.schemas import ErrorResponse

def _error_response(exc: AppError) -> JSONResponse:
    """Build the error body every route uses."""
    body = ErrorResponse(error_name=exc.error_name, message=exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content=body.model_dump(),
        # headers=exc.headers, NOTE: not sure about this
    )

# NOTE: FastAPI requires request for all custom exc handlers even if it doesn't get used so that's why it's here
def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    """Convert any AppError into a response."""
    return _error_response(exc)

def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, app_error_handler)

# TODO: add PlayerFinishedAllPuzzles handler, but need to look into separation reasoning more