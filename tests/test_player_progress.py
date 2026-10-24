from game_engine.models import PlayerState, MatchConfig, FinishedPuzzleResult
from game_engine.player_progress import GuessResult, update_player_progress
from game_engine.scoring import LetterStatus
 
C, P, I = LetterStatus.CORRECT, LetterStatus.PRESENT, LetterStatus.INCORRECT

# Helpers

def make_player() -> PlayerState:
    return PlayerState(player_id="p1", name="Izzy")
 
 
def make_config(words=("crane", "slate"), guess_limit=6) -> MatchConfig:
    return MatchConfig(match_id="m1", word_sequence=list(words), guess_limit=guess_limit)

def fail_puzzle(player, config, tries):
    result = None
    for _ in range(tries):
        result = update_player_progress(player, "wrong", config)
    return result


# HW5 Cycle 1:
def test_correct_guess_updates_correctly():
    result = update_player_progress(make_player(), guess="crane", config=make_config())
    assert result == GuessResult(colors=[C, C, C, C, C], puzzle_ended=True, solved=True)

# Cycle 2:
def test_incorrect_guess_updates_correctly():
    result = update_player_progress(make_player(), guess="wrong", config=make_config())
    assert result == GuessResult(colors=[I, C, I, C, I], puzzle_ended=False, solved=False)

# Cycle 3:
def test_incorrect_final_guess_updates_correctly():
    player = make_player()
    result = fail_puzzle(player, make_config, 6)
    assert result.puzzle_ended is True
    assert result.solved is False
    assert result.colors == [I, C, I, C, I]