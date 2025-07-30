"""Utility helpers for the Arma 3 Modpack Updater."""

from typing import Callable, Optional


def log(message: str, logger: Optional[Callable[[str], None]] = None) -> None:
    """Log a message using the provided logger and stdout."""
    if logger:
        logger(message)
    print(message)
