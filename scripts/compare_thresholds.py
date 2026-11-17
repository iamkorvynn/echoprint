"""Reproduce the threshold experiment from docs/THRESHOLD_TUNING.md.

    python scripts/compare_thresholds.py

Compares a percentile peak threshold against the fraction-of-max
threshold on a clean clip and noisy versions of it, and prints
how many hashes each shares with the true track.
"""

from __future__ import annotations

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from echoprint.audio import add_noise, load_wav, slice_clip  # noqa: E402
from echoprint.constellation import constellation_from_audio  # noqa: E402
from echoprint.hashes import hashes_from_peaks  # noqa: E402
from echoprint.peaks import find_peaks  # noqa: E402
from echoprint.stft import log_spectrogram  # noqa: E402


def hashes_with_threshold(y, mode):
    _f, _t, log_mag = log_spectrogram(y)
    if mode == "percentile":
        from scipy.ndimage import maximum_filter
        neigh = maximum_filter(log_mag, size=(11, 11))
        thr = np.percentile(log_mag, 90)
        mask = (log_mag == neigh) & (log_mag > thr)
        fy, tx = np.where(mask)
        peaks = sorted(zip(tx.tolist(), fy.tolist()))
    else:
        peaks = find_peaks(log_mag)
    return hashes_from_peaks(peaks), len(peaks)


def main() -> int:
    _sr, y = load_wav(os.path.join("tracks", "03-empty-rooms.wav"))
    clip = slice_clip(y, 3.0, 5.0)
    for mode in ("percentile", "fraction-of-max"):
        print(f"\n== {mode} threshold ==")
        base, _ = hashes_with_threshold(clip, mode)
        for noise in (0.0, 0.05, 0.10, 0.20):
            noisy = add_noise(clip, noise, seed=1) if noise else clip
            hashes, n_peaks = hashes_with_threshold(noisy, mode)
            shared = len(set(hashes) & set(base)) if noise else len(base)
            print(f"  noise {noise:<4} peaks {n_peaks:>5}  "
                  f"shared hashes {shared}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
