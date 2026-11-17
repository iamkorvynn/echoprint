"""Noise robustness: a noisy clip still matches, with a lower score."""

from echoprint import identify_audio
from echoprint.audio import add_noise, slice_clip


def test_noisy_clip_still_matches(small_db, track03_audio):
    clean = slice_clip(track03_audio, 1.0, 5.0)
    noisy = add_noise(clean, std=0.08, seed=42)
    ident_clean = identify_audio(clean, small_db)
    ident_noisy = identify_audio(noisy, small_db)
    assert ident_noisy.matched, ident_noisy.reason
    assert ident_noisy.track_id == "03-empty-rooms"
    assert ident_noisy.aligned_score <= ident_clean.aligned_score


def test_heavy_noise_degrades_gracefully(small_db, track03_audio):
    # Very heavy noise (std 0.2) may or may not match — but it must
    # never confidently match the WRONG track.
    clean = slice_clip(track03_audio, 1.0, 5.0)
    noisy = add_noise(clean, std=0.2, seed=1)
    ident = identify_audio(noisy, small_db)
    if ident.matched:
        assert ident.track_id == "03-empty-rooms"
