ERROR_TEXT = {
    "not_in_word_list": "Not in word list",
    "server_unreachable": "Can't reach the server",
    "match_not_found": "Match not found",
    "match_full": "Match is full",
    "match_already_started": "Match already started",
}


DEFAULT_ERROR_TEXT = "Something went wrong."


def error_text(error_name: str | None) -> str:
    return ERROR_TEXT.get(error_name, DEFAULT_ERROR_TEXT)