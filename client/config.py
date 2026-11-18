"""Client settings and feature flags."""
import os
from pathlib import Path

WINDOW_TITLE = "Wordle Duel"
# Window size is this fraction of the user's screen
WINDOW_SCALE = 0.8
BACKGROUND_COLOR = (30, 30, 30)
TEXT_COLOR = (240, 240, 240)
# HOVER_COLOR = (180, 180, 180)
HOVER_COLOR = (108, 169, 101)
ERROR_COLOR = (220, 80, 80)

HEADER_FONT_PATH = Path(__file__).parent / "assets" / "fonts" / "ZillaSlab-Medium.ttf"
BODY_FONT_PATH = Path(__file__).parent / "assets" / "fonts" / "LibreFranklin-VariableFont_wght.ttf"

# For testing
SERVER_URL = "http://127.0.0.1:8000"
REQUEST_TIMEOUT = 3

DEFAULT_DURATION = 180
DURATION_CHOICES = (60, 120, 180, 240, 300)
NAME_MAX_LENGTH = 20
CODE_MAX_LENGTH = 6

# == "0" -> currently enabled
def home_ui_enabled() -> bool:
    return os.getenv("home_ui", "0") == "0"

def create_match_ui_enabled() -> bool:
    return os.getenv("create_match_ui", "0") == "1"

def join_match_ui_enabled() -> bool:
    return os.getenv("join_match_ui", "0") == "1"