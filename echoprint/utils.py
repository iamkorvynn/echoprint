"""Small shared helpers: file discovery and library scanning."""

from __future__ import annotations

import os

__all__ = ["find_wavs", "track_id_from_path"]


def find_wavs(directory: str) -> list[str]:
    """All ``.wav`` files under ``directory``, sorted by name."""
    found = []
    for root, _dirs, files in os.walk(directory):
        for name in sorted(files):
            if name.lower().endswith(".wav"):
                found.append(os.path.join(root, name))
    return sorted(found)


def track_id_from_path(path: str) -> str:
    """``tracks/03-piano-solo.wav`` -> ``03-piano-solo``."""
    return os.path.splitext(os.path.basename(path))[0]
