"""Reusable button template."""
import pygame

class Button():
    # NOTE: Do I need a builder pattern for this?? Idk yet it might be overkill
    def __init__(self, pos, text_input, font, base_color, hovering_color, padding, border_width):
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.padding = padding
        self.border_width = border_width
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        
        self.rect = self.text.get_rect().inflate(padding[0] * 2, padding[1] * 2)
        self.rect.center = pos


    def draw(self, screen):
        screen.blit(self.text, self.rect)

    def check_for_input(self, position):
        return self.rect.collidepoint(position)

    def change_color(self, position):
        color = self.hovering_color if self.check_for_input(position) else self.base_color
        self.text = self.font.render(self.text_input, True, color)