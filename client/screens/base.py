from abc import ABC, abstractmethod

import pygame

class Screen(ABC):
    """Screen base, subclasses must implement draw"""
    def __init__(self, app):
        self.app = app
        self.screen = app.screen
        self.font = app.fonts


    @abstractmethod
    def draw(self) -> None:
        """Draw this screen onto self.screen."""


    def update(self) -> None:
        """Changes state w/o user action, for example the timer counting down."""


    def handle_input(self, event: pygame.event.Event) -> None:
        """ Changes state w/ user action, a reaction to a pygame input event."""