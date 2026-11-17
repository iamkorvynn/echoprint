"""Minimal example: show a track's spectrogram + constellation.

Run from the repo root:

    python examples/show_example.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from echoprint.show import show_track  # noqa: E402

stats = show_track("tracks/03-empty-rooms.wav", out_dir="plots")
print(f"\n{stats['count']} peaks, {stats['n_hashes']} unique hashes")
