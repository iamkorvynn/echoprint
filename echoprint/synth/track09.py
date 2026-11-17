"""Track 09 — "Rainy Window": lo-fi mellow.

72 BPM half-time, F Lydian. Soft piano chords, a warm pad, and a
lazy melody that drifts — the quietest, dreamiest track. Few
drums, lots of sustain, low overall brightness.
"""

from __future__ import annotations

import numpy as np

from .engine import TrackBuilder
from .chords import chord
from .instruments import pad, piano_note

TITLE = "Rainy Window"
GENRE = "lo-fi"
BPM = 72
DESCRIPTION = "Mellow lo-fi: soft piano and pad in F Lydian."


def build_track(duration_s: float = 12.0) -> np.ndarray:
    b = TrackBuilder(duration_s=duration_s, bpm=BPM)
    bars = int(duration_s / b.bar_s) + 1
    b.drums("half_time", bars=bars, kick_amp=0.55, snare_amp=0.3, hat_amp=0.1)
    roots = [(53, "major7"), (50, "major7"), (48, "major7"), (55, "dom7")]
    for bar, (root, kind) in enumerate(roots * 3):
        t = bar * b.bar_s
        if t < duration_s - b.bar_s:
            b.chord_notes(piano_note, [m + 12 for m in chord(root, kind)],
                          t, b.bar_s * 0.9, amp=0.28)
            freqs = [440.0 * (2 ** ((m - 69) / 12))
                     for m in chord(root, kind)]
            b._place(pad(freqs, b.bar_s, amp=0.14), t)
    melody = [77, 76, 74, 72, 74, 76, 77, 79, 77, 76, 74, 72]
    t = 0.0
    for midi in melody * 2:
        if t >= duration_s - b.beat_s:
            break
        b.note(piano_note, midi, t, b.beat_s * 1.2, amp=0.32)
        t += b.beat_s
    return b.render()
