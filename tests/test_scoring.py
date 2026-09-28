"""Week 5 activity: unit tests for game_engine.scoring.score_guess."""
import pytest
from game_engine.scoring import LetterStatus, score_guess

C, P, A = LetterStatus.CORRECT, LetterStatus.PRESENT, LetterStatus.ABSENT


# EP: valid class "exact match"
def test_exact_match_all_correct():
    assert score_guess("crane", "crane") == [C, C, C, C, C]


# EP: valid class "no shared letters"
def test_no_shared_letters_all_absent():
    assert score_guess("sulky", "crane") == [A, A, A, A, A]


# EP: valid class "duplicate letters" (guess has more copies than answer)
def test_duplicate_letter_only_one_marked_present():
    assert score_guess("speed", "abide") == [A, A, P, A, P]


# BVA: length just below the boundary (4) is invalid
def test_boundary_length_four_raises():
    with pytest.raises(ValueError):
        score_guess("cran", "crane")


# BVA: length just above the boundary (6) is invalid
def test_boundary_length_six_raises():
    with pytest.raises(ValueError):
        score_guess("cranes", "crane")