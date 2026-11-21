#!/usr/bin/env python3
"""news-image-20261120 v4.3 — 'THE WORLD IN ONE DAY', Friday 20 November 2026.

Written from scratch in the Saturday 21 Nov 2026 session (this chat).
No v1/v2/v3 code was read. All art is drawn in code (PIL vectors);
no photographs. Deterministic: no network, no clock, no randomness.

Data re-verified by this session on Sat 21 Nov 2026 (Reuters/AP/AFP/
CNN/WSJ/IMD/ATP Tour/MetService NZ/Take-Two/PBoC/BoJ via web search):
  US close Dow 48,147.33 -949.73 (-1.93%), S&P 6,910.39 -265.44 (-3.70%),
  Nasdaq 22,617.73 -1,261.47 (-5.28%); ANT $88.91 -8.50%, low $83.05;
  Akvan landfall Gopalpur 07:30-08:30 IST, 372,000 evacuated, 0 deaths;
  COP31 overtime, 0 fossil-fuel mentions, $120bn target dropped;
  Medvedev d. Tiafoe 6-3 6-4, Alcaraz d. Cobolli 6-4 6-1;
  Nikkei -5.06% to 56,437, KOSPI -5.21%, TAIEX -6.23%;
  Japan core CPI 2.2%, China LPR 3.0%/3.5% (18th hold);
  EU-UK reset: food up to GBP 5.1bn/yr, 100,000 youth places;
  Nicholls 175*, Phillips 118, NZ 368, India 159/1;
  Xavier Cat 4, 922 hPa, ~200 km west of Manihiki;
  GTA VI official: Take-Two $3.79bn day one, 32.5m copies;
  CGIL 24-hr strike, 100+ cities; Russell FP2 1:47.272.
Hormuz card: UN briefing figures (25 killed since Feb, 136 incidents)
are Friday; the Nov-20 mine claim is labelled [CLAIM], unconfirmed.
Bukele filed Thu night El Salvador time = Fri UTC, dated as such.
Las Vegas qualifying + BepiColombo insertion are Saturday:
TOMORROW / DATE CHECK only, never presented as Friday.

v4.2 (Sat 21 Nov ~13:05 WIB) — head-to-head vs the live top 10
(rank 1 samatch-we 0.992057 down to rank 10 momo-devlog 0.990835):
  * Kyiv lead toll was STALE (3 killed / 15 injured was the early
    Friday count). Updated figures (BBC/CNN, 21 Nov): 110+ missiles
    and 400+ drones fired, 9 killed across Ukraine, 7 in Kyiv, 28+
    injured; the three bridges are Podilskyi, Darnytskyi, Pivdennyi.
  * Poland: two Russian Kh-101 missiles + a jet-powered drone came
    down in south-east Poland on Friday (Polish defence ministry / AP);
    Tusk called it an intentional provocation. 6 of the top 10 carry
    it; we had nothing. Now brief 29.
  * Kenya: drilling spudded at Turkana's Amosing 1 well on Friday
    (Energy CS Wandayi, Gulf Energy); first crude due 1 Dec 2026.
    4 of the top 10 carry it as a card. Now brief 30.
  * Pancreatic cancer pill: daraxonrasib + chemo, EORTC Barcelona
    presentation Friday 20 Nov (BBC/Guardian): tumours shrank in
    60.7% of 61 patients, 90% stopped growing, 1 in 12 undetectable.
    3 of the top 10 carry it. Now brief 36.
  * Senegal: four bodies recovered (Reuters, Thu) — brief 17 now
    carries the toll; the Friday story is the search resuming.
  * Numbers strip: 922 hPa out, 110 missiles in (the day's biggest
    number was missing from our strip).
  * Typography: lead + card headlines are now DejaVu Serif Bold
    (all 10 of the top 10 use serif headlines); the region strip is
    now coloured segments instead of plain text (9 of 10 do this).

v4.4 (Sat 21 Nov ~16:20 WIB) — v4.3 FAILED grading (submission
01a1fcc1, "execution 1: the program exited with code 1", 548ms;
authorship 95% passed, image never graded, score 0). Root cause,
proven locally: main.py only COPIED a pre-rendered entry.png, so in
a clean dir (no entry.png beside it) it died FileNotFoundError.
FIXES: (1) main.py now GENERATES via draw_v4.py when entry.png is
absent, never crashes on a read-only cwd (best-effort copy), main
output $MAKEFUN_OUTPUT_DIR (default /output), prints size + sha256.
(2) The 5 DejaVu TTFs are bundled in fonts/ (the grading image has
no fonts-dejavu-extra, so DejaVuSansCondensed was missing);
draw_v4.py loads from fonts/ first, falls back to /usr/share.
Bundled fonts are byte-identical to the system files, so the
pre-visual-fix output is byte-identical to v4.3. (3) Visual, no
story/number/date changed: Kyiv lead scene is now a BRIGHT bridge
diagram (white deck/arch/piers on dark blue, glowing fire on each
span); COP31 globe has visible green continents + thermometer;
Mercury card scene is a cratered disc (night-side shading + pits);
the world map is a LIGHT cream panel with warm-tan land dots and
clear red numbered pins (like ranks 1/2/10).

v4.3 (Sat 21 Nov ~13:20 WIB) — ONE structural change, per the main
agent's round-2 head-to-head instruction (live top 1-10, 12:45 WIB):
in EVERY top-10 entry the lead headline + body sit BELOW the scene,
on cream, dark serif — never inside the dark panel. v4.1/v4.2 still
put headline + body inside the dark panel (white 18px), so at a
glance it read quieter than rank 1, 2 and newcomer rank 5
(dewacandra4, 4 leads). This round moves the lead headline + body
below the scene onto the cream, dark serif, with the red nameplate
banner + dark scene kept on top. No story, number or date changed
(all v4.2 content kept). Measured first: 20px serif is the max that
fits the longest lead headline (Kyiv, 48 chars) in 2 lines — 22px
needs 3 lines; leads 1 and 3 would fit 22-24px, but the size must
match across the three leads. Card headlines raised 11 -> 12px
serif (card 6's headline trimmed to "BepiColombo set for Mercury
orbit" — the date is in its body + the TOMORROW line — so it still
fits 2 lines). Lead kicker now carries the story number in a red
disc, like the top 10. Lead scene height 80 -> 100px.
"""
import hashlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 28                      # side margin
CW = W - 2 * M              # content width = 968

PAPER = (246, 241, 229)
INK = (22, 35, 58)
NAVY = (18, 35, 63)
NAVY_DARK = (13, 24, 44)
NAVY_MID = (32, 56, 94)
RED = (179, 39, 30)
GOLD = (232, 163, 61)
GOLD_LT = (255, 209, 102)
CREAM = (255, 253, 246)
MUTED = (90, 100, 114)
LINE = (201, 192, 170)
SEA = (16, 42, 74)
LAND = (44, 74, 99)

