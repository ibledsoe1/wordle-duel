"""PyGame entry point."""
import pygame

from client.config import lobby_ui_enabled

def main() -> None:
    pygame.init()

    screen = pygame.display.set_mode((600, 600))

    if lobby_ui_enabled():
        from client.screens.lobby import draw_lobby
        draw_screen = draw_lobby

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