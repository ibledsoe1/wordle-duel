"""Client settings and feature flags."""
import json
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

# For HW10 3320:
DEPLOY_DIR = Path(__file__).parent.parent / "deploy"

def live_flags() -> dict:
    live = (DEPLOY_DIR / "live_version.txt").read_text().strip()
    return json.loads((DEPLOY_DIR / live / "config.json").read_text())

def home_ui_enabled() -> bool:
    return live_flags()["home_ui"]

def create_match_ui_enabled() -> bool:
    return live_flags()["create_match_ui"]

def join_match_ui_enabled() -> bool:
    return live_flags()["join_match_ui"]