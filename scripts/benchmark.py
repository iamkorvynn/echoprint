"""Benchmark: fingerprint + identify every track's middle 5 s.

    python scripts/benchmark.py [--db echoprint.db.json]

Prints a table: per-track peak count, hash count, fingerprint time,
identify time, and whether the middle clip identifies correctly.
Used to keep the PERFORMANCE doc honest.
"""

from __future__ import annotations

import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from echoprint import FingerprintDatabase, fingerprint_audio, identify_audio  # noqa: E402
from echoprint.audio import load_wav, slice_clip  # noqa: E402
from echoprint.utils import find_wavs, track_id_from_path  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark EchoPrint.")
    parser.add_argument("--db", default="echoprint.db.json")
    args = parser.parse_args()
    db = FingerprintDatabase.load(args.db)
    print(f"{'track':<28} {'peaks':>6} {'hashes':>7} {'fp ms':>7} "
          f"{'id ms':>7}  result")
    n_ok = 0
    for path in find_wavs("tracks"):
        tid = track_id_from_path(path)
        sr, y = load_wav(path)
        t0 = time.perf_counter()
        fp = fingerprint_audio(y, sr)
        fp_ms = (time.perf_counter() - t0) * 1000
        clip = slice_clip(y, 3.0, 5.0)
        t0 = time.perf_counter()
        ident = identify_audio(clip, db)
        id_ms = (time.perf_counter() - t0) * 1000
        ok = ident.matched and ident.track_id == tid
        n_ok += ok
        print(f"{tid:<28} {len(fp['peaks']):>6} {len(fp['hashes']):>7} "
              f"{fp_ms:>7.1f} {id_ms:>7.1f}  "
              f"{'OK ' + str(ident.aligned_score) if ok else 'FAIL'}")
    print(f"\n{n_ok}/10 middle clips identified correctly.")
    return 0 if n_ok == 10 else 1


if __name__ == "__main__":
    raise SystemExit(main())
