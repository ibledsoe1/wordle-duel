import os

def lobby_ui_enabled() -> bool:
    return os.getenv("lobby_ui", "0") == "1"