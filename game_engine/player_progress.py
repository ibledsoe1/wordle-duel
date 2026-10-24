# Cycle 1:
from dataclasses import dataclass
from game_engine.scoring import LetterStatus, score_guess, is_solved
from game_engine.models import PlayerState, MatchConfig

@dataclass
class GuessResult:
    colors: list[LetterStatus]
    puzzle_ended: bool
    solved: bool


def update_player_progress(player: PlayerState, guess: str, config: MatchConfig) -> GuessResult:
    answer = config.word_sequence[player.puzzle_number]

    colors = score_guess(guess, answer)
    solved = is_solved(colors)
    puzzle_ended = solved

    return GuessResult(colors=colors, puzzle_ended=puzzle_ended, solved=solved)