"""TrackBuilder — a tiny timeline mixer for synthesized tracks.

Usage::

    b = TrackBuilder(duration_s=12.0, bpm=128)
    b.note(pluck, midi=69, start=0.0, duration=0.25)
    b.drums("four_on_floor", bars=6)
    y = b.render()

Notes and drums are added as events, then rendered by summing
everything into one mono array and normalising. Deterministic:
the same builder calls always produce the same samples.
"""

from __future__ import annotations

import numpy as np

from .. import config
from ..audio import midi_to_freq
from . import instruments
from .effects import normalize
from .rhythm import PATTERNS, steps_to_times

SR = config.SAMPLE_RATE

__all__ = ["TrackBuilder"]


class TrackBuilder:
    def __init__(self, duration_s: float = 12.0, bpm: float = 120.0):
        self.duration_s = duration_s
        self.bpm = bpm
        self.y = np.zeros(int(duration_s * SR))
        self.beat_s = 60.0 / bpm
        self.bar_s = self.beat_s * 4

    # -- placing sounds ------------------------------------------------
    def _place(self, sound: np.ndarray, start_s: float) -> None:
        start = int(start_s * SR)
        if start >= len(self.y):
            return
        end = min(len(self.y), start + len(sound))
        self.y[start:end] += sound[: end - start]

    def note(self, func, midi: int, start: float, duration: float,
             amp: float = 0.5, **kwargs) -> None:
        """Play one note: ``func`` is an instrument from ``instruments``."""
        self._place(func(midi_to_freq(midi), duration, amp=amp, **kwargs), start)

    def chord_notes(self, func, midis, start: float, duration: float,
                    amp: float = 0.3) -> None:
        for midi in midis:
            self.note(func, midi, start, duration, amp=amp / max(len(midis), 1))

    def melody(self, func, midis, start: float, note_duration: float,
               amp: float = 0.5, gap: float = 0.0) -> None:
        """A sequence of notes, one after another."""
        t = start
        for midi in midis:
            if midi is not None and midi > 0:
                self.note(func, midi, t, note_duration, amp=amp)
            t += note_duration + gap

    def drums(self, pattern_name: str, bars: int = 1, start_bar: float = 0.0,
              kick_amp: float = 0.9, snare_amp: float = 0.5,
              hat_amp: float = 0.25) -> None:
        """Lay down a drum pattern for ``bars`` bars."""
        pattern = PATTERNS[pattern_name]
        step_s = self.bar_s / 16
        for bar in range(bars):
            bar_start = (start_bar + bar) * self.bar_s
            for t in steps_to_times(pattern["kick"], bar_start, step_s):
                self._place(instruments.kick(amp=kick_amp), t)
            for t in steps_to_times(pattern["snare"], bar_start, step_s):
                self._place(instruments.snare(seed=int(t * 100)), t)
            for t in steps_to_times(pattern["hat"], bar_start, step_s):
                self._place(instruments.hat(seed=int(t * 100)), t)

    def render(self, normalize_peak: float = 0.85) -> np.ndarray:
        """Mix down and normalise. Returns mono float audio."""
        return normalize(self.y, normalize_peak)
