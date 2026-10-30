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


def spoken(who, word):
    """Kokoro word -> kid formants (pitch kept), trimmed, cached."""
    c = kidvoice.CHARACTERS[who]
    key = hashlib.md5(f"{who}|{word}|{c}".encode()).hexdigest()[:10]
    p = CACHE / f"{who}_{key}.wav"
    if not p.exists():
        a, sr = kidvoice.kokoro(word, c["voice"], 1.0)
        s = parselmouth.Sound(a.astype(np.float64), sampling_frequency=sr)
        s = call(s, "Change gender", 75, 600, c["formant"], 0, 1.0, 1.0)
        x = s.values[0]
        thr = 0.02 * np.abs(x).max()
        idx = np.where(np.abs(x) > thr)[0]
        x = x[max(0, idx[0] - int(0.01 * sr)): idx[-1] + int(0.03 * sr)]
        sf.write(p, x / np.abs(x).max() * 0.9, sr)
    return p


def sing(who, word, beats, midi):
    """Return mono float array at SR: word stretched to the note length with a flat sung pitch."""
    snd = parselmouth.Sound(str(spoken(who, word)))
    dur = snd.get_total_duration()
    target = beats * song.BEAT * 0.92
    notes = midi if isinstance(midi, list) else [midi]
    m = call(snd, "To Manipulation", 0.01, 75, 700)
    pt = call("Create PitchTier", "p", 0, dur)
    n = len(notes)
    for i, nt in enumerate(notes):                       # each syllable gets an even share; hold the pitch
        f = mtof(nt + TRANSPOSE[who])
        a, b = dur * i / n, dur * (i + 1) / n
        for k in range(6):
            t = a + (b - a) * (0.08 + 0.84 * k / 5)
            vib = 1 + 0.012 * np.sin(2 * np.pi * 5.5 * t) * min(1, (t - a) / 0.25)
            call(pt, "Add point", t, f * vib)
    call([pt, m], "Replace pitch tier")
    dt = call("Create DurationTier", "d", 0, dur)
    call(dt, "Add point", 0, max(0.6, target / dur))
    call([dt, m], "Replace duration tier")
    out = call(m, "Get resynthesis (overlap-add)")
    out = call(out, "Resample", SR, 50)
    x = out.values[0]
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
            voc[s][i:i + len(x)] += x[: n - i] * (0.8 if who == "both" else 1.0)
            events.append(dict(who=s, word=word, t=round(beat * song.BEAT, 3), dur=round(len(x) / SR, 3)))
    for s, x in voc.items():
        x = x / max(1e-9, np.abs(x).max()) * 0.9
        sf.write(HERE / f"vocal_{s}.wav", x.astype(np.float32), SR, subtype="PCM_16")
    json.dump(dict(events=events, total=round(total_beats * song.BEAT, 3), bpm=song.BPM), open(HERE / "notes.json", "w"), indent=1)
    print("vocals done", round(total_beats * song.BEAT, 1), "s,", len(events), "sung words")
