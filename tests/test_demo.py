"""Demo cases as tests: the four filmed outcomes, via the real library.

These mirror demo.py but run against the generated WAVs in tracks/
and demo_clips/, so a regression in the demo is caught by pytest.
"""

import os

import pytest

from echoprint import FingerprintDatabase, fingerprint_audio, identify_audio
from echoprint.audio import load_wav
from echoprint.utils import find_wavs, track_id_from_path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope="module")
def full_db():
    db = FingerprintDatabase()
    for path in find_wavs(os.path.join(ROOT, "tracks")):
        sr, y = load_wav(path)
        fp = fingerprint_audio(y, sr)
        db.add_track(track_id_from_path(path), fp["hashes"],
                     duration_s=len(y) / sr)
    return db


def _clip(name):
    _sr, y = load_wav(os.path.join(ROOT, "demo_clips", name))
    return y


def test_demo_clean_matches(full_db):
    ident = identify_audio(_clip("clean.wav"), full_db)
    assert ident.matched
    assert ident.track_id == "03-empty-rooms"


def test_demo_noisy_matches_with_lower_score(full_db):
    clean = identify_audio(_clip("clean.wav"), full_db)
    noisy = identify_audio(_clip("noisy.wav"), full_db)
    assert noisy.matched
    assert noisy.track_id == "03-empty-rooms"
    assert noisy.aligned_score < clean.aligned_score


def test_demo_sped_up_no_match(full_db):
    assert not identify_audio(_clip("sped-up.wav"), full_db).matched


def test_demo_unknown_no_match(full_db):
    assert not identify_audio(_clip("unknown.wav"), full_db).matched
