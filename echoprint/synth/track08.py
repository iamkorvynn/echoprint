"""Track 08 — "Monsoon Raag": Bollywood-scale melody.

100 BPM, Bhairavi scale (flat 2nd and flat 6th) rooted on D.
Plucked melody with vocal ornaments and a bossa-ish groove — the
only track in the library using this scale, so its note set (and
therefore its peak frequencies) barely overlaps the others.
"""

from __future__ import annotations

import numpy as np

from .engine import TrackBuilder
from .instruments import pluck, vocal_note

TITLE = "Monsoon Raag"
GENRE = "bollywood-scale"
BPM = 100
DESCRIPTION = "Melody on a Bollywood (Bhairavi) scale with pluck and vocal."


def build_track(duration_s: float = 12.0) -> np.ndarray:
    b = TrackBuilder(duration_s=duration_s, bpm=BPM)
    bars = int(duration_s / b.bar_s) + 1
    b.drums("bossa", bars=bars, kick_amp=0.7, snare_amp=0.35, hat_amp=0.2)
    # Bhairavi on D (62): D Eb F G A Bb C.
    scale = [62, 63, 65, 67, 69, 70, 72, 74, 75, 77, 79, 81]
    melody = [74, 75, 77, 79, 77, 75, 74, 72, 74, 75, 74, 72, 70, 69, 70, 72]
    t = 0.0
    step = b.beat_s / 2
    while t < duration_s - step:
        for midi in melody:
            if t >= duration_s:
                break
            b.note(pluck, midi, t, step * 1.5, amp=0.42)
            t += step
    # Vocal ornaments answering the pluck, one per bar.
    t = b.bar_s / 2
    for midi in [81, 79, 77, 75, 74, 75, 77, 79]:
        if t >= duration_s - b.beat_s:
            break
        b.note(vocal_note, midi, t, b.beat_s * 0.9, amp=0.32)
        t += b.bar_s
    return b.render()
