from abc import ABC, abstractmethod

import pygame

class Screen(ABC):
    """Screen base, subclasses must implement draw"""
    def __init__(self, screen: pygame.Surface, font: pygame.font.Font):
        self.screen = screen
        self.font = font


    @abstractmethod
    def draw(self) -> None:
        """Draw this screen onto self.screen."""


    def handle_input(self, event: pygame.event.Event) -> None:
        """React to a pygame input event."""