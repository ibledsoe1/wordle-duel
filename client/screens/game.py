import pygame

from client.config import TEXT_COLOR, ERROR_COLOR, BODY_FONT_PATH
from client.player_view_state import PlayerViewState, MAX_GUESSES, WORD_LENGTH
from client.screens.base import Screen

TILE_COLORS = {
    "correct": (108, 169, 101),
    "present": (200, 182, 83),
    "incorrect": (120, 124, 127),
}
BASE_KEY_COLOR = (129, 131, 132)
EMPTY_OUTLINE = (55, 55, 55)
TYPED_OUTLINE = (90, 90, 90)

KEY_ROWS = ("QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM")
ENTER, DELETE = "ENTER", "DEL"

POPUP_MS = 1500 # how long the popup stays up
PAUSE_MS = 1000 # how long a finished puzzle stays visible


class GameScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        width, height = self.screen.get_size()
        self.width = width
        self.height = height
        self.center_x = width // 2

        self.state = PlayerViewState()
        self.popup = ""
        self.popup_until = 0
        self.clear_at: int | None = None
        self.seconds_left: int | None = None # placeholder until ticks arrive

        self.tile = int(height * 0.078)
        self.gap = self.tile // 10
        board_width = WORD_LENGTH * self.tile + (WORD_LENGTH - 1) * self.gap
        self.board_left = self.center_x - board_width // 2
        self.board_top = int(height * 0.15)

        self.keys: list[tuple[str, pygame.Rect]] = []
        self._build_keys()


    def _build_keys(self) -> None:
        key_h = int(self.height * 0.08)
        key_w = int(key_h * 0.75)
        gap = max(2, key_w // 8)
        wide_key = int(key_w * 1.5) # for enter and delete buttons
        top = int(self.height * 0.70)
        for row, letters in enumerate(KEY_ROWS):
            labels = list(letters)
            if row == 2:
                labels = [ENTER, *labels, DELETE]
            widths = [wide_key if label in (ENTER, DELETE) else key_w for label in labels]
            x = self.center_x - (sum(widths) + gap * (len(labels) - 1)) // 2 # maybe ask about this i only half understand, also ask maybe why its needed, is it just for rect clickability?
            y = top + row * (key_h + gap)
            for label, w in zip(labels, widths):
                self.keys.append((label, pygame.Rect(x, y, w, key_h))) # why do we need y if we already had top earlier? Rect(left, top, width, height) -> Rect
                x += w + gap


    def handle_input(self, event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.submit()
            elif event.key == pygame.K_BACKSPACE:
                self.state.backspace()
            elif event.unicode:
                self.state.type_letter(event.unicode)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for label, rect in self.keys:
                if rect.collidepoint(event.pos):
                    self.press(label)
                    break


    def press(self, label: str) -> None:
        if label == ENTER:
            self.submit()
        elif label == DELETE:
            self.state.backspace()
        else:
            self.state.type_letter(label)


    # TODO: add submit functionality

    # TODO: add ws message handling

    # TODO: add error popups
        

    
    def draw(self) -> None:
        self._draw_top_bar()
        self._draw_board()
        self._draw_keyboard()


    def _draw_top_bar(self) -> None:
        font = self.fonts.body
        y = int(self.height * 0.06)

        if self.seconds_left is None:
            clock = "--:--"
        else:
            clock = f"{self.seconds_left // 60}:{self.seconds_left % 60:02d}"
        text = font.render(clock, True, TEXT_COLOR)
        self.screen.blit(text, text.get_rect(center=(self.center_x, y)))

        solved = font.render(f"Solved: {self.state.solved_count}", True, TEXT_COLOR)
        self.screen.blit(solved, solved.get_rect(midright=(self.width - int(self.width * 0.03), y)))

    def _draw_board(self) -> None:
        rows = self.state.rows
        for row in range(MAX_GUESSES):
            for col in range(WORD_LENGTH):
                rect = pygame.Rect(
                    self.board_left + col * (self.tile + self.gap),
                    self.board_top + row * (self.tile + self.gap),
                    self.tile,
                    self.tile,
                )
                letter, color = "", None
                if row < len(rows):
                    word, colors = rows[row]
                    letter, color = word[col], TILE_COLORS[colors[col]]
                elif row == len(rows) and not self.state.finished and col < len(self.state.current):
                    letter = self.state.current[col]

                if color:
                    pygame.draw.rect(self.screen, color, rect, border_radius=4)
                else:
                    outline = TYPED_OUTLINE if letter else EMPTY_OUTLINE
                    pygame.draw.rect(self.screen, outline, rect, width=2, border_radius=4)
                if letter:
                    char = self.fonts.guess_tiles.render(letter, True, TEXT_COLOR)
                    self.screen.blit(char, char.get_rect(center=rect.center))

    def _draw_keyboard(self) -> None:
        for label, rect in self.keys:
            status = self.state.key_colors.get(label)
            color = TILE_COLORS[status] if status else BASE_KEY_COLOR
            pygame.draw.rect(self.screen, color, rect, border_radius=2)
            font = self.fonts.keyboard_others if label in (ENTER, DELETE) else self.fonts.keyboard_letters
            char = font.render(label, True, TEXT_COLOR)
            self.screen.blit(char, char.get_rect(center=rect.center))