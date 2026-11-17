"""Tests for match reports (terminal + JSON)."""

import json

from echoprint import identify_audio
from echoprint.audio import slice_clip
from echoprint.report import format_result, format_result_json, result_to_dict


def test_format_result_match(small_db, track03_audio):
    clip = slice_clip(track03_audio, 1.0, 5.0)
    ident = identify_audio(clip, small_db)
    text = format_result(ident, clip_name="clip.wav")
    assert "MATCH" in text
    assert "03-empty-rooms" in text
    assert "why:" in text


def test_format_result_no_match(small_db, other_melody):
    ident = identify_audio(other_melody, small_db)
    text = format_result(ident, clip_name="unknown.wav")
    assert "NO MATCH" in text


def test_result_to_dict_json_serialisable(small_db, track03_audio):
    clip = slice_clip(track03_audio, 1.0, 5.0)
    ident = identify_audio(clip, small_db)
    d = result_to_dict(ident)
    assert json.loads(json.dumps(d)) == d
    assert d["matched"] is True
    assert format_result_json(ident).startswith("{")
