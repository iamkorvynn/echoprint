"""Short-time Fourier transform (STFT) and spectrograms.

The spectrogram is the picture fingerprinting works from: time runs
left-to-right, frequency bottom-to-top, brightness is loudness. A
tonal note shows up as a bright horizontal streak; a drum hit as a
bright vertical streak. Peaks (``peaks.py``) are the bright dots in
that picture.
"""

from __future__ import annotations

import numpy as np
from scipy.signal import stft

from . import config

__all__ = ["compute_stft", "magnitude_spectrogram", "log_spectrogram"]


def compute_stft(y: np.ndarray, sr: int = config.SAMPLE_RATE):
    """STFT with a Hann window. Returns ``(freqs, times, Z)``.

    Window 2048 samples (~93 ms) gives ~10.8 Hz frequency bins;
    hop 512 samples (~23 ms) gives the time resolution the hashes
    measure deltas in.
    """
    freqs, times, Z = stft(
        np.asarray(y, dtype=np.float64),
        fs=sr,
        window=config.WINDOW,
        nperseg=config.NPERSEG,
        noverlap=config.NOVERLAP,
        nfft=config.NPERSEG,
        boundary="zeros",
        padded=True,
    )
    return freqs, times, Z


def magnitude_spectrogram(y: np.ndarray, sr: int = config.SAMPLE_RATE):
    """Return ``(freqs, times, |Z|)``."""
    freqs, times, Z = compute_stft(y, sr)
    return freqs, times, np.abs(Z)


def log_spectrogram(y: np.ndarray, sr: int = config.SAMPLE_RATE):
    """Return ``(freqs, times, log1p(10 * |Z|))``.

    The log compresses the huge dynamic range of audio so quiet
    harmonics still count as peaks, and the x10 keeps the values in
    a range where the 0.20 fraction threshold in ``peaks.py`` lands
    on real notes rather than on the noise floor.
    """
    freqs, times, mag = magnitude_spectrogram(y, sr)
    return freqs, times, np.log1p(mag * 10.0)
