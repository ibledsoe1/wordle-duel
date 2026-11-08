"""PyGame entry point."""
import pygame

from client.config import home_ui_enabled

def main() -> None:
    pygame.init()

    screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

    if home_ui_enabled():
        from client.screens.home import draw_home
        draw_screen = draw_home

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if draw_screen is not None:
            draw_screen(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()