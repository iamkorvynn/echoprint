# Demo

Run it:

```bash
python demo.py
```

What it does, in order:

1. Renders the 10-track library if it isn't there yet, and makes
   the four demo clips.
2. Fingerprints all 10 tracks into `echoprint.db.json`.
3. Identifies four clips:
   - **clean.wav** — 5 s from the middle of track 03 → must match
     `03-empty-rooms`.
   - **noisy.wav** — the same clip + white noise → must still
     match, with a lower aligned score.
   - **sped-up.wav** — the same clip at 1.3× speed → must return
     "no match" (the honest failure: pitch/tempo changes break
     the hashes).
   - **unknown.wav** — a melody from no track → must return
     "no match".
4. Shows the work: ASCII spectrogram + constellation for track 03.
5. Prints a PASS/FAIL verdict for all four cases and exits 0
   only if all four are correct.
