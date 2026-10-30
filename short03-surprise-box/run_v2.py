"""python run_v2.py frames 20,48,...  |  python run_v2.py video"""
import subprocess, sys
import make_v2 as M
import frame_v2  # noqa: F401  (patches Scene.frame with the v2 animation)

voices = M.make_voices()
sc = M.Scene(voices)
if sys.argv[1] == "frames":
    for f in [int(x) for x in sys.argv[2].split(",")]:
        sc.frame(f).save(M.HERE / f"_f{f:03d}.png")
    print("ok")
else:
    M.OUT.mkdir(parents=True, exist_ok=True)
    wav = M.HERE / "mix_v2.wav"
    M.build_audio(voices, wav)
    dst = M.OUT / f"Surprise Box - Short {M.VER}.mp4"
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{M.W}x{M.H}",
                          "-r", str(M.FPS), "-i", "-", "-i", str(wav), "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                          "-pix_fmt", "yuv420p", "-af", "volume=6dB,alimiter=limit=0.9", "-ar", "48000", "-c:a", "aac",
                          "-b:a", "192k", "-shortest", "-movflags", "+faststart", str(dst)], stdin=subprocess.PIPE)
    for f in range(M.N):
        p.stdin.write(sc.frame(f).tobytes())
    p.stdin.close()
    p.wait()
    print("wrote", dst)