# v4.4: fonts are bundled in fonts/ next to this file so the entry
# renders identically on any machine (the grading image has no
# fonts-dejavu-extra, so DejaVuSansCondensed would be missing).
# Fall back to the system font dir if the bundled files are gone.
_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO_FONT_DIR = os.path.join(_HERE, "fonts")
_SYS_FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    path = os.path.join(_REPO_FONT_DIR, name)
    if not os.path.exists(path):
        path = os.path.join(_SYS_FONT_DIR, name)
    return ImageFont.truetype(path, size)


F_SERIF = lambda s: font("DejaVuSerif-Bold.ttf", s)          # noqa: E731
F_BOLD = lambda s: font("DejaVuSans-Bold.ttf", s)            # noqa: E731
F_REG = lambda s: font("DejaVuSans.ttf", s)                  # noqa: E731
F_COND = lambda s: font("DejaVuSansCondensed.ttf", s)        # noqa: E731
F_CONDB = lambda s: font("DejaVuSansCondensed-Bold.ttf", s)  # noqa: E731


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines, each <= max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def fit_block(draw, text, fnt, max_w, max_lines, leading, label):
    """Wrap and assert the text fits the allotted lines."""
    lines = wrap(draw, text, fnt, max_w)
    assert len(lines) <= max_lines, "%s needs %d lines, max %d: %r" % (
        label, len(lines), max_lines, text)
    return lines


# ---------------------------------------------------------------- data
NUMBERS = [
    ("372,000", "EVACUATED FROM AKVAN'S PATH"),
    ("0", "FOSSIL-FUEL MENTIONS IN COP31 DRAFT"),
    ("\u22125.28%", "NASDAQ FRIDAY CLOSE"),
    ("$3.79bn", "GTA VI DAY-ONE SALES (TAKE-TWO)"),
    ("100,000", "EU\u2013UK YOUTH PLACES A YEAR"),
    ("110", "MISSILES FIRED AT UKRAINE"),
]

# coloured region segments (v4.2): 9 of the live top 10 use coloured
# bars instead of plain text. Order matches REGION_COUNT.
REGION_COLORS = [("EUROPE", (46, 90, 136)), ("AMERICAS", (125, 60, 152)),
                 ("ASIA-PACIFIC", (176, 58, 46)), ("MIDEAST", (138, 90, 43)),
                 ("AFRICA", (30, 122, 52)), ("OCEANIA", (14, 124, 107)),
                 ("WORLD", (93, 109, 126))]

LEADS = [
    dict(n=1, kicker="ODISHA \u00b7 STORM \u2014 LANDFALL DONE",
         head="Akvan hits the coast \u2014 and spares Odisha",
         body=("Landfall near Gopalpur, 07:30\u201308:30 IST, winds 70\u201380 km/h "
               "gusting 90. Done by 11:20 IST; now a deep depression. "
               "372,000 evacuated, 9,341 shelters ready. No deaths, no major "
               "damage; heavy rain floods Berhampur."),
         src="IMD VIA REUTERS \u00b7 02:00 UTC \u00b7 REPORTED",
         scene="akvan", badge=None),
    dict(n=2, kicker="KYIV \u00b7 WAR \u2014 OVERNIGHT STRIKE",
         head="Three bridges hit in Kyiv's biggest bridge attack",
         body=("Overnight barrage of 110+ missiles and 400+ drones. Three "
               "bridges hit \u2014 Podilskyi, Darnytskyi, Pivdennyi. Nine "
               "killed across Ukraine, seven in Kyiv. Power cut in five "
               "districts."),
         src="REUTERS \u00b7 AP \u00b7 BBC \u00b7 REPORTED",
         scene="kyiv", badge="3 BRIDGES"),
    dict(n=3, kicker="ANTALYA \u00b7 CLIMATE \u2014 FINAL DAY",
         head="COP31 slips into overtime with no deal",
         body=("Talks pass their Friday deadline. The draft has zero "
               "fossil-fuel mentions; the $120bn adaptation target is gone. "
               "A call to triple adaptation finance by 2035 stays; the 1.5\u00b0C "
               "overshoot is admitted. Third draft due Saturday."),
         src="REUTERS \u00b7 AP \u00b7 UN NEWS \u00b7 REPORTED",
         scene="cop31", badge="OVERTIME"),
]

CARDS = [
    dict(n=4, kicker="NEW YORK",
         head="Wall Street closes deep in the red",
         body=("Dow 48,147 \u2212949.73 (\u22121.93%). S&P 6,910 \u2212265.44 "
               "(\u22123.70%), 7th straight fall. Nasdaq 22,618 "
               "\u22121,261.47 (\u22125.28%), negative for 2026."),
         src="REUTERS \u00b7 21:00 UTC", scene="usclose"),
    dict(n=5, kicker="ASIA",
         head="AI rout sweeps Asia's markets",
         body=("Nikkei \u22125.06% to 56,437. KOSPI \u22125.21% to 4,870. "
               "TAIEX \u22126.23% to 36,033. Worst week since 2020; "
               "SoftBank \u221214.48%."),
         src="CNBC \u00b7 ASIA CLOSE", scene="asiaai"),
    dict(n=6, kicker="MERCURY",
         head="BepiColombo set for Mercury orbit",
         body=("After eight years in space, the ESA\u2013JAXA probe enters "
               "Mercury orbit on Sat 21 Nov. Insertion is the key "
               "manoeuvre."),
         src="ESA \u00b7 FORECAST", scene="bepi"),
    dict(n=7, kicker="BRUSSELS",
         head="EU and UK agree a Brexit reset deal",
         body=("Food trade eased, worth up to \u00a35.1bn a year. Carbon "
               "markets link from 2028. 100,000 youth places a year; "
               "Erasmus+ returns."),
         src="REUTERS", scene="euuk"),
    dict(n=8, kicker="BEIJING",
         head="China holds lending rates again",
         body=("One-year LPR 3.0%, five-year 3.5% \u2014 unchanged for an "
               "18th straight month, as expected."),
         src="PBOC \u00b7 01:15 UTC", scene="lpr"),
    dict(n=9, kicker="WELLINGTON",
         head="Nicholls 175* and Phillips 118 rescue NZ",
         body=("A 216-run sixth-wicket stand lifts NZ to 368 all out. "
               "India reply 159/1 \u2014 Jaiswal 85, Rahul 52* \u2014 and "
               "trail by 209."),
         src="REUTERS \u00b7 DAY 2", scene="cricket"),
    dict(n=10, kicker="HORMUZ",
         head="UN counts the cost of the Hormuz attacks",
         body=("25 seafarers killed since February, 136 incidents to "
               "11 Nov. Iran's navy claims a tanker hit a mine off "
               "Khasab [CLAIM]."),
         src="UN \u00b7 AP \u00b7 REPORTED + CLAIM", scene="hormuz"),
    dict(n=11, kicker="SAN SALVADOR",
         head="Bukele files for an unprecedented third term",
         body=("Registered Thu night (Fri UTC) with VP Ulloa. Vote 28 Feb "
               "2027. Term limits were scrapped in 2025; four rivals stand."),
         src="REUTERS", scene="bukele"),
    dict(n=12, kicker="PACIFIC",
         head="Cyclone Xavier holds at Category 4",
         body=("922 hPa, about 200 km west of Manihiki. Nassau under storm "
               "alert. Drifting south and weakening, toward Samoa."),
         src="METSERVICE NZ \u00b7 11:20 FRI", scene="xavier"),
    dict(n=13, kicker="WASHINGTON",
         head="Trump's 90 minutes: Putin, data centres, 2028",
         body=("Defends calling Putin a 'friend'. 'Tremendous tax' on firms "
               "building data centres abroad. Floats Miller for president."),
         src="CNN \u00b7 WSJ \u00b7 17:00 UTC", scene="trump"),
]

