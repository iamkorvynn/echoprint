"""Make the demo clips: clean, noisy, sped-up, and unknown.

    python scripts/make_clips.py [--out demo_clips]

* clean  — 5 s from the middle of track 03 (Empty Rooms)
* noisy  — the same 5 s with white noise (std 0.08) added
* sped   — the same 5 s played 1.3x fast (resampled)
* unknown — 5 s of a melody that is in no track (different notes)

The sped-up clip is the honest failure: pitch + tempo shift
moves every peak, so the hashes never line up.
"""

from __future__ import annotations

import argparse
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from echoprint.audio import add_noise, load_wav, resample_linear, save_wav, slice_clip  # noqa: E402
from echoprint.synth.instruments import pluck  # noqa: E402
from echoprint.synth.tracks import get_track  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Make demo clips.")
    parser.add_argument("--out", default="demo_clips")
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)

    _sr, y = load_wav(os.path.join("tracks", "03-empty-rooms.wav"))
    clean = slice_clip(y, start_s=3.0, duration_s=5.0)
    save_wav(os.path.join(args.out, "clean.wav"), clean)
    print("clean.wav : 5s from the middle of 03-empty-rooms")

    noisy = add_noise(clean, std=0.08, seed=42)
    save_wav(os.path.join(args.out, "noisy.wav"), noisy)
    print("noisy.wav : same clip + white noise (std 0.08)")

    sped = resample_linear(clean, 1.3)
    save_wav(os.path.join(args.out, "sped-up.wav"), sped)
    print("sped-up.wav: same clip at 1.3x speed (shorter, higher pitch)")

    # Unknown: a melody in a key/scale no library track uses (F# minor,
    # notes deliberately off the library's grids).
    rng_notes = [78, 81, 85, 83, 80, 78, 76, 73, 76, 78, 81, 85, 84, 81, 78, 76]
    unknown = np.zeros(int(5.0 * 22050))
    t = 0
    for midi in rng_notes:
        freq = 440.0 * (2 ** ((midi - 69) / 12))
        note = pluck(freq, 0.3, amp=0.5)
        start = int(t * 22050)
        unknown[start:start + len(note)] += note
        t += 0.3
    save_wav(os.path.join(args.out, "unknown.wav"), unknown)
    print("unknown.wav: 5s of a melody from no track in the library")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
