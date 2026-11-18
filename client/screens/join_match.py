import pygame
from client.config import (
    TEXT_COLOR, 
    HOVER_COLOR,
    DEFAULT_DURATION,
    NAME_MAX_LENGTH,
    CODE_MAX_LENGTH,
    ERROR_COLOR,
)
from client import network
from client.network import NetworkError
from client.error_messages import error_text
from client.player import Player
from client.screens.base import Screen
from client.widgets.button import Button
from client.widgets.text_input import TextInput

class JoinMatchScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        width, height = self.screen.get_size()
        font = self.fonts.body
        padding = (height // 30, height // 60)
        self.center_x = width // 2
        self.duration = DEFAULT_DURATION
        self.name_input = TextInput((self.center_x, int(height * 0.3)), int(width * 0.4), font, "Your name", NAME_MAX_LENGTH)
        self.code_input = TextInput((self.center_x, int(height * 0.45)), int(width * 0.4), font, "Match Code", CODE_MAX_LENGTH)
        self.inputs = [self.name_input, self.code_input]
        self.name_input.active = True
        
        self.join_button = Button(
            (self.center_x, int(height * 0.65)), 
            "Join", 
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
        self.error = ""


    def focus(self, target) -> None:
        for text_input in self.inputs:
            text_input.active = text_input is target


    def handle_input(self, event) -> None:
        for text_input in self.inputs:
            if text_input.active:
                text_input.handle_text_input(event)
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.submit()
            elif event.key == pygame.K_ESCAPE:
                self.back()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for text_input in self.inputs:
                if text_input.rect.collidepoint(event.pos):
                    self.focus(text_input)
            if self.join_button.check_for_input(event.pos):
                self.submit()
            elif self.back_button.check_for_input(event.pos):
                self.back()



    def back(self) -> None:
        from client.screens.home import HomeScreen  # local import avoids a cycle
        self.app.switch_screen(HomeScreen)


    def submit(self) -> None:
        name = self.name_input.text.strip()
        code = self.code_input.text.strip()
        if not name:
            self.error = "Enter a name"
            return 
        if not code:
            self.error = "Enter a code"
            return
        try:
            # NOTE: should I change code to match id maybe so it matches?
            data = network.join_match(code, name)
        except NetworkError as e:
            self.error = error_text(e.error_name)
            return
        self.error = ""
        self.app.player = Player(name, data["player_id"], data["match_id"])
        # self.app.switch_screen(WaitingRoomScreen)        
    

    def draw(self) -> None:
        heading = self.fonts.heading.render("Join Match", True, TEXT_COLOR)
        self.screen.blit(heading, heading.get_rect(center=(self.center_x, int(self.screen.get_height() * 0.15))))
        self.name_input.draw(self.screen)

        mouse = pygame.mouse.get_pos()

        for button in (self.join_button, self.back_button):
            button.change_color(mouse)
            button.draw(self.screen)

        for text_input in (self.name_input, self.code_input):
            text_input.draw(self.screen)

        if self.error:
            text = self.fonts.body.render(self.error, True, ERROR_COLOR)
            self.screen.blit(text, text.get_rect(center=(self.center_x, int(self.screen.get_height() * 0.75))))