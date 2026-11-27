# NOTE: idk if I like this here, maybe import from server instead?
# But idk if that would make it too coupled
WORD_LENGTH = 5
MAX_GUESSES = 6

# maybe import this as well?
CORRECT = "correct"
PRESENT = "present"
INCORRECT = "incorrect"

# When a letter has been seen more than once, the highest rank wins
_RANK = {INCORRECT: 0, PRESENT: 1, CORRECT: 2}

class PlayerViewState:
    def __init__(self) -> None:
        self.rows: list[tuple[str, list[str]]] = [] # list of rows on screen, each row contains the guess and the colors of the guess letters
        self.current = "" # letters typed for the next guess
        self.solved_count = 0
        self.key_colors: dict[str, str] = {} # best known color per letter
        self.finished = False

    def type_letter(self, letter: str) -> None:
        if self.finished or len(self.current) >= WORD_LENGTH:
            return
        if len(letter) != 1 or not (letter.isascii() and letter.isalpha()):
            return
        self.current += letter.upper()


    def backspace(self) -> None:
        if not self.finished:
            self.current = self.current[:-1]

    def can_submit(self) -> bool:
        return not self.finished and len(self.current) == WORD_LENGTH

    def apply_result(self, guess: str, colors: list[str], puzzle_ended: bool, solved: bool) -> None:
        guess = guess.upper()
        self.rows.append((guess, list(colors)))

        # this updates the colors on the keyboard UI
        for letter, color in zip(guess, colors):
            old = self.key_colors.get(letter)
            if old is None or _RANK[color] > _RANK[old]:
                self.key_colors[letter] = color

        self.current = ""
        if puzzle_ended:
            self.finished = True
            if solved:
                self.solved_count += 1

    def clear_board(self) -> None:
        self.rows = []
        self.current = ""
        self.key_colors = {}
        self.finished = False