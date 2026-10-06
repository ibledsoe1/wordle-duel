# models describing what shapes the game logic operates on
# so server and client can agree on what a "match" and a "player's progress"
# look like w/o either one owning each others code

# Not sure if later these will have to be separate files?
# Or maybe this will have to be it's own folder? 
# NOTE: I need to research more about project structure

from dataclasses import dataclass, field
from enum import Enum

from .scoring import LetterStatus

@dataclass
class MatchConfig:
    """The fixed rules for a single match."""
    match_id: str # NOTE: should this be an int?
    word_sequence: list[str]
    guess_limit: int = 6
    duration_seconds: int = 180

@dataclass
class FinishedPuzzleResult:
    """A record of one finished wordle puzzle results,
    (either solved or given up on after using all guesses)."""
    word_index: int
    answer_word: str
    solved: bool
    guesses_used: int
    green_tiles: int

@dataclass
class PlayerState:
    """One player's progress through a match's word sequence."""

    player_id: str
    current_word_index: int = 0
    current_word_guesses: list[list[LetterStatus]] = field(default_factory=list)
    finished_puzzles: list[FinishedPuzzleResult] = field(default_factory=list)

    @property
    def solved_count(self) -> int:
        return sum(1 for puzzle in self.finished_puzzles if puzzle.solved)

    @property
    def total_green_tiles(self) -> int:
        return sum(puzzle.green_tiles for puzzle in self.finished_puzzles)

    @property
    def latest_guess_statuses(self) -> list[LetterStatus] | None:
        """Color feedback for player's most recent guess on their current word, 
        or None if they haven't gussed yet.

        The colors get broadcast to their oppopnent."""

        if not self.current_word_guesses:
            return None
        return self.current_word_guesses[-1]

class MatchStatus(str, Enum):
    WAITING = "waiting" # match created, waiting for another player to join
    COUNTDOWN = "countdown" # both players joined, countdown in progress
    ACTIVE = "active" # game active, timer counting down
    FINISHED = "finished" # timer is done

@dataclass
class Match:
    """Match config, players' live state, current lifecycle status."""
    # Server owns and mutates this, game_engine just defines the shape

    config: MatchConfig
    players: list[str, PlayerState] = field(default_factory=dict)
    status: MatchStatus = MatchStatus.WAITING
    start_time: float | None = None # set when countdown ends