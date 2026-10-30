"""Write FACEBOOK/Week 1/posts.md (captions) and FACEBOOK/Page Setup.md."""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
YT = "https://www.youtube.com/@GulAndMishu"
F = "VIDEOS/01 Learn Fruits/Shorts/"
win = lambda p: p.replace("/", "\\")

days = [
 ("Day 1 (Mon)", [("Image", "Day 1 - Meet Gul and Mishu.jpg", f"""Hi friends! 👋 Meet Gul & Mishu! 🌈

Two cheerful kids who love learning fruits, colours, animals, numbers and more. We make fun, calm learning videos for toddlers and preschoolers, where little ones see, hear and say new words out loud. 🍎🐶🔢

👉 Watch all our videos on YouTube: {YT}

Follow our Page for a new video every day! 💛
#toddlerlearning #kidslearning #preschool #gulandmishu"""),
   ("Reel", F + "Short 01 - Apple.mp4", """🍎 Can your little one guess the fruit? Say it together with Gul & Mishu! 👇 Comment your toddler's favourite fruit!
#toddlerlearning #learnfruits #kidslearning #gulandmishu""")]),
 ("Day 2 (Tue)", [("Image", "Day 2 - Tip Teach Colours.jpg", f"""🌈 4 easy ways to teach colours at home (no toys needed!)

1️⃣ Name colours at snack time: "A red apple! A yellow banana!"
2️⃣ Play "find something blue!" around the house
3️⃣ Sort toys into colour piles together
4️⃣ Watch "Learn Colours" with Gul & Mishu 🎈

Which colour does your toddler say first? 👇
📺 {YT}
#parentingtips #toddleractivities #learncolors #gulandmishu"""),
   ("Reel", F + "Short 02 - Banana.mp4", """🍌 Guess the fruit! Long and yellow… can your toddler say it? 🐒
#toddlerlearning #learnfruits #preschool #gulandmishu""")]),
 ("Day 3 (Wed)", [("Video", "VIDEOS/L01 Baby Animals and Fun Learning/UPLOAD THIS - Baby Animals and Fun Learning with Gul and Mishu v2.mp4", """🐶🐱🐮 Baby animals & their real sounds! Plus shapes, vehicles, ocean animals, counting and weather, all in one 13-minute learning video for toddlers.

Woof! Meow! Moo! Can your little one copy the sounds? 🐾
Which animal is your toddler's favourite? 👇

#babyanimals #animalsounds #toddlerlearning #kidslearning #gulandmishu"""),
   ("First comment", "(post this as the first comment under the video)", f"Watch it on YouTube too 👉 {YT}"),
   ("Reel", F + "Short 03 - Orange.mp4", """🍊 Round and orange… and it's called orange too! 😄 Can your toddler guess it?
#toddlerlearning #learnfruits #gulandmishu""")]),
 ("Day 4 (Thu)", [("Image", "Day 4 - Poll.jpg", """🗳️ Help us choose! What should Gul & Mishu learn next?

1️⃣ Numbers 🔢
2️⃣ Shapes 🔺

Comment 1 or 2 👇 We'll make the winner next!
#toddlerlearning #preschool #gulandmishu"""),
   ("Reel", F + "Short 04 - Lemon.mp4", """🍋 Yellow and SOUR! 😝 Can your little one make a sour face like Gul?
#toddlerlearning #learnfruits #gulandmishu""")]),
 ("Day 5 (Fri)", [("Image", "Day 5 - Colouring Page (print A4).jpg", f"""🖍️ FREE colouring page! Print it and let your little one colour Gul, Mishu and the yummy fruits 🍎🍌🍓

Save it, print it (A4), and share a photo of your toddler's colouring in the comments! We'd love to see it 💛

More learning videos 👉 {YT}
#colouringpage #toddleractivities #printables #gulandmishu"""),
   ("Reel", F + "Short 05 - Grapes.mp4", """🍇 So many grapes! Let's count them: one, two, three! 🔢 Count along with your toddler!
#toddlerlearning #counting #learnfruits #gulandmishu""")]),
 ("Day 6 (Sat)", [("Video", "VIDEOS/01 Learn Fruits/UPLOAD THIS - Learn Fruits with Gul and Mishu v2.mp4", """🍎🍌🍇 Learn 12 yummy fruits with Gul & Mishu! Apple, banana, orange, mango and more. Your toddler sees each fruit, hears its name and says it out loud.

Which fruit does your little one love most? 🥭 Comment below!
#learnfruits #toddlerlearning #firstwords #kidslearning #gulandmishu"""),
   ("First comment", "(post this as the first comment under the video)", f"Watch more on YouTube 👉 {YT}"),
   ("Reel", F + "Short 06 - Strawberry.mp4", """🍓 Red with tiny seeds… sweet and yummy! Can your toddler guess it?
#toddlerlearning #learnfruits #gulandmishu""")]),
 ("Day 7 (Sun)", [("Image", "Day 7 - Tip Snack Time Words.jpg", f"""🍎 Snack time = word time! 4 tiny habits that build your toddler's vocabulary:

1️⃣ Say each fruit's name as you cut it
2️⃣ Ask "What colour is it?"
3️⃣ Count the pieces together: 1, 2, 3!
4️⃣ Let your toddler say it back… and clap! 👏

Try it today and tell us how it went 👇
📺 {YT}
#parentingtips #toddlerlearning #firstwords #gulandmishu"""),
   ("Reel", F + "Short 07 - Watermelon.mp4", """🍉 Big, green outside and red inside! Can your toddler guess this fruit?
#toddlerlearning #learnfruits #gulandmishu""")]),
]

