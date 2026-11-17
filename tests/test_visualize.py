"""Tests for the visualisation (the twist)."""

import os

from echoprint import fingerprint_audio
from echoprint.visualize import (ascii_constellation, ascii_spectrogram,
                                 plot_constellation, plot_spectrogram)


def test_ascii_spectrogram_has_content(tone_melody):
    fp = fingerprint_audio(tone_melody)
    art = ascii_spectrogram(fp["log_mag"])
    assert "freq" in art
    assert len(art.splitlines()) > 10
    assert any(ch in art for ch in "*#%@")


def test_ascii_constellation_has_stars(tone_melody):
    fp = fingerprint_audio(tone_melody)
    art = ascii_constellation(fp["peaks"], fp["log_mag"].shape)
    assert "*" in art


def test_plots_are_written(tmp_path, tone_melody):
    fp = fingerprint_audio(tone_melody)
    spec = plot_spectrogram(fp["log_mag"], str(tmp_path / "spec.png"))
    const = plot_constellation(fp["peaks"], fp["log_mag"].shape,
                               str(tmp_path / "const.png"))
    assert os.path.getsize(spec) > 1000
    assert os.path.getsize(const) > 1000
