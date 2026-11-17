"""End-to-end identification tests: a 5 s clip from the middle
of a track must identify it; unknown audio must not match."""

from echoprint import identify_audio
from echoprint.audio import slice_clip
from echoprint.synth import track03


def test_middle_clip_identifies(small_db, track03_audio):
    clip = slice_clip(track03_audio, 1.0, 5.0)
    ident = identify_audio(clip, small_db)
    assert ident.matched, ident.reason
    assert ident.track_id == "03-empty-rooms"
    assert ident.aligned_score >= 5


def test_clip_from_start_identifies(small_db, track03_audio):
    clip = slice_clip(track03_audio, 0.0, 5.0)
    ident = identify_audio(clip, small_db)
    assert ident.matched
    assert ident.track_id == "03-empty-rooms"


def test_unknown_audio_no_match(small_db, other_melody):
    ident = identify_audio(other_melody, small_db)
    assert not ident.matched
    assert ident.track_id is None or ident.aligned_score < 5


def test_identification_breakdown_mentions_score(small_db, track03_audio):
    clip = slice_clip(track03_audio, 1.0, 5.0)
    ident = identify_audio(clip, small_db)
    text = ident.breakdown()
    assert "aligned score" in text
    assert "confidence" in text
