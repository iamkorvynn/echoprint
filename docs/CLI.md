# CLI reference

## `echoprint fingerprint <library-dir> [--db PATH] [-v]`

Build a fingerprint database from every `.wav` under the directory
(recursive). Prints per-track peak/hash counts, then a summary.
`--db` defaults to `echoprint.db.json` in the current directory.
`-v` prints stage timings.

```bash
python -m echoprint fingerprint tracks/
python -m echoprint fingerprint tracks/ --db my.db.json -v
```

## `echoprint identify <clip.wav> [--db PATH] [--json] [--top N] [--min-score N] [-v]`

Identify one clip. Prints `MATCH: <title>` with the score breakdown,
or an honest `NO MATCH`. Exit code is 0 either way (a no-match is a
successful answer, not an error); 2 means a bad file or missing DB.

- `--json` prints one line of JSON instead of the human report.
- `--top N` lists the top N candidates with their aligned scores.
- `--min-score N` overrides the default threshold of 5 aligned hashes.
  Raising it makes matches stricter; lowering it makes them looser
  (and more likely to be wrong).

```bash
python -m echoprint identify demo_clips/clean.wav
python -m echoprint identify demo_clips/clean.wav --top 3 --json
python -m echoprint identify demo_clips/noisy.wav --min-score 10
```

## `echoprint show <track.wav> [--plots DIR]`

Print the track's spectrogram and constellation as ASCII art, with
peak/hash counts. `--plots DIR` also saves `*-spectrogram.png` and
`*-constellation.png` there.

```bash
python -m echoprint show tracks/03-empty-rooms.wav --plots plots/
```

## `echoprint batch <clips-dir> [--db PATH]`

Identify every `.wav` in a directory and print one line per clip:
match / no-match, track, aligned score. Useful for checking a whole
folder of clips at once.

```bash
python -m echoprint batch demo_clips/
```

## `echoprint list [--db PATH]` / `echoprint stats [--db PATH]`

`list` prints every track in the database with duration and hash
count. `stats` prints totals: tracks, unique hashes, hash entries.
