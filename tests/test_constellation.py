"""Tests for the constellation helpers."""

from echoprint.constellation import (constellation_density,
                                     constellation_from_audio)


def test_constellation_from_audio(tone_melody):
    peaks, log_mag = constellation_from_audio(tone_melody)
    assert len(peaks) > 0
    assert log_mag.shape[0] == 1025
    density = constellation_density(peaks, len(tone_melody) / 22050)
    assert 1 < density < 200


def test_density_zero_for_silence():
    assert constellation_density([], 5.0) == 0.0
    assert constellation_density([], 0.0) == 0.0
