"""Instruments — every voice is synthesized from sine waves, noise,
and envelopes. No samples, no recordings: the whole 10-track library
is maths, which is also why it is safe to ship in the repo.

Each function returns a mono float array of ``duration`` seconds at
``SAMPLE_RATE``. Envelopes are baked in, so notes can be placed on a
timeline by simple addition.
"""

from __future__ import annotations

import numpy as np

from .. import config

SR = config.SAMPLE_RATE

__all__ = [
    "sine_note", "pluck", "piano_note", "bass_note", "saw_note",
    "kick", "snare", "hat", "guitar_note", "string_note",
    "vocal_note", "pad",
]


def _t(duration: float) -> np.ndarray:
    return np.arange(int(duration * SR)) / SR


def _adsr(t: np.ndarray, duration: float, attack: float = 0.01,
          decay: float = 0.3) -> np.ndarray:
    env = np.minimum(1.0, t / max(attack, 1e-6))
    env = env * np.exp(-t / max(decay, 1e-6) * 2.0)
    env[t > duration] = 0.0
    return env


def sine_note(freq: float, duration: float, amp: float = 0.5) -> np.ndarray:
    t = _t(duration)
    return amp * np.sin(2 * np.pi * freq * t) * _adsr(t, duration)


def pluck(freq: float, duration: float, amp: float = 0.5) -> np.ndarray:
    """Acoustic-guitar-ish pluck: bright attack, fast decay, harmonics."""
    t = _t(duration)
    y = (np.sin(2 * np.pi * freq * t) * np.exp(-3 * t / duration)
         + 0.4 * np.sin(2 * np.pi * 2 * freq * t) * np.exp(-6 * t / duration)
         + 0.15 * np.sin(2 * np.pi * 3 * freq * t) * np.exp(-9 * t / duration))
    return amp * y * np.minimum(1.0, t * 200)


def piano_note(freq: float, duration: float, amp: float = 0.5) -> np.ndarray:
    """Piano-ish: hammer attack, several decaying harmonics."""
    t = _t(duration)
    y = np.zeros_like(t)
    for harmonic, weight, rate in ((1, 1.0, 2.0), (2, 0.5, 4.0),
                                   (3, 0.25, 6.0), (4, 0.12, 8.0)):
        y += weight * np.sin(2 * np.pi * harmonic * freq * t) * np.exp(-rate * t / duration)
    return amp * y * np.minimum(1.0, t * 300)


def bass_note(freq: float, duration: float, amp: float = 0.6) -> np.ndarray:
    """Round sub bass: sine + a touch of second harmonic."""
    t = _t(duration)
    y = np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(2 * np.pi * 2 * freq * t)
    return amp * y * np.minimum(1.0, t * 100) * (1 - 0.4 * t / duration)


def saw_note(freq: float, duration: float, amp: float = 0.3) -> np.ndarray:
    """Bright synth saw (band-limited-ish via a few harmonics)."""
    t = _t(duration)
    y = np.zeros_like(t)
    for harmonic in range(1, 9):
        y += np.sin(2 * np.pi * harmonic * freq * t) / harmonic
    y *= 2 / np.pi
    return amp * y * _adsr(t, duration, attack=0.02, decay=duration)


def kick(duration: float = 0.25, amp: float = 0.9) -> np.ndarray:
    """Kick drum: sine sweeping 150 Hz -> 45 Hz."""
    t = _t(duration)
    freq = 45 + 105 * np.exp(-t * 30)
    phase = 2 * np.pi * np.cumsum(freq) / SR
    return amp * np.sin(phase) * np.exp(-t * 12)


def snare(duration: float = 0.18, amp: float = 0.5, seed: int = 0) -> np.ndarray:
    """Snare: filtered noise burst + 180 Hz body."""
    rng = np.random.default_rng(seed)
    t = _t(duration)
    noise = rng.normal(0, 1, size=len(t))
    # crude high-pass by differencing
    noise = np.diff(noise, prepend=0)
    body = np.sin(2 * np.pi * 180 * t)
    return amp * (0.7 * noise + 0.3 * body) * np.exp(-t * 18)


def hat(duration: float = 0.06, amp: float = 0.25, seed: int = 0) -> np.ndarray:
    """Hi-hat: short bright noise burst."""
    rng = np.random.default_rng(seed + 7)
    t = _t(duration)
    noise = rng.normal(0, 1, size=len(t))
    noise = np.diff(noise, prepend=0)
    return amp * noise * np.exp(-t * 90)


def guitar_note(freq: float, duration: float, amp: float = 0.4) -> np.ndarray:
    """Distorted-ish guitar: square-ish waveshape through soft clipping."""
    t = _t(duration)
    y = (np.sin(2 * np.pi * freq * t)
         + 0.5 * np.sin(2 * np.pi * 2 * freq * t)
         + 0.3 * np.sin(2 * np.pi * 3 * freq * t))
    y = np.tanh(2.0 * y)  # soft-clip = distortion
    return amp * y * np.minimum(1.0, t * 150) * np.exp(-1.5 * t / duration)


def string_note(freq: float, duration: float, amp: float = 0.3) -> np.ndarray:
    """Orchestral string: slow attack, vibrato, warm harmonics."""
    t = _t(duration)
    vibrato = 1 + 0.006 * np.sin(2 * np.pi * 5.5 * t)
    y = (np.sin(2 * np.pi * freq * vibrato * t)
         + 0.4 * np.sin(2 * np.pi * 2 * freq * t)
         + 0.2 * np.sin(2 * np.pi * 3 * freq * t))
    attack = np.minimum(1.0, t / 0.15)
    release = np.minimum(1.0, (duration - t) / 0.2 + 0.2)
    return amp * y * attack * np.clip(release, 0, 1)


def vocal_note(freq: float, duration: float, amp: float = 0.4) -> np.ndarray:
    """Vocal-ish melody line: formant-flavoured sine stack + vibrato."""
    t = _t(duration)
    vibrato = 1 + 0.008 * np.sin(2 * np.pi * 5 * t)
    y = (np.sin(2 * np.pi * freq * vibrato * t)
         + 0.5 * np.sin(2 * np.pi * 2 * freq * t)
         + 0.25 * np.sin(2 * np.pi * 3 * freq * t))
    env = np.minimum(1.0, t / 0.08) * np.minimum(1.0, (duration - t) / 0.1 + 0.1)
    return amp * y * np.clip(env, 0, 1)


def pad(freqs, duration: float, amp: float = 0.2) -> np.ndarray:
    """Soft chord pad: detuned sines with a slow swell."""
    t = _t(duration)
    y = np.zeros_like(t)
    for f in freqs:
        y += np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 1.005 * t)
    y /= max(len(freqs), 1)
    env = np.minimum(1.0, t / 0.4) * np.minimum(1.0, (duration - t) / 0.4 + 0.1)
    return amp * y * np.clip(env, 0, 1)
