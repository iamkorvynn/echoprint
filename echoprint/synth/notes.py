"""Note helpers for the synthesizer: MIDI, frequencies, names."""

from __future__ import annotations

from ..audio import midi_to_freq, note_name

__all__ = ["midi_to_freq", "note_name", "N", "freq"]


def N(name: str) -> int:
    """Note name -> MIDI number, e.g. ``N('A4')`` -> 69, ``N('C#3')`` -> 49."""
    names = {"C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3, "E": 4,
             "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8, "Ab": 8, "A": 9,
             "A#": 10, "Bb": 10, "B": 11}
    # Split letters+accidental from octave digit(s).
    i = 0
    while i < len(name) and not (name[i].isdigit() or name[i] == "-"):
        i += 1
    pitch, octave = name[:i], int(name[i:])
    return names[pitch] + (octave + 1) * 12


def freq(name_or_midi) -> float:
    """Note name ('A4') or MIDI number -> frequency in Hz."""
    if isinstance(name_or_midi, str):
        return midi_to_freq(N(name_or_midi))
    return midi_to_freq(name_or_midi)
