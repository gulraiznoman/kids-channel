"""Fetch real animal / vehicle / weather clips + animal sounds from Mixkit for the kids channel.

Only clips whose page says data-license="videoFree" (commercial + monetised YouTube, no
attribution) are downloaded; sounds come from Mixkit's free sound effects (sfxFree).
manifest.json records page URL + licence for every file.

python kids_stock.py
"""
import json, os, re, time, urllib.error, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
BASE = "https://mixkit.co"
HERE = os.path.dirname(os.path.abspath(__file__))
PEOPLE = ("woman", "man-", "-man", "girl", "boy", "couple", "people", "person", "child", "kid", "family", "hand",
          "lady", "guy", "owner", "vet", "farmer", "tourist", "diver", "surfer", "fisherman", "driver", "pilot",
          "mother", "daughter", "father", "son-", "dancer", "dance", "rancher", "oven", "rotary", "food", "cook",
          "polluted", "dead", "meat", "roast", "grill", "costume", "toy", "statue", "drawing", "cartoon", "gorilla",
          "crash", "accident", "fire-in", "burning", "smoke")

# key: (video tag pages, words the clip slug must contain, sound tag page, words the sound title should contain)
ITEMS = {
    "puppy": (["dog", "puppy"], ["puppy", "dog"], "dog", ["puppy", "bark"]),
    "kitten": (["cat", "kitten"], ["kitten", "cat"], "cat", ["meow", "kitten"]),
    "duckling": (["duck"], ["duckling", "duck"], "duck", ["quack", "duck"]),
    "chick": (["chicken", "bird"], ["chick", "hen", "chicken"], "chicken", ["chick", "hen", "chicken"]),
    "lamb": (["sheep"], ["lamb", "sheep"], "sheep", ["sheep", "lamb", "bleat"]),
    "piglet": (["pig"], ["piglet", "pig"], "pig", ["pig", "oink"]),
    "calf": (["cow"], ["calf", "cow"], "cow", ["cow", "moo"]),
    "bunny": (["rabbit"], ["bunny", "rabbit"], None, []),
    "foal": (["horse"], ["foal", "horse", "pony"], "horse", ["horse", "neigh", "whinny"]),
    "cub": (["lion"], ["lion"], "lion", ["lion", "roar"]),
    "elephant": (["elephant"], ["elephant"], "elephant", ["elephant"]),
    "monkey": (["monkey"], ["monkey"], "monkey", ["monkey"]),
    "fish": (["fish", "aquarium"], ["fish", "clownfish", "aquarium"], None, []),
    "octopus": (["octopus"], ["octopus"], None, []),
    "whale": (["whale"], ["whale"], None, []),
    "crab": (["crab"], ["crab"], None, []),
    "turtle": (["turtle"], ["turtle"], None, []),
    "starfish": (["starfish", "sea"], ["starfish", "star-fish", "sea-star"], None, []),
    "dolphin": (["dolphin"], ["dolphin"], None, []),
    "jellyfish": (["jellyfish"], ["jellyfish", "jelly"], None, []),
    "car": (["car"], ["car"], "car", ["horn"]),
    "bus": (["bus"], ["bus"], None, []),
    "firetruck": (["fire-truck", "firefighter"], ["fire-truck", "firetruck", "fire-engine", "firefighter-truck"], "siren", ["fire", "siren"]),
    "police": (["police"], ["police-car", "police"], "police", ["police", "siren"]),
    "ambulance": (["ambulance"], ["ambulance"], "ambulance", ["ambulance", "siren"]),
    "train": (["train"], ["train"], "train", ["train", "whistle", "horn"]),
    "airplane": (["airplane", "plane"], ["airplane", "plane", "aircraft"], "airplane", ["airplane", "plane", "jet"]),
    "boat": (["boat"], ["boat", "sailboat"], None, []),
    "tractor": (["tractor"], ["tractor"], None, []),
    "helicopter": (["helicopter"], ["helicopter"], "helicopter", ["helicopter"]),
    "sunny": (["sun"], ["sun", "sunny", "sunshine"], None, []),
    "rainy": (["rain"], ["rain"], "rain", ["rain"]),
    "cloudy": (["clouds"], ["cloud"], None, []),
    "windy": (["wind"], ["wind"], "wind", ["wind"]),
    "snowy": (["snow"], ["snow"], None, []),
    "rainbow": (["rainbow"], ["rainbow"], None, []),
}
PER_ITEM = 2


