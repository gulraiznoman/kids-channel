"""Generate voice lines and build the timeline.

python voices.py        -> Gul & Mishu voices (Kokoro + Praat, licence-safe) in audio_kokoro/  <- PUBLISH THESE
python voices.py edge   -> unlicensed edge-tts previews in audio/ (testing only, never publish)
python voices.py azure  -> Azure voices (needs a key; not used)
Real recordings in audio_rec/ always win over both.
"""
import asyncio, json, subprocess, wave, pathlib
import sys
import edge_tts
from script import beats, VOICES
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "voices"))
ENGINE = sys.argv[1] if len(sys.argv) > 1 else "kokoro"

HERE = pathlib.Path(__file__).resolve().parent
AUD = HERE / {"azure": "audio_azure", "kokoro": "audio_kokoro"}.get(ENGINE, "audio")
AUD.mkdir(exist_ok=True)
GAP = 0.6           # breath between lines (calm pace for toddlers)


async def tts(text, who, out_mp3):
    v = VOICES[who]
    c = edge_tts.Communicate(text, v["voice"], rate=v["rate"], pitch=v["pitch"])
    await c.save(str(out_mp3))


def dur(wav):
    with wave.open(str(wav)) as w:
        return w.getnframes() / w.getframerate()


async def main():
    B = beats()
    t = 0.6
    timeline = []
    for i, b in enumerate(B):
        b = dict(b)
        b["t"] = round(t, 3)
        rec = HERE / "audio_rec" / f"line_{i:03d}.wav"
        if "text" in b and rec.exists():            # a real recorded voice wins
            b["wav"] = "../audio_rec/" + rec.name
            b["dur"] = round(dur(rec), 3)
            t += b["dur"] + GAP
        elif "text" in b:
            import hashlib
            key = hashlib.md5(f'{b["who"]}|{b["text"]}'.encode()).hexdigest()[:10]
            mp3, wav = AUD / f"{b['who']}_{key}.mp3", AUD / f"{b['who']}_{key}.wav"
            if not wav.exists():
                if ENGINE == "kokoro":
                    import kidvoice
                    src = mp3.with_suffix(".raw.wav")
                    kidvoice.say_as(b["who"], b["text"], src)
                elif ENGINE == "azure":
                    import azure_tts
                    v = VOICES[b["who"]]
                    azure_tts.synth(b["text"], v["voice"], v["pitch"], v["rate"], mp3.with_suffix(".raw.wav"))
                    src = mp3.with_suffix(".raw.wav")
                else:
                    await tts(b["text"], b["who"], mp3)
                    src = mp3
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-af",
                                "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,"
                                "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse",
                                "-ac", "1", "-ar", "48000", str(wav)], check=True)
                src.unlink()
            d = dur(wav)
            b["wav"] = wav.name if ENGINE == "edge" else f"../{AUD.name}/" + wav.name
            b["dur"] = round(d, 3)
            t += d + GAP
        else:
            b["dur"] = b["pause"]
            t += b["pause"]
        timeline.append(b)
    json.dump(dict(beats=timeline, total=round(t, 3)), open(HERE / "timeline.json", "w"), indent=1)
    print(f"{len(timeline)} beats, total {t:.1f}s")


asyncio.run(main())
