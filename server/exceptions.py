class AppError(Exception):
    """Base class for every expected, client-facing error"""

    status_code: int = 500
    error_name = "app_error"
    message: str = "An unexpected error occured."

    def __init__(self) -> None:
        super().__init__(self.message)


class MatchNotFoundError(AppError):
    status_code = 404
    error_name = "match_not_found"
    message = "No match exists with the entered ID."


class MatchFullError(AppError):
    status_code = 409
    error_name = "match_full"
    message = "This match is full."


class MatchAlreadyStartedError(AppError):
    status_code = 409
    error_name = "match_already_started"
    message = "This match has already started."


class MatchFinishedError(AppError):
    status_code = 409
    error_name = "match_finished"
    message = "This match has been finished."
    