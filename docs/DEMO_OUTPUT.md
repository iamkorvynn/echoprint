# Demo output (recorded)

`python demo.py` on the build machine. Full output includes the
ASCII spectrogram and constellation for track 03; the
identification results are:

```
[1/6] Fingerprinting the 10-track library...
  10 tracks, ... unique hashes -> echoprint.db.json

clean 5s clip (from the middle of track 03):
  MATCH: 03-empty-rooms
  clip hashes: 169, shared with library: 97
  aligned score: 73 hashes at one offset, offset 3.00 s
  runner-up: 09-rainy-window (2), confidence 43.2%

same clip + white noise:
  MATCH: 03-empty-rooms
  aligned score: 56 (lower than clean, as expected)

same clip at 1.3x speed — expect NO MATCH:
  NO MATCH — best aligned score 1, below the threshold 5

a melody from no track — expect NO MATCH:
  NO MATCH — best aligned score 1, below the threshold 5

Demo verdict:
  clean clip matched track 03:      PASS
  noisy clip still matched:         PASS
  noisy score < clean score:        PASS
  sped-up clip honestly no match:   PASS
  unknown audio honestly no match:  PASS
```

`demo.py` exits 0 only if all four verdicts pass.
