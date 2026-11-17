# Security policy

- **No secrets in this repo.** There are no API keys, tokens, or
  credentials anywhere in EchoPrint, and none are needed to run it.
  If you find something that looks like a credential, treat it as
  a bug and report it.
- **No network access at runtime.** Fingerprinting and identifying
  are fully offline. The only network use is `pip install` and
  `git push`.
- **No copyrighted audio.** The library is synthesized with NumPy.
  Do not add recordings you don't have the right to distribute.
- **WAV parsing:** files are read with `scipy.io.wavfile`, which
  does not execute embedded content. Still, only fingerprint audio
  from sources you trust — a malicious WAV is outside this
  project's threat model, but not worth inviting in.
