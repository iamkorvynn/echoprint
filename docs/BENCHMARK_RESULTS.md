# Benchmark results

Measured on the build machine with `python scripts/benchmark.py`
(VPS, Python 3.12, NumPy 1.26 / SciPy 1.11). Re-run it for your
machine — the numbers below are a snapshot, not a promise.

## Middle-clip identification (5 s clip from 3 s into each track)

| Track | Peaks | Unique hashes | Fingerprint ms | Identify ms | Aligned score |
|---|---|---|---|---|---|
| 01-neon-freeway | 109 | 248 | 57.7 | 14.7 | 105 |
| 02-porch-light | 193 | 775 | 49.8 | 17.0 | 212 |
| 03-empty-rooms | 101 | 249 | 61.7 | 14.5 | 73 |
| 04-low-end-theory-club | 29 | 29 | 39.6 | 15.4 | 8 |
| 05-garage-door | 110 | 196 | 48.9 | 13.9 | 154 |
| 06-confetti-sky | 126 | 387 | 67.3 | 13.0 | 134 |
| 07-slow-goodbye | 468 | 2024 | 42.2 | 15.6 | 354 |
| 08-monsoon-raag | 167 | 605 | 33.6 | 12.4 | 132 |
| 09-rainy-window | 81 | 262 | 37.5 | 13.9 | 63 |
| 10-crown-of-strings | 256 | 973 | 33.9 | 17.1 | 306 |

**10/10 middle clips identified correctly.**

## Clean vs noisy vs sped-up (same 5 s clip per track, noise std 0.08)

| Track | Clean score | Noisy score | Sped-up (1.3×) |
|---|---|---|---|
| 01-neon-freeway | 105 | 74 | no match |
| 02-porch-light | 212 | 90 | no match |
| 03-empty-rooms | 73 | 56 | no match |
| 04-low-end-theory-club | 8 | 8 | no match |
| 05-garage-door | 154 | 147 | no match |
| 06-confetti-sky | 134 | 33 | no match |
| 07-slow-goodbye | 354 | 231 | no match |
| 08-monsoon-raag | 132 | 90 | no match |
| 09-rainy-window | 63 | 12 | no match |
| 10-crown-of-strings | 306 | 206 | no match |

Every noisy clip still matches; every sped-up clip honestly does not.

## Reading the numbers

- Fingerprinting a 12 s track takes ~35–70 ms; identifying a 5 s
  clip takes ~12–17 ms. The STFT dominates both.
- Track 04 is the thin one: 29 peaks, score 8 — it passes, but
  with the least margin in the library. Its bass-heavy, sparse
  arrangement genuinely produces few constellation points. A
  noisier room could push it under the threshold; that's an honest
  limit, not a bug to hide.
- Track 07 is the dense one: 468 peaks and 2024 hashes from
  layered strings + long notes. Density is not accuracy — its
  score is high because there is simply more signal to match.
