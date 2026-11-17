"""Identify — the full pipeline from audio to an answer.

``identify_audio(y, db)`` is the one function everything funnels
through: audio -> STFT -> constellation -> hashes -> votes -> decision.
``identify_file`` is the same thing starting from a WAV path.
"""

from __future__ import annotations

import numpy as np

from . import config
from .audio import load_wav
from .constellation import constellation_from_audio
from .database import FingerprintDatabase
from .hashes import hashes_from_peaks
from .matcher import match_clip
from .scoring import Identification, decide

__all__ = ["identify_audio", "identify_file", "fingerprint_audio"]


def fingerprint_audio(y: np.ndarray,
                      sr: int = config.SAMPLE_RATE) -> dict:
    """Audio -> its hashes (the fingerprint). Also returns the peaks
    and spectrogram for ``show``."""
    peaks, log_mag = constellation_from_audio(y, sr)
    hashes = hashes_from_peaks(peaks)
    return {"peaks": peaks, "log_mag": log_mag, "hashes": hashes}


def identify_audio(y: np.ndarray, db: FingerprintDatabase,
                   sr: int = config.SAMPLE_RATE) -> Identification:
    """Identify mono audio against a fingerprint database."""
    fp = fingerprint_audio(y, sr)
    result = match_clip(fp["hashes"], db)
    return decide(result, db)


def identify_file(path: str, db: FingerprintDatabase) -> Identification:
    """Identify a WAV file against a fingerprint database."""
    _sr, y = load_wav(path)
    return identify_audio(y, db)
