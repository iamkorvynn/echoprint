"""Plot the demo clips' spectrograms + constellations side by side.

    python scripts/plot_clips.py [--out plots/clips]

Renders clean / noisy / sped-up / unknown so the COMPARISON doc's
claim ("same peaks, moved peaks") can be checked by eye.
"""

from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from echoprint.show import show_track  # noqa: E402
from echoprint.utils import find_wavs  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Plot the demo clips.")
    parser.add_argument("--out", default="plots/clips")
    args = parser.parse_args()
    for path in find_wavs("demo_clips"):
        print(f"plotting {os.path.basename(path)} ...")
        show_track(path, out_dir=args.out)
    print(f"\nclip plots in {args.out}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
