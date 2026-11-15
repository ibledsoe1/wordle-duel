"""PyGame entry point."""
import pygame

from client.app import App
from client.config import *
from client.fonts import load_fonts
from client.screens.home import HomeScreen

# NOTE: created separate app file,
# Main shouldn't be doing much besides starting things
# App class owns game loop, current screen, and maybe shared session data
# Screens will never touch the loop, they'll ask the app to switch
def main() -> None:
    if not home_ui_enabled():
        return
    
    pygame.init()

    desktop_w, desktop_h = pygame.display.get_desktop_sizes()[0]
    width, height = int(desktop_w * WINDOW_SCALE), int(desktop_h * WINDOW_SCALE)
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(WINDOW_TITLE)

    # NOTE: add another flag for other screens if needed for next assignment?

    app = App(screen, load_fonts(height))
    app.switch_screen(HomeScreen)
    app.run()

    pygame.quit()

if __name__ == "__main__":
    main()