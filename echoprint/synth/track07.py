"""Track 07 — "Slow Goodbye": slow ballad, long notes.

62 BPM half-time, A minor. String swells and a vocal line that
holds each note for a full bar. The longest notes in the library —
its spectrogram is wide horizontal streaks, almost no vertical
drum lines.
"""

from __future__ import annotations

import numpy as np

from .engine import TrackBuilder
from .instruments import string_note, vocal_note

TITLE = "Slow Goodbye"
GENRE = "ballad"
BPM = 62
DESCRIPTION = "Slow ballad with long string and vocal notes in A minor."


def build_track(duration_s: float = 12.0) -> np.ndarray:
    b = TrackBuilder(duration_s=duration_s, bpm=BPM)
    bars = int(duration_s / b.bar_s) + 1
    b.drums("half_time", bars=bars, kick_amp=0.6, snare_amp=0.35, hat_amp=0.12)
    melody = [69, 72, 76, 79, 76, 72, 69, 67, 69, 72, 74, 76, 72, 69, 67, 64]
    t = 0.0
    for midi in melody:
        if t >= duration_s - b.bar_s:
            break
        b.note(vocal_note, midi, t, b.bar_s * 0.9, amp=0.4)
        b.note(string_note, midi - 12, t, b.bar_s, amp=0.3)
        b.note(string_note, midi - 5, t, b.bar_s, amp=0.2)
        t += b.bar_s / 2
    return b.render()
