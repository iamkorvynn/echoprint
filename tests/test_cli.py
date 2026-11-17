"""Tests for the CLI end to end (fingerprint -> identify -> list)."""

import json
import subprocess
import sys

import pytest

from echoprint.audio import save_wav, slice_clip
from echoprint.cli import main


def _run(argv):
    return main(argv)


def test_cli_fingerprint_identify_list(tmp_path, track03_audio, capsys):
    lib = tmp_path / "lib"
    lib.mkdir()
    save_wav(str(lib / "03-empty-rooms.wav"), track03_audio)
    db = tmp_path / "db.json"
    assert _run(["fingerprint", str(lib), "--db", str(db)]) == 0
    assert db.exists()

    clip = tmp_path / "clip.wav"
    save_wav(str(clip), slice_clip(track03_audio, 1.0, 5.0))
    assert _run(["identify", str(clip), "--db", str(db)]) == 0
    out = capsys.readouterr().out
    assert "MATCH" in out
    assert "03-empty-rooms" in out

    assert _run(["list", "--db", str(db)]) == 0
    assert "03-empty-rooms" in capsys.readouterr().out

    assert _run(["stats", "--db", str(db)]) == 0
    assert "tracks" in capsys.readouterr().out


def test_cli_identify_json(tmp_path, track03_audio, capsys):
    lib = tmp_path / "lib"
    lib.mkdir()
    save_wav(str(lib / "03-empty-rooms.wav"), track03_audio)
    db = tmp_path / "db.json"
    _run(["fingerprint", str(lib), "--db", str(db)])
    capsys.readouterr()
    clip = tmp_path / "clip.wav"
    save_wav(str(clip), slice_clip(track03_audio, 1.0, 5.0))
    assert _run(["identify", str(clip), "--db", str(db), "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["matched"] is True
    assert payload["track_id"] == "03-empty-rooms"


def test_cli_fingerprint_empty_dir(tmp_path):
    assert _run(["fingerprint", str(tmp_path)]) == 2


def test_cli_identify_missing_db(tmp_path):
    clip = tmp_path / "clip.wav"
    save_wav(str(clip), track03_audio)
    assert _run(["identify", str(clip), "--db", str(tmp_path / "no.json")]) == 2


def test_cli_show(tmp_path, track03_audio, capsys):
    path = tmp_path / "track.wav"
    save_wav(str(path), track03_audio)
    assert _run(["show", str(path)]) == 0
    assert "peaks" in capsys.readouterr().out