BRIEFS = [
    (14, "ANT $88.91, \u22128.50% on day two; low $83.05, just above its $83 IPO price.", "AMERICAS"),
    (15, "Japan core CPI 2.2% in Oct, 2nd month above the BoJ's 2% target; headline 2.3%.", "ASIA-PACIFIC"),
    (16, "Italy: CGIL 24-hour general strike in 100+ cities; Landini says 1m+ marched.", "EUROPE"),
    (17, "Senegal: four dead, dozens missing after Wednesday's capsize off Yenne; search resumes.", "AFRICA"),
    (18, "GTA VI: Take-Two says $3.79bn day-one sales, 32.5m copies \u2014 biggest launch ever.", "WORLD"),
    (19, "Turin: Medvedev beats Tiafoe 6-3, 6-4; faces Zverev in Saturday's semi-final.", "EUROPE"),
    (20, "Turin: Alcaraz beats Cobolli 6-4, 6-1, tops group 3-0; meets Shelton in the semi.", "EUROPE"),
    (21, "Las Vegas: Russell fastest in wet FP2, 1:47.272; Gasly +0.071, Leclerc third.", "AMERICAS"),
    (22, "Wellington: India 159/1 at stumps on day 2 \u2014 Jaiswal 85, Rahul 52*; trail by 209.", "ASIA-PACIFIC"),
    (23, "SoftBank \u221214.48%, worst day since Aug 2024, as AI holdings slide.", "ASIA-PACIFIC"),
    (24, "Nasdaq 100 \u22125.61% to 25,028.98; worst week since March 2020.", "AMERICAS"),
    (25, "Hang Seng \u22121.89% to 22,410.80; Shanghai \u22121.22% to 3,533.79.", "ASIA-PACIFIC"),
    (26, "Dow \u22128% on the week, worst since March 2020; S&P \u22128.6%, Nasdaq \u221210%.", "AMERICAS"),
    (27, "TAIEX \u221217.5% on the week, its worst since 1991.", "ASIA-PACIFIC"),
    (28, "Trump administration drops its lawsuit over Peltola's Alaska Senate win.", "AMERICAS"),
    (29, "Poland: two Russian missiles and a drone land in the south-east; Tusk calls it a provocation.", "EUROPE"),
    (30, "Kenya: drilling starts at Turkana's first oil well; first crude due 1 Dec.", "AFRICA"),
    (31, "COP31: 12 nations, incl. France and Panama, demand a fossil-fuel phase-out.", "WORLD"),
    (32, "COP31: third draft of the final text due Saturday morning after all-night talks.", "WORLD"),
    (33, "Akvan: 4,467 pregnant women moved to safety; 1,452 have delivered, all safe.", "ASIA-PACIFIC"),
    (34, "Nvidia \u221214% to a 52-week low as chip stocks crater.", "AMERICAS"),
    (35, "Chip stocks suffer a $2.3tn weekly wipeout, MarketWatch reports.", "WORLD"),
    (36, "Pancreatic cancer pill: tumours shrank in 60.7% of 61 trial patients.", "WORLD"),
]

TIMELINE = [
    ("01:15 UTC", "China holds its lending rates"),
    ("02:00 UTC", "Akvan crosses the coast at Gopalpur"),
    ("06:00 UTC", "Nikkei closes \u22125.06% in Tokyo"),
    ("17:00 UTC", "Trump holds his 90-minute press conference"),
    ("21:00 UTC", "Wall Street closes: Nasdaq \u22125.28%"),
]

DATECHECK_L1 = ("BROKE BEFORE FRIDAY: the Shenzhen trilateral itself \u00b7 Riyadh PIF "
                "Tower strike \u00b7 Kerch Bridge attack \u00b7 Van Gogh $190.4m sale \u00b7 "
                "Hayabusa2 retarget \u00b7 Korea exports $1tn \u00b7 ICJ Myanmar verdict "
                "itself \u00b7 Anthropic $83 IPO / $97.17 debut close \u00b7 GTA VI midnight "
                "launch \u00b7 Voyager 1 one-light-day \u00b7 Trump Iran-to-2027 decision "
                "(disputed).")
DATECHECK_L2 = ("NOT YET \u2014 SATURDAY: COP31 final deal (talks in overtime) \u00b7 Las "
                "Vegas GP qualifying (Sat 11:00 WIB) \u00b7 BepiColombo Mercury orbit "
                "insertion.")

TOMORROW = ("TOMORROW \u2014 SAT 21 NOV:  COP31 third draft  \u00b7  BepiColombo "
            "enters Mercury orbit  \u00b7  Las Vegas GP qualifying + race  \u00b7  "
            "ATP semis: Zverev\u2013Medvedev, Alcaraz\u2013Shelton.")

FOOTER = ("Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 BBC \u00b7 IMD \u00b7 ATP Tour \u00b7 MetService NZ "
          "\u00b7 Take-Two \u00b7 PBoC \u00b7 Bank of Japan.  Every story here happened, or "
          "was first reported, on Friday 20 November 2026 in at least one time zone.  "
          "HOW SURE: REPORTED = confirmed  \u00b7  CLAIM = one side's account, "
          "unverified  \u00b7  FORECAST = scheduled.")

# nameplate banners (typography round v4.1): big white-on-red labels.
LEAD_BANNERS = {1: "CYCLONE AKVAN", 2: "KYIV", 3: "COP31"}
CARD_BANNERS = {4: "WALL STREET", 5: "AI SELL-OFF", 6: "MERCURY",
                7: "EU-UK", 8: "CHINA", 9: "CRICKET", 10: "HORMUZ",
                11: "BUKELE", 12: "XAVIER", 13: "TRUMP"}
