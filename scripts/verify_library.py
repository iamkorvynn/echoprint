"""Verify the library: every track's middle 5 s must identify itself.

    python scripts/verify_library.py [--db echoprint.db.json]

Exits 0 only if all 10 tracks identify correctly, clean and noisy,
and sped-up versions of each do not match. A stricter check than
the demo (which only uses track 03).
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from echoprint import FingerprintDatabase, identify_audio  # noqa: E402
from echoprint.audio import add_noise, load_wav, resample_linear, slice_clip  # noqa: E402
from echoprint.utils import find_wavs, track_id_from_path  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the whole library.")
    parser.add_argument("--db", default="echoprint.db.json")
    args = parser.parse_args()
    db = FingerprintDatabase.load(args.db)
    failures = 0
    for path in find_wavs("tracks"):
        tid = track_id_from_path(path)
        _sr, y = load_wav(path)
        clip = slice_clip(y, 3.0, 5.0)
        checks = [
            ("clean", identify_audio(clip, db)),
            ("noisy", identify_audio(add_noise(clip, 0.08, seed=42), db)),
        ]
        for label, ident in checks:
            ok = ident.matched and ident.track_id == tid
            print(f"{tid:<28} {label:<6} {'OK ' + str(ident.aligned_score) if ok else 'FAIL'}")
            failures += not ok
        sped = identify_audio(resample_linear(clip, 1.3), db)
        ok = not sped.matched
        print(f"{tid:<28} {'sped':<6} {'OK (no match)' if ok else 'FAIL'}")
        failures += not ok
    print(f"\n{'ALL CHECKS PASSED' if failures == 0 else f'{failures} FAILURES'}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
