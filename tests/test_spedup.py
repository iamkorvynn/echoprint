"""The honest failure: a sped-up clip MUST return "no match".

Tempo/pitch changes move every peak to a different frequency bin
and change every time delta, so the hashes never line up. If this
test ever starts matching, the fingerprint is broken, not better.
"""

from echoprint import identify_audio
from echoprint.audio import resample_linear, slice_clip


def test_sped_up_clip_no_match(small_db, track03_audio):
    clip = slice_clip(track03_audio, 1.0, 5.0)
    sped = resample_linear(clip, 1.3)
    ident = identify_audio(sped, small_db)
    assert not ident.matched, (
        f"sped-up clip matched {ident.track_id} with score "
        f"{ident.aligned_score} — hashes should have broken"
    )


def test_slowed_down_clip_no_match(small_db, track03_audio):
    clip = slice_clip(track03_audio, 1.0, 5.0)
    slowed = resample_linear(clip, 0.8)
    ident = identify_audio(slowed, small_db)
    assert not ident.matched


def test_slightly_sped_up_still_breaks(small_db, track03_audio):
    # Even 1.1x is enough to shift frequencies by 10% (~4+ bins).
    clip = slice_clip(track03_audio, 1.0, 5.0)
    sped = resample_linear(clip, 1.1)
    ident = identify_audio(sped, small_db)
    assert not ident.matched
