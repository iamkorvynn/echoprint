# Glossary

- **STFT (short-time Fourier transform):** the Fourier transform
  applied to short sliding windows of audio — "what frequencies
  are present right now, and how loud are they?"
- **Spectrogram:** the STFT drawn as a picture (time × frequency,
  brightness = loudness).
- **Constellation map:** the set of spectrogram peaks — the bright
  dots that survive peak picking. A song's fingerprint starts here.
- **Peak:** a time-frequency bin louder than its neighbours and
  above the loudness threshold.
- **Anchor peak:** the first peak of a hash pair.
- **Target peak:** the second peak of a hash pair.
- **Hash:** `(anchor frequency, target frequency, time delta)` —
  one lookup key. A 5 s clip produces ~100–200 of them.
- **Fan-out:** how many later peaks each anchor pairs with (5 here).
- **Offset:** `database time − clip time` for a matching hash. True
  matches all agree on one offset: where the clip starts in the track.
- **Aligned score:** the number of hashes voting for the best
  (track, offset) bin. The matcher's headline number.
- **Confidence:** aligned score ÷ clip hash count.
- **Runner-up:** the second-best track's aligned score. The winner
  must beat it 2× for a match to be declared.
