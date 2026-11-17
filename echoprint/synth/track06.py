"""Track 06 — "Confetti Sky": bright pop synth chorus.

118 BPM, G major, four-on-the-floor under a chirpy saw chorus
with a soft pad underneath. The brightest track — most energy
in the upper mids, big catchy leaps in the melody.
"""

from __future__ import annotations

import numpy as np

from .engine import TrackBuilder
from .chords import chord
from .instruments import pad, saw_note

TITLE = "Confetti Sky"
GENRE = "pop synth"
BPM = 118
DESCRIPTION = "Bright pop synth chorus in G major with a soft pad."


def build_track(duration_s: float = 12.0) -> np.ndarray:
    b = TrackBuilder(duration_s=duration_s, bpm=BPM)
    bars = int(duration_s / b.bar_s) + 1
    b.drums("four_on_floor", bars=bars, kick_amp=0.8, snare_amp=0.4, hat_amp=0.22)
    # Pad chords: G - Em - C - D, one per bar.
    roots = [(55, "major"), (52, "minor"), (48, "major"), (50, "major")]
    for bar, (root, kind) in enumerate(roots * 3):
        t = bar * b.bar_s
        if t < duration_s - b.bar_s:
            midis = [m + 12 for m in chord(root, kind)]
            freqs = [440.0 * (2 ** ((m - 69) / 12)) for m in midis]
            from .instruments import pad as _pad
            b._place(_pad(freqs, b.bar_s, amp=0.16), t)
    chorus = [79, 83, 86, 83, 79, 76, 79, 83, 86, 88, 86, 83, 79, 76, 74, 79]
    t = 0.0
    step = b.beat_s / 2
    while t < duration_s - step:
        for midi in chorus:
            if t >= duration_s:
                break
            b.note(saw_note, midi, t, step * 0.9, amp=0.26)
            t += step
    return b.render()
