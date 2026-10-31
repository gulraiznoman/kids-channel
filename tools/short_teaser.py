"""Vertical weekly Shorts cut from a finished long video (1 a week, not daily).
python tools/short_teaser.py -> VIDEOS/<Sxx>/... + tools/_shorts_check.png
Each Short = chosen scenes from timeline.json, centre-cropped into 1080x1920 over a blurred copy of the same frame."""
import json, pathlib, subprocess
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent
SHORTS = [  # id, out file, long folder, long video path, first scene (kind, nth), last scene, crop width, crop x
    ("S20 Santa Chimney", "Santa Claus Short", "long19-santa", "VIDEOS/L19 Santa Christmas Eve/Santa Claus for Kids v1.mp4", ("chimney", 0), ("snack", 0), 1600, 160),
    ("S21 Surprise Present", "Surprise Present Short", "long21-presents", "VIDEOS/L21 Christmas Presents/Christmas Presents for Kids v1.mp4", ("surprise", 0), ("surprise", 2), 1600, 160),
    ("S22 Write ABC", "Write ABC Short", "long22-writing", "VIDEOS/L22 Learn to Write ABC/Learn to Write ABC for Kids v1.mp4", ("trace", 0), ("trace", 3), 1600, 100),
]


def pick(tl, kind, n):
    return [s for s in tl["scenes"] if s["kind"] == kind][n]


def main():
    for sid, name, here, src, a, b, cw, cx in SHORTS:
        tl = json.load(open(ROOT / here / "timeline.json"))
        t0, t1 = pick(tl, *a)["t0"], pick(tl, *b)["t1"]
        out = ROOT / "VIDEOS" / sid
        out.mkdir(parents=True, exist_ok=True)
        dst = out / f"{name} v1.mp4"
        fc = (f"[0:v]crop={cw}:1080:{cx}:0,scale=1080:-2[fg];"
              "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5,eq=brightness=0.04[bg];"
              "[bg][fg]overlay=0:(H-h)/2,format=yuv420p[v]")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t0), "-to", str(t1), "-i", str(ROOT / src), "-filter_complex", fc,
                        "-map", "[v]", "-map", "0:a", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-r", "30",
                        "-af", f"afade=t=out:st={t1 - t0 - 0.6:.2f}:d=0.6", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(dst)],
                       check=True, stdin=subprocess.DEVNULL)
        print(sid, round(t1 - t0, 1), "s", dst.stat().st_size // 1024 // 1024, "MB", flush=True)


if __name__ == "__main__":
    main()
