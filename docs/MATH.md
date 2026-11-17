# The maths behind EchoPrint

This is a plain-words explanation of Wang's 2003 paper,
*"An Industrial-Strength Audio Search Algorithm"* (ISMIR 2003),
as implemented here. No prior signal-processing knowledge assumed.

## 1. The spectrogram: sound as a picture

Take the audio and slide a window across it. At each window
position (every 23 ms), run a Fourier transform, which answers:
"how much energy is there at each frequency right now?"

Stack those answers side by side and you get a picture:

- **x-axis:** time (each column is one ~23 ms frame)
- **y-axis:** frequency (each row is one ~10.8 Hz bin, 0–11 025 Hz)
- **brightness:** loudness (log scale, so quiet harmonics are visible)

A sung note is a bright horizontal streak. A drum hit is a bright
vertical streak. The whole song is a pattern of streaks.

Parameters used here: 22 050 Hz sample rate, 2048-sample Hann
window (~93 ms), 512-sample hop (~23 ms), 1025 frequency bins.

## 2. The constellation: keep only the brightest dots

The spectrogram has ~350 000 numbers for a 12 s track. Most of
them are uninformative. Wang's move: keep only **local maxima** —
a bin that is louder than everything in its 11×11 neighbourhood —
*and* louder than 20% of the loudest bin in the clip.

The surviving dots are the **constellation map**: a few hundred
points per track. They are robust because they are *relative*:
turn the volume down and the same dots survive (everything scales
together); add moderate noise and the loudest local events are
still the same notes.

Why 20% of the max and not "the top 10% of bins"? White noise
fills the low percentiles — a percentile threshold admits
thousands of noise-only maxima and the real peaks drown. A
fraction-of-max threshold keeps the same ~40 peaks for a clean
clip and its noisy version (measured during development).

## 3. Hashes: pairs of dots

One dot alone is useless — the same frequency appears in many
songs. A *pair* of dots is distinctive. For each anchor dot, pair
it with the next 5 dots and record:

```
hash = (frequency of anchor, frequency of target, time between them)
```

in STFT frames (1 frame ≈ 23 ms). The hash stores no absolute
time and no loudness, so:

- the same 5 s cut from anywhere in the track → the same hashes
- the same 5 s at a different volume → the same hashes

Each track contributes a few hundred unique hashes. The database
is a dictionary: `hash → [(track, anchor time), ...]`.

## 4. Matching: voting with a time offset

To identify a clip, hash it the same way, then look every hash up:

```
for each shared hash:
    for each (track, db_time) stored under it:
        for each clip_time the hash occurs at in the clip:
            vote[(track, db_time - clip_time)] += 1
```

If the clip comes from track X starting at time T, then for
every true hash `db_time - clip_time = T` — **all the votes land
in one bin**. Hashes from other tracks (or noise) scatter across
many bins and never pile up. The score for a track is the size of
its biggest bin.

This is the heart of the algorithm: it's not "most shared hashes
wins", it's "most hashes *agreeing on when the clip starts* wins".

## 5. Decision: thresholds, not vibes

A match is declared only when:

1. aligned score ≥ 5 hashes at one offset, and
2. winner's score ≥ 2× the runner-up's score.

Otherwise the answer is "no match". The 2× rule matters: two
tracks in similar keys can share a handful of hashes, but they
can't both pile votes at one offset.

## 6. Why sped-up audio fails (and why that's correct)

Speeding audio by 1.3× does two things:

- **Frequencies × 1.3** — a 440 Hz peak moves to 572 Hz, a
  different bin, so `(f1, f2, dt)` hashes no longer exist.
- **Time deltas ÷ 1.3** — peaks that were 10 frames apart are now
  ~8 frames apart, changing `dt` as well.

Both parts of every hash change, so essentially zero hashes match.
That's not a bug in this implementation — it's a property of the
method, and the demo treats it as a feature: an honest "no match"
is better than a confident wrong answer. Tempo-invariant
fingerprinting (e.g. hashing frequency *ratios* and normalising
time deltas) is a known extension, out of scope for v1.
