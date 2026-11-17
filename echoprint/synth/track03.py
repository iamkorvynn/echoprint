"""Track 03 — "Empty Rooms": piano-like solo.

80 BPM, D minor, no drums at all. A lone piano line with space
between the notes — the sparsest constellation in the library,
which makes it a good test: few peaks, but they are unmistakable.
"""

from __future__ import annotations

import numpy as np

from .engine import TrackBuilder
from .instruments import piano_note

TITLE = "Empty Rooms"
GENRE = "piano solo"
BPM = 80
DESCRIPTION = "Solo piano-like melody in D minor, no drums."


def build_track(duration_s: float = 12.0) -> np.ndarray:
    b = TrackBuilder(duration_s=duration_s, bpm=BPM)
    melody = [74, 77, 81, 79, 77, 74, 72, 74, 77, 81, 84, 81, 79, 77, 76, 74,
              72, 74, 77, 79, 81, 79, 77, 74]
    t = 0.0
    for midi in melody:
        if t >= duration_s - b.beat_s:
            break
        b.note(piano_note, midi, t, b.beat_s * 1.4, amp=0.5)
        # Left-hand root, a beat behind the melody note.
        b.note(piano_note, midi - 24, t, b.beat_s * 1.8, amp=0.25)
        t += b.beat_s * 0.75
    return b.render()
