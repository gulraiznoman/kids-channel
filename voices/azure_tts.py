"""Microsoft Azure Speech (official, commercially licensed) text-to-speech.

Put your free-tier key in kids-channel/voices/azure.json:
    {"key": "xxxxxxxx", "region": "eastus"}
(or set AZURE_SPEECH_KEY / AZURE_SPEECH_REGION environment variables).
"""
import json, os, pathlib, time, urllib.request
from xml.sax.saxutils import escape

HERE = pathlib.Path(__file__).resolve().parent


def creds():
    p = HERE / "azure.json"
    if p.exists():
        c = json.loads(p.read_text())
        return c["key"].strip(), c["region"].strip()
    k, r = os.environ.get("AZURE_SPEECH_KEY"), os.environ.get("AZURE_SPEECH_REGION")
    if not (k and r):
        raise SystemExit("No Azure key yet: create kids-channel/voices/azure.json with your key and region.")
    return k, r


def synth(text, voice, pitch, rate, out_wav):
    key, region = creds()
    ssml = (f'<speak version="1.0" xml:lang="en-US"><voice name="{voice}">'
            f'<prosody pitch="{pitch}" rate="{rate}">{escape(text)}</prosody></voice></speak>')
    req = urllib.request.Request(
        f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1",
        data=ssml.encode("utf-8"),
        headers={"Ocp-Apim-Subscription-Key": key,
                 "Content-Type": "application/ssml+xml",
                 "X-Microsoft-OutputFormat": "riff-48khz-16bit-mono-pcm",
                 "User-Agent": "gul-mishu"})
    for attempt in range(4):
        try:
            data = urllib.request.urlopen(req, timeout=60).read()
            pathlib.Path(out_wav).write_bytes(data)
            return
        except urllib.error.HTTPError as e:
            if e.code == 429:                      # free tier rate limit: wait and retry
                time.sleep(3 * (attempt + 1))
                continue
            raise SystemExit(f"Azure error {e.code}: {e.read()[:300]!r}")
    raise SystemExit("Azure kept rate-limiting; try again in a minute.")


if __name__ == "__main__":
    synth("Hi friends! I'm Mishu!", "en-US-AnaNeural", "+12Hz", "-4%", HERE / "_azure_test.wav")
    print("ok: wrote _azure_test.wav")
