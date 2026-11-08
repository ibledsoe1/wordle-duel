"""PyGame entry point."""
import pygame

def main() -> None:
    pygame.init()

    screen = pygame.display.set_mode((600, 600))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()