"""Per-track fingerprint statistics, printed as a table.

    python scripts/fingerprint_stats.py

For every library track: peaks, peaks/second, unique hashes,
hash entries per second, and the clean 5 s clip's aligned score.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from echoprint import FingerprintDatabase, fingerprint_audio, identify_audio  # noqa: E402
from echoprint.audio import load_wav, slice_clip  # noqa: E402
from echoprint.utils import find_wavs, track_id_from_path  # noqa: E402


def main() -> int:
    db = FingerprintDatabase.load("echoprint.db.json")
    print(f"{'track':<28} {'peaks':>6} {'peaks/s':>8} {'hashes':>7} "
          f"{'hashes/s':>9} {'score':>6}")
    for path in find_wavs("tracks"):
        tid = track_id_from_path(path)
        _sr, y = load_wav(path)
        fp = fingerprint_audio(y)
        dur = len(y) / 22050
        clip = slice_clip(y, 3.0, 5.0)
        ident = identify_audio(clip, db)
        print(f"{tid:<28} {len(fp['peaks']):>6} "
              f"{len(fp['peaks']) / dur:>8.1f} {len(fp['hashes']):>7} "
              f"{len(fp['hashes']) / dur:>9.1f} {ident.aligned_score:>6}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
