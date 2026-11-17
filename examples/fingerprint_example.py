"""Minimal example: fingerprint a library, then identify a clip.

Run from the repo root after generating the library:

    python scripts/generate_library.py
    python examples/fingerprint_example.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from echoprint import FingerprintDatabase, fingerprint_audio  # noqa: E402
from echoprint.audio import load_wav  # noqa: E402
from echoprint.utils import find_wavs, track_id_from_path  # noqa: E402

db = FingerprintDatabase()
for path in find_wavs("tracks"):
    sr, y = load_wav(path)
    fp = fingerprint_audio(y, sr)
    db.add_track(track_id_from_path(path), fp["hashes"])
db.save("echoprint.db.json")
print(f"fingerprinted {len(db)} tracks -> echoprint.db.json")
