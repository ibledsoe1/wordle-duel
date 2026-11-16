import pygame

from client.screens.base import Screen
from client.widgets.button import Button
from client.config import TEXT_COLOR, HOVER_COLOR, create_match_ui_enabled, join_match_ui_enabled

class HomeScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        width, height = self.screen.get_size()
        font = self.fonts.body
        self.center_x = width // 2
        self.heading_y = int(height * 0.2)
        self.create_button = Button(
            (self.center_x, int(height * 0.4)),
            "Create Match",
            font,
            TEXT_COLOR,
            HOVER_COLOR,
            (height // 30, height // 60),
            3
        )
        self.join_button = Button(
            (self.center_x, int(height * 0.6)),
            "Join Match",
            font,
            TEXT_COLOR,
            HOVER_COLOR,
            (height // 30, height // 60),
            3
        )



    def handle_input(self, event: pygame.event.Event) -> None:
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return
        if self.create_button.check_for_input(event.pos):
            if create_match_ui_enabled():
                from client.screens.create_match import CreateMatchScreen
                self.app.switch_screen(CreateMatchScreen)
        if self.join_button.check_for_input(event.pos):
            if join_match_ui_enabled():
                from client.screens.join_match import JoinMatchScreen
                self.app.switch_screen(JoinMatchScreen)

    def draw(self) -> None:
        heading = self.fonts.heading.render("Wordle Duel", True, TEXT_COLOR)
        self.screen.blit(heading, heading.get_rect(center=(self.center_x, self.heading_y)))

        mouse_pos = pygame.mouse.get_pos()
        for button in (self.create_button, self.join_button):
            button.change_color(mouse_pos)
            button.draw(self.screen)