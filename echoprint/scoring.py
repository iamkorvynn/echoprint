"""Scoring — turning vote counts into a yes/no answer with a reason.

EchoPrint never guesses a title. A clip is identified only when:
1. the winner's aligned score (hashes agreeing on one time offset)
   reaches ``MIN_ALIGNED_SCORE`` (5), and
2. the winner beats the runner-up by ``MIN_WINNER_RATIO`` (2x).

Anything else is an honest "no match": too few hashes lined up, or
two tracks tied. The breakdown (shared hashes, aligned score,
offset, confidence) is always reported so you can see *why*.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from . import config
from .matcher import MatchResult

__all__ = ["Identification", "decide", "confidence"]


def confidence(aligned: int, n_clip_hashes: int) -> float:
    """Fraction of the clip's hashes that lined up at the best offset."""
    if n_clip_hashes <= 0:
        return 0.0
    return round(aligned / n_clip_hashes, 3)


@dataclass
class Identification:
    """The full, explainable answer to "what is this clip?"."""

    matched: bool
    track_id: str | None = None
    title: str | None = None
    aligned_score: int = 0
    total_shared_hashes: int = 0
    n_clip_hashes: int = 0
    best_offset_frames: int = 0
    best_offset_seconds: float = 0.0
    runner_up_score: int = 0
    runner_up_track: str | None = None
    reason: str = ""
    ranked: list = field(default_factory=list)

    @property
    def confidence(self) -> float:
        return confidence(self.aligned_score, self.n_clip_hashes)

    def breakdown(self) -> str:
        """Human-readable score breakdown (used by the CLI and demo)."""
        lines = [
            f"clip hashes:        {self.n_clip_hashes}",
            f"shared with library: {self.total_shared_hashes}",
            f"aligned score:      {self.aligned_score} hashes at one offset",
            f"offset in track:    {self.best_offset_seconds:.2f} s",
            f"runner-up:          {self.runner_up_track or '-'} "
            f"({self.runner_up_score})",
            f"confidence:         {self.confidence:.1%}",
        ]
        return "\n".join(lines)


def decide(result: MatchResult, db) -> Identification:
    """Apply the thresholds to a MatchResult and build an Identification."""
    ranked = result.ranked_tracks()
    if not ranked:
        return Identification(
            matched=False,
            total_shared_hashes=result.total_shared,
            n_clip_hashes=result.n_clip_hashes,
            reason="no hashes shared with any track in the library",
            ranked=[],
        )
    winner, offset, score = ranked[0]
    runner_up_track, _o, runner_score = ranked[1] if len(ranked) > 1 else (None, 0, 0)
    ident = Identification(
        matched=False,
        track_id=winner,
        title=db.tracks.get(winner, {}).get("title", winner),
        aligned_score=score,
        total_shared_hashes=result.total_shared,
        n_clip_hashes=result.n_clip_hashes,
        best_offset_frames=offset,
        best_offset_seconds=round(offset * config.HOP / config.SAMPLE_RATE, 3),
        runner_up_score=runner_score,
        runner_up_track=runner_up_track,
        ranked=ranked,
    )
    if score < config.MIN_ALIGNED_SCORE:
        ident.reason = (
            f"best aligned score {score} is below the threshold "
            f"{config.MIN_ALIGNED_SCORE} — too few hashes lined up"
        )
        return ident
    if runner_score > 0 and score < config.MIN_WINNER_RATIO * runner_score:
        ident.reason = (
            f"winner score {score} is not {config.MIN_WINNER_RATIO}x the "
            f"runner-up ({runner_up_track}, {runner_score}) — ambiguous"
        )
        return ident
    ident.matched = True
    ident.reason = f"{score} hashes agree on offset {ident.best_offset_seconds:.2f} s"
    return ident
