# The 10-track library

All tracks are synthesized with NumPy (sine stacks, noise bursts,
envelopes) — no recordings, no samples, no copyrighted audio.
Each is 12 seconds, mono, 22 050 Hz.

| # | File | Title | Genre | BPM | Scale / key | Character |
|---|---|---|---|---|---|---|
| 01 | 01-neon-freeway | Neon Freeway | fast electronic | 132 | A pentatonic major | four-on-the-floor, saw lead, sub bass |
| 02 | 02-porch-light | Porch Light | acoustic | 96 | C major | pluck arpeggios + vocal melody |
| 03 | 03-empty-rooms | Empty Rooms | piano solo | 80 | D minor | lone piano, no drums, sparse |
| 04 | 04-low-end-theory-club | Low End Theory Club | hip-hop | 88 | A minor-ish | sub bass, boom-bap, sparse stabs |
| 05 | 05-garage-door | Garage Door | rock | 140 | E blues | distorted guitar riff, rock drums |
| 06 | 06-confetti-sky | Confetti Sky | pop synth | 118 | G major | bright saw chorus + pad |
| 07 | 07-slow-goodbye | Slow Goodbye | ballad | 62 | A minor | long string + vocal notes, half-time |
| 08 | 08-monsoon-raag | Monsoon Raag | Bollywood-scale | 100 | D Bhairavi | pluck + vocal, flat 2nd/6th scale |
| 09 | 09-rainy-window | Rainy Window | lo-fi | 72 | F Lydian | soft piano chords + pad, dreamy |
| 10 | 10-crown-of-strings | Crown of Strings | orchestral | 110 | E harmonic minor | layered strings, densest constellation |

## Why these 10?

The matcher is only as good as the test that exercises it. The
tracks were chosen to differ along every axis the fingerprint
sees: tempo (62–140 BPM), scale (major / minor / pentatonic /
blues / Bhairavi / Lydian / harmonic minor), instrumentation
(saw / pluck / piano / bass / guitar / strings / vocal), drum
density (none → four-on-the-floor), and note length (eighths →
whole bars). Pairwise hash overlap between tracks is under 25%
of the smaller track's hash set (pinned by `test_synth.py`), so
a clip's votes land on its true track, not a neighbour.
