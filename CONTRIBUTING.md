# Contributing

EchoPrint is a small, clean-room teaching codebase. A few rules:

- **No copyrighted audio, ever.** New library tracks must be
  synthesized with NumPy (see `echoprint/synth/`). No samples,
  no downloads, no "just one MP3 for testing".
- **No Shazam branding, code, or assets.** The method is the
  published Wang (2003) paper; the implementation is original.
- **Tests for behaviour changes.** If you touch the matcher,
  thresholds, or hashing, add or update a test that pins the
  behaviour — especially the sped-up → no-match guarantee.
- **Honest numbers.** If a change affects scores, re-run
  `python scripts/benchmark.py` and update `docs/PERFORMANCE.md`.
- **Small commits.** One file / one feature per commit.
