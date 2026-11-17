"""Tests for the fingerprint database (build / save / load / remove)."""

import pytest

from echoprint import FingerprintDatabase, fingerprint_audio
from echoprint.errors import DatabaseError


def test_add_and_lookup(tone_melody):
    db = FingerprintDatabase()
    fp = fingerprint_audio(tone_melody)
    n = db.add_track("test-track", fp["hashes"], title="Test", duration_s=7.2)
    assert n > 0
    assert "test-track" in db
    assert len(db) == 1
    some_hash = next(iter(fp["hashes"]))
    assert ("test-track", fp["hashes"][some_hash][0]) in db.lookup(some_hash)
    assert db.lookup((9999, 9999, 39)) == []


def test_save_load_roundtrip(tmp_path, tone_melody):
    db = FingerprintDatabase()
    fp = fingerprint_audio(tone_melody)
    db.add_track("test-track", fp["hashes"], title="Test", duration_s=7.2)
    path = tmp_path / "db.json"
    db.save(str(path))
    db2 = FingerprintDatabase.load(str(path))
    assert db2.tracks == db.tracks
    assert db2.hashes == db.hashes
    assert db2.stats()["n_unique_hashes"] == db.stats()["n_unique_hashes"]


def test_load_missing_raises(tmp_path):
    with pytest.raises(DatabaseError):
        FingerprintDatabase.load(str(tmp_path / "nope.json"))


def test_remove_track(tone_melody, other_melody):
    db = FingerprintDatabase()
    for tid, y in (("a", tone_melody), ("b", other_melody)):
        db.add_track(tid, fingerprint_audio(y)["hashes"])
    assert db.remove_track("a") is True
    assert "a" not in db
    assert db.remove_track("a") is False
    assert len(db) == 1


def test_stats_counts(tone_melody):
    db = FingerprintDatabase()
    db.add_track("t", fingerprint_audio(tone_melody)["hashes"])
    stats = db.stats()
    assert stats["n_tracks"] == 1
    assert stats["n_unique_hashes"] > 0
    assert stats["n_hash_entries"] >= stats["n_unique_hashes"]
