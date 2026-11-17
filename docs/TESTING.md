# Testing

```bash
pytest            # full suite (65+ tests, ~10-20 s)
pytest -v         # every test by name
pytest tests/test_spedup.py -v   # just the honest-failure cases
pytest -k noisy   # just the noise-robustness cases
```

## What's covered

- **Determinism:** same audio -> same peaks, same hashes, twice.
- **Identification:** 5 s clips from the middle and start of a
  track identify it; the offset points at the right place.
- **Noise:** a noisy clip still matches, with a lower score; heavy
  noise never matches the *wrong* track.
- **Sped-up:** 1.1×, 1.3×, and 0.8× all return "no match".
- **Unknown:** random noise, an unrelated melody, and a pure tone
  all return "no match".
- **Synthesizer:** all 10 tracks build, are deterministic, are
  audible, and pairwise share < 25% of hashes.
- **Database:** add / lookup / save / load round-trip / remove.
- **Scoring:** threshold, ambiguity, and clear-winner decisions.
- **CLI:** fingerprint -> identify -> list -> stats end to end,
  JSON output, `--top`, `--min-score`, missing-DB error.
- **Visualisation:** ASCII art contains peaks; PNG plots are written.

## The one test that must never be "fixed" by weakening it

`test_spedup.py::test_sped_up_clip_no_match` — if a change makes
sped-up audio match, the fingerprint lost its discrimination, and
the fix belongs in the algorithm, not in the test.
