import pygame
from client.config import (
    TEXT_COLOR, 
    HOVER_COLOR,
    DEFAULT_DURATION,
    DURATION_CHOICES,
    NAME_MAX_LENGTH
)
from client.screens.base import Screen
from client.widgets.button import Button
from client.widgets.text_input import TextInput

class CreateMatchScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        width, height = self.screen.get_size()
        font = self.fonts.body
        padding = (height // 30, height // 60)
        self.center_x = width // 2
        self.duration = DEFAULT_DURATION
        self.name_input = TextInput((self.center_x, int(height * 0.3)), int(width * 0.4), font, "Your name", NAME_MAX_LENGTH)

        last = len(DURATION_CHOICES) - 1
        self.duration_buttons = [
            (
                seconds, 
                Button((int(width * (0.2 + 0.6 * i / last)), int(height * 0.5)), f"{seconds // 60} min", font, TEXT_COLOR, HOVER_COLOR, padding, 3)
            )
            for i, seconds in enumerate(DURATION_CHOICES)
        ]
        self.create_button = Button(
            (self.center_x, int(height * 0.7)),
            "Create",
            font,
            TEXT_COLOR,
            HOVER_COLOR,
            padding,
            3
        )
        self.back_button = Button(
            (int(width * 0.1), int(height * 0.9)),
            "Back",
            font,
            TEXT_COLOR,
            HOVER_COLOR,
            padding,
            3
        )

        # NOTE: add handle_input

    def draw(self) -> None:
        heading = self.fonts.heading.render("Create Match", True, TEXT_COLOR)
        self.screen.blit(heading, heading.get_rect(
        center=(self.center_x, int(self.screen.get_height() * 0.15))))
        self.name_input.draw(self.screen)

        mouse = pygame.mouse.get_pos()
        for seconds, button in self.duration_buttons:
            button.change_color(mouse)
            button.draw(self.screen)
            if seconds == self.duration:
                pygame.draw.rect(self.screen, TEXT_COLOR, button.rect.inflate(10, 10), width=2, border_radius=12)

        for button in (self.create_button, self.back_button):
            button.change_color(mouse)
            button.draw(self.screen)