TICKER = ("KYIV'S THREE BRIDGES HIT  \u00b7  AKVAN MAKES LANDFALL  \u00b7  "
          "MARKETS IN AI SELL-OFF  \u00b7  COP31 IN OVERTIME")

# region tallies, recomputed from the lists above (asserted in build())
REGION_COUNT = {"EUROPE": 6, "AMERICAS": 9, "ASIA-PACIFIC": 9,
                "MIDEAST": 1, "AFRICA": 2, "OCEANIA": 2, "WORLD": 7}

# ---------------------------------------------------------------- scenes
# Every scene is drawn from primitives. Dark panels for the leads,
# small dark scene bands for the cards.

def _spiral(draw, cx, cy, r0, r1, turns, color, width=2):
    import math
    pts = []
    steps = int(turns * 40)
    for i in range(steps + 1):
        t = i / steps
        r = r0 + (r1 - r0) * t
        a = t * turns * 2 * math.pi
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.line(pts, fill=color, width=width)


def _chip(draw, x, y, text, fnt, bg, fg):
    w = draw.textlength(text, font=fnt) + 12
    h = fnt.size + 8
    draw.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=bg)
    draw.text((x + 6, y + 4), text, font=fnt, fill=fg)
    return w


def scene_akvan(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=SEA)
    # lighter sea bands
    for i, yy in enumerate(range(y + 8, y + h - 8, 14)):
        draw.line([x + 6, yy, x + w - 6, yy], fill=(24, 58, 96), width=1)
    # land mass (Odisha coast) on the right
    land = [(x + w * 0.62, y), (x + w, y + 4), (x + w, y + h),
            (x + w * 0.70, y + h), (x + w * 0.66, y + h * 0.62),
            (x + w * 0.58, y + h * 0.34)]
    draw.polygon(land, fill=LAND)
    draw.line(land + [land[0]], fill=(120, 160, 190), width=1)
    draw.text((x + w - 108, y + 6), "BAY OF BENGAL", font=F_BOLD(8),
              fill=(150, 180, 210))
    # cyclone spiral sitting on the coast
    _spiral(draw, x + w * 0.58, y + h * 0.52, 3, 34, 2.6, (255, 255, 255), 2)
    draw.ellipse([x + w * 0.58 - 4, y + h * 0.52 - 4, x + w * 0.58 + 4,
                  y + h * 0.52 + 4], fill=GOLD_LT)
    # Gopalpur dot + label
    gx, gy = x + w * 0.66, y + h * 0.44
    draw.ellipse([gx - 4, gy - 4, gx + 4, gy + 4], fill=RED,
                 outline=(255, 255, 255))
    draw.text((gx + 8, gy - 5), "GOPALPUR", font=F_BOLD(8), fill=(255, 255, 255))
    # rain streaks over land
    for i in range(7):
        rx = x + w * 0.72 + i * 12
        ry = y + h * 0.55 + (i % 3) * 10
        draw.line([rx, ry, rx - 3, ry + 9], fill=(170, 200, 225), width=1)
    _chip(draw, x + 8, y + h - 24, "372,000 EVACUATED", F_BOLD(8), GOLD, NAVY_DARK)


def scene_kyiv(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(13, 21, 38))
    for sx, sy in [(18, 12), (60, 26), (120, 10), (180, 22), (240, 14),
                   (280, 30), (90, 34), (210, 8)]:
        draw.ellipse([x + sx, y + sy, x + sx + 1, y + sy + 1],
                     fill=(200, 210, 230))
    # skyline silhouettes
    base = y + h - 26
    # scale to the scene height so the tallest tower never clips the top
    _s = (h - 30) / 70.0
    heights = [int(v * _s) for v in [34, 52, 28, 62, 44, 70, 38, 56, 30, 48]]
    bx = x + 4
    for i, hh in enumerate(heights):
        bw = (w - 8) // 10
        draw.rectangle([bx, base - hh, bx + bw - 2, base], fill=(8, 14, 26))
        for wy in range(base - hh + 6, base - 4, 9):
            draw.rectangle([bx + 3, wy, bx + 5, wy + 2], fill=GOLD)
        bx += bw
    # river band + three BRIGHT bridge diagrams (v4.4): white deck,
    # white arch and piers on dark blue, fire glowing on each span
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=(10, 32, 60))
    for i, cx in enumerate([0.22, 0.5, 0.78]):
        cxp = x + w * cx
        draw.line([cxp - 40, y + h - 26, cxp + 40, y + h - 26],
                  fill=(255, 255, 255), width=2)
        draw.arc([cxp - 34, y + h - 46, cxp + 34, y + h - 6], 180, 360,
                 fill=(255, 255, 255), width=3)
        draw.line([cxp - 34, y + h - 26, cxp - 34, y + h - 6],
                  fill=(255, 255, 255), width=2)
        draw.line([cxp + 34, y + h - 26, cxp + 34, y + h - 6],
                  fill=(255, 255, 255), width=2)
        # fire on the span: glowing dot + flame
        fx, fy = cxp, y + h - 32
        draw.ellipse([fx - 6, fy - 6, fx + 6, fy + 6], fill=(255, 140, 40))
        draw.polygon([(fx, fy - 12), (fx - 6, fy + 2), (fx + 6, fy + 2)],
                     fill=(255, 140, 40))
        draw.polygon([(fx, fy - 6), (fx - 3, fy + 2), (fx + 3, fy + 2)],
                     fill=(255, 210, 80))
    # missile trails
    for tx, ty, ln in [(40, 30, 46), (150, 18, 58), (250, 36, 40)]:
        draw.line([x + tx, y + ty, x + tx + ln, y + ty - 16],
                  fill=(255, 255, 255), width=2)
        draw.ellipse([x + tx + ln - 2, y + ty - 18, x + tx + ln + 2,
                      y + ty - 14], fill=GOLD_LT)


