# Threshold tuning — why 20% of max, not a percentile

During development the peak threshold was the difference between
a matcher that works and one that doesn't. The experiment, on a
5 s clip from track 03 and the same clip with white noise:

## Percentile threshold (top 10% of spectrogram bins)

| Clip | Peaks | Hashes shared with the true track |
|---|---|---|
| clean | 163 | 123 |
| + noise std 0.05 | 1686 | 0 |
| + noise std 0.10 | 1696 | 0 |

White noise fills the low percentiles, so the threshold admits
thousands of noise-only local maxima and the real peaks drown.
The noisy clip shares **zero** hashes with its own track.

## Fraction-of-max threshold (peak > 20% of the loudest log-magnitude)

| Clip | Peaks | Hashes shared with the true track |
|---|---|---|
| clean | 40 | 81 |
| + noise std 0.05 | 40 | 80 |
| + noise std 0.10 | 40 | 83 |
| + noise std 0.20 | 54 | 69 |

Noise bins sit far below 20% of the loudest bin, so the same ~40
peaks survive at every noise level and the hashes line up. The
reproduction script is `scripts/compare_thresholds.py`.

## The other thresholds

- **Neighbourhood 11×11** (STFT frames × freq bins): big enough
  that one note doesn't produce a cluster of adjacent peaks, small
  enough that distinct notes stay distinct.
- **Fan-out 5, max dt 40 frames (~0.93 s):** the classic Wang
  fan-out. Wider fan-outs add hashes but also add accidental
  collisions between tracks.
- **Min aligned score 5, winner ratio 2×:** low enough that the
  sparsest track (04, score 8) passes, high enough that unknown
  audio (best aligned score 1–2) and sped-up audio (0) never do.
