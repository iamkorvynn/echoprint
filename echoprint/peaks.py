"""Peak picking — the constellation map.

A spectrogram peak is a time-frequency bin that is louder than all of
its neighbours *and* loud enough in absolute terms. The set of peaks
is the "constellation": a sparse scatter of bright dots that survives
volume changes, background chatter and (to a point) noise, because
the dots are the loudest local events, not the raw waveform.

Why a fraction-of-max threshold and not a percentile: with white
noise, a percentile threshold (e.g. top 10%) admits thousands of
noise-only local maxima — the noise floor fills the percentile. A
peak must instead reach 20% of the loudest log-magnitude in the
clip; noise bins sit far below that, so a noisy clip keeps the
same ~40 peaks as the clean clip (measured in prototyping).
"""

from __future__ import annotations

import numpy as np
from scipy.ndimage import maximum_filter

from . import config

__all__ = ["find_peaks", "peak_stats"]

#: A peak is ``(time_frame_index, freq_bin_index)``.
Peak = tuple[int, int]


def find_peaks(log_mag: np.ndarray,
               neighbourhood: int = config.PEAK_NEIGHBOURHOOD,
               fraction: float = config.PEAK_FRACTION) -> list[Peak]:
    """Find constellation peaks in a log-magnitude spectrogram.

    Returns peaks sorted by time frame, then frequency bin — the
    ordering the hash fan-out in ``hashes.py`` relies on.
    """
    log_mag = np.asarray(log_mag, dtype=np.float64)
    if log_mag.size == 0:
        return []
    # Local maxima: a bin equal to the max of its neighbourhood.
    neigh_max = maximum_filter(log_mag, size=(neighbourhood, neighbourhood))
    threshold = float(log_mag.max()) * fraction
    mask = (log_mag == neigh_max) & (log_mag > threshold)
    freq_idx, time_idx = np.where(mask)
    peaks = sorted(zip(time_idx.tolist(), freq_idx.tolist()))
    return peaks


def peak_stats(peaks: list[Peak], n_frames: int, n_bins: int) -> dict:
    """Small summary of a constellation, for ``show`` / stats."""
    if not peaks:
        return {"count": 0, "per_second": 0.0, "freq_min": None,
                "freq_max": None, "time_span_frames": 0}
    freqs = [p[1] for p in peaks]
    times = [p[0] for p in peaks]
    duration_s = n_frames * config.HOP / config.SAMPLE_RATE
    return {
        "count": len(peaks),
        "per_second": len(peaks) / max(duration_s, 1e-9),
        "freq_min": min(freqs),
        "freq_max": max(freqs),
        "time_span_frames": max(times) - min(times),
    }
