# This is an in-game error, not a server error, that's why I put this here
class PlayerFinishedAllPuzzlesError(Exception):
    """Raised when a guess is applied to a player who
    already finished every puzzle in the matches word sequence"""