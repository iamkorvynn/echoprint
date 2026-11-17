"""Track 01 — "Neon Freeway": fast electronic, steady beat.

132 BPM four-on-the-floor kick, driving sub bass, bright saw lead
on an A pentatonic-major run. The fastest, most regular track in
the library — its constellation is a tight, repeating grid.
"""

from __future__ import annotations

import numpy as np

from .engine import TrackBuilder
from .instruments import bass_note, saw_note

TITLE = "Neon Freeway"
GENRE = "fast electronic"
BPM = 132
DESCRIPTION = "Fast electronic with a steady four-on-the-floor beat."


def build_track(duration_s: float = 12.0) -> np.ndarray:
    b = TrackBuilder(duration_s=duration_s, bpm=BPM)
    bars = int(duration_s / b.bar_s)
    b.drums("four_on_floor", bars=bars)
    # Driving bass: A1/A2 eighth-note pulse.
    bass_line = [33, 33, 45, 33, 36, 33, 45, 43]
    t = 0.0
    step = b.beat_s / 2
    while t < duration_s - step:
        for midi in bass_line:
            if t >= duration_s:
                break
            b.note(bass_note, midi, t, step * 0.95, amp=0.6)
            t += step
    # Bright saw lead, pentatonic major in A (69 = A4).
    lead = [69, 72, 76, 81, 76, 72, 69, 76, 81, 84, 81, 76, 72, 69, 64, 67]
    t = 0.0
    while t < duration_s - b.beat_s / 2:
        for midi in lead:
            if t >= duration_s:
                break
            b.note(saw_note, midi, t, b.beat_s / 2 * 0.9, amp=0.28)
            t += b.beat_s / 2
    return b.render()
