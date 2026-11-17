"""Chords — triads and sevenths built from a root MIDI note."""

from __future__ import annotations

__all__ = ["chord", "CHORDS"]

CHORDS: dict[str, list[int]] = {
    "major": [0, 4, 7],
    "minor": [0, 3, 7],
    "major7": [0, 4, 7, 11],
    "minor7": [0, 3, 7, 10],
    "dom7": [0, 4, 7, 10],
    "sus4": [0, 5, 7],
    "dim": [0, 3, 6],
}


def chord(root_midi: int, kind: str = "major") -> list[int]:
    """MIDI notes of a chord, e.g. ``chord(60, 'minor7')``."""
    return [root_midi + step for step in CHORDS[kind]]
