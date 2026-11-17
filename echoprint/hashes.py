"""Hashing — turning a constellation into lookup keys.

For each anchor peak, pair it with the next ``FANOUT`` peaks and
make one hash per pair::

    hash = (freq_anchor, freq_target, time_delta_in_frames)

A hash is deliberately *relative*: it stores frequencies and a time
difference, never an absolute time or volume. So the same 5 seconds
of audio cut from anywhere in a track produces the same hashes, and
the database can answer "which track, and at what offset?" by
looking up each hash and voting (see ``matcher.py``).

Hash determinism is a core guarantee: the same audio always yields
the same hashes, byte for byte. Tests pin this down.
"""

from __future__ import annotations

from . import config
from .peaks import Peak

__all__ = ["hashes_from_peaks", "hash_key", "parse_hash_key"]

#: A hash is (anchor freq bin, target freq bin, delta in STFT frames).
Hash = tuple[int, int, int]


def hashes_from_peaks(peaks: list[Peak],
                      fanout: int = config.FANOUT,
                      min_dt: int = config.MIN_DT_FRAMES,
                      max_dt: int = config.MAX_DT_FRAMES) -> dict[Hash, list[int]]:
    """Build ``{hash: [anchor_time_frame, ...]}`` from sorted peaks.

    Peaks must be sorted by time (``find_peaks`` already does this).
    Each anchor pairs with the next ``fanout`` peaks whose time
    delta is within ``[min_dt, max_dt]`` frames.
    """
    hashes: dict[Hash, list[int]] = {}
    n = len(peaks)
    for i in range(n):
        t1, f1 = peaks[i]
        for j in range(i + 1, min(n, i + 1 + fanout)):
            t2, f2 = peaks[j]
            dt = t2 - t1
            if dt < min_dt:
                continue
            if dt > max_dt:
                break  # peaks are time-sorted, later ones only get further
            hashes.setdefault((f1, f2, dt), []).append(t1)
    return hashes


def hash_key(h: Hash) -> str:
    """Serialisable form of a hash, for the JSON database."""
    return f"{h[0]},{h[1]},{h[2]}"


def parse_hash_key(key: str) -> Hash:
    """Inverse of ``hash_key``."""
    a, b, c = key.split(",")
    return (int(a), int(b), int(c))
