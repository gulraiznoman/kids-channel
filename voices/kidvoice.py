"""Free, licence-safe kid voices: Kokoro TTS (Apache-2.0) + Praat 'Change gender' reshaping.

Kids sound young because of a smaller vocal tract (higher formants), not just higher pitch,
so we raise both: formant_shift ~1.15-1.3 and a child pitch median.
"""
import pathlib, subprocess
import numpy as np, soundfile as sf
import parselmouth
from parselmouth.praat import call

HERE = pathlib.Path(__file__).resolve().parent
_pipe = None

# final character settings (picked by Gulraiz from the audition)
CHARACTERS = {
    "mishu": dict(voice="af_heart", speed=0.95, formant=1.18, pitch=330, range=1.3),  # "New Mishu 1", picked 2026-10-08
    "gul": dict(voice="am_adam", speed=1.0, formant=1.12, pitch=190, range=1.2),     # "Gul 4", picked 2026-10-08
}


def kokoro(text, voice, speed):
    global _pipe
    if _pipe is None:
        from kokoro import KPipeline
        _pipe = KPipeline(lang_code="a")
    return np.concatenate([a.numpy() for _, _, a in _pipe(text, voice=voice, speed=speed)]), 24000


def childify(audio, sr, formant, pitch, rng):
    s = parselmouth.Sound(audio.astype(np.float64), sampling_frequency=sr)
    out = call(s, "Change gender", 75, 600, formant, pitch, rng, 1.0)
    return out.values[0], sr


def say(text, out_wav, voice, speed, formant, pitch, range):
    a, sr = kokoro(text, voice, speed)
    b, sr = childify(a, sr, formant, pitch, range)
    tmp = pathlib.Path(out_wav).with_suffix(".tmp.wav")
    sf.write(tmp, b / max(1e-9, np.abs(b).max()) * 0.9, sr)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp), "-ar", "48000", "-ac", "1", str(out_wav)],
                   check=True)
    tmp.unlink()


def say_as(who, text, out_wav):
    say(text, out_wav, **CHARACTERS[who])


if __name__ == "__main__":
    LINES = {
        "mishu": "Hi friends! I'm Mishu! Gul, look! What's this? Apple! Can you say apple?",
        "gul": "Hi friends! I'm Gul! It's a red, shiny apple! Great job! Let's go!",
    }
    cands = [
        ("New Mishu 1", "mishu", "af_heart", 0.95, 1.18, 330, 1.3),
        ("New Mishu 2", "mishu", "af_bella", 0.95, 1.20, 330, 1.3),
        ("New Mishu 3", "mishu", "af_nicole", 0.95, 1.22, 340, 1.3),
        ("New Gul 1", "gul", "af_sarah", 1.0, 1.12, 265, 1.25),
        ("New Gul 2", "gul", "af_heart", 1.0, 1.10, 255, 1.25),
        ("New Gul 3", "gul", "am_puck", 1.0, 1.30, 260, 1.2),
    ]
    out = HERE / "round 3"
    out.mkdir(exist_ok=True)
    for label, who, voice, speed, f, p, r in cands:
        say(LINES[who], out / f"{label}.wav", voice, speed, f, p, r)
        s = parselmouth.Sound(str(out / f"{label}.wav"))
        pp = s.to_pitch(pitch_floor=100, pitch_ceiling=700).selected_array["frequency"]
        pp = pp[pp > 0]
        print(f"{label}: median pitch {np.median(pp):.0f} Hz")
