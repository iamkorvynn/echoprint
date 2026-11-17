# Performance notes

Measured on the build machine (VPS, Python 3.12, NumPy 1.26 /
SciPy 1.11). Numbers are indicative, not benchmarks — re-run
`python scripts/benchmark.py` for your machine.

## What was measured while tuning

- **Peak threshold:** a percentile threshold (top 10% of bins)
  admits ~1 700 noise peaks for a noisy clip and the true peaks
  drown (0 shared hashes). A fraction-of-max threshold (20% of
  the loudest log-magnitude) keeps ~40 peaks for both clean and
  noisy clips, sharing ~80 hashes. That's why `PEAK_FRACTION`
  is 0.20 — it was measured, not guessed.
- **Clean clip (5 s, middle of track 03):** ~80+ shared hashes,
  aligned score in the dozens.
- **Noisy clip (same + white noise std 0.08):** still matches,
  aligned score lower than clean.
- **Sped-up clip (1.3×):** 0 shared hashes. No match, as designed.
- **Identification:** a 5 s clip identifies in well under a second
  against the 10-track database; fingerprinting a 12 s track is
  a fraction of a second. The STFT dominates the cost.

## Scaling

- Fingerprinting is O(track length): one STFT + one pass over peaks.
- Identification is O(clip hashes × average hash fan-out in the DB).
  With a small library this is trivial; with a huge library the
  hash table is the bottleneck and wants a real key-value store.
- The JSON database is human-readable on purpose. For a large
  library, swap it for SQLite / RocksDB — the `FingerprintDatabase`
  interface (`add_track` / `lookup` / `save` / `load`) is the seam.
