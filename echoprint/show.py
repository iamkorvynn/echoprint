"""`echoprint show` — print and plot one track's fingerprint internals."""

from __future__ import annotations

import os

from .audio import load_wav
from .identify import fingerprint_audio
from .peaks import peak_stats
from .visualize import (ascii_constellation, ascii_spectrogram,
                        plot_constellation, plot_spectrogram)

__all__ = ["show_track"]


def show_track(path: str, out_dir: str | None = None,
               width: int = 72, height: int = 20) -> dict:
    """Load a track, print its spectrogram + constellation as ASCII,
    optionally save PNG plots to ``out_dir``. Returns a stats dict."""
    sr, y = load_wav(path)
    fp = fingerprint_audio(y, sr)
    peaks, log_mag = fp["peaks"], fp["log_mag"]
    stats = peak_stats(peaks, log_mag.shape[1], log_mag.shape[0])
    stats.update({
        "path": path,
        "duration_s": round(len(y) / sr, 2),
        "n_hashes": len(fp["hashes"]),
        "spectrogram_shape": log_mag.shape,
    })

    print(f"== {os.path.basename(path)} ==")
    print(f"duration {stats['duration_s']} s | "
          f"{stats['count']} peaks ({stats['per_second']:.1f}/s) | "
          f"{stats['n_hashes']} unique hashes")
    print()
    print(ascii_spectrogram(log_mag, width=width, height=height))
    print()
    print(ascii_constellation(peaks, log_mag.shape, width=width, height=height))

    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        stem = os.path.splitext(os.path.basename(path))[0]
        spec_png = os.path.join(out_dir, f"{stem}-spectrogram.png")
        const_png = os.path.join(out_dir, f"{stem}-constellation.png")
        plot_spectrogram(log_mag, spec_png, title=f"Spectrogram — {stem}")
        plot_constellation(peaks, log_mag.shape, const_png,
                           title=f"Constellation — {stem}")
        stats["spectrogram_png"] = spec_png
        stats["constellation_png"] = const_png
        print(f"\nplots saved: {spec_png}\n             {const_png}")
    return stats
