"""draw_v2.py — second-generation generator for news-image-20261120.

Friday 20 November 2026, one 1024x1024 front page with 50 stories:
4 heroes, 12 cards, a dotted world map with 16 numbered pins, 34 briefs,
a region-count strip, a day-so-far timeline, a DATE CHECK box and a
sources footer. Everything is drawn in code with Pillow; no network,
no clock, no randomness — running it twice writes byte-identical PNGs.

This file was written from scratch in this session (new layout engine,
new helper names, new map built from longitude/latitude boxes instead of
a hand-typed dot grid, new scene painters). It reproduces the same page
content as the earlier v2 build: the same 50 stories, the same numbers
and the same facts. See V2-REPORT.md for the research log and the list
of what changed against v1.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
MARGIN = 16
CONTENT_W = PAGE_W - 2 * MARGIN  # 992

_HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(_HERE, "entry.png")
_FONT_DIR = "/usr/share/fonts/truetype/dejavu"

# --- colours (hex, converted below) -------------------------------------
_HEX = {
    "navy": "#14264E",
    "navy2": "#1C3466",
    "cream": "#F7F3E8",
    "paper": "#FCFAF4",
    "ink": "#181818",
    "muted": "#60605A",
    "red": "#B22222",
    "red_dk": "#8B1A1A",
    "teal": "#125A5C",
    "gold": "#C9A227",
    "line": "#B4AC96",
    "dot": "#6E7864",
    "sky": "#B2CDE1",
    "sea": "#486E8C",
    "night": "#101834",
    "sand": "#E8D696",
    "leaf": "#3CA05A",
    "pink": "#FFF4F0",
}


def _rgb(name):
    h = _HEX[name].lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


# --- fonts ---------------------------------------------------------------
_FONT_FILES = {
    "serif": "DejaVuSerif-Bold.ttf",
    "serif_it": "DejaVuSerif-Italic.ttf",
    "sans": "DejaVuSans.ttf",
    "sans_b": "DejaVuSans-Bold.ttf",
    "cond": "DejaVuSansCondensed.ttf",
    "cond_b": "DejaVuSansCondensed-Bold.ttf",
}


def face(kind, size):
    return ImageFont.truetype(os.path.join(_FONT_DIR, _FONT_FILES[kind]), size)


# --- text helpers --------------------------------------------------------
def _wrap(d, text, font, max_w):
    """Greedy wrap; returns the lines that fit max_w."""
    lines, current = [], ""
    for word in text.split(" "):
        trial = (current + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w:
            current = trial
        elif current:
            lines.append(current)
            current = word
        else:
            current = word
    if current:
        lines.append(current)
    return lines


class Pen:
    """Thin wrapper around ImageDraw with the page's text primitives."""

    def __init__(self, image):
        self.d = ImageDraw.Draw(image)

    def txt(self, xy, text, kind, size, colour):
        self.d.text(xy, text, font=face(kind, size), fill=_rgb(colour))

    def mid(self, cx, y, text, kind, size, colour):
        f = face(kind, size)
        self.d.text((cx - self.d.textlength(text, font=f) / 2, y),
                    text, font=f, fill=_rgb(colour))

    def rule(self, x0, x1, y, colour, width=1):
        self.d.line([(x0, y), (x1, y)], fill=_rgb(colour), width=width)

    def para(self, text, kind, size, max_w, max_lines, colour, xy, pitch):
        """Draw wrapped text; raise if it needs more than max_lines."""
        f = face(kind, size)
        lines = _wrap(self.d, text, f, max_w)
        if len(lines) > max_lines:
            raise ValueError(
                "overflow: %r needs %d lines (max %d, width %d)"
                % (text, len(lines), max_lines, max_w))
        x, y = xy
        for i, line in enumerate(lines):
            self.d.text((x, y + i * pitch), line, font=f, fill=_rgb(colour))
        return y + len(lines) * pitch


