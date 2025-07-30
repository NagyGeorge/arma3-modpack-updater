"""Simple JSON configuration handling."""

import json
import os

CONFIG_PATH = "config.json"


def load_config() -> dict:
    """Load configuration from ``CONFIG_PATH`` if it exists."""
    if not os.path.exists(CONFIG_PATH):
        return {}
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def save_config(data: dict) -> None:
    """Persist ``data`` to ``CONFIG_PATH``."""
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
