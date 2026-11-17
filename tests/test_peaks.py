"""Tests for peak picking (the constellation)."""

import numpy as np

from echoprint.peaks import find_peaks, peak_stats
from echoprint.stft import log_spectrogram


def test_peaks_sorted_by_time(tone_melody):
    _f, _t, log_mag = log_spectrogram(tone_melody)
    peaks = find_peaks(log_mag)
    times = [p[0] for p in peaks]
    assert times == sorted(times)
    assert len(peaks) > 0


def test_peaks_deterministic(tone_melody):
    _f, _t, log_mag = log_spectrogram(tone_melody)
    assert find_peaks(log_mag) == find_peaks(log_mag)


def test_silence_has_no_peaks():
    _f, _t, log_mag = log_spectrogram(np.zeros(22050))
    assert find_peaks(log_mag) == []


def test_tone_has_few_peaks():
    y = np.sin(2 * np.pi * 440 * np.arange(22050 * 2) / 22050) * 0.5
    _f, _t, log_mag = log_spectrogram(y)
    peaks = find_peaks(log_mag)
    # A pure tone is basically one frequency: a handful of peaks, not hundreds.
    assert 0 < len(peaks) < 100
    freq_bins = {p[1] for p in peaks}
    assert min(freq_bins) <= 41 <= max(freq_bins)  # 440 Hz -> bin ~41


def test_peak_stats(tone_melody):
    _f, _t, log_mag = log_spectrogram(tone_melody)
    peaks = find_peaks(log_mag)
    stats = peak_stats(peaks, log_mag.shape[1], log_mag.shape[0])
    assert stats["count"] == len(peaks)
    assert stats["per_second"] > 0
