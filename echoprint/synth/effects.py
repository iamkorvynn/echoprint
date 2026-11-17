"""Effects — tiny, honest DSP: feedback delay and soft clipping.

No reverb impulse responses, no plugins: a feedback delay (echo)
and tanh soft-clipping are enough to give the synthetic tracks
some space and grit without hiding their fingerprints.
"""

from __future__ import annotations

import numpy as np

from .. import config

SR = config.SAMPLE_RATE

__all__ = ["delay", "soft_clip", "normalize"]


def delay(y: np.ndarray, delay_s: float = 0.28, feedback: float = 0.3,
          mix: float = 0.25) -> np.ndarray:
    """Simple feedback echo. ``mix`` is how much echo is blended in."""
    y = np.asarray(y, dtype=np.float64)
    d = int(delay_s * SR)
    if d <= 0 or len(y) == 0:
        return y.copy()
    out = y.copy()
    for i in range(d, len(y)):
        out[i] += feedback * out[i - d]
    return (1 - mix) * y + mix * out


def soft_clip(y: np.ndarray, drive: float = 1.5) -> np.ndarray:
    """tanh saturation — gentle distortion, keeps peaks bounded."""
    return np.tanh(drive * np.asarray(y, dtype=np.float64)) / np.tanh(drive)


def normalize(y: np.ndarray, target_peak: float = 0.85) -> np.ndarray:
    """Scale so the loudest sample hits ``target_peak`` (no-op if silent)."""
    y = np.asarray(y, dtype=np.float64)
    peak = np.max(np.abs(y)) if y.size else 0.0
    if peak == 0:
        return y
    return y * (target_peak / peak)
