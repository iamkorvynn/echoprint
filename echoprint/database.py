"""The fingerprint database — a hash table on disk.

Layout (JSON, human-inspectable)::

    {
      "version": 1,
      "tracks": {"track-id": {"title": ..., "duration_s": ..., "n_hashes": ...}},
      "hashes": {"f1,f2,dt": [["track-id", anchor_time_frame], ...]}
    }

JSON (not pickle) on purpose: a fingerprint DB you can open in a
text editor and grep is a better teaching artefact than a binary
blob, and the 10-track library is small enough that size does not
matter. A production system would use a real key-value store.
"""

from __future__ import annotations

import json
import os
from collections import defaultdict

from . import config
from .errors import DatabaseError
from .hashes import Hash, hash_key, parse_hash_key

__all__ = ["FingerprintDatabase"]


class FingerprintDatabase:
    """In-memory hash table with JSON persistence."""

    def __init__(self) -> None:
        self.tracks: dict[str, dict] = {}
        # hash -> list of (track_id, anchor time frame)
        self.hashes: dict[Hash, list[tuple[str, int]]] = defaultdict(list)

    # -- building ----------------------------------------------------
    def add_track(self, track_id: str, hashes: dict[Hash, list[int]],
                  title: str = "", duration_s: float = 0.0) -> int:
        """Index one track's hashes. Returns the number of hashes added."""
        n = 0
        for h, times in hashes.items():
            for t in times:
                self.hashes[h].append((track_id, t))
                n += 1
        self.tracks[track_id] = {
            "title": title or track_id,
            "duration_s": round(float(duration_s), 3),
            "n_hashes": n,
            "n_unique_hashes": len(hashes),
        }
        return n

    def remove_track(self, track_id: str) -> bool:
        """Remove a track and all its hash entries. Returns False if absent."""
        if track_id not in self.tracks:
            return False
        for h in list(self.hashes):
            kept = [e for e in self.hashes[h] if e[0] != track_id]
            if kept:
                self.hashes[h] = kept
            else:
                del self.hashes[h]
        del self.tracks[track_id]
        return True

    # -- lookup ------------------------------------------------------
    def lookup(self, h: Hash) -> list[tuple[str, int]]:
        """All (track_id, anchor time) entries stored under hash ``h``."""
        return list(self.hashes.get(h, []))

    def __contains__(self, track_id: str) -> bool:
        return track_id in self.tracks

    def __len__(self) -> int:
        return len(self.tracks)

    # -- stats -------------------------------------------------------
    def stats(self) -> dict:
        total_entries = sum(len(v) for v in self.hashes.values())
        return {
            "version": config.DB_VERSION,
            "n_tracks": len(self.tracks),
            "n_unique_hashes": len(self.hashes),
            "n_hash_entries": total_entries,
            "tracks": dict(self.tracks),
        }

    # -- persistence -------------------------------------------------
    def save(self, path: str) -> None:
        payload = {
            "version": config.DB_VERSION,
            "tracks": self.tracks,
            "hashes": {
                hash_key(h): [[tid, t] for tid, t in entries]
                for h, entries in self.hashes.items()
            },
        }
        tmp = path + ".tmp"
        try:
            with open(tmp, "w", encoding="utf-8") as fh:
                json.dump(payload, fh)
            os.replace(tmp, path)
        except OSError as exc:
            raise DatabaseError(f"could not save database to {path!r}: {exc}") from exc

    @classmethod
    def load(cls, path: str) -> "FingerprintDatabase":
        try:
            with open(path, encoding="utf-8") as fh:
                payload = json.load(fh)
        except FileNotFoundError as exc:
            raise DatabaseError(
                f"database {path!r} not found — run "
                f"`echoprint fingerprint <library-dir>` first"
            ) from exc
        except (OSError, json.JSONDecodeError) as exc:
            raise DatabaseError(f"could not load database {path!r}: {exc}") from exc
        db = cls()
        db.tracks = dict(payload.get("tracks", {}))
        for key, entries in payload.get("hashes", {}).items():
            db.hashes[parse_hash_key(key)] = [(tid, int(t)) for tid, t in entries]
        return db
