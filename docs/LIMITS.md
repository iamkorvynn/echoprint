# Honest limits

What EchoPrint v1 cannot do, stated plainly so nobody is surprised.

## Tempo / pitch changes break it

Speed a clip up or slow it down and the hashes change (frequencies
shift, time deltas change). Even 1.1× is enough. The demo proves
this deliberately. A real-world fix would need tempo-invariant
hashes (frequency ratios, normalised deltas) — not implemented.

## Tiny library

10 tracks × 12 s. The method scales (Shazam's database is a hash
table too), but this repo proves the algorithm, it doesn't ship a
catalogue. Adding real music would need licensing and a real store.

## Noise lowers the score

Moderate white noise (std 0.08) still matches with a lower score.
Heavy noise, a loud room, or a phone held far from a speaker can
push a genuine match below the 5-hash threshold — and then the
answer is "no match", not a guess.

## Short clips

Under ~2 s there are too few hashes to clear the threshold
reliably. 5 s is the demo's sweet spot; 3 s usually still works.

## Mono WAV only

Input is WAV at 22 050 Hz (other rates are linearly resampled,
which is crude but fine for a demo). No MP3/FLAC, no streaming,
no microphone input in v1.

## No cover versions

A different performance of the same song is a different
constellation. EchoPrint recognises *recordings*, not songs.

## Speed

Fingerprinting is ~real-time on a laptop for the library sizes
here (see PERFORMANCE.md). A million-track database would need
an indexed store and is out of scope.
