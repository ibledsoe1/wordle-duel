import pygame
from client.config import (
    TEXT_COLOR, 
    HOVER_COLOR,
    DEFAULT_DURATION,
    DURATION_CHOICES,
    NAME_MAX_LENGTH
)
from client.player import Player
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


    def handle_input(self, event) -> None:
        self.name_input.handle_text_input(event)
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.submit()
            elif event.key == pygame.K_ESCAPE:
                self.back()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for seconds, button in self.duration_buttons:
                if button.check_for_input(event.pos):
                    self.duration = seconds
            if self.create_button.check_for_input(event.pos):
                self.submit()
            elif self.back_button.check_for_input(event.pos):
                self.back()


    def back(self) -> None:
        from client.screens.home import HomeScreen  # local import avoids a cycle
        self.app.switch_screen(HomeScreen)


    def submit(self) -> None:
        name = self.name_input.text.strip()
        if not name:
            self.error = "Enter a name"
            return 
        # TODO: server will try to create match
        # self.app.player = Player()
        # TODO: switch to waiting room screen
    

    def draw(self) -> None:
        heading = self.fonts.heading.render("Create Match", True, TEXT_COLOR)
        self.screen.blit(heading, heading.get_rect(center=(self.center_x, int(self.screen.get_height() * 0.15))))
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