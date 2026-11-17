"""Timing helper — how long each stage takes (for stats / benchmarks)."""

from __future__ import annotations

import time
from contextlib import contextmanager

__all__ = ["Timer", "timed"]


class Timer:
    """Collect wall-clock timings under named labels."""

    def __init__(self) -> None:
        self.times: dict[str, float] = {}

    @contextmanager
    def time(self, label: str):
        start = time.perf_counter()
        try:
            yield
        finally:
            self.times[label] = self.times.get(label, 0.0) + (
                time.perf_counter() - start
            )

    def report(self) -> str:
        total = sum(self.times.values())
        lines = [f"  {label:<14} {t * 1000:7.1f} ms" for label, t in self.times.items()]
        lines.append(f"  {'TOTAL':<14} {total * 1000:7.1f} ms")
        return "\n".join(lines)


@contextmanager
def timed(label: str, store: dict):
    """One-shot version: ``with timed('stft', d): ...`` fills ``d``."""
    start = time.perf_counter()
    try:
        yield
    finally:
        store[label] = time.perf_counter() - start
