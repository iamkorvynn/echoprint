"""Match reports — one place that formats identification results
for the terminal, for JSON output, and for the demo script.
"""

from __future__ import annotations

import json

from . import config
from .scoring import Identification

__all__ = ["format_result", "result_to_dict"]


def result_to_dict(ident: Identification) -> dict:
    """JSON-serialisable form of an Identification."""
    return {
        "matched": ident.matched,
        "track_id": ident.track_id,
        "title": ident.title,
        "aligned_score": ident.aligned_score,
        "total_shared_hashes": ident.total_shared_hashes,
        "n_clip_hashes": ident.n_clip_hashes,
        "best_offset_seconds": ident.best_offset_seconds,
        "runner_up_track": ident.runner_up_track,
        "runner_up_score": ident.runner_up_score,
        "confidence": ident.confidence,
        "reason": ident.reason,
    }


def format_result(ident: Identification, clip_name: str = "clip",
                  top_n: int = 1) -> str:
    """Terminal report for one identification."""
    lines = [f"--- {clip_name} ---"]
    if ident.matched:
        lines.append(f"MATCH: {ident.title}  (id: {ident.track_id})")
    else:
        lines.append("NO MATCH — no track in the library fits this clip")
        if ident.track_id:
            lines.append(
                f"(closest was {ident.title} with aligned score "
                f"{ident.aligned_score})"
            )
    lines.append(ident.breakdown())
    if top_n > 1 and ident.ranked:
        lines.append("top candidates:")
        for rank, (tid, offset, score) in enumerate(ident.ranked[:top_n], 1):
            secs = round(offset * config.HOP / config.SAMPLE_RATE, 2)
            lines.append(f"  {rank}. {tid:<28} score {score:>4}  offset {secs:.2f}s")
    lines.append(f"why: {ident.reason}")
    return "\n".join(lines)


def format_result_json(ident: Identification) -> str:
    """One-line JSON report (for scripts / piping)."""
    return json.dumps(result_to_dict(ident))