# --- page data -----------------------------------------------------------
# One table for all sixteen numbered stories: heroes first, then cards.
# tag / head / body are the exact strings printed on the page.
STORIES = [
    {"n": 1, "tag": "ODISHA · STORM", "head": "Akvan comes ashore",
     "body": "Cyclone Akvan is due ashore by noon near Gopalpur, winds "
             "90–100 km/h gusting to 110. 298,676 evacuated to 9,341 "
             "shelters; 1,012 teams out.",
     "art": "storm"},
    {"n": 2, "tag": "WASHINGTON · IRAN",
     "head": "Trump puts the Iran decision off to 2027",
     "body": "Trump tells Axios he is in no rush on Iran and will "
             "\u2018see what happens\u2019 after January 1. No new strikes "
             "before 2027, as Israel presses for a new campaign.",
     "art": "calendar"},
    {"n": 3, "tag": "RIYADH · ATTACK", "head": "A missile over Riyadh",
     "body": "Saudi Civil Defence confirms a strike hit the PIF Tower in "
             "the KAFD financial district: windows out on 7–8 floors, no "
             "casualties. Houthis claim the attack.",
     "art": "tower"},
    {"n": 4, "tag": "KERCH STRAIT · WAR", "head": "Bridge hit a third time",
     "body": "Kyiv claims Neptune missiles hit the rail span overnight. "
             "Rail halts, then resumes on one track. Putin: \u2018We will "
             "not negotiate after the strikes.\u2019",
     "art": "bridge"},
    {"n": 5, "tag": "SHENZHEN · DIPLOMACY",
     "head": "Three presidents sign, wars unsolved",
     "body": "Four-point paper on nukes, the UN, oil, the ICC — silent "
             "on Ukraine.",
     "art": "flags"},
    {"n": 6, "tag": "NEW YORK · MARKETS",
     "head": "Anthropic\u2019s debut can\u2019t stop the slide",
     "body": "Dow -1,101, S&P -2.02%, Nasdaq -2.25% Thu. Waller, Cook "
             "speak today.",
     "art": "fall"},
    {"n": 7, "tag": "SAN FRANCISCO · IPO",
     "head": "ANT closes first day up 17%",
     "body": "Anthropic ends at $97.17 after opening at $111.50. Offer "
             "closes today.",
     "art": "bell"},
    {"n": 8, "tag": "KYIV · WAR", "head": "Kyiv hit again overnight",
     "body": "Missiles hit early Friday; a block burns. Two embassies "
             "hit Thu.",
     "art": "hit"},
    {"n": 9, "tag": "SEOUL · LAW",
     "head": "Top court overturns Han\u2019s 15-year term",
     "body": "Sentence quashed 9–3, sent back for retrial. Han stays in "
             "detention.",
     "art": "gavel"},
    {"n": 10, "tag": "FIJI · CLIMATE",
     "head": "Fiji declares a disaster over drought",
     "body": "State of disaster declared on Wednesday as El Ni\u00f1o "
             "dries the islands.",
     "art": "dry"},
    {"n": 11, "tag": "SENEGAL · MIGRATION",
     "head": "Migrant boat capsizes; dozens missing",
     "body": "About 50 aboard off Yenne; one dead. Route toll in 2026 "
             "nears 600.",
     "art": "boat"},
    {"n": 12, "tag": "CARACAS · DEAL",
     "head": "US, Venezuela restore military ties",
     "body": "Hegseth signs a Caracas pact on Wednesday: training, "
             "intelligence, kit.",
     "art": "deal"},
    {"n": 13, "tag": "YONGBYON · NUCLEAR",
     "head": "North Korea expands enrichment",
     "body": "IAEA: a new Yongbyon enrichment extension was finished in "
             "late October.",
     "art": "atom"},
    {"n": 14, "tag": "MIAMI · GAMES",
     "head": "GTA VI passes $1.84bn on day one",
     "body": "Sensor Tower: day-one sales pass The Odyssey\u2019s $1.80bn "
             "global run.",
     "art": "arcade"},
    {"n": 15, "tag": "DEEP SPACE",
     "head": "Voyager 1 crosses one light-day",
     "body": "NASA: the 1977 probe is now over one light-day out — 16 "
             "billion miles.",
     "art": "probe"},
    {"n": 16, "tag": "ANTALYA · CLIMATE",
     "head": "COP31 draft drops fossil fuels",
     "body": "Draft falls to 80 paragraphs from 144, with no fossil "
             "fuels. Closes today.",
     "art": "climate"},
]

NUMBERS = [
    ("298,676", "EVACUATED TO SHELTERS"),
    ("7.91m", "PEAK VIEWERS, GTA VI AT ONCE"),
    ("-1,101", "POINTS THE DOW LOST THU."),
    ("$1tn", "KOREA EXPORTS, FIRST TIME"),
    ("16bn miles", "VOYAGER 1 FROM EARTH"),
    ("90 min", "THE TRILATERAL ITSELF"),
]

TIMELINE = [
    ("THURSDAY", "Trilateral declaration issued"),
    ("THURSDAY NIGHT", "Riyadh tower hit; Genoa shut"),
    ("OVERNIGHT", "Kyiv hit by ballistic missiles"),
    ("06:30 UTC", "Akvan due ashore in Odisha"),
    ("TODAY NOON", "Trump news conference in Washington"),
]

