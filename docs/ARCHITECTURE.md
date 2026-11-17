# Architecture

```
audio (.wav)
  -> stft.py            STFT, log-magnitude spectrogram
  -> peaks.py           local maxima -> constellation (list of dots)
  -> hashes.py          anchor + next 5 peaks -> (f1, f2, dt) hashes
  -> database.py        JSON hash table: hash -> [(track, anchor time)]
  -> matcher.py         votes per (track, offset); biggest bin wins
  -> scoring.py         thresholds -> Identification (matched? + why)
  -> report.py          terminal / JSON rendering of the answer
  -> visualize.py       ASCII art + PNG plots (the twist)
```

## Seams (where to change things)

- **A different peak rule?** `peaks.py::find_peaks` only. Everything
  downstream consumes a list of `(time, freq)` peaks.
- **A different hash?** `hashes.py` only. The database stores hashes
  opaquely as `"f1,f2,dt"` strings.
- **A bigger library?** Swap `database.py`'s JSON store for SQLite /
  RocksDB behind the same `add_track` / `lookup` / `save` / `load`
  interface. Nothing else reads the file format.
- **A different decision rule?** `scoring.py::decide` only.
- **A new output format?** `report.py` only.

## Data flow, concretely

Fingerprinting a 12 s track: ~350 000 spectrogram values ->
~100–470 peaks -> ~30–2000 unique hashes -> one JSON entry per hash.
Identifying a 5 s clip: ~170 clip hashes -> lookups -> a few
hundred votes -> one offset bin with dozens of votes -> a decision.

## The synthesizer (`echoprint/synth/`)

Separate from the fingerprinting code on purpose: the library is
test data, not the product. `instruments.py` builds sounds from
sines + noise + envelopes; `engine.py` (`TrackBuilder`) places
them on a timeline; `track01.py` … `track10.py` each build one
track; `tracks.py` is the registry. `scripts/generate_library.py`
renders the WAVs.
