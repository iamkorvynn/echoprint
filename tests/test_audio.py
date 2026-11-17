"""Tests for audio I/O and helpers."""

import numpy as np
import pytest

from echoprint.audio import (add_noise, load_wav, midi_to_freq, note_name,
                             resample_linear, save_wav, slice_clip)
from echoprint.errors import AudioError


def test_save_load_roundtrip(tmp_path):
    y = np.sin(2 * np.pi * 440 * np.arange(22050) / 22050) * 0.5
    path = tmp_path / "tone.wav"
    save_wav(str(path), y)
    sr, back = load_wav(str(path))
    assert sr == 22050
    assert len(back) == len(y)
    assert np.allclose(back, y, atol=1 / 32767 + 1e-9)


def test_load_missing_file_raises():
    with pytest.raises(AudioError):
        load_wav("no-such-file.wav")


def test_load_silent_file_raises(tmp_path):
    path = tmp_path / "silent.wav"
    save_wav(str(path), np.zeros(22050))
    with pytest.raises(AudioError):
        load_wav(str(path))


def test_resample_faster_is_shorter_and_higher():
    y = np.sin(2 * np.pi * 440 * np.arange(22050) / 22050)
    sped = resample_linear(y, 2.0)
    assert len(sped) == len(y) // 2
    # Zero-crossing rate roughly doubles for a pure tone.
    zc = lambda a: int(np.sum(np.diff(np.sign(a)) != 0))
    assert zc(sped) > zc(y) * 0.8


def test_add_noise_is_seeded_and_deterministic():
    y = np.zeros(1000)
    a = add_noise(y, 0.1, seed=7)
    b = add_noise(y, 0.1, seed=7)
    c = add_noise(y, 0.1, seed=8)
    assert np.array_equal(a, b)
    assert not np.array_equal(a, c)


def test_slice_clip(tmp_path):
    y = np.arange(22050 * 4, dtype=float)
    clip = slice_clip(y, 1.0, 2.0)
    assert len(clip) == 22050 * 2
    assert clip[0] == 22050


def test_slice_clip_beyond_end_raises():
    with pytest.raises(AudioError):
        slice_clip(np.zeros(100), 5.0, 1.0)


def test_midi_to_freq_and_note_name():
    assert midi_to_freq(69) == pytest.approx(440.0)
    assert midi_to_freq(81) == pytest.approx(880.0)
    assert note_name(69) == "A4"
    assert note_name(60) == "C4"
