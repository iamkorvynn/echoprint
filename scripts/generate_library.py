"""Render the 10-track library to WAV files.

    python scripts/generate_library.py [--out tracks] [--duration 12]

All tracks are synthesized with NumPy — clearly labelled test
tones, not music. Deterministic: re-running produces identical
files (same samples, same hashes).
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from echoprint.audio import save_wav  # noqa: E402
from echoprint.synth.tracks import TRACKS  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the EchoPrint library.")
    parser.add_argument("--out", default="tracks")
    parser.add_argument("--duration", type=float, default=12.0)
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)
    for entry in TRACKS:
        y = entry["build"](duration_s=args.duration)
        path = os.path.join(args.out, entry["id"] + ".wav")
        save_wav(path, y)
        print(f"{entry['id']:<28} {entry['title']:<22} "
              f"{len(y) / 22050:.1f}s -> {path}")
    print(f"\n{len(TRACKS)} tracks written to {args.out}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
