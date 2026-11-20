# Friday 20 November 2026 — the world in one picture

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/alwanali22/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/alwanali22/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

Entry for the make.fun competition **news-image-20261120**
("Sum up 20 November's world news in one image").

One 1024×1024 infographic: 50 stories — 4 hero stories (Cyclone Akvan's
landfall, Trump putting the Iran decision off to 2027, the Houthi missile
over Riyadh, the third Kerch Bridge strike), 12 cards, a dotted world map
with numbered pins, and 34 numbered briefs — plus a region-count strip, a
DATE CHECK box naming the famous stories that broke before Friday and were
deliberately left out, and a timeline of the day so far.

v2 (morning refresh, 20 Nov ~09:10 WIB): Akvan preparedness updated
(298,676 evacuated to 9,341 shelters); Kyiv hit again overnight into
Friday; Saudi confirmation of the Riyadh tower hit; COP31 draft drops
fossil fuels; Korea passes $1tn in exports; Friday sports (Phillips 118,
NZ 317-6, Nicholls 146* on day two). The Friday US market close and the
Akvan landfall toll did not exist yet at build time (close 21:00 UTC,
landfall 06:30 UTC) — the page keeps Thursday's close, labelled Thursday,
and names both in the TOMORROW line. See `../V2-REPORT.md`.

Every story on the page happened, or was first reported, on Friday
20 November 2026 (any time zone). Stories from 17–19 November carry their
day inside their body text. Claims are attributed, never stated as fact.
All scenes are drawn in code; no photographs are used.

## Files

- `entry.png` — the image (1024×1024, under 1 MiB)
- `main.py` — the entrypoint: copies `entry.png` to `/output/entry.png`
- `draw_v2.py` — the v2 generator that draws `entry.png` (pure PIL, no
  network, no clock, no randomness; two runs write byte-identical PNGs).
  `draw_v1.py` is kept as the v1 generator for provenance.
- `LICENSE` — MIT

## Run it

```sh
python3 draw_v2.py            # regenerate entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

See `../STRATEGY.md` and `../SOURCES.md` for the scoring strategy, the
top-10 comparison, and the verified source list for every story.
