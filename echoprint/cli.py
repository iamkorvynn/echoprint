"""Command-line interface.

    echoprint fingerprint <library-dir> [--db PATH]   build the hash DB
    echoprint identify <clip.wav> [--db PATH] [--json]
    echoprint show <track.wav> [--plots DIR]
    echoprint list [--db PATH]                        tracks in the DB
    echoprint stats [--db PATH]                       DB statistics

Exit codes: 0 = ok (including an honest "no match"), 2 = usage /
bad file / missing database.
"""

from __future__ import annotations

import argparse
import os
import sys

from . import config
from .audio import load_wav
from .database import FingerprintDatabase
from .identify import fingerprint_audio, identify_audio
from .report import format_result, format_result_json
from .show import show_track
from .timing import Timer
from .utils import find_wavs, track_id_from_path

__all__ = ["main", "build_parser"]


def cmd_fingerprint(args) -> int:
    wavs = find_wavs(args.library_dir)
    if not wavs:
        print(f"no .wav files found in {args.library_dir!r}", file=sys.stderr)
        return 2
    db = FingerprintDatabase()
    timer = Timer()
    for path in wavs:
        track_id = track_id_from_path(path)
        with timer.time("load"):
            sr, y = load_wav(path)
        with timer.time("fingerprint"):
            fp = fingerprint_audio(y, sr)
        n = db.add_track(track_id, fp["hashes"],
                         title=track_id, duration_s=len(y) / sr)
        print(f"fingerprinted {track_id}: {len(fp['peaks'])} peaks, "
              f"{len(fp['hashes'])} unique hashes ({n} entries)")
    db.save(args.db)
    stats = db.stats()
    print(f"\nsaved {args.db}: {stats['n_tracks']} tracks, "
          f"{stats['n_unique_hashes']} unique hashes, "
          f"{stats['n_hash_entries']} entries")
    if args.verbose:
        print("timings (total across all tracks):")
        print(timer.report())
    return 0


def cmd_identify(args) -> int:
    db = FingerprintDatabase.load(args.db)
    sr, y = load_wav(args.clip)
    timer = Timer()
    with timer.time("identify"):
        ident = identify_audio(y, db, min_score=args.min_score)
    if args.json:
        print(format_result_json(ident))
    else:
        print(format_result(ident, clip_name=os.path.basename(args.clip),
                            top_n=args.top))
        if args.verbose:
            print(timer.report())
    return 0


def cmd_show(args) -> int:
    show_track(args.track, out_dir=args.plots)
    return 0


def cmd_list(args) -> int:
    db = FingerprintDatabase.load(args.db)
    if not db.tracks:
        print("(database is empty)")
        return 0
    for tid, meta in sorted(db.tracks.items()):
        print(f"{tid:<28} {meta['title']:<28} "
              f"{meta['duration_s']:>6.1f}s  {meta['n_unique_hashes']:>5} hashes")
    return 0


def cmd_stats(args) -> int:
    db = FingerprintDatabase.load(args.db)
    stats = db.stats()
    print(f"database: {args.db}")
    print(f"tracks:          {stats['n_tracks']}")
    print(f"unique hashes:   {stats['n_unique_hashes']}")
    print(f"hash entries:    {stats['n_hash_entries']}")
    if stats["n_tracks"]:
        avg = stats["n_hash_entries"] / stats["n_tracks"]
        print(f"avg entries/track: {avg:.0f}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="echoprint",
        description="Audio fingerprinting from scratch — hear a clip, name the track.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("fingerprint", help="build a fingerprint DB from a library dir")
    p.add_argument("library_dir")
    p.add_argument("--db", default=config.DEFAULT_DB_PATH)
    p.add_argument("--verbose", "-v", action="store_true")
    p.set_defaults(func=cmd_fingerprint)

    p = sub.add_parser("identify", help="identify a clip against the DB")
    p.add_argument("clip")
    p.add_argument("--db", default=config.DEFAULT_DB_PATH)
    p.add_argument("--json", action="store_true", help="print one-line JSON")
    p.add_argument("--top", type=int, default=1,
                   help="show the top N candidates")
    p.add_argument("--min-score", type=int, default=None,
                   help="override the minimum aligned-score threshold (default 5)")
    p.add_argument("--verbose", "-v", action="store_true")
    p.set_defaults(func=cmd_identify)

    p = sub.add_parser("show", help="show a track's spectrogram + constellation")
    p.add_argument("track")
    p.add_argument("--plots", default=None, help="directory to save PNG plots into")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("list", help="list tracks in the DB")
    p.add_argument("--db", default=config.DEFAULT_DB_PATH)
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("stats", help="show DB statistics")
    p.add_argument("--db", default=config.DEFAULT_DB_PATH)
    p.set_defaults(func=cmd_stats)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:  # AudioError / DatabaseError -> clean message
        from .errors import EchoPrintError
        if isinstance(exc, EchoPrintError):
            print(f"echoprint: {exc}", file=sys.stderr)
            return 2
        raise


if __name__ == "__main__":
    raise SystemExit(main())
