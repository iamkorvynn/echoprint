"""Tests for the synthesizer: all 10 tracks build, sound different,
and are deterministic."""

import numpy as np

from echoprint import fingerprint_audio
from echoprint.synth.tracks import TRACKS


def test_all_tracks_build_and_are_audible():
    for entry in TRACKS:
        y = entry["build"](duration_s=6.0)
        assert len(y) == 6 * 22050
        assert np.max(np.abs(y)) > 0.1, entry["id"]
        assert np.isfinite(y).all()


def test_tracks_are_deterministic():
    for entry in TRACKS:
        a = entry["build"](duration_s=6.0)
        b = entry["build"](duration_s=6.0)
        assert np.array_equal(a, b), entry["id"]


def test_tracks_are_distinct():
    # Fingerprint hashes of different tracks barely overlap.
    fps = {e["id"]: fingerprint_audio(e["build"](duration_s=6.0))["hashes"]
           for e in TRACKS}
    ids = list(fps)
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            shared = len(set(fps[ids[i]]) & set(fps[ids[j]]))
            mine = min(len(fps[ids[i]]), len(fps[ids[j]]))
            assert shared < 0.25 * mine, (ids[i], ids[j], shared, mine)


def test_registry_has_ten_tracks():
    assert len(TRACKS) == 10
    assert len({t["id"] for t in TRACKS}) == 10
    assert all(t["title"] and t["genre"] for t in TRACKS)
