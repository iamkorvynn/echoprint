# Examples

Small, runnable scripts that show the library API without the CLI:

- `fingerprint_example.py` — build the database from `tracks/`.
- `identify_example.py` — identify `demo_clips/clean.wav` with a
  top-3 candidate list.
- `show_example.py` — print track 03's ASCII spectrogram and
  constellation, and save its PNG plots.

Run from the repo root, in order:

```bash
python scripts/generate_library.py
python examples/fingerprint_example.py
python examples/identify_example.py
python examples/show_example.py
```
