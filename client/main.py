"""PyGame entry point."""
import pygame
from client.widgets.button import Button

from client.config import *

def main() -> None:
    pygame.init()

    desktop_w, desktop_h = pygame.display.get_desktop_sizes()[0]
    width, height = int(desktop_w * WINDOW_SCALE), int(desktop_h * WINDOW_SCALE)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(WINDOW_TITLE)
    screen.fill(BACKGROUND_COLOR)
    # TODO: add a different font w/ larger size for the header, find official wordle fonts
    font = pygame.font.Font(None, height // 15)

    if home_ui_enabled():
        from client.screens.home import HomeScreen
        current_screen = HomeScreen(screen, font)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if current_screen is not None:
            current_screen.draw()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()