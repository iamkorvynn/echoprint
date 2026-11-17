"""Constellation helpers — the peak set as a first-class object.

Wang's insight: you don't need the whole spectrogram to recognise a
song, you need the *pattern* of its brightest dots. Two recordings of
the same audio (different volume, a bit of noise, a different mic)
produce nearly the same constellation; different songs produce
different ones. Everything downstream hashes this list.
"""

from __future__ import annotations

import numpy as np

from .peaks import Peak, find_peaks
from .stft import log_spectrogram
from . import config

__all__ = ["constellation", "constellation_from_audio", "constellation_density"]


def constellation(log_mag: np.ndarray) -> list[Peak]:
    """Peaks of a log-magnitude spectrogram, sorted by time."""
    return find_peaks(log_mag)


def constellation_from_audio(y: np.ndarray,
                             sr: int = config.SAMPLE_RATE) -> tuple[list[Peak], np.ndarray]:
    """Audio -> ``(peaks, log_mag_spectrogram)`` in one call."""
    _freqs, _times, log_mag = log_spectrogram(y, sr)
    return find_peaks(log_mag), log_mag


def constellation_density(peaks: list[Peak], duration_s: float) -> float:
    """Peaks per second — a quick sanity check on a track.

    Healthy synthetic tracks land around 5–30 peaks/second. Near
    zero means silence or a broken threshold; hundreds per second
    means the threshold is admitting noise.
    """
    if duration_s <= 0:
        return 0.0
    return len(peaks) / duration_s
