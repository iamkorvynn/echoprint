"""Show the work — ASCII spectrograms, constellations, and PNG plots.

This is EchoPrint's twist: instead of a black box that prints a
title, it shows you the spectrogram, the constellation of peaks,
and the score breakdown, so you can *see* why a clip matched (or
why a sped-up clip did not — its peaks land on different
frequencies and different time deltas, so the hashes never form).
"""

from __future__ import annotations

import numpy as np

from . import config

__all__ = [
    "ascii_spectrogram",
    "ascii_constellation",
    "plot_spectrogram",
    "plot_constellation",
]

_ASCII_LEVELS = " .:-=+*#%@"


def _downsample_2d(arr: np.ndarray, height: int, width: int) -> np.ndarray:
    """Block-average a 2D array down to (height, width)."""
    h, w = arr.shape
    bh = max(1, h // height)
    bw = max(1, w // width)
    trimmed = arr[: bh * height, : bw * width]
    return trimmed.reshape(height, bh, width, bw).mean(axis=(1, 3))


def ascii_spectrogram(log_mag: np.ndarray, width: int = 72,
                      height: int = 20) -> str:
    """Render a log-magnitude spectrogram as ASCII art.

    Time runs left-to-right, frequency bottom-to-top, brightness is
    loudness. Returns a multi-line string.
    """
    if log_mag.size == 0:
        return "(empty spectrogram)"
    small = _downsample_2d(log_mag, height, width)
    lo, hi = float(small.min()), float(small.max())
    span = max(hi - lo, 1e-9)
    norm = (small - lo) / span
    rows = []
    for r in range(height - 1, -1, -1):  # high freq at the top
        row = "".join(
            _ASCII_LEVELS[min(int(v * len(_ASCII_LEVELS)), len(_ASCII_LEVELS) - 1)]
            for v in norm[r]
        )
        rows.append(row)
    axis = f"freq ^  (0-{config.SAMPLE_RATE // 2} Hz, time ->)"
    return axis + "\n" + "\n".join(rows)


def ascii_constellation(peaks, shape: tuple[int, int], width: int = 72,
                        height: int = 20) -> str:
    """Render the constellation (peak dots) as ASCII art.

    Same axes as ``ascii_spectrogram`` so the two can be compared
    side by side: the dots should sit on the bright streaks.
    """
    n_freq, n_time = shape
    grid = [[" " for _ in range(width)] for _ in range(height)]
    for t_idx, f_idx in peaks:
        x = min(int(t_idx / max(n_time - 1, 1) * (width - 1)), width - 1)
        y = min(int(f_idx / max(n_freq - 1, 1) * (height - 1)), height - 1)
        grid[height - 1 - y][x] = "*"
    rows = ["".join(row) for row in grid]
    return "constellation: * = peak  (freq ^, time ->)\n" + "\n".join(rows)


def plot_spectrogram(log_mag: np.ndarray, path: str,
                     title: str = "Spectrogram") -> str:
    """Save a PNG spectrogram plot. Returns the path written."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.imshow(log_mag, origin="lower", aspect="auto", cmap="magma")
    ax.set_title(title)
    ax.set_xlabel("STFT frame (~23 ms each)")
    ax.set_ylabel("Frequency bin (~10.8 Hz each)")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return path


def plot_constellation(peaks, shape: tuple[int, int], path: str,
                       title: str = "Constellation map") -> str:
    """Save a PNG scatter plot of the constellation. Returns the path."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    n_freq, n_time = shape
    fig, ax = plt.subplots(figsize=(10, 4))
    if peaks:
        ts = [p[0] for p in peaks]
        fs = [p[1] for p in peaks]
        ax.scatter(ts, fs, s=8, c="#E10600", marker="x")
    ax.set_xlim(0, max(n_time, 1))
    ax.set_ylim(0, max(n_freq, 1))
    ax.set_title(title)
    ax.set_xlabel("STFT frame (~23 ms each)")
    ax.set_ylabel("Frequency bin (~10.8 Hz each)")
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return path
