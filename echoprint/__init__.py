"""EchoPrint — audio fingerprinting from scratch.

Hear a clip, name the track. Wang (2003) constellation-map method:
STFT -> spectrogram -> peak picking -> anchor/target hashes ->
hash-table lookup -> the track whose matches cluster at one
consistent time offset wins.

Quick start::

    from echoprint import FingerprintDatabase, identify_audio
    from echoprint.audio import load_wav
    db = FingerprintDatabase.load("echoprint.db.json")
    sr, clip = load_wav("clip.wav")
    result = identify_audio(clip, db)
    print(result.matched, result.title, result.aligned_score)
"""

from .audio import add_noise, load_wav, resample_linear, save_wav, slice_clip
from .database import FingerprintDatabase
from .identify import fingerprint_audio, identify_audio, identify_file
from .scoring import Identification

__version__ = "0.1.1"

__all__ = [
    "FingerprintDatabase",
    "Identification",
    "add_noise",
    "fingerprint_audio",
    "identify_audio",
    "identify_file",
    "load_wav",
    "resample_linear",
    "save_wav",
    "slice_clip",
]
