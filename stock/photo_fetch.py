"""Real photos for items Mixkit has no good clip for, from Openverse (CC0 / public domain only).

python photo_fetch.py piglet "piglet" bunny "rabbit" ...   -> photos/<key>_<n>.jpg + photos/manifest.json
Every photo's licence and source page are recorded; nothing but cc0 / pdm is downloaded.
"""
import json, os, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "GulMishuKids/1.0 (kids learning channel; contact via YouTube)"}
PER = 4


def get(url, timeout=60):
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
                return r.read()
        except Exception:
            time.sleep(4 * (i + 1))
    return b""


def main(pairs):
    os.makedirs(os.path.join(HERE, "photos"), exist_ok=True)
    mpath = os.path.join(HERE, "photos", "manifest.json")
    man = json.load(open(mpath)) if os.path.exists(mpath) else {}
    for key, query in pairs:
        q = urllib.parse.urlencode({"q": query, "license": "cc0,pdm", "mature": "false", "page_size": 20,
                                    "aspect_ratio": "wide"})
        data = json.loads(get(f"https://api.openverse.org/v1/images/?{q}") or b"{}")
        got = 0
        man.setdefault(key, [])
        for r in data.get("results", []):
            if got >= PER:
                break
            if (r.get("license") or "").lower() not in ("cc0", "pdm") or (r.get("width") or 0) < 1000:
                continue
            img = get(r["url"])
            if len(img) < 50_000:
                continue
            dest = os.path.join(HERE, "photos", f"{key}_{got + 1}.jpg")
            open(dest, "wb").write(img)
            man[key].append(dict(file=os.path.relpath(dest, HERE), title=r.get("title"), licence=r.get("license"),
                                 source=r.get("foreign_landing_url"), creator=r.get("creator")))
            got += 1
            time.sleep(1)
        print(f"{key}: {got} photos")
        json.dump(man, open(mpath, "w"), indent=1)
        time.sleep(2)


if __name__ == "__main__":
    a = sys.argv[1:]
    main(list(zip(a[0::2], a[1::2])))
