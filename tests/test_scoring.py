import pytest
from game_engine.scoring import LetterStatus, score_guess, is_solved, score_guess

C, P, I = LetterStatus.CORRECT, LetterStatus.PRESENT, LetterStatus.INCORRECT


# EP: valid class "exact match"
def test_all_correct_guess():
    assert score_guess("crane", "crane") == [C, C, C, C, C]


# EP: valid class "no shared letters"
def test_all_incorrect_guess():
    assert score_guess("sulky", "crane") == [I, I, I, I, I]

# EP: valid class "some shared letters"
def test_mixed_statuses():
    assert score_guess("crest", "crane") == [C, C, P, I, I]

# EP: valid class "duplicate letters" (guess has more copies than answer)
def test_duplicate_letter_only_one_marked_present():
    assert score_guess("speed", "abide") == [I, I, P, I, P]

# Structural check
def test_result_has_one_status_per_letter():
    result = score_guess("crane", "slate")
    assert len(result) == 5
    assert all(isinstance(status, LetterStatus) for status in result)

# General behavioral property (normalization)
def test_scoring_is_case_insensitive():
    assert score_guess("CRANE", "crane") == score_guess("crane", "CRANE")
    assert score_guess("CrAnE", "cRaNe") == [C, C, C, C, C]

# BVA: length just below the boundary (4) is invalid
def test_boundary_length_too_short():
    with pytest.raises(ValueError):
        score_guess("cran", "crane")


# BVA: length just above the boundary (6) is invalid
def test_boundary_length_too_long():
    with pytest.raises(ValueError):
        score_guess("cranes", "crane")

def test_is_solved_true_when_all_correct():
    assert is_solved([C, C, C, C, C]) is True
    assert is_solved([C, C, C, C, P]) is False
    assert is_solved([I, I, I, I, I,]) is False

def test_count_correct_tiles():
    assert is_solved([C, C, C, C, C]) == 5
    assert is_solved([C, P, I, C, P]) == 2
    assert is_solved([I, I, I, I, I,]) == 0