"""Track 10 — "Crown of Strings": orchestral-ish, many voices.

110 BPM, E harmonic minor. Layered strings playing chords plus a
soaring string melody plus a low bass line — the most voices at
once in the library, so its constellation is the densest.
"""

from __future__ import annotations

import numpy as np

from .engine import TrackBuilder
from .chords import chord
from .instruments import bass_note, string_note

TITLE = "Crown of Strings"
GENRE = "orchestral"
BPM = 110
DESCRIPTION = "Orchestral-ish: many string voices in E harmonic minor."


def build_track(duration_s: float = 12.0) -> np.ndarray:
    b = TrackBuilder(duration_s=duration_s, bpm=BPM)
    # String chords: Em - C - Am - B, one per bar.
    roots = [(52, "minor"), (48, "major"), (45, "minor"), (47, "major")]
    for bar, (root, kind) in enumerate(roots * 3):
        t = bar * b.bar_s
        if t < duration_s - b.bar_s:
            b.chord_notes(string_note, [m + 12 for m in chord(root, kind)],
                          t, b.bar_s, amp=0.26)
            b.note(bass_note, root - 12, t, b.bar_s, amp=0.5)
    melody = [76, 79, 83, 84, 83, 79, 76, 79, 83, 86, 84, 83, 79, 76, 74, 76]
    t = 0.0
    for midi in melody:
        if t >= duration_s - b.beat_s:
            break
        b.note(string_note, midi, t, b.beat_s * 0.95, amp=0.34)
        b.note(string_note, midi + 12, t, b.beat_s * 0.95, amp=0.18)
        t += b.beat_s * 0.75
    return b.render()
