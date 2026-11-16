"""Turn application's expected errors in HTTP responses."""

"""
NOTE: LOOK AT 3310 MODULE 10

It uses a class 'problem_response' along with JSON response
IT also has 'problem_details' class/file
It also has handle_http_exception in the error_handler file 
    That doesn't mean necessarily I have to do that, just think about the pros and cons of doing it that way
It also has an unexpected error handler for any unexpected exceptions
It uses Exception premade for exc, but I use AppError, see if that's needed or not

In routers don't have to pass message by hand, just use the errors outlined from problem_response


Another way to approach this w/o adding tons of error types is to have a base class (ex: DomainError)
and whenever we need a new error we can extend from that base class
in our error handler we can say 'handle all DomainErrors this way'
so we don't have to add handler for each individual type every new one added, because we already have the DomainError handler registered
this is essentially polymorphism

"""

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