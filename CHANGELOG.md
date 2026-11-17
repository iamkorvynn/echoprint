# Changelog

All notable changes to EchoPrint, newest first.

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
