# Clean vs noisy vs sped-up — what changes in the constellation

The same 5 s of track 03, three ways. The constellation is what
the matcher actually sees, so this is the whole story:

- **Clean:** ~40 peaks. Every peak is a note of the piano melody
  or its harmonics. Hashes line up at one offset; aligned score 73.
- **Noisy (+ white noise std 0.08):** still ~40 peaks, in the same
  places — the noise is too quiet, bin by bin, to beat the 20%
  threshold. A few hashes are lost (score 56 instead of 73), but
  the offset bin still wins by a mile.
- **Sped-up (1.3×):** the peaks are still there in spirit, but
  every one has moved: frequencies × 1.3, time gaps ÷ 1.3. The
  hashes are all different, so 0 hashes are shared and the answer
  is "no match". The constellation *looks* similar if you squint;
  the hashes are not similar at all — which is the point of hashing
  exact (frequency, frequency, delta) triples.

Run `python scripts/plot_clips.py` to render the three
spectrograms and constellations side by side (plots/clips/).
