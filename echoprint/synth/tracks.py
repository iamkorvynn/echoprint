"""The 10-track library registry.

Every track is synthesized from scratch with NumPy — no
copyrighted music, no samples. Each entry names its builder
module, so ``scripts/generate_library.py`` can render the whole
library, and tests can import any single track.
"""

from __future__ import annotations

from . import (track01, track02, track03, track04, track05, track06,
               track07, track08, track09, track10)

__all__ = ["TRACKS", "TRACK_IDS", "get_track"]

TRACKS = [
    {"id": "01-neon-freeway", "title": track01.TITLE, "genre": track01.GENRE,
     "bpm": track01.BPM, "description": track01.DESCRIPTION,
     "build": track01.build_track},
    {"id": "02-porch-light", "title": track02.TITLE, "genre": track02.GENRE,
     "bpm": track02.BPM, "description": track02.DESCRIPTION,
     "build": track02.build_track},
    {"id": "03-empty-rooms", "title": track03.TITLE, "genre": track03.GENRE,
     "bpm": track03.BPM, "description": track03.DESCRIPTION,
     "build": track03.build_track},
    {"id": "04-low-end-theory-club", "title": track04.TITLE, "genre": track04.GENRE,
     "bpm": track04.BPM, "description": track04.DESCRIPTION,
     "build": track04.build_track},
    {"id": "05-garage-door", "title": track05.TITLE, "genre": track05.GENRE,
     "bpm": track05.BPM, "description": track05.DESCRIPTION,
     "build": track05.build_track},
    {"id": "06-confetti-sky", "title": track06.TITLE, "genre": track06.GENRE,
     "bpm": track06.BPM, "description": track06.DESCRIPTION,
     "build": track06.build_track},
    {"id": "07-slow-goodbye", "title": track07.TITLE, "genre": track07.GENRE,
     "bpm": track07.BPM, "description": track07.DESCRIPTION,
     "build": track07.build_track},
    {"id": "08-monsoon-raag", "title": track08.TITLE, "genre": track08.GENRE,
     "bpm": track08.BPM, "description": track08.DESCRIPTION,
     "build": track08.build_track},
    {"id": "09-rainy-window", "title": track09.TITLE, "genre": track09.GENRE,
     "bpm": track09.BPM, "description": track09.DESCRIPTION,
     "build": track09.build_track},
    {"id": "10-crown-of-strings", "title": track10.TITLE, "genre": track10.GENRE,
     "bpm": track10.BPM, "description": track10.DESCRIPTION,
     "build": track10.build_track},
]

TRACK_IDS = [t["id"] for t in TRACKS]


def get_track(track_id: str) -> dict:
    """Registry entry for ``track_id`` (KeyError if unknown)."""
    for entry in TRACKS:
        if entry["id"] == track_id:
            return entry
    raise KeyError(f"unknown track id {track_id!r}")