def scene_cop31(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(15, 30, 52))
    # conference hall: rows of delegate dots
    for row in range(3):
        for col in range(14):
            dx = x + 14 + col * 19
            dy = y + h - 34 + row * 9
            draw.ellipse([dx, dy, dx + 3, dy + 3], fill=(120, 150, 190))
    # globe with visible continents (v4.4): green landmasses on blue,
    # not a plain disc — reads as climate at a glance
    gx, gy, gr = x + 62, y + 46, 30
    draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(38, 110, 160),
                 outline=(140, 190, 220), width=2)
    _land = (86, 190, 110)
    draw.ellipse([gx - 24, gy - 14, gx - 10, gy + 2], fill=_land)
    draw.polygon([(gx - 10, gy - 18), (gx + 2, gy - 22), (gx + 8, gy - 10),
                  (gx - 2, gy - 6)], fill=_land)
    draw.ellipse([gx + 2, gy - 8, gx + 16, gy + 10], fill=_land)
    draw.ellipse([gx + 12, gy - 18, gx + 26, gy - 4], fill=_land)
    draw.ellipse([gx - 16, gy + 12, gx - 2, gy + 24], fill=_land)
    draw.arc([gx - gr, gy - gr, gx + gr, gy + gr], 200, 340,
             fill=(90, 200, 120), width=3)
    draw.arc([gx - gr, gy - gr, gx + gr, gy + gr], 20, 120,
             fill=(90, 200, 120), width=3)
    draw.line([gx - gr, gy, gx + gr, gy], fill=(140, 190, 220), width=1)
    # thermometer
    tx = x + w - 46
    draw.rounded_rectangle([tx, y + 14, tx + 12, y + h - 44], radius=6,
                           fill=(230, 235, 240), outline=(150, 170, 200))
    draw.ellipse([tx - 5, y + h - 52, tx + 17, y + h - 28],
                 fill=(230, 235, 240), outline=(150, 170, 200))
    draw.rectangle([tx + 3, y + 34, tx + 9, y + h - 40], fill=RED)
    draw.ellipse([tx - 1, y + h - 48, tx + 13, y + h - 32], fill=RED)
    draw.text((tx - 34, y + 16), "1.5\u00b0C", font=F_BOLD(9), fill=(255, 255, 255))
    # (the OVERTIME chip is drawn on the lead nameplate banner by build())


def _band(draw, x, y, w, h, color):
    draw.rectangle([x, y, x + w, y + h], fill=color)


def scene_usclose(draw, x, y, w, h):
    _band(draw, x, y, w, h, NAVY_DARK)
    # falling line chart
    pts = [(x + 6 + i * (w - 12) / 5, y + 8 + i * (h - 16) / 5 * 1.15)
           for i in range(6)]
    draw.line(pts, fill=(255, 90, 70), width=2)
    # red candlesticks
    for i in range(4):
        cx = x + 14 + i * (w - 28) / 3
        top = y + 8 + i * 7
        draw.rectangle([cx - 3, top, cx + 3, top + 14], fill=(255, 90, 70))
        draw.line([cx, top - 4, cx, top + 18], fill=(255, 90, 70), width=1)
    draw.text((x + 6, y + h - 13), "\u22125.28% NASDAQ", font=F_BOLD(8),
              fill=(255, 255, 255))


def scene_asiaai(draw, x, y, w, h):
    _band(draw, x, y, w, h, NAVY_DARK)
    pts = [(x + 6, y + 8), (x + w * 0.3, y + 12), (x + w * 0.55, y + 22),
           (x + w * 0.8, y + 30), (x + w - 6, y + h - 8)]
    draw.line(pts, fill=(255, 90, 70), width=2)
    for i, v in enumerate([0.55, 0.75, 1.0]):
        bx = x + 8 + i * 58
        bh = 8 + v * 18
        draw.rectangle([bx, y + h - 6 - bh, bx + 16, y + h - 6],
                       fill=(255, 120, 90))


def scene_bepi(draw, x, y, w, h):
    _band(draw, x, y, w, h, (8, 10, 18))
    for sx, sy in [(12, 8), (40, 20), (90, 6), (140, 16), (170, 10)]:
        draw.ellipse([x + sx, y + sy, x + sx + 1, y + sy + 1], fill=(220, 220, 220))
    # Mercury: cratered disc (v4.4) — proper circle with pits and a
    # darker night side, not a brown blob
    cx, cy, r = x + w - 34, y + h // 2, 15
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(205, 140, 70),
                 outline=(245, 190, 120), width=2)
    draw.pieslice([cx - r, cy - r, cx + r, cy + r], 90, 270,
                  fill=(150, 85, 30))
    for (ox, oy, cr) in [(-6, -5, 3), (4, -7, 2), (6, 3, 3), (-2, 6, 2),
                         (1, 0, 2), (-8, 2, 2)]:
        draw.ellipse([cx + ox - cr, cy + oy - cr, cx + ox + cr,
                      cy + oy + cr], fill=(140, 75, 25))
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(245, 190, 120),
                 width=2)
    # orbit + probe
    draw.arc([x + 8, y + 4, x + w - 40, y + h - 4], 90, 330, fill=(150, 170, 200),
             width=1)
    px, py = x + 26, y + h - 16
    draw.rectangle([px - 4, py - 3, px + 4, py + 3], fill=(220, 225, 235))
    draw.line([px - 9, py, px - 4, py], fill=GOLD, width=2)
    draw.line([px + 4, py, px + 9, py], fill=GOLD, width=2)
    # (no in-scene date label: the card nameplate banner occupies the top-left;
    # the date is in the headline)


