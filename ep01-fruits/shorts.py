"""Cut one vertical Short per fruit from episode 1.

python shorts.py preview      -> a few vertical PNG frames
python shorts.py render       -> VIDEOS/01 Learn Fruits/Shorts/Short NN - Fruit.mp4
Needs _mix.wav (python audio_mix.py _mix.wav) and timeline.json.
"""
import os, sys, json, subprocess, pathlib
os.environ["LAYOUT"] = "vertical"                # must be set before render is imported (and for workers)
from multiprocessing import Pool
import render as R

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE.parent / "VIDEOS" / "01 Learn Fruits" / "Shorts"
FPS = R.FPS


def spans():
    R.init()
    out = []
    for i, fr in enumerate(R.G["spans"]["fruit"]):
        name = [b for b in R.G["beats"] if b.get("label")][i]["label"]
        out.append((i + 1, fr["key"], name, max(0, fr["tin"] - 0.15), fr["tout"] + 0.7))
    return out


def job(args):
    lo, hi, path = args
    return R.render_chunk((lo, hi, path))


if __name__ == "__main__":
    S = spans()
    if sys.argv[1] == "preview":
        _, key, name, t0, t1 = S[0]
        for k, dt in enumerate((0.4, (t1 - t0) * 0.35, (t1 - t0) * 0.6, (t1 - t0) * 0.75)):
            R.render_frame(int((t0 + dt) * FPS)).save(HERE / f"_s{k}.png")
        print("preview ok", S[0])
        sys.exit()
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = HERE / "_shorts"
    tmp.mkdir(exist_ok=True)
    jobs = []
    for n, key, name, t0, t1 in S:
        jobs.append((int(t0 * FPS), int(t1 * FPS), str(tmp / f"v{n:02d}.mp4")))
    with Pool(8, initializer=R.worker_init) as pool:
        pool.map(job, jobs)
    for (n, key, name, t0, t1), (_, _, vpath) in zip(S, jobs):
        dur = (int(t1 * FPS) - int(t0 * FPS)) / FPS
        dst = OUT / f"Short {n:02d} - {name}.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", vpath,
                        "-ss", f"{int(t0 * FPS) / FPS:.3f}", "-t", f"{dur:.3f}", "-i", str(HERE / "_mix.wav"),
                        "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                        "-af", f"afade=t=in:d=0.12,afade=t=out:st={dur - 0.45:.2f}:d=0.45,loudnorm=I=-14:TP=-1.5:LRA=11",
                        "-ar", "48000", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(dst)],
                       check=True)
        print(f"{dst.name}: {dur:.1f}s")
