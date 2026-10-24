from dataclasses import dataclass
from game_engine.scoring import LetterStatus, score_guess, is_solved
from game_engine.models import PlayerState, MatchConfig, FinishedPuzzleResult

@dataclass
class GuessResult:
    colors: list[LetterStatus]
    puzzle_ended: bool
    solved: bool


def update_player_progress(player: PlayerState, guess: str, config: MatchConfig) -> GuessResult:
    answer = config.word_sequence[player.puzzle_number]
    colors = score_guess(guess, answer)
    player.current_word_guesses.append(colors)

    solved = is_solved(colors)
    guesses_used = len(player.current_word_guesses)
    puzzle_ended = solved or guesses_used >= config.guess_limit

    if puzzle_ended:
        player.finished_puzzles.append(FinishedPuzzleResult(solved=solved, guesses_used=guesses_used))
        player.current_word_guesses.clear()

    return GuessResult(colors=colors, puzzle_ended=puzzle_ended, solved=solved)