import pygame
from client.config import TEXT_COLOR, HOVER_COLOR

class TextInput:
    def __init__(self, pos, width, font, placeholder, max_length):
        self.font = font
        self.placeholder = placeholder
        self.max_length = max_length
        self.text = ""
        self.active = False
        height = font.get_height() + font.get_height() // 2
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = pos

    def draw(self, screen) -> None:
        color = TEXT_COLOR if self.active else HOVER_COLOR
        pygame.draw.rect(screen, color, self.rect, width=3, border_radius=8)
        shown = self.text or self.placeholder
        label = self.font.render(shown, True, color if self.text else HOVER_COLOR)
        screen.blit(label, label.get_rect(midleft=(self.rect.left + 12, self.rect.centery)))


    def check_for_input(self, position):
        return self.rect.collidepoint(position)


    def handle_text_input(self, event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isprintable() and event.unicode and len(self.text) < self.max_length:
                self.text += event.unicode