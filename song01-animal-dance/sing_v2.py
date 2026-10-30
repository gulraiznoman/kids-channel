"""Make Gul & Mishu sing: Kokoro speaks each word, Praat moves it onto the melody notes and beat length.

python sing.py          -> vocals.wav (+ notes.json for the video)
"""
import hashlib, json, pathlib, sys, wave
import numpy as np, soundfile as sf, parselmouth
from parselmouth.praat import call

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "voices"))
import kidvoice
import song

SR = 48000
CACHE = HERE / "words"
CACHE.mkdir(exist_ok=True)
TRANSPOSE = {"gul": 0, "mishu": 0}


def mtof(m):
    return 440 * 2 ** ((m - 69) / 12)


def raw_word(who, word):
    """Kokoro word, trimmed, cached (no processing yet)."""
    c = kidvoice.CHARACTERS[who]
    key = hashlib.md5(f"{who}|{word}|{c['voice']}".encode()).hexdigest()[:10]
    p = CACHE / f"raw_{who}_{key}.wav"
    if not p.exists():
        a, sr = kidvoice.kokoro(word + "!", c["voice"], 1.0)
        thr = 0.02 * np.abs(a).max()
        idx = np.where(np.abs(a) > thr)[0]
        a = a[max(0, idx[0] - int(0.01 * sr)): idx[-1] + int(0.03 * sr)]
        sf.write(p, a / np.abs(a).max() * 0.9, sr)
    return p


MAX_STRETCH = 1.5          # longer stretching smears consonants ("hop" -> "hab"); hold the rest as silence


def sing(who, word, beats, midi):
    """One Praat pass per syllable: kid formants + flat sung pitch + modest stretch."""
    c = kidvoice.CHARACTERS[who]
    snd = parselmouth.Sound(str(raw_word(who, word)))
    dur = snd.get_total_duration()
    notes = midi if isinstance(midi, list) else [midi]
    n = len(notes)
    target = beats * song.BEAT * 0.9
    stretch = min(MAX_STRETCH, max(0.8, target / dur))
    parts = []
    xf = 0.012
    for i, nt in enumerate(notes):
        a, b = dur * i / n, dur * (i + 1) / n
        seg = snd.extract_part(max(0, a - (xf if i else 0)), min(dur, b + (xf if i < n - 1 else 0)))
        f0 = mtof(nt + TRANSPOSE[who])
        out = call(seg, "Change gender", 75, 600, c["formant"], f0, 0.03, stretch)
        out = call(out, "Resample", SR, 50)
        parts.append(out.values[0])
    x = parts[0]
    k = int(xf * stretch * SR)
    for p in parts[1:]:                                # short crossfade between syllables
        k2 = min(k, len(x), len(p))
        r = np.linspace(0, 1, k2)
        x = np.concatenate([x[:-k2], x[-k2:] * (1 - r) + p[:k2] * r, p[k2:]]) if k2 else np.concatenate([x, p])
    fade = int(0.02 * SR)
    x[-fade:] *= np.linspace(1, 0, fade)
    return x


if __name__ == "__main__":
    notes, total_beats = song.notes()
    n = int((total_beats * song.BEAT + 0.5) * SR)
    voc = {w: np.zeros(n) for w in ("gul", "mishu")}
    events = []
    for who, word, beat, beats, midi in notes:
        singers = ["gul", "mishu"] if who == "both" else [who]
        for s in singers:
            x = sing(s, word.strip("!"), beats, midi)
            i = int(beat * song.BEAT * SR)
            voc[s][i:i + len(x)] += x[: n - i] * ((0.55 if s == "gul" else 0.9) if who == "both" else 1.0)
            events.append(dict(who=s, word=word, t=round(beat * song.BEAT, 3), dur=round(len(x) / SR, 3)))
    for s, x in voc.items():
        x = x / max(1e-9, np.abs(x).max()) * 0.9
        sf.write(HERE / f"vocal_{s}.wav", x.astype(np.float32), SR, subtype="PCM_16")
    json.dump(dict(events=events, total=round(total_beats * song.BEAT, 3), bpm=song.BPM), open(HERE / "notes.json", "w"), indent=1)
    print("vocals done", round(total_beats * song.BEAT, 1), "s,", len(events), "sung words")
