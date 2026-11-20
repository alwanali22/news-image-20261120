#!/usr/bin/env python3
"""draw_v3.py — news-image-20261120 v3, Friday 20 November 2026.
One-page newspaper, 50 stories, every one first reported on Friday
20 November 2026. Pure PIL, no network, no clock, no randomness.
Written from scratch in this session for the v3 rebuild.
"""
import os
from collections import Counter
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (22, 32, 63)
RED = (163, 31, 45)
TEAL = (18, 90, 92)
GOLD = (176, 124, 28)
GREY = (90, 88, 80)
LINE = (180, 172, 150)
CARD = (255, 253, 247)
SKY = (214, 230, 238)

FD = "/usr/share/fonts/truetype/dejavu"


def fnt(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


SERIF = lambda s: fnt("DejaVuSerif-Bold.ttf", s)
SANS = lambda s: fnt("DejaVuSans.ttf", s)
SANSB = lambda s: fnt("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, font, width):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


class Sheet:
    def __init__(self):
        self.img = Image.new("RGB", (W, H), PAPER)
        self.d = ImageDraw.Draw(self.img)
        self.d.rectangle([0, 0, W - 1, H - 1], outline=INK, width=3)

    def box(self, x, y, w, h, fill=CARD, outline=LINE, width=1):
        self.d.rectangle([x, y, x + w, y + h], fill=fill, outline=outline, width=width)

    def text(self, x, y, s, font, fill=INK):
        self.d.text((x, y), s, font=font, fill=fill)

    def centred(self, cx, y, s, font, fill=INK):
        self.d.text((cx - self.d.textlength(s, font=font) / 2, y), s, font=font, fill=fill)

    def para(self, x, y, s, font, width, lh, fill=INK, max_lines=None):
        lines = wrap(self.d, s, font, width)
        if max_lines is not None:
            assert len(lines) <= max_lines, f"overflow: {s!r} -> {len(lines)} lines"
        for i, ln in enumerate(lines):
            self.d.text((x, y + i * lh), ln, font=font, fill=fill)
        return y + len(lines) * lh

    def tag(self, x, y, label):
        col = RED if label in ("CLAIM", "ESTIMATE") else (TEAL if label == "FORECAST" else INK)
        w = int(self.d.textlength(label, font=SANSB(8))) + 10
        self.d.rectangle([x, y, x + w, y + 12], fill=col)
        self.d.text((x + 5, y + 2), label, font=SANSB(8), fill=(255, 255, 255))
        return w


# ---- the 50 stories: (n, region, place, label, headline, body, source) ----
LEADS = [
    (1, "ASIA-PACIFIC", "ODISHA · STORM", "REPORTED",
     "Akvan comes ashore, spares Odisha",
     "Cyclone Akvan crossed near Gopalpur at 07:30-08:30 IST, winds "
     "70-80 km/h gusting 90, weakening fast. No major damage or loss of "
     "life so far, officials say. 372,000 people were evacuated; "
     "Patrapur saw 209 mm of rain. Landfall done by 11:20 IST.",
     "IMD / Reuters · 07:30 IST"),
    (2, "EUROPE", "KYIV · WAR", "REPORTED",
     "Russia hits Kyiv bridges in overnight barrage",
     "Ballistic missiles struck three Dnipro bridges — Podilskyi, "
     "Darnytskyi and Pivdennyi — killing three people and injuring 15, "
     "the mayor says. Two more were killed in Lviv. Moscow calls it a "
     "massive strike on military and energy sites.",
     "Reuters / CNN · 01:22 UTC"),
    (3, "EUROPE", "ANTALYA · CLIMATE", "REPORTED",
     "COP31 reaches its final day with no deal",
     "Negotiators enter the closing day divided over a draft that drops "
     "every mention of fossil fuels and the $120bn adaptation-finance "
     "target. The text is due by midnight; talks look set to run over.",
     "Reuters / AFP · FINAL DAY"),
]

SMALL = [
    (4, "ASIA-PACIFIC", "ASIA · MARKETS", "REPORTED",
     "AI rout sweeps Asia: Nikkei -5.1%",
     "Nikkei -5.06% to 56,437; KOSPI -5.21%; TAIEX -6.23%. Worst week since 2020.",
     "Reuters / CNBC · ASIA CLOSE"),
    (5, "ASIA-PACIFIC", "TOKYO · ECONOMY", "REPORTED",
     "Japan inflation 2.2% backs a BoJ hike",
     "Core CPI +2.2% in October, up from 2.1% in September; above the BoJ's 2% target again.",
     "Reuters · 08:30 JST"),
    (6, "WORLD", "MERCURY · SPACE", "FORECAST",
     "BepiColombo set for Mercury orbit tomorrow",
     "After eight years in space, the ESA-JAXA craft ends its approach today; orbit insertion is Saturday.",
     "ESA / JAXA · SAT 21 NOV"),
    (7, "EUROPE", "BRUSSELS · EUROPE", "REPORTED",
     "Burnham holds first EU-UK reset summit",
     "Food deal worth £5.1bn a year, carbon markets to link, and 100,000 youth places agreed.",
     "Reuters / Irish Times · FRI"),
    (8, "ASIA-PACIFIC", "BEIJING · RATES", "REPORTED",
     "China holds lending rates for 18th month",
     "One-year LPR stays 3.0%, five-year 3.5%. The overnight repo, now "
     "the main policy signal, is 1.25%.",
     "PBOC / Reuters · 09:00 CST"),
    (9, "OCEANIA", "WELLINGTON · CRICKET", "REPORTED",
     "Phillips 118 makes history vs India",
     "First batter with centuries in all three formats vs India in one year. NZ made 368; Nicholls 175*.",
     "Reuters / ICC · DAY 2"),
    (10, "EUROPE", "ROME · LABOUR", "REPORTED",
     "Italy's CGIL holds a 24-hour general strike",
     "Buses, metros and trams hit in ~100 rallies against the 2027 budget law; a rail strike starts 21:00.",
     "ANSA / ETUC · ALL DAY"),
    (11, "AFRICA", "SENEGAL · MIGRATION", "REPORTED",
     "Senegal boat search goes on; toll now four",
     "Four bodies now recovered after the pirogue capsized off Yenne on Wednesday; dozens still missing.",
     "Reuters / Al Jazeera · FRI"),
    (12, "WORLD", "WORLD · GAMES", "ESTIMATE",
     "GTA VI: $2.36bn on day one, Sensor Tower says",
     "An estimated 24.58m copies sold by Thursday evening — the biggest entertainment launch ever.",
     "Sensor Tower / BBC · FRI"),
    (13, "AMERICAS", "LAS VEGAS · F1", "REPORTED",
     "Russell fastest in a wet Las Vegas practice",
     "Russell's 1:47.272 beat Gasly by 0.071s in FP2; Leclerc third. FP1 set no lap times in the rain.",
     "Formula 1 · 04:00 UTC"),
]

BRIEFS = [
    (14, "AMERICAS", "WASHINGTON — Trump to hold a noon news conference, 12:00 ET, after his Asia trip."),
    (15, "MIDEAST", "S. SAUDI — Coalition intercepts a Houthi missile; drones downed over Jazan and Abha."),
    (16, "ASIA-PACIFIC", "JAKARTA — Prabowo meets Xi; South China Sea cooperation and investment on the table."),
    (17, "MIDEAST", "IRAQ — Forces to deploy in Jurf al-Sakhar, a Kataib Hezbollah stronghold, in a deal."),
    (18, "EUROPE", "MOSCOW — Russia rejects the US idea of NATO-style security guarantees for Ukraine."),
    (19, "EUROPE", "POLAND — Army probes unknown objects near Ukraine border; jets scrambled."),
    (20, "ASIA-PACIFIC", "MYANMAR — Government calls the ICJ genocide ruling 'unfair' (ruling itself: Thursday)."),
    (21, "ASIA-PACIFIC", "DHAKA — Rohingya return possible in 1-1.5 years if safe passage is secured."),
    (22, "ASIA-PACIFIC", "KUALA LUMPUR — Malaysia to resettle 10,000 Rohingya refugees in Turkey via training."),
    (23, "EUROPE", "EUROPE — STOXX 600 -1% to 631.89; weekly -4.5%, steepest since March. DAX -1.3%."),
    (24, "WORLD", "MARKETS — Gold $3,601.40, -0.6%, weekly -7.3%; silver -1.7%. Brent flat at $91.98."),
    (25, "AMERICAS", "DOLLAR — Index 103.86, strongest since April 2025; 10-yr yield 5.026%."),
    (26, "AMERICAS", "SAN SALVADOR — Bukele files for a third term (Thu night, Fri UTC); vote 28 Feb 2027."),
    (27, "EUROPE", "KHARKIV — Russian drone hits a hospital; four injured, more than 50 windows shattered."),
    (28, "EUROPE", "KYIV — Missile debris sets fire to a three-storey block in the Obolonskyi district."),
    (29, "EUROPE", "BLACK SEA — Russia says it hit sea vessels and energy sites; claims a ship hit. [CLAIM]"),
    (30, "EUROPE", "TURIN — ATP Finals: Alcaraz v Cobolli, then Medvedev v Tiafoe; both 1-1."),
    (31, "EUROPE", "ANTALYA — Youth delegates protest inside COP31, demanding the phase-out return."),
    (32, "EUROPE", "BRUSSELS — EU agrees a two-year delay to methane rules for importers."),
    (33, "EUROPE", "LONDON — BAE Systems to cut 1,000+ jobs at its head office and air business."),
    (34, "MIDEAST", "HORMUZ — Iran says three tankers hit mines east of the strait; unverified. [CLAIM]"),
    (35, "EUROPE", "PARIS — Parliament adopts a law raising press pay from Google and Meta."),
    (36, "OCEANIA", "COOK ISLANDS — Xavier, a Category 4 cyclone, nears Manihiki; Nassau in emergency."),
    (37, "EUROPE", "GERMANY — Teenager held over a suspected mosque plot; 3D-printed weapons found."),
    (38, "AMERICAS", "NEW YORK — S&P futures -0.4%, Nasdaq -0.7% in Asia; Anthropic $92.60 after hours."),
    (39, "ASIA-PACIFIC", "SINGAPORE — STI -1.86% to 4,985.22 by late morning as the Asia sell-off spreads."),
    (40, "ASIA-PACIFIC", "SYDNEY — ASX 200 -1.58% to 8,592.6; a 490-point weekly drubbing."),
    (41, "ASIA-PACIFIC", "TOKYO — SoftBank -14.48% to ¥3,025, worst day since August 2024."),
    (42, "ASIA-PACIFIC", "SEOUL — Samsung -7.1%, SK Hynix -6.6%; TSMC -4.8% as the chip rout deepens."),
    (43, "AMERICAS", "CUPERTINO — Apple is hiring to build its own agentic AI assistant, Bloomberg reports."),
    (44, "EUROPE", "ANTALYA — Draft keeps a 35% electricity share by 2035 and a 500m-tonne CCUS target."),
    (45, "ASIA-PACIFIC", "ODISHA — Assembly adjourns to 23 Nov for relief; 9,341 shelters, 2,523 camps open."),
    (46, "EUROPE", "LVIV — Two killed in the western city in the same overnight barrage, officials say."),
    (47, "OCEANIA", "WELLINGTON — India close Day 2 on 159/1, Jaiswal 85, Rahul 52*, trailing by 209."),
    (48, "EUROPE", "BRUSSELS — Euro-zone flash consumer confidence for November is due later today."),
    (49, "AMERICAS", "LAS VEGAS — FP3 at 16:30 local, qualifying at 20:00; a dry weekend is expected."),
    (50, "ASIA-PACIFIC", "KOLKATA — Akvan rain disrupts morning transport as storm bands reach West Bengal."),
]

NUMBERS = [
    ("372,000", "EVACUATED FROM AKVAN'S PATH"),
    ("3", "KYIV BRIDGES HIT OVERNIGHT"),
    ("-5.06%", "NIKKEI ON FRIDAY'S CLOSE"),
    ("2.2%", "JAPAN CORE CPI, OCTOBER"),
    ("0", "FOSSIL-FUEL MENTIONS IN COP31 DRAFT"),
    ("$2.36bn", "GTA VI DAY-ONE SALES, EST."),
]

TIMELINE = [
    ("01:00", "China holds its lending rates, 3.0% / 3.5%"),
    ("01:22", "Kyiv: ballistic strikes reported, three killed"),
    ("02:00", "Akvan landfall begins near Gopalpur"),
    ("06:00", "Asia closes deep in red: Nikkei, KOSPI, TAIEX"),
    ("17:00", "Trump news conference due, noon ET"),
]

DATECHECK = (
    "LEFT OUT — THEY BROKE BEFORE FRIDAY: the trilateral meeting itself, Shenzhen (Thu) · "
    "the PIF Tower missile strike, Riyadh (Thu) · the Kerch Bridge attack (Thu) · "
    "Van Gogh sells for $190.4m (Thu) · Hayabusa2 retargets to 2015 BM510 (Tue) · "
    "Korea exports pass $1tn (Thu) · the ICJ Myanmar genocide verdict itself (Thu) · "
    "Anthropic's $83 IPO price and $97.17 debut close (Thu) · GTA VI's midnight launch in "
    "New Zealand (Thu) · Voyager 1 confirmed one light-day away (Thu) · Trump's Iran "
    "decision put off to 2027 (Thu, disputed — left out to be safe)."
)

# land boxes (lon_min, lon_max, lat_min, lat_max) for the dot map
LAND = [
    (-168, -52, 15, 72), (-118, -86, 14, 32), (-92, -66, 7, 15),
    (-80, -34, -35, 5), (-17, 32, 36, 70), (32, 50, 36, 42),
    (19, 30, 35, 42), (-10, 28, 35, 45), (28, 45, 58, 71),
    (30, 60, 41, 55), (60, 100, 42, 77), (100, 135, 50, 77),
    (135, 180, 42, 72), (68, 90, 8, 37), (90, 105, 5, 28),
    (95, 141, -11, 6), (113, 154, -39, -11), (166, 178, -47, -34),
    (32, 42, -35, -17), (12, 34, -29, -18), (35, 51, -18, -5),
    (43, 52, 11, 18), (-17, -10, 14, 17), (32, 44, 3, 15),
]

PINS = {  # story -> (lon, lat)
    1: (84.8, 19.1), 2: (30.5, 50.4), 3: (30.7, 36.9), 4: (127.0, 37.5),
    5: (139.7, 35.7), 6: (8.6, 49.9), 7: (-74.0, 40.7), 8: (116.4, 39.9),
    9: (174.8, -41.3), 10: (12.5, 41.9), 11: (-17.2, 14.7),
    12: (-80.2, 25.8), 13: (-115.1, 36.1),
}


def draw_cyclone(d, x, y, w, h):
    # Bay of Bengal coast: tan land left, blue sea right, spiral on the coast
    d.rectangle([x, y, x + w, y + h], fill=(216, 228, 235))
    d.polygon([(x, y), (x + 22, y), (x + 30, y + h // 3), (x + 24, y + 2 * h // 3),
               (x + 30, y + h), (x, y + h)], fill=(214, 196, 150))
    d.line([x + 22, y, x + 30, y + h // 3, x + 24, y + 2 * h // 3, x + 30, y + h],
           fill=(120, 100, 60), width=1)
    cx, cy = x + w // 2 + 4, y + h // 2
    for r in (26, 18, 10):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=(255, 255, 255), width=3)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)
    for i in range(4):
        d.line([x + 4 + i * 5, y + h - 6, x + 8 + i * 5, y + h - 14], fill=TEAL, width=2)
    d.ellipse([x + 24, cy - 3, x + 30, cy + 3], fill=RED, outline=(255, 255, 255))


def draw_bridge(d, x, y, w, h):
    # night skyline, missile trails, bridge arc below
    d.rectangle([x, y, x + w, y + h], fill=(24, 32, 56))
    for bx, bw, bh in ((x + 4, 12, 26), (x + 20, 9, 34), (x + 33, 14, 20), (x + 51, 10, 30)):
        d.rectangle([bx, y + h - 12 - bh, bx + bw, y + h - 12], fill=(52, 62, 92))
        for wy in range(y + h - 10 - bh, y + h - 14, 7):
            d.point((bx + 3, wy), fill=(255, 210, 90))
    for sx, sy, ex, ey in ((x + 8, y + 4, x + 26, y + 22), (x + 34, y + 2, x + 48, y + 20),
                           (x + 56, y + 6, x + 68, y + 20)):
        d.line([sx, sy, ex, ey], fill=(255, 140, 40), width=2)
        d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=(255, 200, 60))
    d.line([x + 4, y + h - 12, x + w - 4, y + h - 12], fill=(200, 200, 200), width=2)
    d.arc([x + w // 2 - 18, y + h - 30, x + w // 2 + 18, y + h - 8], 180, 360,
          fill=(200, 200, 200), width=2)


def draw_globe(d, x, y, w, h):
    # globe + thermometer (red mercury) + $120bn gap badge
    d.ellipse([x + 4, y + 4, x + w - 26, y + h - 4], outline=TEAL, width=3)
    d.ellipse([x + w // 2 - 20, y + 4, x + w // 2 + 4, y + h - 4], outline=TEAL, width=2)
    d.line([x + 4, y + h // 2, x + w - 26, y + h // 2], fill=TEAL, width=2)
    d.polygon([(x + 10, y + h - 16), (x + 24, y + 14), (x + 36, y + h - 16)], outline=TEAL)
    tx = x + w - 16
    d.rounded_rectangle([tx, y + 4, tx + 8, y + h - 12], radius=4, outline=RED, width=2)
    d.rectangle([tx + 2, y + h - 22, tx + 6, y + h - 14], fill=RED)
    d.ellipse([tx - 2, y + h - 14, tx + 10, y + h - 2], fill=RED)


ART = {1: draw_cyclone, 2: draw_bridge, 3: draw_globe}


def _chart(d, x, y, w, h):
    d.line([x + 2, y + h - 4, x + w - 2, y + h - 4], fill=INK, width=1)
    pts = [(x + 3, y + 4), (x + 12, y + 8), (x + 21, y + 7), (x + 30, y + 14), (x + 39, y + 20)]
    d.line(pts, fill=RED, width=2)


def _bars(d, x, y, w, h):
    for i, bh in enumerate((8, 13, 18)):
        d.rectangle([x + 4 + i * 12, y + h - 3 - bh, x + 12 + i * 12, y + h - 3], fill=TEAL)
    d.line([x + 2, y + 4, x + w - 2, y + h - 8], fill=RED, width=2)


def _orbit(d, x, y, w, h):
    d.ellipse([x + 4, y + 3, x + w - 4, y + h - 3], outline=TEAL, width=2)
    d.ellipse([x + w // 2 - 5, y + h // 2 - 5, x + w // 2 + 5, y + h // 2 + 5], fill=GOLD)
    d.ellipse([x + w - 8, y + 2, x + w - 3, y + 7], fill=INK)


def _flags(d, x, y, w, h):
    d.rectangle([x + 2, y + 3, x + 19, y + h - 3], fill=(30, 60, 150))
    for dx, dy in ((6, 5), (13, 5), (6, 13), (13, 13)):
        d.ellipse([x + dx, y + dy, x + dx + 2, y + dy + 2], fill=(255, 210, 60))
    d.rectangle([x + 23, y + 3, x + 40, y + h - 3], fill=(255, 255, 255), outline=LINE)
    d.line([x + 31, y + 3, x + 31, y + h - 3], fill=RED, width=3)
    d.line([x + 23, y + h // 2, x + 40, y + h // 2], fill=RED, width=3)


def _bank(d, x, y, w, h):
    d.polygon([(x + 2, y + 8), (x + w // 2, y + 2), (x + w - 2, y + 8)], fill=INK)
    for i in range(3):
        d.rectangle([x + 6 + i * 12, y + 10, x + 10 + i * 12, y + h - 4], fill=INK)
    d.rectangle([x + 2, y + h - 4, x + w - 2, y + h - 2], fill=INK)


def _bat(d, x, y, w, h):
    d.rectangle([x + 2, y + h - 6, x + w - 2, y + h - 2], fill=(90, 140, 70))
    d.line([x + 8, y + h - 8, x + 28, y + 4], fill=(214, 180, 120), width=5)
    d.ellipse([x + 30, y + 2, x + 38, y + 10], fill=RED)


def _mega(d, x, y, w, h):
    d.polygon([(x + 4, y + 6), (x + 34, y + 2), (x + 34, y + 16), (x + 4, y + 12)], fill=RED)
    d.rectangle([x + 2, y + 6, x + 6, y + 12], fill=INK)
    d.rectangle([x + 24, y + 16, x + 28, y + 22], fill=INK)


def _boat(d, x, y, w, h):
    d.polygon([(x + 20, y + 2), (x + 20, y + 14), (x + 32, y + 14)], fill=(255, 255, 255),
              outline=INK)
    d.polygon([(x + 6, y + 14), (x + 36, y + 14), (x + 30, y + 20), (x + 12, y + 20)], fill=INK)
    d.line([x + 2, y + 22, x + 14, y + 22], fill=TEAL, width=2)
    d.line([x + 26, y + 22, x + 40, y + 22], fill=TEAL, width=2)


def _pad(d, x, y, w, h):
    d.rounded_rectangle([x + 4, y + 5, x + w - 4, y + h - 5], radius=6, fill=(40, 40, 60))
    d.line([x + 10, y + 12, x + 16, y + 12], fill=(255, 255, 255), width=2)
    d.line([x + 13, y + 9, x + 13, y + 15], fill=(255, 255, 255), width=2)
    d.ellipse([x + 26, y + 9, x + 30, y + 13], fill=RED)
    d.ellipse([x + 32, y + 12, x + 36, y + 16], fill=(255, 210, 60))


def _flag(d, x, y, w, h):
    for r in range(3):
        for c in range(4):
            if (r + c) % 2 == 0:
                d.rectangle([x + 4 + c * 8, y + 3 + r * 6, x + 11 + c * 8, y + 8 + r * 6],
                            fill=INK)
    d.line([x + 4, y + 3, x + 4, y + h - 2], fill=INK, width=2)


SMALL_ART = {4: _chart, 5: _bars, 6: _orbit, 7: _flags, 8: _bank,
             9: _bat, 10: _mega, 11: _boat, 12: _pad, 13: _flag}


def build():
    s = Sheet()
    d = s.d
    mx = 28
    # top bar
    d.rectangle([mx, 10, W - mx, 30], fill=INK)
    s.text(mx + 10, 14, "THE WORLD IN ONE DAY", SANSB(12), fill=(255, 255, 255))
    s.centred(W // 2 + 120, 14, "50 STORIES  ·  EVERY ONE FROM THIS FRIDAY", SANSB(10), fill=(220, 220, 220))
    # masthead
    s.centred(W // 2, 36, "Friday 20 November 2026", SERIF(34))
    s.centred(W // 2, 74, "Akvan comes ashore  ·  Kyiv's bridges hit  ·  COP31's final day  ·  Asia's AI rout",
              SANS(12), fill=GREY)
    # numbers strip
    y = 96
    bw = (W - 2 * mx - 5 * 6) // 6
    for i, (num, lab) in enumerate(NUMBERS):
        x = mx + i * (bw + 6)
        s.box(x, y, bw, 42, fill=CARD, outline=LINE)
        s.centred(x + bw // 2, y + 3, num, SANSB(17), fill=RED)
        s.centred(x + bw // 2, y + 25, lab, SANSB(7), fill=GREY)
    # region strip
    regs = Counter([r for _, r, *_ in LEADS + SMALL] + [r for _, r, _ in BRIEFS])
    order = ["EUROPE", "AMERICAS", "ASIA-PACIFIC", "MIDEAST", "AFRICA", "OCEANIA", "WORLD"]
    strip = "  ·  ".join(f"{r} {regs.get(r, 0)}" for r in order)
    s.centred(W // 2, 144, strip, SANSB(10), fill=INK)
    # leads
    y = 162
    lw = (W - 2 * mx - 2 * 8) // 3
    lh = 168
    for (n, reg, place, label, head, body, src) in LEADS:
        x = mx + (n - 1) * (lw + 8)
        s.box(x, y, lw, lh, fill=CARD, outline=INK, width=2)
        s.text(x + 8, y + 6, f"{n}  {place}", SANSB(9), fill=RED)
        s.tag(x + lw - 78, y + 6, label)
        ART[n](d, x + 8, y + 24, 74, 52)
        s.para(x + 90, y + 26, head, SANSB(13), lw - 98, 16, max_lines=3)
        s.para(x + 8, y + 84, body, SANS(10), lw - 16, 13, max_lines=5)
        s.text(x + 8, y + lh - 16, f"Source: {src}", SANS(8), fill=GREY)
    # small cards, 5 x 2
    y = 338
    cw = (W - 2 * mx - 4 * 6) // 5
    ch = 116
    for idx, (n, reg, place, label, head, body, src) in enumerate(SMALL):
        row, col = divmod(idx, 5)
        x = mx + col * (cw + 6)
        yy = y + row * (ch + 6)
        s.box(x, yy, cw, ch, fill=CARD, outline=LINE)
        s.text(x + 6, yy + 5, f"{n}  {place}", SANSB(8), fill=RED)
        s.tag(x + cw - 62, yy + 5, label)
        SMALL_ART[n](d, x + cw - 48, yy + 20, 42, 24)
        s.para(x + 6, yy + 22, head, SANSB(10), cw - 60, 13, max_lines=3)
        s.para(x + 6, yy + 64, body, SANS(9), cw - 12, 12, max_lines=3)
        s.text(x + 6, yy + ch - 13, f"Source: {src}", SANS(7), fill=GREY)
    # map + timeline
    y = 584
    mw, mh = 640, 76
    s.box(mx, y, mw, mh, fill=(232, 240, 244), outline=LINE)
    s.text(mx + 8, y + 4, "WHERE IT HAPPENED — PINS 1-13", SANSB(9), fill=INK)
    cols, rows = 64, 22
    for ci in range(cols):
        lon = -180 + (ci + 0.5) * 360 / cols
        for ri in range(rows):
            lat = 75 - (ri + 0.5) * 110 / rows
            if any(lo <= lon <= hi and la <= lat <= hb for lo, hi, la, hb in LAND):
                px = mx + 8 + ci * (mw - 16) / cols
                py = y + 20 + ri * (mh - 26) / rows
                d.ellipse([px - 1, py - 1, px + 1, py + 1], fill=(120, 140, 160))
    for n, (lon, lat) in PINS.items():
        px = mx + 8 + (lon + 180) / 360 * (mw - 16)
        py = y + 20 + (75 - lat) / 110 * (mh - 26)
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255), width=1)
        d.text((px - 3 if n < 10 else px - 6, py - 6), str(n), font=SANSB(8), fill=(255, 255, 255))
    tx = mx + mw + 8
    tw = W - mx - tx
    s.box(tx, y, tw, mh, fill=CARD, outline=LINE)
    s.text(tx + 8, y + 4, "THE DAY IN UTC — FRIDAY ONLY", SANSB(9), fill=INK)
    yy = y + 20
    for t, what in TIMELINE:
        s.text(tx + 8, yy, t, SANSB(9), fill=RED)
        s.text(tx + 46, yy, what, SANS(9))
        yy += 11
    # briefs
    y = 668
    s.text(mx, y, "ALSO ON FRIDAY 20 NOVEMBER", SANSB(11), fill=INK)
    legend = "HOW SURE: REPORTED = confirmed · CLAIM = one side · FORECAST = set for today"
    s.text(W - mx - int(s.d.textlength(legend, font=SANSB(8))), y + 2, legend,
           SANSB(8), fill=GREY)
    y += 16
    d.line([mx, y, W - mx, y], fill=INK, width=1)
    y += 5
    colw = (W - 2 * mx - 20) // 2
    for i, (n, reg, txt) in enumerate(BRIEFS):
        col, row = divmod(i, 19)
        x = mx + col * (colw + 20)
        yy = y + row * 12
        s.text(x, yy, f"{n}.", SANSB(10), fill=RED)
        lines = wrap(d, txt, SANS(10), colw - 22)
        assert len(lines) <= 1, f"brief {n} too long: {txt!r}"
        s.text(x + 22, yy, lines[0], SANS(10))
    # date check
    y = 668 + 16 + 6 + 19 * 12 + 8
    s.box(mx, y, W - 2 * mx, 54, fill=(253, 238, 238), outline=RED, width=2)
    s.text(mx + 8, y + 4, "DATE CHECK — deliberately NOT on this page", SANSB(10), fill=RED)
    s.para(mx + 8, y + 20, DATECHECK, SANS(9), W - 2 * mx - 16, 11, max_lines=3)
    # tomorrow + footer
    y += 62
    s.text(mx, y, "TOMORROW:  COP31 final text  ·  the US Friday market close  ·  BepiColombo enters Mercury orbit  ·  ATP Finals semi-finals",
           SANSB(9), fill=INK)
    y += 15
    s.text(mx, y, "Every story here happened, or was first reported, on Friday 20 November 2026 in at least one time zone. "
                  "All scenes are drawn in code; no photographs are used. Sources: Reuters, AP, AFP, BBC, IMD, ESA/JAXA, PBOC, Formula 1, ICC.",
           SANS(8), fill=GREY)
    assert y + 12 <= H - 8, "page overflow"
    return s.img


if __name__ == "__main__":
    img = build()
    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)
