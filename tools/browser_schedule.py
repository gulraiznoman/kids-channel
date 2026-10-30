"""Upload schedule for Claude in Chrome: every row has full copy + a ready prompt.

python tools/browser_schedule.py  -> kids-channel/Upload Schedule v4.xlsx
Pulls titles/descriptions/tags from each episode's 'Episode N Upload Details.xlsx'.
"""
import datetime as dt, pathlib
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "Upload Schedule v4.xlsx"
TODAY = dt.date(2026, 10, 9)
SHORTS_FROM = dt.date(2026, 10, 10)          # next Short goes out tomorrow
TIME = "6:00 PM"
UPLOADED = {"Episode 1 (full video)", "Short 01|1", "Short 02|1"}   # done on 9 Oct

EPS = [(1, "01 Learn Fruits", dt.date(2026, 10, 10)), (2, "02 Learn Colours", dt.date(2026, 10, 17))]
FUTURE = [("Animal Sounds", "🐮🐶", "Animal", ["Cow", "Dog", "Cat", "Duck", "Sheep", "Lion", "Horse", "Chicken", "Pig", "Elephant"]),
          ("Count 1 to 10", "🔢", "Number", ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"]),
          ("Learn Shapes", "🔺⭐", "Shape", ["Circle", "Square", "Triangle", "Star", "Heart", "Rectangle", "Oval", "Diamond"]),
          ("Learn Vegetables", "🥕🥦", "Vegetable", ["Carrot", "Tomato", "Potato", "Corn", "Peas", "Broccoli", "Onion", "Cucumber", "Pumpkin", "Eggplant"])]


def read_episode(n, folder):
    ws = openpyxl.load_workbook(ROOT / "VIDEOS" / folder / f"Episode {n} Upload Details.xlsx").active
    rows = []
    for r in ws.iter_rows(min_row=2, values_only=True):
        if not r[0]:
            continue
        rows.append(dict(video=r[0], file=str(ROOT / "VIDEOS" / folder / r[2]).replace("/", "\\"), title=r[3],
                         desc=r[4], tags=r[5], thumb=r[6], playlist=r[7], ep=n))
    return rows


def prompt(x, date):
    thumb = ""
    if x["type"] == "Long":
        thumb = (f"\n- Thumbnail: click 'Upload file' under Thumbnail and tell me to choose "
                 f"{str(pathlib.Path(x['file']).parent / 'THUMBNAIL option B.jpg')}")
    return (f"In YouTube Studio (studio.youtube.com), upload one video for my Gul & Mishu channel. "
            f"Click Create > Upload videos, then STOP and tell me to pick this file myself:\n{x['file']}\n\n"
            f"After I pick it, fill in exactly:\n"
            f"- Title: {x['title']}\n"
            f"- Description:\n{x['desc']}\n"
            f"- Playlist: {x['playlist']}{thumb}\n"
            f"- Audience: Yes, it's made for kids\n"
            f"- Show more > Tags: {x['tags']}\n"
            f"- Show more > Category: Education\n"
            f"- Altered or synthetic content / AI use: No\n"
            f"- Visibility: Schedule, {date.strftime('%A %d %B %Y')} at {TIME} (Pakistan time). If Studio shows a "
            f"different time zone, convert it and tell me.\n\n"
            f"Don't click Schedule until you've shown me a summary of all fields and I say yes.")


def build():
    queue, longs = [], []
    for n, folder, date in EPS:
        for x in read_episode(n, folder):
            x["type"] = "Long" if x["video"].startswith("Episode") else "Short"
            (longs if x["type"] == "Long" else queue).append((date, x))
    rows = []
    for date, x in longs:
        done = x["video"] in UPLOADED
        rows.append((TODAY if done else date, x, "Uploaded" if done else "Ready"))
    day = SHORTS_FROM
    for _, x in queue:
        key = f"{x['video']}|{x['ep']}"
        if key in UPLOADED:
            rows.append((TODAY, x, "Uploaded"))
            continue
        rows.append((day, x, "Ready"))
        day += dt.timedelta(days=1)
    # future episodes (not made yet): Saturdays after episode 2, their Shorts continue the daily chain
    sat = dt.date(2026, 10, 24)
    for e, (topic, em, noun, items) in enumerate(FUTURE, 3):
        rows.append((sat, dict(type="Long", video=f"Episode {e} (full video)", ep=e, file="not made yet",
                               title=f"{topic} for Kids {em} {noun} Names for Toddlers | Gul & Mishu", desc="", tags="",
                               playlist="Learn with Gul & Mishu"), "To make"))
        for k, it in enumerate(items, 1):
            rows.append((day, dict(type="Short", video=f"Short {k:02d}", ep=e, file="not made yet",
                                   title=f"Guess the {noun}! {it} | {topic} for Toddlers #shorts", desc="", tags="",
                                   playlist=""), "To make"))
            day += dt.timedelta(days=1)
        sat += dt.timedelta(days=7)
    rows.sort(key=lambda r: (r[0], r[1]["type"] != "Long", r[2] != "Uploaded"))

    wb = Workbook()
    ws = wb.active
    ws.title = "Schedule"
    hdr = ["Date", "Day", "Time (PKT)", "Type", "Episode", "Video", "Status", "File (full path)", "Title", "Description",
           "Tags", "Playlist", "Made for kids", "Category", "AI use", "Prompt for Claude in Chrome"]
    widths = [12, 6, 10, 8, 8, 18, 11, 60, 55, 60, 45, 20, 11, 11, 8, 70]
    thin = Side(style="thin", color="C8CED9")
    box = Border(left=thin, right=thin, top=thin, bottom=thin)
    for c, (h, w) in enumerate(zip(hdr, widths), 1):
        cell = ws.cell(1, c, h)
        cell.font = Font(name="Arial", bold=True, color="FFFFFF", size=10)
        cell.fill = PatternFill("solid", fgColor="2E5AAC")
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.column_dimensions[cell.column_letter].width = w
    dv = DataValidation(type="list", formula1='"Uploaded,Scheduled,Ready,To make"', allow_blank=True)
    ws.add_data_validation(dv)
    fills = {"Uploaded": "D9F2D9", "Ready": "FFFFFF", "To make": "EEEEEE"}
    for r, (date, x, status) in enumerate(rows, 2):
        p = prompt(x, date) if status == "Ready" else ""
        vals = [date, date.strftime("%a"), TIME, x["type"], f"Ep {x['ep']}", x["video"], status, x["file"], x["title"],
                x["desc"], x["tags"], x["playlist"], "Yes", "Education", "No", p]
        for c, v in enumerate(vals, 1):
            cell = ws.cell(r, c, v)
            cell.font = Font(name="Arial", size=10, bold=(x["type"] == "Long"), color="777777" if status == "To make" else "000000")
            cell.alignment = Alignment(wrap_text=True, vertical="top")
            cell.border = box
            cell.fill = PatternFill("solid", fgColor="FFF1C2" if (x["type"] == "Long" and status == "Ready") else fills[status])
        ws.cell(r, 1).number_format = "ddd dd mmm"
        dv.add(ws.cell(r, 7))
        ws.row_dimensions[r].height = 120 if status == "Ready" else 30
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = f"A1:P{len(rows) + 1}"

    # how-to tab
    h = wb.create_sheet("How to use", 0)
    h.column_dimensions["A"].width = 110
    lines = [
        ("Gul & Mishu: upload schedule for Claude in Chrome", True),
        ("", False),
        ("Rhythm: 1 Short every day at 6:00 PM Pakistan time + 1 full episode every Saturday.", False),
        ("Already uploaded on Thu 9 Oct: Episode 1, Short Apple, Short Banana (green rows).", False),
        ("", False),
        ("How to schedule with Claude in Chrome:", True),
        ("1. Open studio.youtube.com in Chrome and open the Claude extension.", False),
        ("2. In the Schedule tab, click the 'Prompt for Claude in Chrome' cell of the next 'Ready' row.", False),
        ("3. Copy it (click the formula bar at the top, Ctrl+A, Ctrl+C) and paste it into the extension.", False),
        ("4. When it asks, pick the video file yourself (extensions can't open the Windows file picker).", False),
        ("5. Check its summary, say yes, then set Status to 'Scheduled' in this sheet.", False),
        ("Tip: do a whole week in one sitting. YouTube posts each one on its date automatically.", False),
        ("", False),
        ("Grey rows ('To make') aren't made yet. Ask Claude to 'make episode 3' before Sat 24 Oct.", False),
    ]
    for i, (t, b) in enumerate(lines, 1):
        c = h.cell(i, 1, t)
        c.font = Font(name="Arial", size=12 if i == 1 else 10, bold=b, color="2E5AAC" if b else "000000")
    for w_ in wb.worksheets:
        w_.sheet_view.showGridLines = False
    wb.active = 1
    wb.save(OUT)
    ready = [r for r in rows if r[2] == "Ready"]
    print("rows", len(rows), "ready", len(ready), "first ready", ready[0][0], ready[0][1]["title"][:40])


if __name__ == "__main__":
    build()
