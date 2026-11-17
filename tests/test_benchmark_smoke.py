"""Smoke test for the benchmark script's logic on a small database."""

from echoprint import FingerprintDatabase, fingerprint_audio, identify_audio
from echoprint.audio import slice_clip


def test_benchmark_logic_on_small_db(small_db, track03_audio):
    clip = slice_clip(track03_audio, 1.0, 5.0)
    ident = identify_audio(clip, small_db)
    assert ident.matched
    assert ident.track_id == "03-empty-rooms"
    assert ident.aligned_score >= 5
    # Fingerprinting the same audio twice is deterministic.
    assert (fingerprint_audio(track03_audio)["hashes"]
            == fingerprint_audio(track03_audio)["hashes"])
