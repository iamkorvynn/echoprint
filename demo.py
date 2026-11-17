"""EchoPrint demo — the filmed cases, end to end.

    python demo.py

1. Fingerprint the 10-track library (renders it first if missing).
2. Identify a clean 5 s clip            -> must match 03-empty-rooms
3. Identify the same clip with noise     -> must still match, lower score
4. Identify the same clip sped up 1.3x   -> MUST be "no match"
5. Identify an unknown melody            -> MUST be "no match"
6. Show the work: ASCII spectrogram + constellation of track 03.

The sped-up failure is the point, not a bug: pitch/tempo changes
move every peak, so the hashes break. An honest "no match" beats
a confident wrong guess.
"""

from __future__ import annotations

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from echoprint import FingerprintDatabase, identify_audio, load_wav  # noqa: E402
from echoprint.report import format_result  # noqa: E402
from echoprint.show import show_track  # noqa: E402

DB_PATH = os.path.join(HERE, "echoprint.db.json")


def ensure_library() -> None:
    if not os.path.isdir(os.path.join(HERE, "tracks")) or not os.listdir(
            os.path.join(HERE, "tracks")):
        print("rendering the 10-track library (synthesized, no real music)...")
        subprocess.run([sys.executable, "scripts/generate_library.py"],
                       cwd=HERE, check=True)
    if not os.path.exists(os.path.join(HERE, "demo_clips", "clean.wav")):
        print("making demo clips...")
        subprocess.run([sys.executable, "scripts/make_clips.py"],
                       cwd=HERE, check=True)


def main() -> int:
    print("=" * 64)
    print("EchoPrint demo — Shazam from scratch, in Python")
    print("=" * 64)
    ensure_library()

    print("\n[1/6] Fingerprinting the 10-track library...")
    db = FingerprintDatabase()
    for name in sorted(os.listdir(os.path.join(HERE, "tracks"))):
        if not name.endswith(".wav"):
            continue
        sr, y = load_wav(os.path.join(HERE, "tracks", name))
        from echoprint import fingerprint_audio
        fp = fingerprint_audio(y, sr)
        db.add_track(name[:-4], fp["hashes"], title=name[:-4],
                     duration_s=len(y) / sr)
    db.save(DB_PATH)
    stats = db.stats()
    print(f"  {stats['n_tracks']} tracks, {stats['n_unique_hashes']} unique "
          f"hashes, {stats['n_hash_entries']} entries -> {DB_PATH}")

    cases = [
        ("clean.wav", "clean 5s clip (from the middle of track 03)"),
        ("noisy.wav", "same clip + white noise"),
        ("sped-up.wav", "same clip at 1.3x speed — expect NO MATCH"),
        ("unknown.wav", "a melody from no track — expect NO MATCH"),
    ]
    print("\n[2-5/6] Identifying clips...")
    results = {}
    for filename, label in cases:
        sr, y = load_wav(os.path.join(HERE, "demo_clips", filename))
        ident = identify_audio(y, db)
        results[filename] = ident
        print(f"\n{label}:")
        print(format_result(ident, clip_name=filename))

    print("\n[6/6] Showing the work — track 03, spectrogram + constellation:")
    show_track(os.path.join(HERE, "tracks", "03-empty-rooms.wav"))

    print("\n" + "=" * 64)
    print("Demo verdict:")
    ok_clean = results["clean.wav"].matched and results["clean.wav"].track_id == "03-empty-rooms"
    ok_noisy = results["noisy.wav"].matched and results["noisy.wav"].track_id == "03-empty-rooms"
    ok_sped = not results["sped-up.wav"].matched
    ok_unknown = not results["unknown.wav"].matched
    print(f"  clean clip matched track 03:      {'PASS' if ok_clean else 'FAIL'}")
    print(f"  noisy clip still matched:         {'PASS' if ok_noisy else 'FAIL'}")
    print(f"  noisy score < clean score:        "
          f"{'PASS' if results['noisy.wav'].aligned_score < results['clean.wav'].aligned_score else 'CHECK'}")
    print(f"  sped-up clip honestly no match:   {'PASS' if ok_sped else 'FAIL'}")
    print(f"  unknown audio honestly no match:  {'PASS' if ok_unknown else 'FAIL'}")
    print("=" * 64)
    return 0 if (ok_clean and ok_noisy and ok_sped and ok_unknown) else 1


if __name__ == "__main__":
    raise SystemExit(main())
