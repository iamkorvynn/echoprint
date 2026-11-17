"""Render spectrogram + constellation PNGs for every library track.

    python scripts/plot_all.py [--out plots]

Used by the README and by `echoprint show --plots`.
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from echoprint.show import show_track  # noqa: E402
from echoprint.utils import find_wavs  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Plot every track.")
    parser.add_argument("--out", default="plots")
    args = parser.parse_args()
    for path in find_wavs("tracks"):
        print(f"plotting {os.path.basename(path)} ...")
        show_track(path, out_dir=args.out)
    print(f"\nplots in {args.out}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
