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
     "IMD / Reuters"),
    (2, "EUROPE", "KYIV · WAR", "REPORTED",
     "Russia hits Kyiv bridges in overnight barrage",
     "Ballistic missiles struck three Dnipro bridges — Podilskyi, "
     "Darnytskyi and Pivdennyi — killing three people and injuring 15, "
     "the mayor says. Two more were killed in Lviv. Moscow calls it a "
     "massive strike on military and energy sites.",
     "Reuters / CNN"),
    (3, "EUROPE", "ANTALYA · CLIMATE", "REPORTED",
     "COP31 reaches its final day with no deal",
     "Negotiators enter the closing day divided over a draft that drops "
     "every mention of fossil fuels and the $120bn adaptation-finance "
     "target. The text is due by midnight; talks look set to run over.",
     "Reuters / AFP"),
]

SMALL = [
    (4, "ASIA-PACIFIC", "ASIA · MARKETS", "REPORTED",
     "AI rout sweeps Asia: Nikkei -5.1%",
     "Nikkei -5.06% to 56,437; KOSPI -5.21% to 4,870; TAIEX -6.23% to "
     "36,033. Worst week since 2020; TAIEX -17.5% for the week.",
     "Reuters / CNBC"),
    (5, "ASIA-PACIFIC", "TOKYO · ECONOMY", "REPORTED",
     "Japan inflation 2.2% backs a BoJ hike",
     "Core CPI rose 2.2% in October, up from 2.1% in September and above "
     "the Bank of Japan's 2% target for a second month.",
     "Reuters"),
    (6, "WORLD", "MERCURY · SPACE", "FORECAST",
     "BepiColombo set for Mercury orbit tomorrow",
     "After eight years in space, the ESA-JAXA craft ends its approach "
     "phase today. Orbit insertion is set for Saturday 21 Nov.",
     "ESA / JAXA"),
    (7, "AMERICAS", "NEW YORK · MARKETS", "REPORTED",
     "Wall Street futures point lower again",
     "S&P futures -0.4%, Nasdaq futures -0.7% in Asia. Anthropic, up 17% "
     "on its Thursday debut, fell to $92.60 after hours.",
     "Reuters / Bloomberg"),
    (8, "ASIA-PACIFIC", "BEIJING · RATES", "REPORTED",
     "China holds lending rates for 18th month",
     "One-year LPR stays 3.0%, five-year 3.5%. The overnight repo, now "
     "the main policy signal, is 1.25%.",
     "PBOC / Reuters"),
    (9, "OCEANIA", "WELLINGTON · CRICKET", "REPORTED",
     "Phillips 118 makes history vs India",
     "Glenn Phillips is the first batter with centuries in all three "
     "formats against India in one year. NZ made 368; Nicholls 175*.",
     "Reuters / ICC"),
    (10, "EUROPE", "ROME · LABOUR", "REPORTED",
     "Italy's CGIL holds a 24-hour general strike",
     "Buses, metros and trams hit in about 100 rallies against the 2027 "
     "budget law. A separate rail strike starts at 21:00.",
     "ANSA / ETUC"),
    (11, "AFRICA", "SENEGAL · MIGRATION", "REPORTED",
     "Senegal boat search goes on; toll now four",
     "Four bodies are now recovered after the pirogue capsized off Yenne "
     "on Wednesday; dozens are still missing. Search resumes today.",
     "Reuters / Al Jazeera"),
    (12, "WORLD", "WORLD · GAMES", "ESTIMATE",
     "GTA VI: $2.36bn on day one, Sensor Tower says",
     "An estimated 24.58m copies sold by Thursday evening — the biggest "
     "entertainment launch on record. Take-Two has published no figure.",
     "Sensor Tower / BBC"),
    (13, "AMERICAS", "LAS VEGAS · F1", "REPORTED",
     "Russell fastest in a wet Las Vegas practice",
     "George Russell's 1:47.272 beat Gasly by 0.071s in FP2; Leclerc was "
     "third. FP1 set no lap times at all in the rain.",
     "Formula 1"),
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
    (26, "EUROPE", "BRUSSELS — EU-UK summit: Burnham seeks a reset; deal tied to EU student tuition fees."),
    (27, "EUROPE", "KHARKIV — Russian drone hits a hospital; four injured, more than 50 windows shattered."),
    (28, "EUROPE", "KYIV — Missile debris sets fire to a three-storey block in the Obolonskyi district."),
    (29, "EUROPE", "BLACK SEA — Russia says it hit sea vessels and energy sites; claims a ship hit. [CLAIM]"),
    (30, "EUROPE", "TURIN — ATP Finals: Alcaraz v Cobolli, then Medvedev v Tiafoe; both 1-1."),
    (31, "EUROPE", "ANTALYA — Youth delegates protest inside COP31, demanding the phase-out return."),
    (32, "EUROPE", "BRUSSELS — EU agrees a two-year delay to methane rules for importers."),
    (33, "EUROPE", "LONDON — BAE Systems to cut 1,000+ jobs at its head office and air business."),
    (34, "EUROPE", "LONDON — UK launches 'Be Ready', urging households to stockpile food for emergencies."),
    (35, "EUROPE", "PARIS — Parliament adopts a law raising press pay from Google and Meta."),
    (36, "EUROPE", "BERLIN — Germany raises its IT threat level to 'tense towards critical'."),
    (37, "EUROPE", "GERMANY — Teenager held over a suspected mosque plot; 3D-printed weapons found."),
    (38, "EUROPE", "MADRID — Sánchez and Feijóo clash in an election debate ahead of next week's vote."),
    (39, "ASIA-PACIFIC", "SINGAPORE — STI -1.86% to 4,985.22 by late morning as the Asia sell-off spreads."),
    (40, "ASIA-PACIFIC", "SYDNEY — ASX 200 -1.58% to 8,592.6; a 490-point weekly drubbing."),
    (41, "ASIA-PACIFIC", "TOKYO — SoftBank -14.48% to ¥3,025, worst day since August 2024."),
    (42, "ASIA-PACIFIC", "SEOUL — Samsung -7.1%, SK Hynix -6.6%; TSMC -4.8% as the chip rout deepens."),
    (43, "AMERICAS", "CUPERTINO — Apple is hiring to build its own agentic AI assistant, Bloomberg reports."),
    (44, "EUROPE", "ANTALYA — Draft keeps a 35% electricity share by 2035 and a 500m-tonne CCUS target."),
    (45, "ASIA-PACIFIC", "ODISHA — Assembly adjourns to 23 Nov for relief; 9,341 shelters, 2,523 camps open."),
    (46, "EUROPE", "LVIV — Two killed in the western city in the same overnight barrage, officials say."),
    (47, "EUROPE", "ANALYSIS — Ukraine's bridge strikes strain Russian logistics to Crimea, Reuters reports."),
    (48, "EUROPE", "BRUSSELS — Euro-zone flash consumer confidence for November is due later today."),
    (49, "AMERICAS", "LAS VEGAS — FP3 at 16:30 local, qualifying at 20:00; a dry weekend is expected."),
    (50, "ASIA-PACIFIC", "KOLKATA — Akvan rain disrupts morning transport as storm bands reach West Bengal."),
]

