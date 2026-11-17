"""Track 04 — "Low End Theory Club": bass-heavy hip-hop.

88 BPM hip-hop pattern, sub bass doing the talking, sparse saw
stabs on top. The lowest-frequency track in the library — most of
its constellation sits in the bottom third of the spectrogram.
"""

from __future__ import annotations

import numpy as np

from .engine import TrackBuilder
from .instruments import bass_note, saw_note

TITLE = "Low End Theory Club"
GENRE = "hip-hop"
BPM = 88
DESCRIPTION = "Bass-heavy hip-hop with a laid-back boom-bap groove."


def build_track(duration_s: float = 12.0) -> np.ndarray:
    b = TrackBuilder(duration_s=duration_s, bpm=BPM)
    bars = int(duration_s / b.bar_s) + 1
    b.drums("hiphop", bars=bars, kick_amp=1.0, snare_amp=0.45, hat_amp=0.2)
    bass_line = [36, 0, 36, 41, 0, 39, 36, 0, 34, 0, 36, 43, 0, 41, 39, 0]
    t = 0.0
    step = b.beat_s / 2
    while t < duration_s - step:
        for midi in bass_line:
            if t >= duration_s:
                break
            if midi:
                b.note(bass_note, midi, t, step * 1.6, amp=0.7)
            t += step
    # Sparse minor-key stabs, one per bar.
    stabs = [63, 66, 68, 63]
    for bar, midi in enumerate(stabs * 3):
        t = bar * b.bar_s + b.beat_s
        if t < duration_s - b.beat_s:
            b.note(saw_note, midi, t, b.beat_s * 0.5, amp=0.25)
            b.note(saw_note, midi + 7, t, b.beat_s * 0.5, amp=0.2)
    return b.render()