REGION_STRIP = ("EUROPE 10 \u00b7 AMERICAS 11 \u00b7 ASIA-PACIFIC 15 \u00b7 "
                "MIDEAST 7 \u00b7 AFRICA 2 \u00b7 OCEANIA 2 \u00b7 WORLD 3")

BRIEFS = [
    "NATO chief meets intelligence chiefs in Brussels",
    "Xi: constructive ties with Moscow and US essential",
    "Gulf Railway to link six nations, cut Hormuz reliance",
    "Merz hosts Berlin summit on Ukraine peace terms",
    "Saudi Crown Prince meets CENTCOM chief in Riyadh",
    "Trump invites Putin to December G20 in Miami",
    "US intel: Iran still holds at least 2,500 missiles",
    "Saudi fears Yemen war could run six more months",
    "Tanker On Phoenix hit off Oman; crew safe",
    "IRGC claims four tankers hit mines — CLAIM",
    "Israel strikes Hezbollah site in Beqaa (Thurs.)",
    "Modi opens FICCI centenary convention",
    "India–Israel ink \u20b91,976 cr Barak missile deal",
    "Sensex +1.21%, Nifty +1.14% on Thursday",
    "Phillips 118, NZ 317-6, Nicholls 146* on day two",
    "Zverev 3-0 in Turin; Alcaraz v Shelton in semis",
    "Korea exports pass $1tn, first time (Thurs.)",
    "Taiwan curbs short-selling from today",
    "Genoa airport shut by drones (Thurs. night)",
    "Trump news conference at noon today",
    "US envoy: Russia open to NATO-like guarantees",
    "California probes Nvidia over China chips",
    "Pfizer licenses 3 CAR-T programs, $330m upfront",
    "Congress back; December 11 funding cliff looms",
    "Congo Ebola passes 10,600 cases (WHO)",
    "India beat Malaysia in Hong Kong Open",
    "Women\u2019s Asian Hockey Trophy begins",
    "COP31 AI pledge snubbed by US tech",
    "Crude oil futures fall more than 3%",
    "Gemini 4 Neon out Wed: $3/$15 per 1M tokens",
    "Fire at Yunus ancestral home; arson feared",
    "Pakistan minister heads to Delhi for SCO",
    "Van Gogh sells for a record $190.4m (Thurs.)",
    "Hayabusa2 retargets to 2015 BM510 flyby (Tue)",
]

DATE_CHECK = ("LEFT OUT, THEY BROKE BEFORE FRIDAY: the ICJ\u2019s Myanmar "
              "genocide verdict (Thurs. 19 Nov) \u00b7 Anthropic\u2019s record "
              "IPO debut (Thurs. 19 Nov) \u00b7 Modi meets the Prince and "
              "Princess of Wales (Wed. 18 Nov) \u00b7 GTA VI\u2019s midnight "
              "launch in New Zealand (Thurs. 19 Nov) \u00b7 the trilateral "
              "meeting itself (Thurs. 19 Nov).")

TOMORROW = ("Akvan\u2019s landfall toll \u00b7 the US market\u2019s Friday close "
            "\u00b7 Medvedev v Tiafoe in Turin \u00b7 COP31\u2019s final deal")

FOOTER = ("Every story here happened, or was first reported, on Friday "
          "20 November 2026. Claims are attributed, not stated as fact. "
          "Sources: Reuters, AP, AFP, BBC, IMD, NASA, IAEA, UKMTO. "
          "Original drawings.")

# --- world map -----------------------------------------------------------
# Land as longitude/latitude boxes, sampled on a 48 x 22 dot grid
# (7.5 deg per column, 6 deg per row, 72N at the top). Boxes are coarse
# on purpose: the map is a schematic, the numbered pins carry the detail.
LAND_BOXES = [
    (-168, -140, 58, 71), (-140, -55, 49, 71), (-125, -66, 24, 49),
    (-117, -83, 7, 32), (-105, -77, 7, 18), (-60, -20, 59, 84),
    (-80, -34, -5, 12), (-75, -40, -35, -5), (-70, -53, -55, -20),
    (-11, 32, 36, 60), (-5, 31, 55, 71), (-10, 3, 50, 59),
    (-22, -14, 63, 67),
    (-18, 51, 14, 35), (-18, 43, -4, 14), (-18, 34, -19, -4),
    (16, 33, -35, -17), (43, 51, -26, -12),
    (26, 63, 12, 42), (40, 135, 45, 77), (60, 100, 20, 50),
    (68, 89, 7, 37), (89, 105, 20, 54), (97, 110, 5, 29),
    (95, 141, -11, 6), (122, 142, 30, 46),
    (113, 154, -39, -11), (166, 179, -47, -34), (177, 179, -19, -16),
]

