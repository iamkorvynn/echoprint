"""Minimal example: identify one clip against the database.

Run from the repo root after fingerprinting:

    python examples/fingerprint_example.py
    python examples/identify_example.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from echoprint import FingerprintDatabase, identify_audio, load_wav  # noqa: E402
from echoprint.report import format_result  # noqa: E402

db = FingerprintDatabase.load("echoprint.db.json")
_sr, clip = load_wav("demo_clips/clean.wav")
ident = identify_audio(clip, db)
print(format_result(ident, clip_name="clean.wav", top_n=3))
