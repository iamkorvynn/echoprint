"""Tests for hashing — determinism is the core guarantee."""

from echoprint.constellation import constellation_from_audio
from echoprint.hashes import hash_key, hashes_from_peaks, parse_hash_key


def test_hash_determinism(tone_melody):
    peaks, _ = constellation_from_audio(tone_melody)
    h1 = hashes_from_peaks(peaks)
    h2 = hashes_from_peaks(peaks)
    assert h1 == h2
    # Same audio fingerprinted twice gives identical hashes.
    peaks2, _ = constellation_from_audio(tone_melody)
    assert hashes_from_peaks(peaks2) == h1


def test_hash_key_roundtrip():
    h = (41, 87, 12)
    assert parse_hash_key(hash_key(h)) == h


def test_empty_peaks_give_no_hashes():
    assert hashes_from_peaks([]) == {}


def test_fanout_limits_pairs():
    # 20 peaks in a row: anchor 0 pairs with at most FANOUT later peaks.
    peaks = [(t, 10 + t) for t in range(20)]
    hashes = hashes_from_peaks(peaks, fanout=5)
    anchor0 = [h for h, times in hashes.items() if 0 in times]
    assert len(anchor0) <= 5


def test_time_delta_bounds():
    peaks = [(0, 10), (1, 20), (100, 30)]
    hashes = hashes_from_peaks(peaks, min_dt=1, max_dt=40)
    assert (10, 20, 1) in hashes
    assert (10, 30, 100) not in hashes  # dt 100 > max
    assert all(1 <= h[2] <= 40 for h in hashes)
