import pygame
from client.config import TEXT_COLOR, HOVER_COLOR
from client.screens.base import Screen
from client.widgets.button import Button

class WaitingRoomScreen(Screen):
    def __init__(self, app):
        super().__init__(app)
        width, height = self.screen.get_size()
        self.center_x = width // 2
        padding = (height // 30, height //60)

        self.phase = "waiting"  # In waiting room can be waiting or countdown
        self.seconds_left = 0

        self.leave_button = Button(
            (int(width * 0.1), int(height * 0.9)),
            "Leave",
            self.fonts.body, 
            TEXT_COLOR, 
            HOVER_COLOR, 
            padding, 
            3
        )

    # TODO: handle websocket messages 


    def handle_input(self, event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            # NOTE: maybe add a 'are you sure' double check if there's time
            self.leave()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.leave_button.check_for_input(event.pos):
                self.leave()


    def leave(self) -> None:
        from client.screens.home import HomeScreen  # local import avoids a cycle
        # TODO: close websocket here
        self.app.switch_screen(HomeScreen)


    def draw(self) -> None:
        height = self.screen.get_height()

        heading = self.fonts.heading.render("Waiting Room", True, TEXT_COLOR)
        self.screen.blit(heading, heading.get_rect(center=(self.center_x, int(height * 0.15))))

        code = self.fonts.body.render(f"Match code: {self.app.player.match_code}", True, TEXT_COLOR)
        self.screen.blit(code, code.get_rect(center=(self.center_x, int(height * 0.4))))

        if self.phase == "waiting":
            status = "Waiting for opponent..."
        else:
            status = f"Starting in {self.seconds_left}"
        text = self.fonts.body.render(status, True, TEXT_COLOR)
        self.screen.blit(text, text.get_rect(center=(self.center_x, int(height * 0.55))))

        self.leave_button.change_color(pygame.mouse.get_pos())
        self.leave_button.draw(self.screen)