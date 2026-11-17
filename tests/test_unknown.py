"""Unknown audio: anything not in the library must say "no match",
never guess a title."""

import numpy as np

from echoprint import identify_audio


def test_random_noise_no_match(small_db):
    rng = np.random.default_rng(0)
    noise = rng.normal(0, 0.3, size=22050 * 5)
    ident = identify_audio(noise, small_db)
    assert not ident.matched


def test_unrelated_melody_no_match(small_db, other_melody):
    ident = identify_audio(other_melody, small_db)
    assert not ident.matched


def test_pure_tone_no_match(small_db):
    tone = np.sin(2 * np.pi * 880 * np.arange(22050 * 5) / 22050) * 0.5
    ident = identify_audio(tone, small_db)
    assert not ident.matched
