"""Audio I/O and small signal helpers.

Everything in EchoPrint works on mono float64 audio in [-1, 1] at
``config.SAMPLE_RATE`` (22050 Hz). WAV files are the only format v1
reads — no ffmpeg, no codecs, no surprises.
"""

from __future__ import annotations

import numpy as np
from scipy.io import wavfile

from . import config
from .errors import AudioError

__all__ = [
    "load_wav",
    "save_wav",
    "to_mono_float",
    "resample_linear",
    "add_noise",
    "slice_clip",
    "midi_to_freq",
    "note_name",
]


def to_mono_float(data: np.ndarray) -> np.ndarray:
    """Convert integer / stereo WAV data to mono float64 in [-1, 1]."""
    arr = np.asarray(data)
    if arr.ndim == 2:  # stereo -> mono by averaging channels
        arr = arr.mean(axis=1)
    if np.issubdtype(arr.dtype, np.integer):
        info = np.iinfo(arr.dtype)
        arr = arr.astype(np.float64) / max(abs(info.min), info.max)
    else:
        arr = arr.astype(np.float64)
    peak = np.max(np.abs(arr)) if arr.size else 0.0
    if peak > 1.0:
        arr = arr / peak
    return arr


def load_wav(path: str) -> tuple[int, np.ndarray]:
    """Load a WAV file, returning ``(sample_rate, mono float audio)``.

    Raises AudioError for missing files, non-WAV data, or silence.
    """
    try:
        sr, data = wavfile.read(path)
    except Exception as exc:  # unreadable / not a WAV
        raise AudioError(f"could not read audio file {path!r}: {exc}") from exc
    y = to_mono_float(data)
    if y.size == 0:
        raise AudioError(f"audio file {path!r} is empty")
    if not np.any(y):
        raise AudioError(f"audio file {path!r} is silent")
    if sr != config.SAMPLE_RATE:
        # v1 keeps it simple: resample linearly instead of refusing.
        y = resample_linear(y, sr / config.SAMPLE_RATE)
        sr = config.SAMPLE_RATE
    return sr, y


def save_wav(path: str, y: np.ndarray, sr: int = config.SAMPLE_RATE) -> None:
    """Save mono float audio as 16-bit PCM WAV."""
    y = np.asarray(y, dtype=np.float64)
    peak = np.max(np.abs(y)) if y.size else 0.0
    if peak > 1.0:
        y = y / peak
    wavfile.write(path, sr, (y * 32767).astype(np.int16))


def resample_linear(y: np.ndarray, factor: float) -> np.ndarray:
    """Resample by ``factor`` with linear interpolation.

    ``factor > 1`` plays faster (shorter, higher pitch) — exactly what
    a sped-up clip is, which is why it breaks fingerprint hashes.
    ``factor`` is output_len / input_len inverted: new[i] = y[i * factor].
    """
    y = np.asarray(y, dtype=np.float64)
    if factor == 1.0 or y.size == 0:
        return y.copy()
    n_out = max(1, int(len(y) / factor))
    idx = np.arange(n_out) * factor
    return np.interp(idx, np.arange(len(y)), y)


def add_noise(y: np.ndarray, std: float, seed: int = 0) -> np.ndarray:
    """Return ``y`` with white Gaussian noise of std ``std`` added."""
    rng = np.random.default_rng(seed)
    return np.asarray(y, dtype=np.float64) + rng.normal(0.0, std, size=len(y))


def slice_clip(y: np.ndarray, start_s: float, duration_s: float,
               sr: int = config.SAMPLE_RATE) -> np.ndarray:
    """Cut ``duration_s`` seconds starting at ``start_s`` seconds."""
    start = int(start_s * sr)
    end = min(len(y), start + int(duration_s * sr))
    if end <= start:
        raise AudioError("clip slice is empty (start beyond end of audio)")
    return np.asarray(y[start:end], dtype=np.float64)


def midi_to_freq(midi: int | float) -> float:
    """MIDI note number -> frequency in Hz (A4 = 69 = 440 Hz)."""
    return 440.0 * (2.0 ** ((midi - 69) / 12.0))


_NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def note_name(midi: int) -> str:
    """MIDI note number -> name, e.g. 69 -> 'A4'."""
    return f"{_NOTE_NAMES[midi % 12]}{midi // 12 - 1}"