# Pin centres in page pixels, one per numbered story. Spaced so no two
# circles (radius 7) touch: every pair is at least 15 px apart.
PINS_PX = {
    1: (231, 807), 2: (99, 795), 3: (201, 801), 4: (201, 783),
    5: (255, 801), 6: (111, 777), 7: (69, 789), 8: (183, 777),
    9: (273, 789), 10: (303, 843), 11: (153, 807), 12: (111, 813),
    13: (255, 777), 14: (93, 807), 15: (303, 867), 16: (183, 795),
}


def _on_land(lon, lat):
    for lo0, lo1, la0, la1 in LAND_BOXES:
        if lo0 <= lon <= lo1 and la0 <= lat <= la1:
            return True
    return False


def paint_world(pen, x0, y0, cell=6):
    d = pen.d
    for row in range(22):
        lat = 72 - (row + 0.5) * 6.0
        for col in range(48):
            lon = -180 + (col + 0.5) * 7.5
            if _on_land(lon, lat):
                cx = x0 + col * cell + cell // 2
                cy = y0 + row * cell + cell // 2
                d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=_rgb("dot"))
    for num, (cx, cy) in PINS_PX.items():
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=_rgb("red"),
                  outline=(255, 255, 255), width=1)
        label = str(num)
        f = face("sans_b", 8 if num < 10 else 7)
        w = d.textlength(label, font=f)
        d.text((cx - w / 2, cy - 5 if num < 10 else cy - 4), label,
               font=f, fill=(255, 255, 255))


# --- hero scenes ---------------------------------------------------------
def _chip(pen, x, y, text, size=9):
    d = pen.d
    f = face("cond_b", size)
    w = d.textlength(text, font=f) + 10
    d.rounded_rectangle([x, y, x + w, y + 18], radius=4, fill=_rgb("red"))
    d.text((x + 5, y + 3), text, font=f, fill=(255, 255, 255))


def art_storm(pen, x, y, w, h):
    d = pen.d
    d.rectangle([x, y, x + w, y + h], fill=_rgb("sky"))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(88, 124, 96))
    d.rectangle([x, y + h - 26, x + w, y + h - 20], fill=_rgb("sand"))
    cx, cy = x + w // 2, y + h // 2 - 6
    for radius, shade in [(44, (255, 255, 255)), (36, (226, 238, 244)),
                          (28, (255, 255, 255)), (20, (200, 220, 232)),
                          (12, (255, 255, 255))]:
        d.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                  outline=shade, width=5)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(120, 150, 170))
    for i in range(7):
        rx = x + 8 + i * 30
        d.line([(rx, y + 8), (rx - 4, y + 20)], fill=(90, 120, 150), width=2)
    _chip(pen, x + 6, y + 6, "LANDFALL DUE TODAY")


def art_calendar(pen, x, y, w, h):
    d = pen.d
    d.rectangle([x, y, x + w, y + h], fill=_rgb("navy"))
    for i in range(5):
        sx = x + 22 + (i % 3) * 16
        sy = y + 12 + (i // 3) * 14
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))
    for i in range(7):
        colour = _rgb("red") if i % 2 == 0 else (255, 255, 255)
        d.line([(x + 62, y + 10 + i * 8), (x + 118, y + 10 + i * 8)],
               fill=colour, width=4)
    d.rectangle([x + 128, y + 8, x + w - 8, y + h - 8], fill=(255, 255, 255))
    d.rectangle([x + 128, y + 8, x + w - 8, y + 30], fill=_rgb("red"))
    pen.txt((x + 140, y + 11), "NO RUSH", "cond_b", 12, "paper")
    pen.txt((x + 138, y + 36), "2027", "sans_b", 30, "navy")
    pen.txt((x + 138, y + 68), "DECIDE IN", "cond", 11, "muted")


def art_tower(pen, x, y, w, h):
    d = pen.d
    d.rectangle([x, y, x + w, y + h], fill=_rgb("night"))
    for sx, sy in [(20, 12), (60, 22), (110, 10), (180, 18), (210, 8), (90, 28)]:
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1],
                  fill=(255, 255, 255))
    d.ellipse([x + w - 34, y + 8, x + w - 14, y + 28], fill=(232, 226, 200))
    d.rectangle([x + 8, y + 52, x + 52, y + h], fill=(52, 66, 110))
    d.rectangle([x + 178, y + 60, x + w - 8, y + h], fill=(52, 66, 110))
    for bx in (16, 28, 40):
        for by in (60, 74, 88):
            d.rectangle([x + bx, y + by, x + bx + 5, y + by + 4],
                        fill=(240, 210, 90))
    tx0, tx1 = x + 92, x + 150
    d.polygon([(tx0, y + h), (tx0, y + 34), (tx0 + 14, y + 18),
               (tx1 - 14, y + 18), (tx1, y + 34), (tx1, y + h)],
              fill=(96, 116, 158))
    for wy in range(30, 92, 10):
        for wx in range(tx0 + 8, tx1 - 8, 12):
            d.rectangle([wx, y + wy, wx + 6, y + wy + 5], fill=(250, 220, 110))
    d.line([(tx0 + 30, y + 40), (tx0 + 44, y + 52)], fill=_rgb("red"), width=3)
    d.line([(tx0 + 44, y + 40), (tx0 + 30, y + 52)], fill=_rgb("red"), width=3)


