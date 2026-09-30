import pytest

from game_engine.word_list import (
    WORD_LENGTH,
    load_answer_words,
    load_valid_guesses,
    is_valid_guess,
)

# Test against small temp files (for controlled behavior of functions) 
# Then test against real word lists (to catch problems with the lists)

# load_answer_words and load_valid_guesses tests
def write_words(path, lines):
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path
 
 
def test_load_answer_words_uppercases_and_preserves_order(tmp_path):
    f = write_words(tmp_path / "answers.txt", ["crane", "Slate", "ABOUT"])
    assert load_answer_words(f) == ["CRANE", "SLATE", "ABOUT"]
 
 
def test_load_answer_words_skips_malformed_lines(tmp_path):
    f = write_words(
        tmp_path / "answers.txt",
        ["crane", "", "   ", "cat", "toolong", "cr4ne", "sla-e", "slate"],
    )
    assert load_answer_words(f) == ["CRANE", "SLATE"]
 
 
def test_load_answer_words_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_answer_words(tmp_path / "does_not_exist.txt")
 
 
def test_load_valid_guesses_is_union_of_both_files(tmp_path):
    answers = write_words(tmp_path / "answers.txt", ["crane", "slate"])
    extras = write_words(tmp_path / "guesses.txt", ["aahed", "zzzzy"])
    result = load_valid_guesses(answers_path=answers, guesses_path=extras)
    assert result == {"CRANE", "SLATE", "AAHED", "ZZZZY"}
 
 
def test_answers_are_always_guessable(tmp_path):
    answers = write_words(tmp_path / "answers.txt", ["crane"])
    extras = write_words(tmp_path / "guesses.txt", ["aahed"])
    result = load_valid_guesses(answers_path=answers, guesses_path=extras)
    assert "CRANE" in result

# is_valid_guess tests
@pytest.fixture
def guesses():
    return {"CRANE", "SLATE", "ABOUT"}
 
 
def test_accepts_word_in_set(guesses):
    assert is_valid_guess("CRANE", guesses) is True
 
 
def test_is_case_insensitive_and_strips_whitespace(guesses):
    assert is_valid_guess("crane", guesses) is True
    assert is_valid_guess("  Crane \n", guesses) is True
 
 
def test_rejects_word_not_in_set(guesses):
    assert is_valid_guess("zzzzz", guesses) is False
 
 
@pytest.mark.parametrize("bad", ["", "cran", "cranes", "cr4ne", "cra ne", "cran-"])
def test_rejects_wrong_length_or_non_letters(guesses, bad):
    assert is_valid_guess(bad, guesses) is False


@pytest.fixture(scope="module")
def real_answers():
    return load_answer_words()
 
 
@pytest.fixture(scope="module")
def real_guesses():
    return load_valid_guesses()
 
 
def test_real_answer_list_is_well_formed(real_answers):
    assert len(real_answers) > 2000
    assert all(len(w) == WORD_LENGTH and w.isalpha() and w.isupper() for w in real_answers)
 
 
def test_real_answer_list_has_no_duplicates(real_answers):
    assert len(real_answers) == len(set(real_answers))
 
 
def test_every_answer_is_a_valid_guess(real_answers, real_guesses):
    assert set(real_answers) <= real_guesses
 
 
def test_answer_and_guess_only_files_do_not_overlap(real_answers, real_guesses):
    # valid_guesses.txt holds guess-only words; the union is answers + extras.
    from game_engine.word_list import DEFAULT_GUESSES_PATH, read_words
 
    extras = set(read_words(DEFAULT_GUESSES_PATH))
    assert extras.isdisjoint(real_answers)
 
 
def test_common_words_are_valid_guesses(real_guesses):
    for word in ["crane", "slate", "about", "audio"]:
        assert is_valid_guess(word, real_guesses), word
 
 
def test_invalid_guess_with_real_data(real_guesses):
    assert not is_valid_guess("zzzzz", real_guesses)
 