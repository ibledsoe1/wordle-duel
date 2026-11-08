import os

def home_ui_enabled() -> bool:
    return os.getenv("home_ui", "0") == "1"