# FAQ

**Is this Shazam?**
No. It's a clean-room implementation of the *published method*
behind Shazam (Wang 2003), written from scratch, with a new name,
new UI, and a synthesized test library. No Shazam code, branding,
or audio is used.

**Why does a sped-up song not match?**
Speeding audio shifts every frequency up and squeezes every time
gap, so every hash changes. The method matches *recordings* at
their original speed. See `docs/MATH.md` §6.

**Why does it say "no match" instead of guessing?**
Because a confident wrong answer is worse than an honest "I don't
know". The thresholds (≥5 hashes at one offset, ≥2× the runner-up)
exist so that unknown audio, noise, and sped-up clips all land in
"no match" instead of on a random track.

**Can I fingerprint my own music?**
Technically yes — drop WAVs in a folder and run `fingerprint` —
but only do that with audio you have the right to use. The repo
ships synthesized tracks precisely so nobody needs real music to
try it.

**How big can the library get?**
The JSON database is fine for tens of tracks. For thousands you'd
want SQLite or a key-value store behind the same interface (see
`docs/ARCHITECTURE.md`).

**Why 22 050 Hz?**
Half of CD quality, plenty for fingerprinting (human hearing tops
out ~20 kHz and most musical energy is below 11 kHz), and it keeps
the STFT cheap. Other sample rates are linearly resampled on load.

**Does it work on a phone recording of a song playing from a speaker?**
In principle — that's the use case the method was built for — but
v1 has no microphone input and was only tested on clean/noisy
synthesized clips. Room noise and speaker distortion lower the
score, same as added white noise.
