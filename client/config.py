"""Client settings and feature flags."""
import os
from pathlib import Path

WINDOW_TITLE = "Wordle Duel"
# Window size is this fraction of the user's screen
WINDOW_SCALE = 0.8
BACKGROUND_COLOR = (30, 30, 30)
HEADER_FONT_PATH = Path(__file__).parent / "assets" / "fonts" / "ZillaSlab-Medium.ttf"
BODY_FONT_PATH = Path(__file__).parent / "assets" / "fonts" / "LibreFranklin-VariableFont_wght.ttf"

# == "0" -> currently enabled
def home_ui_enabled() -> bool:
    return os.getenv("home_ui", "0") == "0"