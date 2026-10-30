---
name: project-youtube-kids
description: "Gulraiz wants a second YouTube channel for kids nursery rhymes, modelled on Lalafun, to earn money"
metadata:
  node_type: memory
  type: project
  originSessionId: d1f1a697-375c-44d2-8803-51a4bddc7fe8
  modified: 2026-10-07T12:42:16.746Z
---

On 2026-10-07 Gulraiz asked to start a kids nursery-rhyme channel modelled on
Lalafun (@lalafun-kids-nursery-rhymes: 3D "Baby Lala" character, 13M subs, launched
Oct 2022, a funded studio). Goal is earning from YouTube on a $0 budget [[user-gulraiz]].

Facts gathered that day: Made for Kids RPM is about $1-3 (no personalised ads);
YouTube's "inauthentic content" policy (July 2025) and a Jan 2026 wave terminated
16 AI kids channels for templated mass uploads. So: original character, own
music arrangements, public-domain lyrics only, a human-sung vocal, low upload volume
with real variation. Same deliverable rules as [[feedback-youtube-uploads]] apply,
but kids rhymes can run 2-3 min each plus longer compilations.

No pilot built yet at time of writing; next step was his choice of language
(English vs Urdu) and art style.

Update 2026-10-08: he chose the kids channel after all. A scan of ~740 kids videos from
the past month showed kids is the strongest niche for tiny channels (many under 5K subs
with 0.5-4M views). Strongest small-channel angles: Urdu/Islamic moral stories (Karvaan
Kids, Kids Sunnah: 600K+ on ~3-5K subs), English learning videos (colors, ABC, animal
sounds), twisted classic rhymes in 3D (Baby Bon Bon, Choo Choo Learning TV), Spanish
songs (NinnaNote 2M on 715 subs). Stories and learning videos need SPOKEN narration
only, which avoids the singing-voice problem. Our visuals would be code-made 2D,
while most winners use 3D. Asked him to pick an angle; pilot not built yet.
Characters (2026-10-08): Gulraiz and his wife Misheal AS KIDS (about 4-5). He rejected
English names for himself. Final names (2026-10-08): **Gul & Mishu**. Kit file ids stay gul/misheal.
Faces and hair are fixed across every video; outfits change per video. Kit lives in
`~/kids-channel/characters/` (characters.py = SVG source, layers/<name>/*.png = 1200x2000
stackable parts, README.md = character bible + layer order, Character Sheet v1.png).
Rendered with headless Chrome (no cairosvg). They could voice the characters themselves.

Episode 1 "Learn Fruits with Gul & Mishu" v1 delivered 2026-10-08 (3:11, 1080p) in
`~/kids-channel/VIDEOS/01 Learn Fruits/` with 3 thumbnails + upload details. Source in
`~/kids-channel/ep01-fruits/`: script.py (beats as data) -> voices.py (edge-tts placeholder
voices, both en-US-AnaNeural: Gul -40Hz, Mishu +12Hz; trim TTS silence or pacing drags)
-> art.py (bg + fruits) -> render.py (PIL compositor, NW=8, ~4.5 min) -> audio_mix.py
(music ~12 dB under voice) -> ffmpeg loudnorm. Reuse this pipeline for new episodes.
Voices must be re-recorded by Gulraiz and Misheal before monetization.
Voice decision (2026-10-08): he wants a free voice usable long-term without buying
anything. edge-tts (Edge Read Aloud) is not licensed for commercial use; same Ana voice
legally = Azure Speech free tier (needs card verification). Fully free alternative:
Kokoro TTS (Apache-2.0, offline, installed) with rubberband pitch shift; auditions in
`~/kids-channel/voices/` (Mishu 1-3, Gul 1-3 + current Ana clips). Awaiting his pick.
Profile picture options A/B/C in `~/kids-channel/branding/` (profile.py).
Decisions 2026-10-08: voice = Misheal records BOTH characters (best for monetization),
no computer voices for published videos. Workflow: `python voices/recording.py script <ep>`
writes RECORD/<ep> lines; recordings go in RECORD/<ep>/mishu|gul/; `recording.py ingest <ep>`
transcribes with faster-whisper (decode via ffmpeg; PyAV arg bug), keeps the LAST good take,
applies kid effect (+3 st Mishu, +2 st Gul, untested on her real voice), writes
<ep>/audio_rec/ which voices.py prefers. Episode 1 waits for her recording (YouTube can't
swap audio after upload). Profile picture = option B (rainbow) -> branding/PROFILE PICTURE - FINAL.png;
banner = branding/CHANNEL BANNER.jpg (banner.py, safe area 1546x423).
Channel created by him 2026-10-08; setup is done via a Claude-in-Chrome prompt at kids-channel/branding/BROWSER SETUP PROMPT.txt (channel set Made for Kids, uploads default Private, category Education). WATERMARK.png made from the profile picture.
UPDATE 2026-10-08 (supersedes the Misheal-voice decision): they have no real voices for now.
Published videos use Microsoft Azure Speech (official, commercial-licensed) en-US-AnaNeural,
free F0 tier. `voices/azure_tts.py` reads kids-channel/voices/azure.json {"key","region"};
`ep01-fruits/voices.py azure` (default) writes audio_azure/; `voices.py edge` is preview-only,
never publish. Waiting for him to create the Azure Speech F0 resource and send key + region.
Human recordings (audio_rec/) still override if Misheal ever records.
UPDATE 2026-10-08: he refuses to put a card anywhere, so Azure is OUT. Voice route now =
Kokoro (Apache-2.0, no account) + Praat "Change gender" (parselmouth) to reshape formants
and pitch to kid levels (`voices/kidvoice.py`; targets match Ana: Mishu ~330 Hz, Gul ~260 Hz).
Plain rubberband pitch shift sounded "not like kids" to him. Round 3 auditions in
`voices/round 3/`; awaiting his pick, then wire kidvoice.say_as into voices.py and make ep01 v2.
Mishu voice LOCKED 2026-10-08: Kokoro af_heart, speed 0.95, formant 1.18, pitch 330, range 1.3 ('New Mishu 1'). Gul from female bases sounded girlish; round 4 tries male bases (am_*) with formant 1.22-1.30, pitch ~230 Hz.
2026-10-08: Gul voice LOCKED = Kokoro am_adam, formant 1.12, pitch 190, range 1.2 ("Gul 4").
voices.py default engine "kokoro" (audio_kokoro/, cached by md5 of who|text). Ep01 v2 delivered:
12 fruits (added lemon, kiwi), calmer pacing (GAP 0.6, prompt 3 s), 3:20. 12 vertical Shorts via
`ep01-fruits/shorts.py` (LAYOUT=vertical in render.py; label_w 720 so long words fit).
Schedule: `kids-channel/Upload Schedule v1.xlsx`: 1 Short daily + 1 episode every Saturday,
6 PM PKT, start Sat 10 Oct 2026; 8 episode topics planned (colours, animal sounds, 1-10,
shapes, vegetables, vehicles, body parts). AI-use disclosure answer for these videos: "No".
Schedule v2 (2026-10-09) replaces v1 (moved to kids-channel/old versions): Shorts run one a day in strict order across episodes (fruit Shorts 10-21 Oct, colours from 22 Oct); episodes still every Saturday (Ep2 Colours due Sat 17 Oct). Per-item emojis in titles. Generator: scratchpad kids_schedule_v2.py.
Episode 2 "Learn Colours" built 2026-10-09 in `~/kids-channel/ep02-colours/` (copy of ep01 engine; script.py now
holds TOPIC, NOUN, OUTFITS, LABEL_COLOURS; render.py imports script as EP). 11 colours (grey added to reach 3:08),
balloon + same-colour object art, rainbow background, music in a new key/tempo (BPM 112, +2 st). New outfits added
to characters.py: gul "bluetee", misheal "pink" (Character Sheet v3). Upload sheets now come from
`kids-channel/tools/upload_sheet.py <epNN>` (add an EPISODES entry per episode). Schedule v3 (Grey added) is current;
v1/v2 in kids-channel/old versions. Ep2 uploads Sat 17 Oct; its Shorts run 22 Oct - 1 Nov.
2026-10-09: he uploaded Episode 1 + Shorts Apple and Banana on 9 Oct. Current schedule = kids-channel/Upload Schedule v4.xlsx from tools/browser_schedule.py (reads each episode's upload-details xlsx; each Ready row has a Claude-in-Chrome prompt; user picks files himself). Shorts daily from 10 Oct (Orange), colour Shorts 20-30 Oct, Ep2 Sat 17 Oct, Ep3 Animal Sounds due Sat 24 Oct. Update UPLOADED set + rerun as v5 when status changes.
2026-10-11: after 2 days the channel had ~3 views total (all 4 uploads public, nothing broken). He wants a
SEPARATE long-video series (15-20 min, all new content, not episode compilations). Long-video scan
(576 videos, past month, 8 min+): surprise eggs are WEAK for small channels (medians 150-4K, zero
winners) so I dropped that idea. Winners for tiny channels: dinosaur adventure stories (Saina_Storyworld
5K subs 720K/660K, CocoBob 1.7K subs 300K), mixed "Baby Animals & Fun Learning: Animals, Colors,
Fruits & More" 11-17 min (Geniee Rhymes 6K subs: 864K, 541K, 386K), colour vehicles (police cars,
fire trucks; 108-248K on 6-31K subs). Scan files: scratchpad yt_long/, long_niches.json.
Long video 1 "Baby Animals & Fun Learning" built 2026-10-11 in `~/kids-channel/long01-animals-fun/` (engine copy +
per-section backgrounds via beat "bg" and title cards via beat "section"; art.py draws 54 items: baby animals,
shapes with faces, vehicles, ocean animals, weather, counting n1-n10 from ep01 fruit art; farm/road/beach bgs).
~12.5 min, 6 sections; output VIDEOS/L01 Baby Animals and Fun Learning/ with chapters in the description.
Planned upload Wed 14 Oct 6 PM; long videos go out on Wednesdays. Next long videos: dinosaur adventure, rainbow vehicles.
Video elements: MFK videos can't have end screens/cards; give an English SRT built from timeline.json (every spoken line, 'Gul: ...'), saved as 'SUBTITLES - English.srt' in the video folder. Do this for every new episode/long video. SEO metadata v3 format for L01 is in its 'upload details v3 SEO.md'.
2026-10-12 SHORTS PIVOT: 5 public fruit "Guess the Fruit" Shorts had 6 views total. Shorts scan (703 kids Shorts, 462 from
channels <50K subs): song/nursery-rhyme clips median ~213K views on small channels; guess/quiz format median ~30 (worst).
He asked for catchy sing-along Shorts like NuNu TV (29.6M subs; 15-28 s song clips, Music category, generic tags + boilerplate
description, so tags aren't why they win). Pilot S01 "Animal Dance" (original lyrics/melody, 25.5 s) in
`~/kids-channel/song01-animal-dance/`: song.py (notes) -> sing.py (Kokoro word -> Praat Manipulation onto melody pitch +
beat length; ~2 cents accurate) -> music.py (upbeat backing, glockenspiel doubles the tune, sfx) -> render.py (farm bg,
animal acts out the verb, karaoke word, kids dance). Output VIDEOS/S01 Animal Dance/. Awaiting his verdict on the singing.
Fruit Shorts still scheduled 13-19 Oct.
2026-10-12 S01 v2 (after "sound not clear, add moving visuals"): sing.py now one Praat "Change gender" pass per syllable
(formant + flat note pitch + stretch capped at 1.5x), bunny verse "Hop" -> "Jump" (Hop was misheard). music.py ducks music
under vocals, quiet glockenspiel, vocal presence boost. clarity.py = faster-whisper word check: full mix went 25/34 -> 34/34.
render.py v2: spinning rays, beat zoom pulse, stomp shake, animals fly in/out, star bursts, clouds, chorus orbit + confetti.
Output "VIDEOS/S01 Animal Dance/Animal Dance - Short v2.mp4" (VER env var names the version). v1 file was overwritten by mistake.
2026-10-12 S01 v3: he said v2 voice "broken and distorted" -> pitch-forcing TTS into notes is DEAD (Gul's am_adam base gets
pushed ~2 octaves). No GPU (Intel UHD only), so AI singing models are out; Suno free tier isn't licensed for monetised use.
v3 = CHANT: sing.chant() uses the approved kidvoice.say_as voice untouched, words placed on the beat. He also asked for
"more children sounds": music.py v3 = toy piano tune, xylophone fills, boom-chick tuba + ukulele, claps, shaker, slide
whistles, cartoon quack/boing, kids "Yay!" ending. Mix clarity 33/34. Output "Animal Dance - Short v3.mp4" (VER=v3).
v2 scripts kept as sing_v2.py / music_v2.py.
2026-10-12: S01 Animal Dance v3 PUBLISHED (title "Stomp! Jump! Swing! ... Animal Dance Song ... #shorts", Music category,
SEO in VIDEOS/S01 Animal Dance/upload details v1 SEO.md, THUMBNAIL v1.png 1080x1920). Playlists on channel: Learn with
Gul & Mishu, Fruits & Food, Numbers & Counting, Animals, Colours & Shapes; advised adding S01 to Animals + new "Kids Songs & Dance".
Next song ideas: wash your hands, brush your teeth, vehicles, colours. Compare S01 views vs fruit quiz Shorts after 48 h.
2026-10-12 S02 "Vehicle Sounds" built in `~/kids-channel/song02-vehicles/` (song.py now holds ALL per-song settings: SLUG, TITLE_LINES,
INTRO_WORDS, CHORUS, BG, VERSES with animation type, RAY_COL, FACES_RIGHT, STAGE_Y, LIGHTS; copy the folder + edit song.py
for the next song). Sound words picked by whisper test: Beep, Choo-choo, Woo-woo (Gul only; Mishu's sounded "we will"),
Ding ding (Nee-naw/Wee-woo/Choo alone failed). chant() re-speaks too-long words faster instead of cutting. Clarity 32/32 in mix.
render NW default 4 (8 workers hit a MemoryError). Output VIDEOS/S02 Vehicle Sounds/ (Short v1, THUMBNAIL v1, upload details v1 SEO.md).
2026-10-12 S02 v1 (chant song, rays/tint/confetti) REJECTED by him: "very bad and confusing; make it fun, informative,
educational". Lesson: too much visual noise + shouted sound words with nothing to learn. Top small-channel Shorts I watched
(8.5M toy police cars, 7M counting 1-20) are calm, one thing at a time. S02 v2 = edu.py + render_edu.py in song02-vehicles:
5 vehicles one at a time (drive in, Mishu says name + big label, Gul says its job + icon bubble, real sound + comic burst,
drive out), clean pastel bg + road, soft music, outro line-up "Which one do you like best?". 34.5 s, 13/13 lines clear.
Output VIDEOS/S02 Vehicle Sounds/: "Vehicles for Kids - Short v2.mp4", THUMBNAIL v2.png, upload details v2 SEO.md (Education).
Facebook (2026-10-12): pack in kids-channel/FACEBOOK/ (Page Setup.md, cover 1640x624 cropped from YouTube banner, profile pic, Week 1/ with 5 images + posts.md captions). Generators: tools/facebook_week1.py (images: intro, tip cards, poll, A4 colouring page via line-art SVG) and tools/facebook_week1_text.py. Week 1 = daily fruit Reel + one extra post/day; full videos uploaded natively with YouTube link in first comment. Monetization on FB unverified; treat as promotion.
2026-10-12: Facebook Page set up (profanity filter + hidden words + Messenger auto-reply done). He posted Episode 1 + Apple Reel on FB on 12 Oct (earlier than Week 1 plan), so Baby Animals long video goes on FB Saturday instead. Pending: Long video 2 (dinosaur) for Wed 21 Oct, FB Week 2, Episode 2 YouTube upload Sat 17 Oct.
2026-10-13: S03 'Surprise Box' 10 s seamless-loop Short (gift box shakes -> POP -> puppy springs out, real bark, 'PUPPY!' label, Gul 'A puppy!', Mishu 'Hello, puppy!', puppy hops back, lid closes; first/last frame identical). Source ~/kids-channel/short03-surprise-box/make.py (ANIMAL/LABEL/SOUND/LINES at top -> easy series: kitten, duckling, lion cub...). Output VIDEOS/S03 Surprise Box/ (Short v1, COVER FRAME v1, upload details v1 SEO.md incl. FB caption). Whisper check: all 3 lines clear. Loudness via volume=6dB+alimiter (-15 LUFS); single-pass loudnorm left it at -17.
2026-10-13: he asked to 'make it fun for kids' -> S03 v2 (make_v2.py + frame_v2.py + run_v2.py): box hops/squishes, PEEKABOO eyes under lifted lid (lift 150 so the gap shows), hard shake, POP + slide whistle, puppy spins out, squash landing, happy dance with hearts, kids jump + 'Yay!', backflip (230 px high, label hidden during flip), dive back head-first, lid falls back; bouncy 120 bpm ukulele/xylophone loop exactly 10 s. Whisper: 'Wow!' misheard as 'Well' -> 'Wow, a flip!'. Output Short v2 + COVER FRAME v2 + upload details v2 SEO.md; loop diff 0.12, -14.0 LUFS. Lesson: 'fun' = playful character actions + cartoon sfx, still one focus at a time (not visual noise).
2026-10-15 HOLIDAYS: Halloween now (upload by ~28 Oct), Thanksgiving Thu 26 Nov (upload 10-22 Nov), Christmas (upload from
~25 Nov; story "decorating" format, public-domain Jingle Bells only). He prefers STORY format: "Gul & Mishu preparing for X,
doing things". H01 "Getting Ready for Halloween" built in `~/kids-channel/halloween01/` (art.py SVG items: pumpkin,
jackolantern, blackcat, bat, ghost, candy; hats.py costume hats on the 1200x2000 char canvas; make.py STEPS script ->
voices/timeline/mix; render.py scene fills up; thumb.py). 31.9 s, 14/14 lines clear. Output VIDEOS/H01 Getting Ready for
Halloween/ (Short v1, THUMBNAIL v1, upload details v1 SEO.md). Suggested schedule Sat 17 Oct 6 PM PKT.
2026-10-17 NEW PLAN (his): 2 long videos/week, 10-30 min, new topics (animals, colors, numbers, shapes, ABCs). Titles: topic
first, channel last ("Learn Colors for Toddlers | Gul & Mishu"). Long thumbnails: Gul & Mishu + ONE big object on a plain
colour background, 2-3 words max -> `kids-channel/tools/thumb_simple.py OUT ITEM "WORDS" "#hex"`. L01 given to upload now
with "THUMBNAIL v2 simple.jpg" + "upload details v4 SEO.md". Proposed calendar: Wed+Sat 6 PM PKT; next L02 Learn Colors
(Wed 21 Oct), L03 Count 1 to 10 (Sat 24 Oct), then Animal Sounds (farm/jungle/pets), Shapes, ABC, Fruits & Veg.
Long engine = long01-animals-fun (script.py SECTIONS data-driven). Policy risk: vary formats so it isn't "templated mass content".
2026-10-18: Ep2 "Learn Colours" (3:08) had NOT been uploaded; given to him with THUMBNAIL v2 simple + "Episode 2 upload details v2.md".
L01 had 0 views after a week; told him to swap to THUMBNAIL v2 simple + topic-first title. Audience widened to kids ~2-7
(see [[feedback-kids-channel-safety]]). L02 "Count 1 to 10 for Kids" built in `~/kids-channel/long02-counting/` (make.py
timeline builder TL class: say/count/prompt/scene; render.py 1920x1080 scene renderer: number, count, add, song, rhyme_end,
rocket, intro, outro, title; art pulled from ep01/long01/halloween01). 11:10, all synthesized audio (no stock sounds).
Output VIDEOS/L02 Count 1 to 10/ (video v1, THUMBNAIL v1.jpg, SUBTITLES - English.srt, upload details v1 SEO.md).
Clarity: counting runs transcribe perfectly in context; single-word checks are unreliable for whisper.
H01 Halloween uses a Mixkit meow, which breaks the new own-sounds rule: offer a v2 with a synthesized meow.
2026-10-18 L03 "Learn Fruits and Vegetables Names for Kids" built in `~/kids-channel/long03-fruits-veg/` (art.py: 8 new fruits +
cut halves, 11 veg, basket/bowl/pot/crates, market/patch/kitchen bgs; make.py TL timeline; render.py imports long02 render as R
for helpers). 10:29, all own sounds, 173/175 lines clear (only "peas" heard as "peace"). Outputs in VIDEOS/L03 Fruits and
Vegetables/ (video v1, THUMBNAIL v1.jpg, SUBTITLES, upload details v1 SEO.md). Used his Studio search terms in metadata.
`kids-channel/CONTENT LOG.md` = no-repeats registry + varied Shorts plan (7 different formats replacing colour quiz Shorts).
2026-10-20 L04 "Good Habits for Kids" (his chosen topic; his plan next: Body Parts, then Feelings) built in
`~/kids-channel/long04-good-habits/` (art.py ~53 props + bedroom/bathroom/hall bgs; make.py TL with +0.25 s calmer gap;
render.py full-day story, outfit change polo/kurta -> bluetee/pink at "get dressed"). First draft was only 4.2 min: a story
needs MANY sections to reach 10 min (17 sections here). 9:48, own chants only, 159/162 lines clear. Outputs in
VIDEOS/L04 Good Habits/ (video v1, THUMBNAIL v1.jpg purple+toothbrush, SUBTITLES, upload details v1 SEO.md). Logged in CONTENT LOG.
2026-10-20 ANALYTICS (his paste, last 28 d): 357 views, 8.1 h watch, 4 subs. L02 Count (Oct 18) ~170 views, L03 Fruits&Veg
(Oct 18) ~150 views: both brought ~85% of views. Avg view duration ~1.5 min on long videos (14%) AND on the 3-min Ep1 (46%):
kids watch ~1.5 min regardless -> front-load the best hook in the first 10-20 s, no slow "Hi I'm Gul" intro. L01 got only 7
views. L04 Good Habits CTR 8% in first 12 h. Shorts: high retention (>100%) but tiny views. Uploaded: Ep1, L01, L02, L03,
L04, S01, S02 (Vehicles), fruit Shorts. NOT uploaded yet: Ep2 Learn Colours, H01 Halloween (now v2 with own-voice meow),
S04 What's Inside, S03 Surprise Box (status unknown).
2026-10-21 L05 "Body Parts for Kids" built in `~/kids-channel/long05-body-parts/` (hook-first: "Where is my nose?!" in the first
seconds; big presenter close-ups via render.big_char/face_view/body_view with pulsing rings on PTS part coords; 12 short
sections incl. Mishu Says, what's missing, who's peeking window, trad. If You're Happy + Head Shoulders Knees Toes). 9:46,
167/174 lines clear (misses = homophones like "two feet"/"to feed"). Outputs VIDEOS/L05 Body Parts/ (video v1, THUMBNAIL v1.jpg
via tools/thumb_fun.py body, SUBTITLES, upload details v1 SEO.md). H01 Halloween re-rendered as v2 with Gul's own "Meow, meow!".
Next long video in his plan: Feelings & Emotions.
2026-10-21 L05 Body Parts v2 (make2.py, render2.py, art2.py organs, bg_stage): 9:21, dance-beat music, big opening, 30 parts,
x-ray organs. Upload v2 + THUMBNAIL v2 + SUBTITLES v2 + upload details v2 SEO.md. Clarity 195/219 (misses: single words,
"Mishu says" heard as "miss who says", numbers written as digits).
2026-10-21 L05 v3 (render3.py + art3.py): he rejected v2 because the cartoon had no real hands/feet. v3 = detailed barefoot Gul body
(5-finger hands, thumbs, elbows, knees, ankles, toes) + labelled close-up cards (hand/foot/arm/leg). UPLOAD v3 + THUMBNAIL v2 +
SUBTITLES v2 + upload details v3 SEO.md. Lesson: when the topic is about a body/object, the character art must actually show it.
2026-10-22 REFERENCE RESEARCH (his links): Lalafun Short 2.4B views = 17 s, NO tags, one cute action (baby shares food with
farm animals), music, category Music; most Lalafun hits 12-17 s. CoComelon Shorts 1-2.6M, 17-31 s, toy play, generic tags.
Duck AI Studio = AI mass clips, not MFK, spam hashtags: do NOT copy. Conclusion: virality = short seamless LOOPS, no talking,
catchy music, one cute action; tags barely matter. Built `kids-channel/tools/loop_shorts.py` (share, ducks): S12 Gul Shares
Food (16 s) + S13 Mishu Dances with Ducklings (12 s). He stopped the 7 hook-cut Shorts (tools/make_short.py) midway; only
S08 Rocket was finished.
2026-10-22 Rhyme Shorts (tools/rhyme_shorts.py, PD tunes Old MacDonald + Twinkle, own instruments): chanted versions he
rejected as "reading lyrics, not singing" (TTS can't sing; pitch-forcing sounded broken in S01 v2). Made INSTRUMENTAL v3
versions (tune on bells/toy piano + bouncing words). Real singing options: Gulraiz/Misheal record vocals on phone (free) or
instrumental-only. Also: say E-I-E-I-O as "Ee-eye-ee-eye-oh" in one phrase if chanting again.
2026-10-22: he dropped Old MacDonald ('go with some topic'); made S16 Opposites Short (tools/short_opposites.py), talk over rhyme_v4 exciting music. He likes: Gul & Mishu talking + exciting kids music behind.
2026-10-22 L06 "Dinosaurs for Kids" built in `~/kids-channel/long06-dinosaurs/` (art.py 12 cute SVG dinos + eggs/footprint/fossil/
explorer hats + valley/dig bgs; make.py TL + code-made roars/honks/squeaks + adventure dance beat; render.py). 9:02, 143/152
lines clear (misses = dino names/homophones). Outputs VIDEOS/L06 Dinosaurs/ (video v1, THUMBNAIL v1.jpg via thumb_fun.py dinos,
SUBTITLES). No meta file made (his no-meta rule). Next long: Feelings & Emotions, then Space.
2026-10-22 L07 "Feelings & Emotions for Kids" built in `~/kids-channel/long07-feelings/` (art.py props + room bg; make.py 12 sections:
face-flip opening, 10 feelings, 10 stories, guess, mirror game, calm tools, dance, kind friend, quiz; render.py uses
characters/expressions.py EMOTIONS face layers). 8:56, clarity 161/168. Outputs VIDEOS/L07 Feelings/ (video v1, THUMBNAIL v1.jpg,
SUBTITLES). Next long: Space & Planets.
2026-10-24 channel scan (public pages via python, no browser): 6 subs; longs 9-11 min get 176-561 views in first week vs 11-16 for old 3-min ones;
Counting + Fruits&Veg best; Shorts dead except Vehicles (146) and What's Inside (85). He uploaded Dinos+Feelings same day (remind: 1/day).
Demand ranking -> next longs: Colors&Shapes (done L08), Trucks & Diggers, Wild Animals Safari, Bugs, ABC Phonics, Christmas mid-Nov, Space later.
L08 "Colors & Shapes" in `~/kids-channel/long08-colors-shapes/` (crayon surprise, paint mixing, rainbow, colour train, shapes on chalkboard
with side counting, shape hunt, build-with-shapes, 3D, patterns, dance, quiz). 9:00. Thumbnail = thumb_fun.py colorshapes.
2026-10-25 "viral now" scan (search sp=CAMSBAgEEAE%3D = this month by views, script scratchpad fresh.py): hot = egg-surprise/hatch
(TigiBoo "Knock Knock What's in the Egg" 11.5M, dino eggs 13M), funny 1.5-2.5 min problem songs (Bang Bang Monkey 77.7K subs got 12M
on "Mosquito Go Away"; Kids Funny Songs "I Want It!" sharing 6.7M in 10 days), Lalafun "Kick the Color Balls" 21.9M, construction trucks,
"Dudi Dudi Dam Dam" dance trend (5+ channels, copyright risk - skip). Top hits are SUNG songs: our TTS can't sing = real ceiling.
2026-10-25: S17 Garbage Truck + S18 I'm Angry Shorts made (tools/short_garbage.py, short_angry.py). L09 "Who's in the Egg?" built in
`~/kids-channel/long09-eggs/` (eggs drawn+cracked in render.py egg_parts; 9:00; clarity 147/159, misses = cheep/cheap homophones).
He now ASKED for meta (YT + FB, keyword research via YT autocomplete suggestqueries ds=yt + top-video tags) - give it when he asks.
Gotchas: alimiter needs level=0 (else make-up gain to 0 dB); don't rm _c*.png when the sheet is _chk.png. Shorts research: BabyBus
habit/emotion micro-stories 19-61M (angry, overeat, snacks, boo-boo), Lalafun cute-action 84M-2.4B; next Shorts: Too Much Candy, Boo-Boo, egg-hatch cut, Santa mid-Nov.
2026-10-30: he stopped daily uploads; Shorts dead, long videos win (ABC 375 views in 3 days, Dinos 735, Fruits&Veg 706). 3-month plan saved
in `~/kids-channel/PLAN Nov 2026 - Jan 2027.md`: 2 long/week (Tue+Fri) by search demand + 3 compilations; Christmas live early Dec.
