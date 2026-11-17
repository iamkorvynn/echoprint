"""EchoPrint configuration — every magic number in one place.

Tuning notes (measured, not guessed — see docs/PERFORMANCE.md):
* PEAK_FRACTION = 0.20: a spectrogram peak must reach 20% of the
  loudest log-magnitude in the clip. A percentile threshold fails badly
  under white noise (noise fills the low percentiles and drowns the
  real peaks); a fraction-of-max threshold keeps clean and noisy clips
  sharing ~80 hashes while sped-up audio shares 0.
* FANOUT = 5, MAX_DT_FRAMES = 40: each anchor peak pairs with the next
  5 peaks up to ~0.93 s ahead. Classic Wang (2003) fan-out.
"""

SAMPLE_RATE = 22050
NPERSEG = 2048          # STFT window length (samples) -> ~93 ms
NOVERLAP = 1536         # overlap -> hop of 512 samples (~23 ms)
HOP = NPERSEG - NOVERLAP
WINDOW = "hann"

# Peak picking: local maxima over this (freq, time) neighbourhood.
PEAK_NEIGHBOURHOOD = 11
# Peak must exceed this fraction of the max log-magnitude.
PEAK_FRACTION = 0.20

# Hashing: anchor + target peak pairs.
FANOUT = 5
MIN_DT_FRAMES = 1
MAX_DT_FRAMES = 40

# Matching: a track only counts as identified when at least this many
# hashes line up at one consistent time offset.
MIN_ALIGNED_SCORE = 5
# ... and the winner must beat the runner-up by at least this factor.
MIN_WINNER_RATIO = 2.0

DB_VERSION = 1
DEFAULT_DB_PATH = "echoprint.db.json"
