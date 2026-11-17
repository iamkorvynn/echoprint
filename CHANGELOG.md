# Changelog

All notable changes to EchoPrint, newest first.

## 0.1.1 — 2026-11-18

- New `batch` command: identify every `.wav` in a directory.
- New `identify` flags: `--top N` (list top candidates) and
  `--min-score N` (override the aligned-score threshold).
- New scripts: `verify_library.py` (all-track checks),
  `plot_clips.py`, `compare_thresholds.py`, `fingerprint_stats.py`.
- Docs: per-track profiles, benchmark results with measured scores,
  threshold-tuning experiment, architecture, CLI reference, FAQ,
  roadmap, glossary, testing guide.
- Threshold-tuning doc corrected to the reproduction script's real
  numbers (percentile threshold: noisy clip shares 1–3 hashes;
  fraction-of-max: 62–137).

## 0.1.0 — 2026-11-18

- Wang (2003) constellation-map fingerprinting: STFT, peak picking,
  anchor/target hashes, hash-table lookup, offset-vote matching.
- CLI: `fingerprint`, `identify`, `show`, `list`, `stats`.
- Twist: `show` renders spectrogram + constellation as ASCII art
  and PNG plots; every identification prints a score breakdown.
- 10-track synthesized library (NumPy only, no copyrighted audio).
- Demo script with the four filmed cases: clean match, noisy match,
  sped-up honest no-match, unknown honest no-match.
- pytest suite covering determinism, identification, noise, sped-up,
  unknown audio, CLI, and visualisation.
