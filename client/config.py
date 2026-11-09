"""Client settings and feature flags."""
import os

WINDOW_TITLE = "Wordle Duel"
# Window size is this fraction of the user's screen
WINDOW_SCALE = 0.8
BACKGROUND_COLOR = (30, 30, 30)
# FONT = 

def home_ui_enabled() -> bool:
    return os.getenv("home_ui", "0") == "1"