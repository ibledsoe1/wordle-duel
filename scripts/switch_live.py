import sys
from pathlib import Path

DEPLOY_DIR = Path(__file__).parent.parent / "deploy"
COLORS = ("blue", "green")


# This runs with the command 'uv run python scripts/switch_live.py (color_arg)'
def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in COLORS:
        sys.exit("Usage: switch_live.py blue|green")
    color = sys.argv[1]
    (DEPLOY_DIR / "live_version.txt").write_text(color + "\n")
    print(f"Live is now: {color}")


if __name__ == "__main__":
    main()
