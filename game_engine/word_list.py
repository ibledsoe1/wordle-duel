# Word list loading and guess validation

from pathlib import Path

WORD_LENGTH = 5

_DATA_DIR = Path(__file__).parent / "word_lists"
DEFAULT_ANSWERS_PATH = _DATA_DIR / "answer_words.txt"
DEFAULT_GUESSES_PATH = _DATA_DIR / "valid guesses.txt"

def read_words(path: Path) -> list[str]:
    if not path.exists():
        raise FileNotFoundError("Word list file not found.")

    words = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            word = line.strip().upper()
            if not word:
                continue
            if len(word) != WORD_LENGTH or not word.isalpha():
                continue
            words.append(word)

    return words

def load_answer_words(path: Path = DEFAULT_ANSWERS_PATH) -> list[str]:
    return read_words(path)

def load_valid_guesses(answers_path: Path = DEFAULT_ANSWERS_PATH,
                       guesses_path: Path = DEFAULT_GUESSES_PATH) -> set[str]:
    answers = load_answer_words(answers_path)
    valid_guesses = read_words(guesses_path)
    # Set union, combine the two sets since answers should also be valid guesses
    return set(answers) | set(valid_guesses)

def is_valid_guess(guess: str, valid_guesses: set[str]) -> bool:
    guess = guess.strip().upper()

    if len(guess) != WORD_LENGTH or not guess.isalpha():
        return False

    return guess in valid_guesses