import pygame

from client.screens.base import Screen
from client.widgets.button import Button

TEXT_COLOR = (240, 240, 240)
HOVER_COLOR = (200, 200, 200)

class HomeScreen(Screen):
    def __init__(self, screen: pygame.Surface, font: pygame.font.Font):
        super().__init__(screen, font)
        width, height = screen.get_size()
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
        # TODO: add actions on create and join
        
    def draw(self) -> None:
        heading = self.font.render("Wordle Duel", True, TEXT_COLOR)
        self.screen.blit(heading, heading.get_rect(center=(self.center_x, self.heading_y)))

        mouse_pos = pygame.mouse.get_pos()
        for button in (self.create_button, self.join_button):
            button.change_color(mouse_pos)
            button.draw(self.screen)