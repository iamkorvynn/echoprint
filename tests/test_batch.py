"""Tests for `echoprint batch`."""

from echoprint.audio import save_wav, slice_clip
from echoprint.cli import main


def test_batch_identifies_all_clips(tmp_path, track03_audio, other_melody,
                                    capsys):
    lib = tmp_path / "lib"
    lib.mkdir()
    save_wav(str(lib / "03-empty-rooms.wav"), track03_audio)
    db = tmp_path / "db.json"
    assert main(["fingerprint", str(lib), "--db", str(db)]) == 0
    capsys.readouterr()

    clips = tmp_path / "clips"
    clips.mkdir()
    save_wav(str(clips / "clean.wav"), slice_clip(track03_audio, 1.0, 5.0))
    save_wav(str(clips / "unknown.wav"), other_melody)
    assert main(["batch", str(clips), "--db", str(db)]) == 0
    out = capsys.readouterr().out
    assert "clean.wav" in out and "MATCH" in out
    assert "unknown.wav" in out and "NO MATCH" in out
    assert "1/2 clips matched" in out


def test_batch_empty_dir(tmp_path):
    assert main(["batch", str(tmp_path)]) == 2
