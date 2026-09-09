"""Refresh only installer-owned hooks, without initializing project state."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import goal_compass


def main() -> None:
    path = Path('.codex/hooks.json')
    current = goal_compass.load_json(path, {})
    updated = goal_compass.merge_hooks_json(current, goal_compass.hooks_json())
    if updated != current:
        goal_compass.write_json(path, updated)


if __name__ == '__main__':
    main()
