"""Shared fixtures: small synthetic signals and a tiny database.

Tests use short (6 s) synthesized tracks so the suite stays fast
while still exercising the real pipeline end to end.
"""

from __future__ import annotations

import numpy as np
import pytest

from echoprint import FingerprintDatabase, fingerprint_audio
from echoprint.audio import midi_to_freq
from echoprint.synth import track01, track03, track05


def melody_audio(midis, note_s: float = 0.3, sr: int = 22050) -> np.ndarray:
    """A simple plucked melody — deterministic, no randomness."""
    from echoprint.synth.instruments import pluck
    y = np.zeros(int(len(midis) * note_s * sr))
    for i, midi in enumerate(midis):
        note = pluck(midi_to_freq(midi), note_s, amp=0.5)
        start = int(i * note_s * sr)
        y[start:start + len(note)] += note
    return y


@pytest.fixture(scope="session")
def tone_melody():
    return melody_audio([69, 72, 76, 79, 76, 72, 69, 64] * 3)


@pytest.fixture(scope="session")
def other_melody():
    return melody_audio([62, 65, 69, 72, 69, 65, 62, 57] * 3)


@pytest.fixture(scope="session")
def small_db():
    """A 3-track database built from short synthesized tracks."""
    db = FingerprintDatabase()
    for tid, builder in (("03-empty-rooms", track03.build_track),
                         ("01-neon-freeway", track01.build_track),
                         ("05-garage-door", track05.build_track)):
        y = builder(duration_s=6.0)
        fp = fingerprint_audio(y)
        db.add_track(tid, fp["hashes"], title=tid, duration_s=6.0)
    return db


@pytest.fixture(scope="session")
def track03_audio():
    return track03.build_track(duration_s=6.0)
