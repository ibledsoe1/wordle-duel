from game_engine.models import (
    FinishedPuzzleResult,
    Match,
    MatchConfig,
    MatchStatus,
    PlayerState,
)
from game_engine.scoring import LetterStatus

C, P, I = LetterStatus.CORRECT, LetterStatus.PRESENT, LetterStatus.INCORRECT


def make_player() -> PlayerState:
    return PlayerState(player_id="p1", name="Ada")


def test_match_config_defaults():
    config = MatchConfig(match_id="m1", word_sequence=["crane", "slate"])
    assert config.guess_limit == 6
    assert config.duration_seconds == 180


def test_match_config_keeps_word_sequence_in_order():
    words = ["crane", "slate", "pious"]
    config = MatchConfig(match_id="m1", word_sequence=words)
    assert config.word_sequence == ["crane", "slate", "pious"]


def test_finished_puzzle_result_stores_its_fields():
    result = FinishedPuzzleResult(solved=True, guesses_used=3)
    assert result.solved is True
    assert result.guesses_used == 3


def test_new_player_has_no_guesses_and_no_finished_puzzles():
    player = make_player()
    assert player.current_word_guesses == []
    assert player.finished_puzzles == []


def test_two_players_do_not_share_lists():
    # Guards against the mutable-default-argument bug: every instance
    # must get its own lists.
    a = make_player()
    b = make_player()
    a.current_word_guesses.append([C, C, C, C, C])
    a.finished_puzzles.append(FinishedPuzzleResult(solved=True, guesses_used=1))
    assert b.current_word_guesses == []
    assert b.finished_puzzles == []


def test_solved_count_is_zero_with_no_finished_puzzles():
    assert make_player().solved_count == 0


def test_solved_count_counts_only_solved_puzzles():
    player = make_player()
    player.finished_puzzles = [
        FinishedPuzzleResult(solved=True, guesses_used=3),
        FinishedPuzzleResult(solved=False, guesses_used=6),
        FinishedPuzzleResult(solved=True, guesses_used=5),
    ]
    assert player.solved_count == 2


def test_solved_count_ignores_failed_puzzles():
    player = make_player()
    player.finished_puzzles = [
        FinishedPuzzleResult(solved=False, guesses_used=6),
        FinishedPuzzleResult(solved=False, guesses_used=6),
    ]
    assert player.solved_count == 0


def test_puzzle_number_is_zero_for_a_new_player():
    assert make_player().puzzle_number == 0


def test_puzzle_number_counts_finished_puzzles():
    player = make_player()
    player.finished_puzzles = [
        FinishedPuzzleResult(solved=True, guesses_used=3),
        FinishedPuzzleResult(solved=True, guesses_used=4),
    ]
    assert player.puzzle_number == 2


def test_puzzle_number_advances_for_failed_puzzles_too():
    player = make_player()
    player.finished_puzzles = [FinishedPuzzleResult(solved=False, guesses_used=6)]
    assert player.puzzle_number == 1


def test_latest_guess_statuses_is_none_before_any_guess():
    assert make_player().latest_guess_statuses is None


def test_latest_guess_statuses_returns_the_most_recent_guess():
    player = make_player()
    player.current_word_guesses = [
        [I, I, I, I, I],
        [C, P, I, I, I],
    ]
    assert player.latest_guess_statuses == [C, P, I, I, I]


def test_match_status_values():
    assert MatchStatus.WAITING == "waiting"
    assert MatchStatus.COUNTDOWN == "countdown"
    assert MatchStatus.ACTIVE == "active"
    assert MatchStatus.FINISHED == "finished"


def test_new_match_defaults():
    config = MatchConfig(match_id="m1", word_sequence=["crane"])
    match = Match(config=config)
    assert match.config is config
    assert match.players == {}
    assert match.status == MatchStatus.WAITING
    assert match.start_time is None


def test_two_matches_do_not_share_players_dict():
    config = MatchConfig(match_id="m1", word_sequence=["crane"])
    a = Match(config=config)
    b = Match(config=config)
    a.players["p1"] = make_player()
    assert b.players == {}