"""Track 02 — "Porch Light": acoustic pluck + vocal-ish melody.

96 BPM, C major. Fingerpicked-style pluck arpeggios under a
singing vocal line. Warm, sparse, and slow-moving compared to
track 01 — its peaks are fewer and longer-lived.
"""

from __future__ import annotations

import numpy as np

from .engine import TrackBuilder
from .instruments import pluck, vocal_note

TITLE = "Porch Light"
GENRE = "acoustic"
BPM = 96
DESCRIPTION = "Acoustic-like pluck arpeggios with a vocal-ish melody."


def build_track(duration_s: float = 12.0) -> np.ndarray:
    b = TrackBuilder(duration_s=duration_s, bpm=BPM)
    # Plucked arpeggio: C - Am - F - G, eighth notes.
    chords = [[60, 64, 67], [57, 60, 64], [53, 57, 60], [55, 59, 62]]
    t = 0.0
    step = b.beat_s / 2
    chord_idx = 0
    while t < duration_s - step:
        notes = chords[chord_idx % len(chords)]
        for midi in notes + [notes[0] + 12]:
            if t >= duration_s:
                break
            b.note(pluck, midi, t, step * 1.8, amp=0.45)
            t += step
        chord_idx += 1
    # Vocal melody on top, half-note phrases.
    melody = [72, 76, 79, 76, 74, 72, 71, 72, 76, 79, 81, 79, 76, 74, 72, 67]
    t = 0.0
    for midi in melody * 2:
        if t >= duration_s - b.beat_s:
            break
        b.note(vocal_note, midi, t, b.beat_s * 0.95, amp=0.38)
        t += b.beat_s
    return b.render()