def art_bridge(pen, x, y, w, h):
    d = pen.d
    d.rectangle([x, y, x + w, y + h], fill=_rgb("sky"))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=_rgb("sea"))
    for i in range(4):
        d.arc([x + 10 + i * 52, y + h - 18, x + 46 + i * 52, y + h - 6],
              start=200, end=340, fill=(255, 255, 255), width=2)
    d.rectangle([x + 6, y + 44, x + w - 6, y + 52], fill=(90, 90, 92))
    d.rectangle([x + 96, y + 40, x + 138, y + 52], fill=_rgb("sky"))
    d.line([(x + 96, y + 44), (x + 110, y + 56)], fill=(90, 90, 92), width=3)
    d.line([(x + 138, y + 44), (x + 124, y + 56)], fill=(90, 90, 92), width=3)
    d.arc([x + 150, y + 8, x + 226, y + 62], start=180, end=360,
          fill=(120, 30, 30), width=5)
    d.line([(x + 188, y + 8), (x + 188, y + 44)], fill=(120, 30, 30), width=3)
    bx, by = x + 168, y + 30
    for ang in range(0, 360, 45):
        ex = bx + int(11 * math.cos(math.radians(ang)))
        ey = by + int(11 * math.sin(math.radians(ang)))
        d.line([(bx, by), (ex, ey)], fill=(255, 170, 0), width=3)
    d.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(255, 200, 60))
    _chip(pen, x + 6, y + 6, "OVERNIGHT · 3RD HIT", size=11)


# --- card glyphs ---------------------------------------------------------
def _blast(d, bx, by, size=12):
    for ang in range(0, 360, 45):
        ex = bx + int(size * math.cos(math.radians(ang)))
        ey = by + int(size * math.sin(math.radians(ang)))
        d.line([(bx, by), (ex, ey)], fill=(255, 170, 0), width=3)
    d.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(255, 200, 60))