md = ["# Facebook Week 1: Gul & Mishu", "",
      "Post time: around **6:00 PM Pakistan time** (or schedule them all in Meta Business Suite).",
      "Images are in this folder. Reels and videos are your existing files (paths are inside kids-channel).", ""]
for day, posts in days:
    md += [f"## {day}", ""]
    for kind, file, cap in posts:
        md += [f"**{kind}:** `{win(file)}`", "```", cap, "```", ""]
(ROOT / "FACEBOOK" / "Week 1" / "posts.md").write_text("\n".join(md), encoding="utf-8")

setup = f"""# Facebook Page setup: Gul & Mishu

Create at **facebook.com/pages/create** (logged in to your personal account; the Page is separate from it).

| Setting | What to enter |
|---|---|
| Page name | **Gul & Mishu - Kids Learning** |
| Category | **Video Creator**, plus **Education** (you can add up to 3) |
| Bio | Fun learning videos for toddlers: animals, colours, fruits & more! 🌈 New video every day 💛 |
| Profile picture | `FACEBOOK PROFILE PICTURE.png` |
| Cover photo | `FACEBOOK COVER 1640x624.jpg` |
| Username (Settings > Page setup) | **@GulAndMishu** (or the closest free one) |
| Website | {YT} |
| Action button | **Add button > Learn more / Visit website** → {YT} |
| Email / phone | Optional; leave blank if you prefer privacy |

## Settings (Settings & privacy > Settings)
- **Professional mode / Professional Dashboard:** ON (gives insights and shows monetization options later)
- **Page visibility:** Public
- **Age restrictions:** none (family content)
- **Profanity filter:** Strong
- **Moderation > Blocked words:** sub4sub, followback, crypto, giveaway, whatsapp me
- **Comments:** hide comments that contain links (stops spam)
- **Messaging > Instant reply:** "Hi! 👋 Thanks for messaging Gul & Mishu. Watch our learning videos here: {YT} 🌈"
- **Linked accounts:** link Instagram (if you make one) so Reels post to both

## After setup
1. Post **Day 1 (Meet Gul & Mishu)** first, then **pin it** to the top (⋯ > Pin post).
2. Invite your Facebook friends to like the Page (Page menu > Invite friends).
3. Share the Page once in your family WhatsApp groups.

## Rules to stay safe
- Write for **parents** (Facebook is 13+). Never ask kids to message or comment.
- Post in groups only where the rules allow it; ask the admin when unsure.
- Use only your own characters (Gul & Mishu), never Peppa Pig, Cocomelon and so on.
"""
(ROOT / "FACEBOOK" / "Page Setup.md").write_text(setup, encoding="utf-8")
print("ok")
