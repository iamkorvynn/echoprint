"""Tests for the STFT / spectrogram stage."""

import numpy as np

from echoprint import config
from echoprint.stft import (compute_stft, log_spectrogram,
                            magnitude_spectrogram)


def test_stft_shape(tone_melody):
    freqs, times, Z = compute_stft(tone_melody)
    assert Z.shape[0] == config.NPERSEG // 2 + 1  # 1025 freq bins
    assert Z.shape[1] == len(times)
    assert len(freqs) == Z.shape[0]
    # Frequency resolution ~10.8 Hz.
    assert abs(freqs[1] - freqs[0] - config.SAMPLE_RATE / config.NPERSEG) < 0.01


def test_pure_tone_peak_bin(tone_melody):
    # A 440 Hz tone's spectrogram should be brightest near bin 440/10.77.
    _f, _t, mag = magnitude_spectrogram(
        np.sin(2 * np.pi * 440 * np.arange(22050) / 22050))
    brightest_bin = int(np.argmax(mag.mean(axis=1)))
    assert abs(brightest_bin - 440 / (22050 / 2048)) <= 2


def test_log_spectrogram_nonnegative(tone_melody):
    _f, _t, log_mag = log_spectrogram(tone_melody)
    assert np.all(log_mag >= 0)
    assert np.isfinite(log_mag).all()