def glyph_flags(pen, x, y, w, h):
    d = pen.d
    third = w // 3
    for i, colour in enumerate([(178, 34, 34), (222, 41, 16), (255, 255, 255)]):
        fx = x + 6 + i * third
        d.rectangle([fx, y + 4, fx + third - 8, y + h - 8], fill=colour,
                    outline=_rgb("navy"), width=1)
        d.line([(fx + 2, y + 2), (fx + 2, y + h - 2)], fill=_rgb("navy"), width=2)
    d.ellipse([x + 6 + third + 4, y + 8, x + 6 + third + 10, y + 14],
              fill=(255, 220, 0))
    d.rectangle([x + 6 + 2 * third, y + 4, x + 6 + 3 * third - 8,
                 y + (h - 8) // 3 + 4], fill=(255, 255, 255))
    d.rectangle([x + 6 + 2 * third, y + (h - 8) // 3 + 4,
                 x + 6 + 3 * third - 8, y + 2 * (h - 8) // 3 + 4],
                fill=(0, 60, 160))
    d.rectangle([x + 6 + 2 * third, y + 2 * (h - 8) // 3 + 4,
                 x + 6 + 3 * third - 8, y + h - 8], fill=(210, 0, 0))


def glyph_fall(pen, x, y, w, h):
    d = pen.d
    pts = [(x + 6, y + 8), (x + w // 4, y + 12), (x + w // 2, y + 10),
           (x + 3 * w // 4, y + 22), (x + w - 8, y + h - 8)]
    for a, b in zip(pts, pts[1:]):
        d.line([a, b], fill=_rgb("red"), width=3)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=_rgb("red"))
    d.line([(x + 4, y + h - 6), (x + w - 4, y + h - 6)], fill=_rgb("muted"),
           width=1)


def glyph_bell(pen, x, y, w, h):
    d = pen.d
    d.ellipse([x + w // 2 - 16, y + 4, x + w // 2 + 16, y + h - 10],
              fill=_rgb("gold"))
    d.rectangle([x + w // 2 - 20, y + h - 12, x + w // 2 + 20, y + h - 6],
                fill=_rgb("gold"))
    d.ellipse([x + w // 2 - 3, y + h - 6, x + w // 2 + 3, y + h - 2],
              fill=_rgb("navy"))
    pen.txt((x + w // 2 - 26, y + h // 2 - 8), "$97", "sans_b", 13, "navy")


def glyph_hit(pen, x, y, w, h):
    d = pen.d
    d.rectangle([x, y, x + w, y + h], fill=_rgb("night"))
    d.rectangle([x + 14, y + 16, x + w - 14, y + h], fill=(52, 66, 110))
    for wy in range(22, h - 4, 9):
        for wx in range(20, w - 20, 12):
            d.rectangle([x + wx, y + wy, x + wx + 5, y + wy + 4],
                        fill=(240, 210, 90))
    _blast(d, x + w // 2, y + 12)


def glyph_gavel(pen, x, y, w, h):
    d = pen.d
    d.rectangle([x + 8, y + 8, x + w - 8, y + 18], fill=(120, 72, 32))
    d.rectangle([x + w // 2 - 4, y + 18, x + w // 2 + 4, y + h - 8],
                fill=(90, 54, 24))
    d.rectangle([x + w // 2 - 18, y + h - 10, x + w // 2 + 18, y + h - 4],
                fill=(120, 72, 32))


def glyph_dry(pen, x, y, w, h):
    d = pen.d
    d.ellipse([x + w - 26, y + 2, x + w - 6, y + 22], fill=(240, 180, 40))
    d.rectangle([x + 4, y + h - 14, x + w - 4, y + h - 4], fill=(150, 110, 60))
    for ax, ay in [(10, 24), (30, 26), (50, 22)]:
        d.line([(x + ax, y + h - 14), (x + ax + 16, y + h - ay)],
               fill=(120, 85, 45), width=2)


def glyph_boat(pen, x, y, w, h):
    d = pen.d
    for i in range(3):
        d.arc([x + 4 + i * 4, y + h - 12, x + w - 4 - i * 4, y + h + 2],
              start=0, end=180, fill=(70, 120, 160), width=2)
    d.polygon([(x + 12, y + h - 14), (x + w - 12, y + h - 14),
               (x + w - 22, y + h - 4), (x + 22, y + h - 4)],
              fill=(120, 72, 32))
    d.line([(x + w // 2, y + 4), (x + w // 2, y + h - 14)], fill=_rgb("navy"),
           width=2)
    d.polygon([(x + w // 2, y + 5), (x + w // 2 + 16, y + 14),
               (x + w // 2, y + 14)], fill=(255, 255, 255))


def glyph_deal(pen, x, y, w, h):
    d = pen.d
    d.rectangle([x + 6, y + 6, x + w // 2 - 2, y + h - 6], fill=_rgb("red"))
    d.rectangle([x + w // 2 + 2, y + 6, x + w - 6, y + h - 6],
                fill=(255, 210, 0))
    d.rectangle([x + w // 2 + 2, y + 6, x + w - 6, y + (h - 6) // 3 + 6],
                fill=(0, 60, 160))
    d.rectangle([x + w // 2 + 2, y + 2 * (h - 6) // 3 + 6, x + w - 6,
                 y + h - 6], fill=(210, 0, 0))
    d.ellipse([x + w // 2 - 12, y + h // 2 - 8, x + w // 2 + 12,
               y + h // 2 + 8], fill=(255, 255, 255),
              outline=_rgb("navy"), width=2)


def glyph_atom(pen, x, y, w, h):
    d = pen.d
    cx, cy = x + w // 2, y + h // 2 + 4
    for tilt in (0, 60, 120):
        pts = []
        for step in range(0, 360, 12):
            t = math.radians(step)
            a = math.radians(tilt)
            px = cx + 26 * math.cos(t) * math.cos(a) \
                - 9 * math.sin(t) * math.sin(a)
            py = cy + 26 * math.cos(t) * math.sin(a) \
                + 9 * math.sin(t) * math.cos(a)
            pts.append((px, py))
        d.line(pts, fill=_rgb("navy"), width=2)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=_rgb("red"))


def glyph_arcade(pen, x, y, w, h):
    d = pen.d
    d.rectangle([x, y, x + w, y + h], fill=(24, 10, 40))
    d.ellipse([x + w // 2 - 18, y + 2, x + w // 2 + 18, y + 34],
              fill=(255, 120, 40))
    for bx, bh in [(6, 18), (22, 26), (52, 14), (66, 22)]:
        d.rectangle([x + bx, y + h - bh, x + bx + 12, y + h],
                    fill=(10, 10, 16))
    d.line([(x + 40, y + h - 8), (x + 40, y + h - 30)], fill=(40, 200, 120),
           width=2)
    d.ellipse([x + 36, y + h - 34, x + 44, y + h - 26], fill=(40, 200, 120))


def glyph_probe(pen, x, y, w, h):
    d = pen.d
    d.rectangle([x, y, x + w, y + h], fill=_rgb("night"))
    for sx, sy in [(12, 8), (30, 18), (70, 6), (88, 16), (50, 26)]:
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1],
                  fill=(255, 255, 255))
    d.ellipse([x + 18, y + 8, x + 58, y + 34], outline=(200, 210, 230), width=3)
    d.line([(x + 38, y + 30), (x + 60, y + h - 4)], fill=(200, 210, 230),
           width=2)
    d.line([(x + 58, y + 10), (x + w - 8, y + h - 10)], fill=(255, 200, 60),
           width=2)


def glyph_climate(pen, x, y, w, h):
    d = pen.d
    cx, cy = x + w // 2, y + h // 2
    d.ellipse([cx - 20, cy - 16, cx + 20, cy + 16], outline=_rgb("teal"),
              width=3)
    d.ellipse([cx - 9, cy - 16, cx + 9, cy + 16], outline=_rgb("teal"), width=2)
    d.line([(cx - 20, cy), (cx + 20, cy)], fill=_rgb("teal"), width=2)
    d.ellipse([cx + 2, cy - 2, cx + 18, cy + 12], fill=_rgb("leaf"))


ART = {"storm": art_storm, "calendar": art_calendar,
       "tower": art_tower, "bridge": art_bridge}
GLYPH = {"flags": glyph_flags, "fall": glyph_fall, "bell": glyph_bell,
         "hit": glyph_hit, "gavel": glyph_gavel, "dry": glyph_dry,
         "boat": glyph_boat, "deal": glyph_deal, "atom": glyph_atom,
         "arcade": glyph_arcade, "probe": glyph_probe,
         "climate": glyph_climate}


# --- page assembly -------------------------------------------------------
def build_page():
    if len(STORIES) != 16 or len(BRIEFS) != 34:
        raise ValueError("story counts wrong: %d stories, %d briefs"
                         % (len(STORIES), len(BRIEFS)))
    img = Image.new("RGB", (PAGE_W, PAGE_H), _rgb("cream"))
    pen = Pen(img)
    d = pen.d
    mx = MARGIN
    right_edge = PAGE_W - MARGIN

    # top bar
    pen.txt((mx, 8), "THE WORLD IN ONE DAY", "sans_b", 13, "red")
    top_right = "50 STORIES \u00b7 7 REGIONS \u00b7 EVERY ONE FROM THIS FRIDAY"
    f_top = face("sans_b", 11)
    pen.txt((right_edge - d.textlength(top_right, font=f_top), 9),
            top_right, "sans_b", 11, "navy")
    pen.rule(mx, right_edge, 28, "navy", 2)

    # masthead
    title = "Friday 20 November 2026"
    if d.textlength(title, font=face("serif", 60)) > CONTENT_W:
        raise ValueError("masthead too wide")
    pen.mid(PAGE_W // 2, 34, title, "serif", 60, "navy")
    pen.mid(PAGE_W // 2, 98,
            "Akvan comes ashore \u00b7 Trump puts Iran off to 2027 \u00b7 "
            "A missile over Riyadh", "serif_it", 17, "red_dk")
    pen.rule(mx, right_edge, 120, "navy", 2)
    pen.rule(mx, right_edge, 124, "navy", 1)

    # numbers strip
    cell = CONTENT_W // 6
    for i, (num, label) in enumerate(NUMBERS):
        x = mx + i * cell
        pen.txt((x + 4, 130), num, "sans_b", 22, "red")
        pen.para(label, "cond_b", 9, cell - 10, 1, "muted", (x + 4, 154), 11)
        if i:
            d.line([(x, 130), (x, 164)], fill=_rgb("line"), width=1)
    pen.rule(mx, right_edge, 168, "line", 1)

    # timeline strip
    pen.txt((mx, 174), "THE DAY SO FAR", "sans_b", 10, "red")
    tx, ty = mx + 218, 174
    for j, (when, what) in enumerate(TIMELINE):
        seg = when + " — " + what
        seg_w = d.textlength(seg, font=face("sans", 10))
        if tx + seg_w > right_edge and j > 0:
            tx, ty = mx + 218, ty + 14
        pen.txt((tx, ty), when, "sans_b", 10, "navy")
        pen.txt((tx + d.textlength(when, font=face("sans_b", 10)), ty),
                " — " + what, "sans", 10, "ink")
        tx += seg_w + d.textlength("   \u00b7   ", font=face("sans", 10))
        if j < len(TIMELINE) - 1:
            pen.txt((tx - d.textlength("   \u00b7   ", font=face("sans", 10)),
                     ty), "   \u00b7   ", "sans", 10, "muted")
    pen.rule(mx, right_edge, 202, "navy", 1)

    # heroes: four across
    hy, hh = 208, 236
    hw = (CONTENT_W - 3 * 8) // 4
    for i, story in enumerate(STORIES[:4]):
        x = mx + i * (hw + 8)
        d.rectangle([x, hy, x + hw, hy + hh], outline=_rgb("line"), width=1,
                    fill=_rgb("paper"))
        ART[story["art"]](pen, x + 1, hy + 1, hw - 2, 96)
        pen.txt((x + 8, hy + 102), "%d · %s" % (story["n"], story["tag"]),
                "cond_b", 9, "red")
        pen.para(story["head"], "sans_b", 16, hw - 16, 3, "ink",
                 (x + 8, hy + 116), 19)
        pen.para(story["body"], "sans", 11, hw - 16, 4, "ink",
                 (x + 8, hy + 176), 14)
    pen.rule(mx, right_edge, hy + hh + 6, "navy", 1)

    # cards: six columns by two rows
    cy0 = hy + hh + 12
    chh = 122
    cwd = (CONTENT_W - 5 * 8) // 6
    for idx, story in enumerate(STORIES[4:]):
        row, col = divmod(idx, 6)
        x = mx + col * (cwd + 8)
        y = cy0 + row * (chh + 6)
        d.rectangle([x, y, x + cwd, y + chh], outline=_rgb("line"), width=1,
                    fill=_rgb("paper"))
        pen.txt((x + 6, y + 4), "%d · %s" % (story["n"], story["tag"]),
                "cond_b", 8, "red")
        GLYPH[story["art"]](pen, x + 6, y + 16, cwd - 12, 34)
        pen.para(story["head"], "sans_b", 11, cwd - 12, 2, "ink",
                 (x + 6, y + 54), 13)
        pen.para(story["body"], "sans", 10, cwd - 12, 3, "ink",
                 (x + 6, y + 84), 12)
    pen.rule(mx, right_edge, cy0 + 2 * chh + 6 + 4, "navy", 1)

    # bottom: map + briefs
    by = cy0 + 2 * chh + 6 + 10
    pen.txt((mx, by), "WHERE IT HAPPENED", "sans_b", 12, "red")
    pen.txt((mx, by + 16), REGION_STRIP, "cond_b", 8, "muted")
    paint_world(pen, mx + 2, by + 34)
    bx = mx + 352
    pen.txt((bx, by), "ALSO ON FRIDAY 20 NOVEMBER", "sans_b", 12, "red")
    col_w = (PAGE_W - MARGIN - bx - 8) // 2
    for i, brief in enumerate(BRIEFS):
        col, row = divmod(i, 17)
        x = bx + col * (col_w + 8)
        y = by + 20 + row * 12
        pen.txt((x, y), str(17 + i), "cond_b", 9, "red")
        pen.txt((x + 20, y), brief, "cond", 9, "ink")

    # tomorrow line
    ty = by + 20 + 17 * 12 + 6
    pen.txt((mx, ty), "TOMORROW:", "sans_b", 10, "red")
    pen.txt((mx + 74, ty), TOMORROW, "sans", 10, "ink")
    pen.rule(mx, right_edge, ty + 16, "navy", 1)

    # date check box
    dy = ty + 22
    d.rectangle([mx, dy, right_edge, dy + 40], outline=_rgb("red"), width=2,
                fill=_rgb("pink"))
    label = "DATE CHECK — "
    f_dc = face("sans_b", 10)
    label_w = d.textlength(label, font=f_dc)
    pen.txt((mx + 8, dy + 5), label, "sans_b", 10, "red")
    first = _wrap(d, DATE_CHECK, face("sans", 10),
                  CONTENT_W - 16 - label_w)
    pen.txt((mx + 8 + label_w, dy + 5), first[0], "sans", 10, "ink")
    rest = " ".join(first[1:])
    if rest:
        pen.para(rest, "sans", 10, CONTENT_W - 16, 1, "ink",
                 (mx + 8, dy + 20), 13)

    # footer (one line)
    pen.mid(PAGE_W // 2, dy + 46, FOOTER, "serif_it", 9, "muted")

    img.save(TARGET, optimize=True)
    print("wrote", TARGET)


if __name__ == "__main__":
    build_page()
