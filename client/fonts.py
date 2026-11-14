"""Fonts for the game.

NOTE: Idk if I like this placement very much? I'm not sure why but it seems off but maybe I'm wrong.
But fonts can't be built at import time in config.py which would crash the game.
I could change this later if something better comes to mind.

"""

from dataclasses import dataclass
import pygame
from client.config import HEADER_FONT_PATH, BODY_FONT_PATH

@dataclass(frozen=True)
class Fonts:
    heading: pygame.font.Font
    body: pygame.font.Font

def load_fonts(height: int) -> Fonts:
    """Call after pygame.init()"""
    return Fonts(
        heading=pygame.font.Font(HEADER_FONT_PATH, height // 12),
        body=pygame.font.Font(BODY_FONT_PATH, height // 15)
    )