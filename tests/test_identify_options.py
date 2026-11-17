"""Tests for the identify options: --top candidates and --min-score."""

from echoprint import identify_audio
from echoprint.audio import slice_clip
from echoprint.report import format_result


def test_min_score_override_can_reject(small_db, track03_audio):
    clip = slice_clip(track03_audio, 1.0, 5.0)
    assert identify_audio(clip, small_db).matched
    # A threshold above the real score must turn a match into no-match.
    assert not identify_audio(clip, small_db, min_score=10_000).matched


def test_min_score_override_reason_names_threshold(small_db, track03_audio):
    clip = slice_clip(track03_audio, 1.0, 5.0)
    ident = identify_audio(clip, small_db, min_score=10_000)
    assert "10000" in ident.reason


def test_top_candidates_listed(small_db, track03_audio):
    clip = slice_clip(track03_audio, 1.0, 5.0)
    ident = identify_audio(clip, small_db)
    text = format_result(ident, top_n=3)
    assert "top candidates:" in text
    assert "03-empty-rooms" in text


def test_top_one_hides_candidate_list(small_db, track03_audio):
    clip = slice_clip(track03_audio, 1.0, 5.0)
    ident = identify_audio(clip, small_db)
    assert "top candidates:" not in format_result(ident, top_n=1)
