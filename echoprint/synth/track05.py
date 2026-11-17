"""Track 05 — "Garage Door": rock drums + distorted-ish guitar.

140 BPM rock pattern, E blues riff through the tanh-distorted
guitar voice. The loudest, grittiest track — distortion adds
harmonics, so its constellation is dense in the mid frequencies.
"""

from __future__ import annotations

import numpy as np

from .engine import TrackBuilder
from .instruments import bass_note, guitar_note

TITLE = "Garage Door"
GENRE = "rock"
BPM = 140
DESCRIPTION = "Rock drums with a distorted-ish guitar riff in E blues."


def build_track(duration_s: float = 12.0) -> np.ndarray:
    b = TrackBuilder(duration_s=duration_s, bpm=BPM)
    bars = int(duration_s / b.bar_s) + 1
    b.drums("rock", bars=bars, kick_amp=0.9, snare_amp=0.55, hat_amp=0.28)
    riff = [64, 64, 67, 64, 70, 69, 67, 64, 62, 64, 67, 70, 69, 67, 64, 62]
    t = 0.0
    step = b.beat_s / 2
    while t < duration_s - step:
        for midi in riff:
            if t >= duration_s:
                break
            b.note(guitar_note, midi, t, step * 0.9, amp=0.42)
            t += step
    # Root bass pounding eighths underneath.
    t = 0.0
    while t < duration_s - step:
        b.note(bass_note, 40, t, step * 0.9, amp=0.5)
        t += step
    return b.render()
