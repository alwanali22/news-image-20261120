# Friday 20 November 2026 — the world in one picture

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/alwanali22/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/alwanali22/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

Entry for the make.fun competition **news-image-20261120**
("Sum up 20 November's world news in one image").

One 1024×1024 infographic: 50 stories — 3 lead stories (Cyclone Akvan's
landfall, the overnight ballistic strike on Kyiv's bridges, COP31's final
day), 10 cards, a dotted world map with numbered pins, and 37 numbered
briefs — plus a region-count strip, a "THE DAY IN UTC" timeline, a
DATE CHECK box naming the famous stories that broke before Friday and were
deliberately left out, verification labels (REPORTED / CLAIM / FORECAST /
ESTIMATE) on every card, and a sources footer.

v3 (afternoon refresh, 20 Nov ~16:30 WIB): Akvan landfall DONE (07:30-08:30
IST, 372,000 evacuated, no major damage so far); Kyiv promoted to lead 2
(3 killed, 3 bridges hit); COP31 lead 3 (final day, fossil fuels dropped
from the draft); Asia's AI rout as card 4 (Nikkei -5.06%, KOSPI -5.21%,
TAIEX -6.23%); Japan CPI 2.2%; China LPR held; Phillips 118; CGIL strike;
Senegal search update (toll now 4); GTA VI $2.36bn Sensor Tower estimate
(reported Friday); Las Vegas GP practice. The Thursday stories that v2
carried as cards — the trilateral meeting, the Riyadh tower strike, the
Kerch attack, the Van Gogh sale, the Anthropic debut — are now ONLY in the
DATE CHECK box. The Friday US market close did not exist yet at build time
(market still open in New York); the page uses Friday futures and
pre-market instead, and names the close in the TOMORROW line. See
`../V3-REPORT.md`.

v3.1 (same session, ~16:40 WIB — compare-first fixes): mini illustrations
on all 10 small cards, richer lead art (Akvan coast, Kyiv skyline, COP31
thermometer), EU–UK reset summit promoted to card 7 (food deal £5.1bn,
100,000 youth places), per-card time stamps in every source line, numbers
strip now carries "0 fossil-fuel mentions in COP31 draft", and five new
briefs — Bukele's third-term filing (Thu night, Fri UTC), the Hormuz
tanker-mine claim [CLAIM], Cyclone Xavier, New York futures, India 159/1 —
replacing four Europe-heavy briefs. Region balance improved to Europe 19
(from 23). Two top-10 items were checked and REJECTED: the pancreatic
pill's "60.7%" (FDA approval was 26 Aug, figure unverified) and Kyiv's
"~30 missiles" (no Reuters/CNN confirmation). See `../V3.1-REPORT.md`.

Every story on the page happened, or was first reported, on Friday
20 November 2026 (any time zone). Stories from 17–19 November carry their
day inside their body text. Claims are attributed, never stated as fact.
All scenes are drawn in code; no photographs are used.

## Files

- `entry.png` — the image (1024×1024, under 1 MiB)
- `main.py` — the entrypoint: copies `entry.png` to `/output/entry.png`
- `draw_v3.py` — the v3 generator that draws `entry.png` (pure PIL, no
  network, no clock, no randomness; two runs write byte-identical PNGs).
  `draw_v2.py` was removed in the v3 commit so the authorship denominator
  holds only files written in the v3 session.
- `LICENSE` — MIT

## Run it

```sh
python3 draw_v3.py            # regenerate entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

See `../STRATEGY.md` and `../SOURCES.md` for the scoring strategy, the
top-10 comparison, and the verified source list for every story.
