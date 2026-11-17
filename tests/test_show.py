"""Tests for `echoprint show`."""

from echoprint.audio import save_wav
from echoprint.show import show_track


def test_show_track_returns_stats(tmp_path, track03_audio, capsys):
    path = tmp_path / "track.wav"
    save_wav(str(path), track03_audio)
    stats = show_track(str(path))
    assert stats["count"] > 0
    assert stats["n_hashes"] > 0
    assert stats["duration_s"] == 6.0
    out = capsys.readouterr().out
    assert "peaks" in out
    assert "constellation" in out


def test_show_track_writes_plots(tmp_path, track03_audio):
    import os
    path = tmp_path / "track.wav"
    save_wav(str(path), track03_audio)
    stats = show_track(str(path), out_dir=str(tmp_path / "plots"))
    assert os.path.exists(stats["spectrogram_png"])
    assert os.path.exists(stats["constellation_png"])
