"""Matching — voting for the track whose hashes line up in time.

For every hash the clip shares with the database, each stored entry
votes for ``(track, offset)`` where ``offset = db_time - clip_time``.
If the clip really comes from that track, all its hashes agree on
ONE offset (the clip's position inside the track) and that bin
collects dozens of votes. Hashes from other tracks, or from noise,
scatter their votes across many offsets and never pile up.

The score for a track is the size of its biggest offset bin.
That single number is what ``identify`` reports and thresholds on.
"""

from __future__ import annotations

from collections import Counter, defaultdict

from .database import FingerprintDatabase
from .hashes import Hash

__all__ = ["match_clip", "MatchResult"]


class MatchResult:
    """Outcome of matching one clip against the database."""

    def __init__(self, votes: dict[str, Counter], total_shared: int,
                 n_clip_hashes: int):
        self.votes = votes              # track_id -> Counter[offset -> count]
        self.total_shared = total_shared  # hashes the clip shares with anyone
        self.n_clip_hashes = n_clip_hashes

    def best_offset(self, track_id: str) -> tuple[int, int]:
        """(offset, count) of the track's biggest vote bin, or (0, 0)."""
        counter = self.votes.get(track_id)
        if not counter:
            return (0, 0)
        offset, count = counter.most_common(1)[0]
        return (offset, count)

    def ranked_tracks(self) -> list[tuple[str, int, int]]:
        """[(track_id, best_offset, aligned_score)] best first."""
        ranked = [
            (tid, *self.best_offset(tid)) for tid in self.votes
        ]
        ranked.sort(key=lambda row: row[2], reverse=True)
        return ranked

    def runner_up_score(self, winner: str) -> int:
        """Best aligned score of any track other than ``winner``."""
        best = 0
        for tid, _offset, score in self.ranked_tracks():
            if tid != winner:
                best = max(best, score)
        return best


def match_clip(clip_hashes: dict[Hash, list[int]],
               db: FingerprintDatabase) -> MatchResult:
    """Vote every shared hash and return the per-track offset counts."""
    votes: dict[str, Counter] = defaultdict(Counter)
    total_shared = 0
    for h, clip_times in clip_hashes.items():
        entries = db.lookup(h)
        if not entries:
            continue
        total_shared += 1
        for track_id, db_time in entries:
            for clip_time in clip_times:
                votes[track_id][db_time - clip_time] += 1
    return MatchResult(dict(votes), total_shared, len(clip_hashes))
