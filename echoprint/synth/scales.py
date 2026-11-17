"""Scales — the melodic DNA that makes each track distinguishable.

Each track is built on a different scale (and root), so the
constellations genuinely differ: a major-scale pop chorus and a
minor-scale ballad do not share many peak frequencies, which is
exactly what the matcher relies on.
"""

from __future__ import annotations

__all__ = ["SCALES", "scale_notes"]

# Semitone steps from the root, one octave.
SCALES: dict[str, list[int]] = {
    "major": [0, 2, 4, 5, 7, 9, 11],
    "minor": [0, 2, 3, 5, 7, 8, 10],
    "pentatonic_major": [0, 2, 4, 7, 9],
    "pentatonic_minor": [0, 3, 5, 7, 10],
    "dorian": [0, 2, 3, 5, 7, 9, 10],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
    # Bollywood / Hindustani-flavoured: Bhairavi-ish flat 2nd + flat 6th.
    "bhairavi": [0, 1, 3, 5, 7, 8, 10],
    # Whole-tone-ish dreamy scale for the lo-fi track.
    "lydian": [0, 2, 4, 6, 7, 9, 11],
    # Harmonic minor for the orchestral track's drama.
    "harmonic_minor": [0, 2, 3, 5, 7, 8, 11],
    "blues": [0, 3, 5, 6, 7, 10],
}


def scale_notes(root_midi: int, scale: str, octaves: int = 2) -> list[int]:
    """All MIDI notes of ``scale`` starting at ``root_midi``."""
    steps = SCALES[scale]
    notes = []
    for octave in range(octaves):
        for step in steps:
            notes.append(root_midi + step + 12 * octave)
    return notes
