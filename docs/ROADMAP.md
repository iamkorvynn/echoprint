# Roadmap

Things v1 deliberately does not do, in rough order of value:

1. **Tempo-invariant hashes.** Hash frequency *ratios* instead of
   absolute bins and normalise time deltas, so a slightly sped-up
   or slowed-down clip still matches. The honest no-match for 1.3×
   would become a match for small shifts (1.05–1.1×) while big
   shifts still fail.
2. **A real database.** SQLite or a key-value store behind the
   `FingerprintDatabase` interface, so the library can grow past
   dozens of tracks without the JSON file getting silly.
3. **Microphone / live listening.** Record a few seconds from the
   mic and identify it — the use case the whole method exists for.
4. **More formats.** MP3/FLAC input via a decoder, instead of WAV only.
5. **Cover tolerance.** Chroma-based features alongside the
   constellation, so a different performance of the same song has
   a chance (a much harder problem — listed last on purpose).
6. **Batch fingerprinting progress + parallel hashing** for large
   libraries (multiprocessing over tracks).

Non-goals: identifying songs from a couple of notes, Shazam-scale
catalogues, or anything that needs copyrighted audio in this repo.