NUMBERS = [
    ("372,000", "EVACUATED FROM AKVAN'S PATH"),
    ("3", "KYIV BRIDGES HIT OVERNIGHT"),
    ("-5.06%", "NIKKEI ON FRIDAY'S CLOSE"),
    ("2.2%", "JAPAN CORE CPI, OCTOBER"),
    ("118", "PHILLIPS RUNS VS INDIA"),
    ("$2.36bn", "GTA VI DAY-ONE SALES, EST."),
]

TIMELINE = [
    ("01:00", "China holds its lending rates, 3.0% / 3.5%"),
    ("01:22", "Kyiv: ballistic strikes reported, three killed"),
    ("02:00", "Akvan landfall begins near Gopalpur"),
    ("06:00", "Asia closes deep in red: Nikkei, KOSPI, TAIEX"),
    ("17:00", "Trump news conference due, noon ET"),
    ("19:30", "Medvedev v Tiafoe, ATP Finals, Turin"),
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
    d.ellipse([x + 8, y + 6, x + w - 8, y + h - 6], outline=TEAL, width=3)
    for r in (34, 24, 14):
        d.arc([x + w // 2 - r, y + h // 2 - r, x + w // 2 + r, y + h // 2 + r],
              20, 300, fill=TEAL, width=3)
    d.ellipse([x + w // 2 - 5, y + h // 2 - 5, x + w // 2 + 5, y + h // 2 + 5], fill=RED)
    for i in range(5):
        d.line([x + 6 + i * 12, y + h - 8, x + 12 + i * 12, y + h - 16], fill=TEAL, width=2)


def draw_bridge(d, x, y, w, h):
    d.line([x + 6, y + h - 14, x + w - 6, y + h - 14], fill=INK, width=3)
    d.arc([x + w // 2 - 22, y + 8, x + w // 2 + 22, y + 44], 180, 360, fill=INK, width=3)
    for i, px in enumerate((x + 16, x + w // 2, x + w - 16)):
        d.line([px, y + h - 14, px, y + 18 + (i % 2) * 8], fill=INK, width=2)
    d.line([x + w - 34, y + 4, x + w - 10, y + 22], fill=RED, width=3)
    d.ellipse([x + w - 14, y + 18, x + w - 6, y + 26], fill=RED)


def draw_globe(d, x, y, w, h):
    d.ellipse([x + 10, y + 4, x + w - 10, y + h - 4], outline=TEAL, width=3)
    d.ellipse([x + w // 2 - 14, y + 4, x + w // 2 + 14, y + h - 4], outline=TEAL, width=2)
    d.line([x + 10, y + h // 2, x + w - 10, y + h // 2], fill=TEAL, width=2)
    d.polygon([(x + 14, y + h - 18), (x + 30, y + 12), (x + 44, y + h - 18)], outline=TEAL)


ART = {1: draw_cyclone, 2: draw_bridge, 3: draw_globe}


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
    ch = 108
    for idx, (n, reg, place, label, head, body, src) in enumerate(SMALL):
        row, col = divmod(idx, 5)
        x = mx + col * (cw + 6)
        yy = y + row * (ch + 6)
        s.box(x, yy, cw, ch, fill=CARD, outline=LINE)
        s.text(x + 6, yy + 5, f"{n}  {place}", SANSB(8), fill=RED)
        s.tag(x + cw - 62, yy + 5, label)
        s.para(x + 6, yy + 22, head, SANSB(10), cw - 12, 13, max_lines=2)
        s.para(x + 6, yy + 50, body, SANS(9), cw - 12, 12, max_lines=4)
        s.text(x + 6, yy + ch - 13, f"Source: {src}", SANS(7), fill=GREY)
    # map + timeline
    y = 568
    mw, mh = 640, 92
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
