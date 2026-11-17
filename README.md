# EchoPrint — Shazam from scratch, in Python

Hear a 5-second clip, name the track. EchoPrint implements the classic
**Wang (2003) constellation-map fingerprinting** method from scratch with
NumPy/SciPy: STFT → spectrogram → peak picking → anchor/target hashes →
hash-table lookup → the track whose matches cluster at one consistent
time offset wins.

No copyrighted music anywhere in this repo. The 10-track library is
**synthesized with NumPy** — distinct electronic, acoustic, piano,
hip-hop, rock, pop, ballad, Bollywood-scale, lo-fi, and orchestral
test tones — so the matcher is genuinely tested, not memorised.

## The twist: show the work

EchoPrint doesn't just print a title. `echoprint show` prints the
spectrogram and the constellation of peaks as ASCII art in your
terminal (and saves PNG plots), and every identification prints a
score breakdown — shared hashes, aligned score, time offset,
runner-up — so you can *see* why a clip matched, or why a sped-up
clip didn't.

## Quick start

```bash
pip install -r requirements.txt

# 1. Render the library (synthesized, ~10 s)
python scripts/generate_library.py

# 2. Build the fingerprint database
python -m echoprint fingerprint tracks/

# 3. Identify a clip
python -m echoprint identify demo_clips/clean.wav
# MATCH: 03-empty-rooms ...

# 4. See the whole demo (clean / noisy / sped-up / unknown)
python demo.py

# 5. Show a track's spectrogram + constellation
python -m echoprint show tracks/03-empty-rooms.wav --plots plots/
```

Or install the CLI: `pip install -e .` then use `echoprint ...` directly.

## Commands

| Command | What it does |
|---|---|
| `echoprint fingerprint <library-dir> [--db PATH]` | Build the hash DB from a folder of `.wav` files |
| `echoprint identify <clip.wav> [--db PATH] [--json]` | Top match + score, or an honest "no match" |
| `echoprint show <track.wav> [--plots DIR]` | ASCII spectrogram + constellation, optional PNGs |
| `echoprint list [--db PATH]` | Tracks in the DB |
| `echoprint stats [--db PATH]` | DB statistics |

## The maths, in plain words

1. **Spectrogram.** Chop the audio into ~93 ms windows, 23 ms apart,
   and take the Fourier transform of each. You get a picture: time
   left-to-right, frequency bottom-to-top, brightness = loudness.
2. **Constellation.** Keep only the brightest dots — local maxima
   that are louder than their neighbours *and* reach 20% of the
   loudest point in the clip. A song becomes a scatter of a few
   hundred dots. Volume changes and a bit of noise barely move them.
3. **Hashes.** For each dot (anchor), pair it with the next 5 dots
   and store `(anchor frequency, target frequency, time between them)`.
   A hash is relative — no absolute time, no volume — so a 5-second
   clip cut from anywhere in a track produces the same hashes.
4. **Lookup + voting.** Each hash in the clip looks itself up in the
   database. Every stored copy votes for `(track, offset)` where
   `offset = database time − clip time`. If the clip really comes
   from that track, all its hashes agree on **one** offset and that
   bin collects dozens of votes. Other tracks scatter their votes.
5. **Decision.** The winner needs ≥ 5 hashes at one offset **and**
   at least 2× the runner-up's score. Otherwise: honest "no match".

See [docs/MATH.md](docs/MATH.md) for the full write-up.

## Honest limits

- **Tempo/pitch changes break it.** Speed a clip up 1.3× and every
  peak moves to a different frequency and every time delta changes,
  so no hashes line up. The demo proves this on purpose — the
  sped-up clip *must* return "no match". (Real Shazam has the same
  weakness for large shifts; fixing it needs tempo-invariant hashes.)
- **Tiny library.** 10 synthesized tracks, 12 s each. It proves the
  method; it is not a music catalogue.
- **Noise lowers the score.** A noisy clip still matches, but with
  fewer aligned hashes. Heavy noise (or a loud room) can push a
  real match below the threshold.
- **Short clips struggle.** Under ~2 s there aren't enough hashes
  to clear the threshold reliably.
- **Mono WAV only, 22 050 Hz** (other rates are linearly resampled).

## The library

| # | Track | Genre | BPM |
|---|---|---|---|
| 01 | Neon Freeway | fast electronic | 132 |
| 02 | Porch Light | acoustic pluck + vocal | 96 |
| 03 | Empty Rooms | piano solo | 80 |
| 04 | Low End Theory Club | bass-heavy hip-hop | 88 |
| 05 | Garage Door | rock drums + distorted guitar | 140 |
| 06 | Confetti Sky | bright pop synth | 118 |
| 07 | Slow Goodbye | slow ballad, long notes | 62 |
| 08 | Monsoon Raag | Bollywood (Bhairavi) scale | 100 |
| 09 | Rainy Window | lo-fi mellow | 72 |
| 10 | Crown of Strings | orchestral, many voices | 110 |

Each track's profile is in [docs/TRACKS.md](docs/TRACKS.md).

## Tests

```bash
pytest            # ~50 tests: determinism, identification, noise,
                  # sped-up -> no match, unknown -> no match, CLI
pytest -v         # see every case
```

## Project layout

```
echoprint/          the library (stft, peaks, hashes, database, matcher, ...)
echoprint/synth/    the synthesizer: instruments, rhythms, 10 track builders
scripts/            generate_library.py, make_clips.py, benchmark.py, plot_all.py
tracks/             the 10 synthesized .wav files (generated, not recorded)
demo_clips/         clean / noisy / sped-up / unknown clips for the demo
tests/              pytest suite
demo.py             the filmed cases, end to end
docs/               MATH.md, TRACKS.md, PERFORMANCE.md, LIMITS.md, ...
```

## License

MIT. Built clean-room from the published Wang (2003) method —
no Shazam code, branding, or audio was used.
