# Character bible: Gul & Mishu

Names: **Gul** (from Gulraiz) and **Mishu** (from Misheal). Internal file ids stay `gul` and `misheal`.

The two main characters of the kids channel. They're Gulraiz and Misheal **as little kids**
(about 4-5 years old). Their faces and hair never change between videos; clothes do.

## Gul (Gulraiz as a kid)
- **Face (fixed):** warm light-brown skin `#DCA27A` (lightened in v2), big dark-brown eyes, thick black eyebrows, rosy cheeks.
- **Hair (fixed):** black `#1F1A1C`, swept up and back with volume on top, like the real photo.
- **Personality:** curious, brave, a bit of a show-off. Loves trucks, planes and building things.
- **Special look:** rectangular silver sunglasses ("cool Gul").

## Mishu (Misheal as a kid)
- **Face (fixed):** light warm skin `#EDC2A0`, big brown eyes with eyelashes, rosy cheeks.
- **Hair (fixed):** brown with auburn highlights `#6B3826` / `#9A5634`, shoulder length, side part.
- **Always wears:** small gold hoop earrings `#E2B23C`.
- **Personality:** kind, clever, the one who explains things. Loves animals, colours and singing.
- **Special look:** round gold-framed sunglasses.

## Outfits (swappable per video)
| Character | Outfit | Use for |
|---|---|---|
| Gul | `polo`: cream/beige/brown zip polo + brown shorts (from the real photo) | Family outings, special episodes |
| Gul | `tee`: red T-shirt with a yellow star + blue shorts | **Default** everyday look |
| Misheal | `kurta`: maroon tunic with gold dots (from the real photo) | Eid, family, special episodes |
| Misheal | `yellow`: yellow dress with white dots + pink shoes | **Default** everyday look |

New outfits (pyjamas, school uniform, raincoat, swimsuit and so on) get added in
`characters.py` under `OUTFITS`. The face and hair layers stay untouched.

## Files
- `Character Sheet v2.png`: both characters, all outfits and expressions.
- `layers/gul/`, `layers/misheal/`: every body part as a transparent 1200x2000 PNG on the
  same canvas. Stack them in this order:
  `hair_back` (Misheal only) > `body_<outfit>` > `arm_l_<outfit>` > `arm_r_down_<outfit>` or
  `arm_r_wave_<outfit>` > `neck` > `head` > `eyes_open|blink|closed` > `brows` >
  `mouth_smile|open|o|closed` > `hair_front` > `earrings` (Misheal) > `glasses` (optional).
- **Talking** = swap `mouth_open` / `mouth_o` / `mouth_closed` in time with the voice.
- **Blinking** = show `eyes_blink` for 3 frames every 3-5 seconds.
- `characters.py`: the source. `python characters.py export` rebuilds every layer and the sheet.
  Save changed designs as a new version (v3 and so on); old versions live in `old versions/`.