def get(url, timeout=60, tries=5):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return b""
            if e.code != 429 and i == tries - 1:
                return b""
            time.sleep(8 * (i + 1))
        except Exception:                       # timeouts / dropped connections: wait and retry
            time.sleep(6 * (i + 1))
    return b""


def head_ok(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA, method="HEAD"), timeout=30) as r:
            return r.status == 200
    except Exception:
        return False


def main():
    os.makedirs(os.path.join(HERE, "clips"), exist_ok=True)
    os.makedirs(os.path.join(HERE, "sounds"), exist_ok=True)
    mpath = os.path.join(HERE, "manifest.json")
    man = json.load(open(mpath)) if os.path.exists(mpath) else {}
    for key, (tags, want, sfx_tag, sfx_words) in ITEMS.items():
        entry = man.setdefault(key, {"clips": [], "sound": None})
        # ---------------- video clips (skipped when SOUNDS_ONLY=1)
        if os.environ.get("SOUNDS_ONLY") != "1" and len(entry["clips"]) < PER_ITEM:
            slugs = []
            for tag in tags:
                html = get(f"{BASE}/free-stock-video/{tag}/").decode("utf8", "ignore")
                time.sleep(3)
                for s in re.findall(r"/free-stock-video/([a-z0-9-]+-\d+)/", html):
                    if s in slugs or any(p in s for p in PEOPLE):
                        continue
                    if any(w in s for w in want):
                        slugs.append(s)
            have = {c["slug"] for c in entry["clips"]}
            for s in slugs:
                if len(entry["clips"]) >= PER_ITEM:
                    break
                if s in have:
                    continue
                page = get(f"{BASE}/free-stock-video/{s}/").decode("utf8", "ignore")
                time.sleep(3)
                lic = re.search(r'data-license="(video\w+)"', page)
                if not lic or lic.group(1) != "videoFree":
                    print(f"  {key}: skip {s} (licence {lic.group(1) if lic else '?'})")
                    continue
                prev = re.search(r"(https://assets\.mixkit\.co/[^\"']+)-360\.mp4", page)
                if not prev:
                    continue
                url = next((f"{prev.group(1)}-{r}.mp4" for r in ("720", "1080") if head_ok(f"{prev.group(1)}-{r}.mp4")), None)
                if not url:
                    continue
                dest = os.path.join(HERE, "clips", f"{key}__{s}.mp4")
                if not os.path.exists(dest):
                    data = get(url, timeout=240)
                    if not data:
                        continue
                    open(dest, "wb").write(data)
                entry["clips"].append({"slug": s, "file": os.path.relpath(dest, HERE), "page": f"{BASE}/free-stock-video/{s}/",
                                       "licence": "videoFree"})
                print(f"  {key}: OK {s} ({os.path.getsize(dest) / 1e6:.1f} MB)")
            if not entry["clips"]:
                print(f"  {key}: NO CLIP FOUND")
        # ---------------- sound
        if sfx_tag and not entry["sound"]:
            html = get(f"{BASE}/free-sound-effects/{sfx_tag}/").decode("utf8", "ignore")
            time.sleep(3)
            best = None
            for card in html.split('class="item-grid__item"')[1:]:
                pid = re.search(r'item-id-value="(\d+)"', card)
                t = re.search(r"item-grid-card__title[^>]*>\s*([^<]+)", card)
                if not (pid and t):
                    continue
                title = t.group(1).strip().lower()
                if any(w in title for w in ("angry", "aggressive", "growl", "scream", "horde", "crash", "alarm")):
                    continue
                if any(w in title for w in sfx_words):
                    best = (pid.group(1), title)
                    break
            if best:
                url = f"https://assets.mixkit.co/active_storage/sfx/{best[0]}/{best[0]}-preview.mp3"
                dest = os.path.join(HERE, "sounds", f"{key}.mp3")
                data = get(url)
                if data:
                    open(dest, "wb").write(data)
                    entry["sound"] = {"id": best[0], "title": best[1], "file": os.path.relpath(dest, HERE),
                                      "page": f"{BASE}/free-sound-effects/{sfx_tag}/", "licence": "sfxFree"}
                    print(f"  {key}: sound '{best[1]}'")
        json.dump(man, open(mpath, "w"), indent=1)
    print("done:", sum(1 for v in man.values() if v["clips"]), "items with clips,",
          sum(1 for v in man.values() if v["sound"]), "with sounds")


if __name__ == "__main__":
    main()
