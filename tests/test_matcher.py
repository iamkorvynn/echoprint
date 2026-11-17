"""Tests for the matcher — votes must pile up at one offset."""

from echoprint import fingerprint_audio
from echoprint.matcher import match_clip


def test_matcher_aligns_at_one_offset(tone_melody, small_db):
    # A clip cut from the middle of track 03 should vote overwhelmingly
    # for track 03 at a single offset.
    import numpy as np
    from echoprint.audio import slice_clip
    from echoprint.synth import track03
    y = track03.build_track(duration_s=6.0)
    clip = slice_clip(y, 1.0, 3.0)
    clip_hashes = fingerprint_audio(clip)["hashes"]
    result = match_clip(clip_hashes, small_db)
    ranked = result.ranked_tracks()
    assert ranked, "no track got any votes"
    winner, offset, score = ranked[0]
    assert winner == "03-empty-rooms"
    assert score >= 5
    # The offset should point ~1 s into the track (~43 STFT frames).
    assert abs(offset * 512 / 22050 - 1.0) < 0.5


def test_matcher_empty_clip_hashes(small_db):
    result = match_clip({}, small_db)
    assert result.total_shared == 0
    assert result.ranked_tracks() == []


def test_matcher_unknown_audio_gets_few_votes(small_db, other_melody):
    clip_hashes = fingerprint_audio(other_melody)["hashes"]
    result = match_clip(clip_hashes, small_db)
    ranked = result.ranked_tracks()
    if ranked:
        assert ranked[0][2] < 5  # no track piles up votes
