"""Week 5 activity: unit tests for game_engine.scoring.score_guess."""
import pytest
from game_engine.scoring import LetterStatus, score_guess

C, P, I = LetterStatus.CORRECT, LetterStatus.PRESENT, LetterStatus.INCORRECT


# EP: valid class "exact match"
def test_all_correct_guess():
    assert score_guess("crane", "crane") == [C, C, C, C, C]


# EP: valid class "no shared letters"
def test_all_incorrect_guess():
    assert score_guess("sulky", "crane") == [I, I, I, I, I]


# EP: valid class "duplicate letters" (guess has more copies than answer)
def test_duplicate_letter_only_one_marked_present():
    assert score_guess("speed", "abide") == [I, I, P, I, P]


# BVA: length just below the boundary (4) is invalid
def test_boundary_length_too_short():
    with pytest.raises(ValueError):
        score_guess("cran", "crane")


# BVA: length just above the boundary (6) is invalid
def test_boundary_length_too_long():
    with pytest.raises(ValueError):
        score_guess("cranes", "crane")