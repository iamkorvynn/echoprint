"""Tests for scoring / the identification decision."""

from echoprint.matcher import MatchResult
from echoprint.scoring import confidence, decide
from collections import Counter


def test_confidence():
    assert confidence(10, 100) == 0.1
    assert confidence(0, 0) == 0.0
    assert confidence(5, 5) == 1.0


def test_decide_no_votes_is_no_match(small_db):
    result = MatchResult({}, total_shared=0, n_clip_hashes=10)
    ident = decide(result, small_db)
    assert not ident.matched
    assert "no hashes" in ident.reason


def test_decide_low_score_is_no_match(small_db):
    votes = {"03-empty-rooms": Counter({10: 3})}
    result = MatchResult(votes, total_shared=3, n_clip_hashes=50)
    ident = decide(result, small_db)
    assert not ident.matched
    assert "below the threshold" in ident.reason


def test_decide_ambiguous_is_no_match(small_db):
    votes = {"03-empty-rooms": Counter({10: 20}),
             "01-neon-freeway": Counter({5: 15})}
    result = MatchResult(votes, total_shared=35, n_clip_hashes=60)
    ident = decide(result, small_db)
    assert not ident.matched
    assert "ambiguous" in ident.reason


def test_decide_clear_winner_matches(small_db):
    votes = {"03-empty-rooms": Counter({10: 40}),
             "01-neon-freeway": Counter({5: 3})}
    result = MatchResult(votes, total_shared=43, n_clip_hashes=60)
    ident = decide(result, small_db)
    assert ident.matched
    assert ident.track_id == "03-empty-rooms"
    assert ident.aligned_score == 40
    assert ident.best_offset_seconds == 10 * 512 / 22050
