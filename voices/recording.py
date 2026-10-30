"""Human voice workflow for Gul & Mishu episodes.

1) python recording.py script ep01-fruits
     -> RECORD/<episode> - lines to record.md  (numbered lines per character)
2) Misheal records on her phone (any app, any number of files), drops them into
     RECORD/<episode>/mishu/   and   RECORD/<episode>/gul/
3) python recording.py ingest ep01-fruits
     -> transcribes, matches every script line to the LAST matching take,
        cuts it, adds the kid-voice effect, writes <episode>/audio_rec/line_NNN.wav
     voices.py then uses those files instead of computer voices.
"""
import difflib, json, re, subprocess, sys, pathlib, importlib.util, wave
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
REC = ROOT / "RECORD"

# kid-voice effect per character (tuned for an adult female voice; adjust once real takes exist)
EFFECT = {
    "mishu": "highpass=f=90,afftdn=nf=-25,rubberband=pitch={p}:formant=shifted,acompressor=threshold=-20dB:ratio=3:attack=5:release=80",
    "gul": "highpass=f=90,afftdn=nf=-25,rubberband=pitch={p}:formant=shifted,equalizer=f=250:t=q:w=1:g=2,acompressor=threshold=-20dB:ratio=3:attack=5:release=80",
}
SEMITONES = {"mishu": 3.0, "gul": 2.0}


def load_beats(ep):
    spec = importlib.util.spec_from_file_location("script", ROOT / ep / "script.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.beats()


def lines(ep):
    out = {"mishu": [], "gul": []}
    for i, b in enumerate(load_beats(ep)):
        if "text" in b:
            out[b["who"]].append((i, b["text"]))
    return out


def write_script(ep):
    L = lines(ep)
    REC.mkdir(exist_ok=True)
    (REC / ep / "mishu").mkdir(parents=True, exist_ok=True)
    (REC / ep / "gul").mkdir(parents=True, exist_ok=True)
    md = [f"# Lines to record: {ep}", "",
          "**Who:** Misheal reads BOTH characters (Gulraiz can do Gul if he likes).",
          "",
          "**How:**",
          "- Quiet room, phone 20 cm from your mouth, any voice-recorder app (WhatsApp voice notes work too).",
          "- Speak **happy, bright and a little slow**, like talking to a 3-year-old. Smile while you talk!",
          "- Read the lines in order with a **short pause (1-2 seconds) between lines**.",
          "- Made a mistake? No problem: just pause and **say the whole line again**. I keep the last take.",
          "- You can record in one long file or many small ones.",
          f"- Put Mishu's recordings in `RECORD/{ep}/mishu/` and Gul's in `RECORD/{ep}/gul/` (or just send them to Gulraiz).",
          ""]
    for who, title in (("mishu", "MISHU (girl, cheerful, curious)"), ("gul", "GUL (boy, excited, a bit cheeky)")):
        md += [f"## {title}: {len(L[who])} lines", ""]
        for k, (_, text) in enumerate(L[who], 1):
            md.append(f"{k}. {text}")
        md.append("")
    p = REC / f"{ep} - lines to record.md"
    p.write_text("\n".join(md), encoding="utf-8")
    print("wrote", p, {k: len(v) for k, v in L.items()})


def norm(s):
    s = s.lower().replace("’", "'")
    return re.sub(r"[^a-z0-9' ]+", " ", s).split()


def transcribe(files):
    from faster_whisper import WhisperModel
    model = WhisperModel("small.en", device="cpu", compute_type="int8")
    words = []                                      # (file, start, end, word)
    for f in files:
        raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(f), "-ac", "1", "-ar", "16000",
                              "-f", "f32le", "-"], capture_output=True, check=True).stdout
        audio = np.frombuffer(raw, np.float32)
        segs, _ = model.transcribe(audio, word_timestamps=True, vad_filter=True)
        for s in segs:
            for w in s.words:
                words.append((f, w.start, w.end, w.word))
    return words


def match(script_lines, words):
    """For each script line, find the LAST take that matches it about as well as the best take."""
    flat = [(i, t) for i, w in enumerate(words) for t in norm(w[3])]
    seq = [t for _, t in flat]
    res = {}
    for idx, text in script_lines:
        target = norm(text)
        n = len(target)
        cands = []
        for start in range(len(seq)):
            for L in (n - 1, n, n + 1):
                if L >= 1 and start + L <= len(seq):
                    sc = difflib.SequenceMatcher(None, seq[start:start + L], target).ratio()
                    if sc >= 0.72:
                        cands.append((sc, start, L))
        if not cands:
            continue
        top = max(c[0] for c in cands)
        good = [c for c in cands if c[0] >= top - 0.08]
        sc, start, L = max(good, key=lambda c: (c[1], c[0]))     # latest good take
        # among windows starting there, prefer the best-scoring length
        sc, start, L = max((c for c in good if c[1] == start), key=lambda c: c[0])
        w0, w1 = flat[start][0], flat[start + L - 1][0]
        if words[w0][0] == words[w1][0]:
            res[idx] = (words[w0][0], words[w0][1], words[w1][2], round(sc, 2))
    return res


def ingest(ep):
    out_dir = ROOT / ep / "audio_rec"
    out_dir.mkdir(exist_ok=True)
    L = lines(ep)
    report = {}
    for who in ("mishu", "gul"):
        files = sorted(p for p in (REC / ep / who).glob("*") if p.suffix.lower() in
                       (".wav", ".mp3", ".m4a", ".ogg", ".opus", ".aac", ".flac", ".mp4", ".3gp"))
        if not files:
            print(who, ": no recordings yet")
            continue
        words = transcribe(files)
        found = match(L[who], words)
        ratio = 2 ** (SEMITONES[who] / 12)
        for idx, text in L[who]:
            if idx not in found:
                report[idx] = ("MISSING", text)
                continue
            f, t0, t1, score = found[idx]
            dst = out_dir / f"line_{idx:03d}.wav"
            af = EFFECT[who].format(p=f"{ratio:.4f}")
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{max(0, t0 - 0.08):.3f}",
                            "-to", f"{t1 + 0.18:.3f}", "-i", str(f), "-af", af + ",aresample=48000",
                            "-ac", "1", str(dst)], check=True)
            report[idx] = (f"ok {score}", text)
    json.dump(report, open(out_dir / "report.json", "w"), indent=1)
    miss = [v[1] for v in report.values() if v[0] == "MISSING"]
    print(f"{len(report) - len(miss)} lines ready, {len(miss)} missing")
    for m in miss:
        print("  missing:", m)


if __name__ == "__main__":
    cmd, ep = sys.argv[1], sys.argv[2]
    write_script(ep) if cmd == "script" else ingest(ep)
