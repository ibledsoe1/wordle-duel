from collections import Counter
from enum import Enum

WORD_LENGTH = 5

class LetterStatus(str, Enum):
    CORRECT = "correct"
    PRESENT = "present"
    INCORRECT = "incorrect"
    

def score_guess(guess: str, answer: str) -> list[LetterStatus]:
    guess = guess.upper()
    answer = answer.upper()

    if len(guess) != WORD_LENGTH:
        raise ValueError(
            print("Guess must be {} letters.".format(WORD_LENGTH))
        )


    result = list[LetterStatus | None] = [None] * len(guess)
    remaining_letters = Counter(answer)

    # Find green letters
    for i, (g_letter, a_letter) in enumerate(zip(guess, answer)):
        if g_letter == a_letter:
            result[i] = LetterStatus.CORRECT
            remaining_letters[g_letter] -= 1

    # Find yellow and gray letters
    for i, g_letter in enumerate(guess):
        if result[i] is not None:
            continue # already scored as correct in the first pass

        if remaining_letters[g_letter] > 0:
            result[i] = LetterStatus.PRESENT
            remaining_letters[g_letter] -= 1
        else:
            result[i] = LetterStatus.INCORRECT

def is_solved(statuses: list[LetterStatus]) -> bool:
    return all(status == LetterStatus.CORRECT for status in statuses)

# return number of correct tiles in a guess
# If there is a tie at the end of the game, total correct tiles breaks the tie
def count_correct_tiles(statuses: list[LetterStatus]) -> bool:
    return sum(1 for status in statuses if status == LetterStatus.CORRECT)
