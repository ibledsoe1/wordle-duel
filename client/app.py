import pygame
from client.config import BACKGROUND_COLOR

class App:
    def __init__(self, screen, fonts):
        self.screen = screen # PyGame window surface
        self.fonts = fonts
        self.running = True
        self.current_screen = None # The screen that gets drawn on the window surface

    def switch_screen(self, target_screen):
        self.current_screen = target_screen(self)

    def quit(self):
        self.running = False

    def run(self):
        # NOTE: what is the clock for? to cap the loop at 60fps
        # this is not for the timer in game
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                else:
                    self.current_screen.handle_input(event)
            self.current_screen.update()
            self.screen.fill(BACKGROUND_COLOR)
            self.current_screen.draw()
            pygame.display.flip()
            clock.tick(60)
                    