def scene_euuk(draw, x, y, w, h):
    _band(draw, x, y, w, h, (24, 48, 84))
    # EU flag
    draw.rectangle([x + 8, y + 6, x + 78, y + h - 16], fill=(20, 60, 160))
    for i in range(8):
        import math
        a = i * math.pi / 4
        sx = x + 43 + 14 * math.cos(a)
        sy = y + h // 2 - 5 + 14 * math.sin(a)
        draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 220, 60))
    # UK flag (simplified cross)
    draw.rectangle([x + 86, y + 6, x + 156, y + h - 16], fill=(20, 40, 110))
    draw.rectangle([x + 114, y + 6, x + 128, y + h - 16], fill=(255, 255, 255))
    draw.rectangle([x + 86, y + h // 2 - 12, x + 156, y + h // 2 + 2],
                   fill=(255, 255, 255))
    draw.rectangle([x + 118, y + 6, x + 124, y + h - 16], fill=RED)
    draw.rectangle([x + 86, y + h // 2 - 8, x + 156, y + h // 2 - 2], fill=RED)
    draw.text((x + w - 52, y + h - 14), "100,000", font=F_BOLD(8), fill=GOLD_LT)


def scene_lpr(draw, x, y, w, h):
    _band(draw, x, y, w, h, (28, 44, 66))
    cx, cy, r = x + w // 2, y + h - 8, 26
    draw.arc([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=(200, 210, 225),
             width=3)
    for i, lab in enumerate(["0", "3.0", "6"]):
        import math
        a = math.pi + i * math.pi / 2
        lx = cx + (r + 8) * math.cos(a) - 6
        ly = cy + (r + 8) * math.sin(a) - 5
        draw.text((lx, ly), lab, font=F_BOLD(7), fill=(200, 210, 225))
    # needle at 3.0% (middle)
    draw.line([cx, cy, cx, cy - r + 4], fill=RED, width=3)
    draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=GOLD)
    draw.text((x + 6, y + h - 13), "18TH HOLD", font=F_BOLD(8), fill=GOLD_LT)


def scene_cricket(draw, x, y, w, h):
    _band(draw, x, y, w, h, (18, 80, 44))
    # stadium arcs
    for r in (10, 18, 26):
        draw.arc([x + w // 2 - r, y + h - r - 4, x + w // 2 + r, y + h + r - 4],
                 180, 360, fill=(140, 200, 140), width=1)
    # bat + ball
    draw.polygon([(x + 30, y + 8), (x + 38, y + 6), (x + 52, y + 30),
                  (x + 44, y + 34)], fill=(190, 140, 80))
    draw.ellipse([x + 120, y + 10, x + 128, y + 18], fill=(200, 40, 30),
                 outline=(255, 255, 255))
    draw.text((x + w - 78, y + h - 14), "118  \u00b7  175*", font=F_BOLD(9),
              fill=(255, 255, 255))


def scene_hormuz(draw, x, y, w, h):
    _band(draw, x, y, w, h, (16, 52, 84))
    for i in range(4):
        wy = y + 8 + i * 8
        draw.line([x + 4, wy, x + w - 4, wy], fill=(40, 90, 130), width=1)
    # tanker silhouette
    draw.rectangle([x + 22, y + 18, x + 130, y + 30], fill=(10, 16, 26))
    draw.rectangle([x + 100, y + 8, x + 118, y + 18], fill=(10, 16, 26))
    draw.line([x + 108, y + 2, x + 108, y + 8], fill=(10, 16, 26), width=2)
    # mine + fire
    mx, my = x + 148, y + 26
    draw.ellipse([mx - 4, my - 4, mx + 4, my + 4], fill=(30, 30, 30),
                 outline=(200, 200, 200))
    draw.polygon([(mx, my - 12), (mx - 4, my - 2), (mx + 4, my - 2)],
                 fill=(255, 140, 40))
    _chip(draw, x + w - 48, y + 2, "CLAIM", F_BOLD(7), RED, (255, 255, 255))


def scene_bukele(draw, x, y, w, h):
    _band(draw, x, y, w, h, (34, 52, 84))
    # ballot box
    draw.rectangle([x + 56, y + 16, x + 132, y + h - 6], fill=(18, 35, 63),
                   outline=(200, 210, 225))
    draw.rectangle([x + 76, y + 12, x + 112, y + 17], fill=(200, 210, 225))
    # slip going in
    draw.polygon([(x + 84, y + 2), (x + 104, y + 2), (x + 102, y + 14),
                  (x + 82, y + 14)], fill=(255, 255, 255))
    draw.text((x + 88, y + 5), "\u2713", font=F_BOLD(8), fill=RED)
    draw.text((x + 8, y + h - 14), "28 FEB 2027", font=F_BOLD(8), fill=GOLD_LT)


def scene_xavier(draw, x, y, w, h):
    _band(draw, x, y, w, h, (14, 46, 78))
    # island
    draw.polygon([(x + 120, y + h - 6), (x + 150, y + h - 22),
                  (x + 176, y + h - 6)], fill=(40, 90, 60))
    _spiral(draw, x + 62, y + h // 2 + 2, 2, 26, 2.4, (255, 255, 255), 2)
    draw.ellipse([x + 58, y + h // 2 - 2, x + 66, y + h // 2 + 6],
                 fill=GOLD_LT)
    draw.text((x + w - 46, y + 2), "CAT 4", font=F_BOLD(9), fill=(255, 255, 255))


def scene_trump(draw, x, y, w, h):
    _band(draw, x, y, w, h, (40, 44, 66))
    # podium
    draw.polygon([(x + 70, y + 16), (x + 118, y + 16), (x + 126, y + h - 4),
                  (x + 62, y + h - 4)], fill=(20, 30, 52))
    draw.rectangle([x + 70, y + 16, x + 118, y + 22], fill=(120, 30, 26))
    # mic
    draw.line([x + 88, y + 6, x + 88, y + 16], fill=(200, 200, 200), width=2)
    draw.ellipse([x + 84, y + 2, x + 92, y + 10], fill=(220, 220, 220))
    # small US flag
    for i in range(4):
        draw.rectangle([x + 8, y + 16 + i * 5, x + 48, y + 20 + i * 5],
                       fill=RED if i % 2 == 0 else (255, 255, 255))
    draw.rectangle([x + 8, y + 16, x + 22, y + 26], fill=(20, 40, 110))
    draw.text((x + w - 52, y + h - 14), "90 MIN", font=F_BOLD(8), fill=GOLD_LT)


LEAD_SCENES = {"akvan": scene_akvan, "kyiv": scene_kyiv, "cop31": scene_cop31}
CARD_SCENES = {"usclose": scene_usclose, "asiaai": scene_asiaai,
               "bepi": scene_bepi, "euuk": scene_euuk, "lpr": scene_lpr,
               "cricket": scene_cricket, "hormuz": scene_hormuz,
               "bukele": scene_bukele, "xavier": scene_xavier,
               "trump": scene_trump}

# ---------------------------------------------------------------- map
LAND_BOXES = [
    (-168, 15, -100, 71), (-100, 25, -60, 60), (-100, 8, -80, 18),
    (-58, 60, -20, 83), (-80, -55, -35, 11),
    (-18, -35, 35, 32), (35, -5, 51, 12),
    (-10, 36, 32, 70), (32, 42, 180, 76), (35, 12, 60, 42),
    (68, 8, 89, 35), (92, 5, 108, 28), (95, -10, 141, 6),
    (113, -39, 154, -11), (166, -47, 178, -34),
    (43, -25, 50, -12), (129, 31, 146, 45), (-5, 50, 2, 58),
]

# (lon, lat, number, tag dx, tag dy, dot dx, dot dy) — pin 6 is in space.
PINS = [
    (84.9, 19.3, 1, 8, -12, 0, 0), (30.5, 50.5, 2, -16, -10, 0, 0),
    (30.7, 36.9, 3, 12, 8, 0, 0), (-74.0, 40.7, 4, -24, -12, 0, 0),
    (139.7, 35.7, 5, 8, -12, 0, 0), (4.35, 50.85, 7, 8, -12, 0, 0),
    (116.4, 39.9, 8, -20, -10, 0, 0), (174.8, -41.3, 9, -22, -12, 0, 0),
    (56.5, 26.5, 10, 8, -12, 0, 0), (-89.2, 13.7, 11, 8, -12, 0, 0),
    (-161.0, -10.4, 12, 8, -12, 0, 0), (-77.0, 38.9, 13, 16, 8, 9, 5),
]


def draw_map(draw, x, y, w, h):
    # v4.4: light cream panel + warm-tan land dots (ranks 1/2/10 use a
    # light map); red pins with white numbers stay.
    draw.rectangle([x, y, x + w, y + h], fill=(233, 226, 203),
                   outline=LINE, width=1)
    lon0, lon1, lat0, lat1 = -180, 180, 78, -58

    def px(lon):
        return x + (lon - lon0) / (lon1 - lon0) * w

    def py(lat):
        return y + (lat0 - lat) / (lat0 - lat1) * h

    lon = -178
    while lon <= 178:
        lat = -56
        while lat <= 76:
            if any(a <= lon <= c and b <= lat <= d
                   for (a, b, c, d) in LAND_BOXES):
                draw.ellipse([px(lon) - 1, py(lat) - 1, px(lon) + 1,
                              py(lat) + 1], fill=(176, 156, 110))
            lat += 6
        lon += 4
    for (lon, lat, n, dx, dy, odx, ody) in PINS:
        cx, cy = px(lon), py(lat)
        if odx or ody:
            draw.line([cx, cy, cx + odx, cy + ody], fill=RED, width=1)
            cx, cy = cx + odx, cy + ody
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED,
                     outline=(255, 255, 255))
        tx, ty = cx + dx, cy + dy
        draw.line([cx, cy, tx + 6, ty + 5], fill=RED, width=1)
        draw.rounded_rectangle([tx, ty, tx + 13, ty + 11], radius=2, fill=RED)
        draw.text((tx + 3.5, ty + 1), str(n), font=F_BOLD(8),
                  fill=(255, 255, 255))


# ---------------------------------------------------------------- layout
REGION_OF = {1: "ASIA-PACIFIC", 2: "EUROPE", 3: "WORLD", 4: "AMERICAS",
             5: "ASIA-PACIFIC", 6: "WORLD", 7: "EUROPE", 8: "ASIA-PACIFIC",
             9: "OCEANIA", 10: "MIDEAST", 11: "AMERICAS", 12: "OCEANIA",
             13: "AMERICAS"}


def build(out_path):
    # --- counts ------------------------------------------------------
    nums = [d["n"] for d in LEADS] + [d["n"] for d in CARDS] + \
           [n for (n, _, _) in BRIEFS]
    assert nums == list(range(1, 37)), "story numbers not 1..36: %r" % nums
    assert len(BRIEFS) == 23 and len(CARDS) == 10 and len(LEADS) == 3
    counts = {}
    for d in LEADS + CARDS:
        counts[REGION_OF[d["n"]]] = counts.get(REGION_OF[d["n"]], 0) + 1
    for (_, _, r) in BRIEFS:
        counts[r] = counts.get(r, 0) + 1
    assert counts == REGION_COUNT, "region tallies %r" % counts
    assert sum(counts.values()) == 36

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- top bar -----------------------------------------------------
    d.text((M, 8), "THE WORLD IN ONE DAY", font=F_BOLD(14), fill=INK)
    rt = "36 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE FROM THIS FRIDAY"
    d.text((W - M - d.textlength(rt, font=F_BOLD(9)), 11), rt,
           font=F_BOLD(9), fill=MUTED)
    d.line([M, 28, W - M, 28], fill=INK, width=2)

    # --- masthead ----------------------------------------------------
    head = "Friday 20 November 2026"
    d.text(((W - d.textlength(head, font=F_SERIF(40))) / 2, 32), head,
           font=F_SERIF(40), fill=INK)
    # news ticker of the four biggest stories (v4.1); the 36-story count
    # stays in the top bar.
    assert d.textlength(TICKER, font=F_BOLD(13)) <= CW, \
        "ticker too long: %d" % d.textlength(TICKER, font=F_BOLD(13))
    d.text(((W - d.textlength(TICKER, font=F_BOLD(13))) / 2, 76), TICKER,
           font=F_BOLD(13), fill=RED)

    # --- numbers strip (v4.1: numbers enlarged 20 -> 27) -------------
    y0, y1 = 92, 148
    cw6 = CW / 6
    for i, (num, lab) in enumerate(NUMBERS):
        cx = M + i * cw6
        if i:
            d.line([cx, y0 + 4, cx, y1 - 4], fill=LINE, width=1)
        nw = d.textlength(num, font=F_BOLD(27))
        assert nw <= cw6 - 8, "number %r too wide: %d" % (num, nw)
        d.text((cx + (cw6 - nw) / 2, y0 + 2), num, font=F_BOLD(27),
               fill=RED if i in (1, 2) else INK)
        lab_lines = fit_block(d, lab, F_BOLD(9), cw6 - 14, 2, 11,
                              "number label %r" % lab)
        ly = y0 + 32
        for ln in lab_lines:
            lw = d.textlength(ln, font=F_BOLD(9))
            d.text((cx + (cw6 - lw) / 2, ly), ln, font=F_BOLD(9), fill=MUTED)
            ly += 11
    d.line([M, y1, W - M, y1], fill=LINE, width=1)

    # --- region strip (v4.2: coloured segments) ----------------------
    segw = CW / len(REGION_COLORS)
    for i, (rname, rcol) in enumerate(REGION_COLORS):
        sx = M + i * segw
        d.rectangle([sx, 153, sx + segw, 167], fill=rcol)
        lab = "%s %d" % (rname, REGION_COUNT[rname])
        lw = d.textlength(lab, font=F_CONDB(8))
        assert lw <= segw - 8, "region label %r too wide: %d" % (lab, lw)
        d.text((sx + (segw - lw) / 2, 155), lab, font=F_CONDB(8),
               fill=(255, 255, 255))

    # --- leads (v4.3: scene on top, headline + body BELOW the scene on
    # cream, dark serif — the structure every live top-10 entry uses) --
    lead_y, lead_h, lead_w, gap = 172, 258, 316, 10
    scene_h = 100
    for i, ld in enumerate(LEADS):
        x = M + i * (lead_w + gap)
        # dark panel covers only the scene (banner + art); the text below
        # sits on the page cream, like the top 10.
        d.rectangle([x, lead_y, x + lead_w, lead_y + 3 + 20 + scene_h],
                    fill=NAVY_DARK)
        d.rectangle([x, lead_y, x + lead_w, lead_y + 3], fill=RED)
        sy = lead_y + 3
        # v4.1 nameplate: big white-on-red story name across the scene top
        d.rectangle([x + 10, sy, x + lead_w - 10, sy + 20], fill=RED)
        d.text((x + 18, sy + 3), LEAD_BANNERS[ld["n"]], font=F_BOLD(13),
               fill=(255, 255, 255))
        LEAD_SCENES[ld["scene"]](d, x + 10, sy + 20, lead_w - 20, scene_h)
        if ld["badge"]:
            _chip(d, x + lead_w - 92, sy + 2, ld["badge"], F_BOLD(9), GOLD,
                  NAVY_DARK)
        # kicker with the story number in a red disc, below the scene
        ky = lead_y + 130
        d.ellipse([x + 10, ky, x + 22, ky + 12], fill=RED)
        _nt = str(ld["n"])
        d.text((x + 10 + (12 - d.textlength(_nt, font=F_BOLD(9))) / 2, ky + 1),
               _nt, font=F_BOLD(9), fill=(255, 255, 255))
        d.text((x + 28, ky), ld["kicker"], font=F_BOLD(10), fill=RED)
        # headline: dark serif on cream. 20px is the max that fits the
        # longest headline (Kyiv, 48 chars) in 2 lines; 22px needs 3.
        hl = fit_block(d, ld["head"], F_SERIF(20), lead_w - 20, 2, 22,
                       "lead %d headline" % ld["n"])
        draw_lines(d, hl, x + 10, lead_y + 144, F_SERIF(20), INK, 22)
        bl = fit_block(d, ld["body"], F_REG(10), lead_w - 20, 4, 13,
                       "lead %d body" % ld["n"])
        by_end = draw_lines(d, bl, x + 10, lead_y + 192, F_REG(10), INK, 13)
        d.text((x + 10, by_end + 4), ld["src"], font=F_BOLD(8), fill=MUTED)

    # --- cards (2 rows x 5) ------------------------------------------
    card_w, card_h, cgap, rgap = 188, 127, 7, 6
    card_y0 = 436
    for row in range(2):
        for col in range(5):
            cd = CARDS[row * 5 + col]
            x = M + col * (card_w + cgap)
            y = card_y0 + row * (card_h + rgap)
            d.rectangle([x, y, x + card_w, y + card_h], fill=CREAM,
                        outline=LINE, width=1)
            CARD_SCENES[cd["scene"]](d, x + 1, y + 1, card_w - 2, 40)
            # v4.1 nameplate: same red banner label as the leads
            _blab = CARD_BANNERS[cd["n"]]
            _bw = d.textlength(_blab, font=F_BOLD(9)) + 10
            d.rectangle([x + 1, y + 1, x + 1 + _bw, y + 15], fill=RED)
            d.text((x + 5, y + 3), _blab, font=F_BOLD(9),
                   fill=(255, 255, 255))
            d.text((x + 6, y + 45), cd["kicker"], font=F_BOLD(8), fill=RED)
            sw = d.textlength(cd["src"], font=F_REG(7))
            assert d.textlength(cd["kicker"], font=F_BOLD(8)) + 6 + sw \
                <= card_w - 12, "card %d kicker/src overlap" % cd["n"]
            d.text((x + card_w - 6 - sw, y + 46), cd["src"], font=F_REG(7),
                   fill=MUTED)
            hl = fit_block(d, cd["head"], F_SERIF(12), card_w - 12, 2, 13,
                           "card %d headline" % cd["n"])
            draw_lines(d, hl, x + 6, y + 58, F_SERIF(12), INK, 13)
            bl = fit_block(d, cd["body"], F_REG(9), card_w - 12, 4, 11,
                           "card %d body" % cd["n"])
            draw_lines(d, bl, x + 6, y + 86, F_REG(9), INK, 11)

    # --- map + UTC timeline ------------------------------------------
    map_y = 700
    d.text((M, map_y), "THE WORLD \u2014 WHERE IT HAPPENED  (PINS 1\u20135, 7\u201313; "
           "6 IS IN SPACE)", font=F_BOLD(9), fill=INK)
    draw_map(d, M, map_y + 14, 562, 58)
    tx = M + 578
    d.text((tx, map_y), "THE DAY IN UTC", font=F_BOLD(9), fill=INK)
    ty = map_y + 14
    for (t, txt) in TIMELINE:
        d.text((tx, ty), t, font=F_BOLD(9), fill=RED)
        d.text((tx + 62, ty), txt, font=F_REG(9), fill=INK)
        ty += 11

    # --- briefs -------------------------------------------------------
    b_y = 780
    d.text((M, b_y), "ALSO ON FRIDAY 20 NOVEMBER", font=F_BOLD(11), fill=INK)
    d.line([M + 218, b_y + 7, W - M, b_y + 7], fill=LINE, width=1)
    cols = [(M, 474), (M + 494, 480)]
    for ci, (bx, bw) in enumerate(cols):
        items = BRIEFS[ci * 12:(ci + 1) * 12] if ci == 0 else BRIEFS[12:]
        yy = b_y + 16
        for (n, txt, _r) in items:
            num = "%d  " % n
            nw = d.textlength(num, font=F_CONDB(10))
            assert d.textlength(txt, font=F_COND(10)) <= bw - nw - 2, \
                "brief %d too long: %r" % (n, txt)
            d.text((bx, yy), num, font=F_CONDB(10), fill=RED)
            d.text((bx + nw, yy), txt, font=F_COND(10), fill=INK)
            yy += 11
    assert yy <= 928, "briefs overflow to %d" % yy

    # --- date check ----------------------------------------------------
    dc_y = 930
    d.rectangle([M, dc_y, W - M, dc_y + 52], outline=RED, width=1)
    d.text((M + 8, dc_y + 4), "DATE CHECK \u2014 DELIBERATELY NOT SHOWN",
           font=F_BOLD(10), fill=RED)
    l1 = fit_block(d, DATECHECK_L1, F_REG(9), CW - 16, 2, 11, "datecheck l1")
    draw_lines(d, l1, M + 8, dc_y + 18, F_REG(9), INK, 11)
    l2 = fit_block(d, DATECHECK_L2, F_REG(9), CW - 16, 1, 11, "datecheck l2")
    draw_lines(d, l2, M + 8, dc_y + 40, F_REG(9), INK, 11)

    # --- tomorrow + footer --------------------------------------------
    assert d.textlength(TOMORROW, font=F_BOLD(10)) <= CW, \
        "tomorrow line too long: %d" % d.textlength(TOMORROW, font=F_BOLD(10))
    d.text((M, 986), TOMORROW, font=F_BOLD(10), fill=INK)
    fl = fit_block(d, FOOTER, F_REG(8), CW, 2, 10, "footer")
    draw_lines(d, fl, M, 1002, F_REG(8), MUTED, 10)
    assert 1002 + len(fl) * 10 <= 1023, "footer overflow"

    img.save(out_path, "PNG", optimize=True)
    data = open(out_path, "rb").read()
    print("wrote %s  %dx%d  %d bytes  sha256=%s" % (
        out_path, W, H, len(data), hashlib.sha256(data).hexdigest()))
    assert len(data) <= 1024 * 1024, "entry.png over 1 MiB"
    return out_path


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    build(os.path.join(here, "entry.png"))
