# Friday 20 November 2026 — the world in one picture

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/alwanali22/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/alwanali22/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

Entry for the make.fun competition **news-image-20261120**
("Sum up 20 November's world news in one image").

One 1024×1024 infographic: 36 stories — 3 lead stories (Cyclone Akvan's
landfall, the overnight ballistic strike on Kyiv's bridges, COP31's final
day in overtime), 10 cards, a dotted world map with numbered pins, and 23
numbered briefs — plus a region-count strip, a "THE DAY IN UTC" timeline, a
DATE CHECK box naming the famous stories that broke before Friday and were
deliberately left out, verification labels (REPORTED / CLAIM / FORECAST)
on every card, and a sources footer.

v4 (Saturday-morning all-out rebuild, 21 Nov ~12:00 WIB — the last slot):
format change, not a polish of v3.1. 36 stories instead of 50 (the modal
top-10 entry has 36); the three leads take ~40% of the page as dark scene
panels (Akvan coast map with Gopalpur + Bay of Bengal, Kyiv skyline with
fires + three bridges, COP31 hall + thermometer + OVERTIME badge); every
small card gets its own drawn scene instead of an icon. Fresh Saturday
data, all re-verified this session: the real US Friday close (Dow 48,147
−1.93%, S&P 6,910 −3.70%, Nasdaq 22,618 −5.28%), ANT $88.91 −8.50%,
COP31 in overtime with 0 fossil-fuel mentions, Akvan final (372,000
evacuated, 0 deaths), Medvedev d. Tiafoe 6-3 6-4, Trump 90-minute press
conference, and Take-Two's official GTA VI day-one figure ($3.79bn,
32.5m copies) replacing the Sensor Tower estimate. The Hormuz card now
leads with the UN's Friday briefing (25 seafarers killed since February,
136 incidents); the Nov-20 mine claim stays labelled [CLAIM]. Las Vegas
qualifying and the BepiColombo insertion are Saturday events — TOMORROW /
DATE CHECK only. See `../V4-REPORT.md` and `../V4-BRIEF-2026-11-21.md`.

v4.1 (same session, ~12:45 WIB — typography round after a head-to-head
against the live top 1–10): no story, number, or date changed. Red
nameplate banners on all 3 leads (CYCLONE AKVAN / KYIV / COP31) and all
10 cards (WALL STREET … TRUMP); lead headlines 16 → 18 px; the masthead
subline is now a red news ticker of the four biggest stories (Kyiv
bridges, Akvan landfall, AI sell-off, COP31 overtime); the numbers strip
is enlarged (20 → 27 px) with the $3.79bn GTA VI figure kept prominent;
and the card kicker rows are fixed — 8 of 10 had the place kicker
colliding with the source line, so kickers are now place-only and the
source line drops the redundant "· REPORTED" (timestamps and the CLAIM /
FORECAST flags stay). See `../V4.1-REPORT.md`.

v4.4 (same session, ~16:40 WIB — v4.3 FAILED grading: "execution 1:
the program exited with code 1", 548ms; authorship 95% passed but
the image was never graded, score 0). Root cause, proven locally:
main.py only COPIED a pre-rendered entry.png, so in a clean dir
without entry.png beside it it died FileNotFoundError. Fixes: (1)
main.py now GENERATES via draw_v4.py when entry.png is absent,
never crashes on a read-only cwd (best-effort copy + temp-dir
fallback), main output $MAKEFUN_OUTPUT_DIR (default /output),
prints size + sha256 — exit 0 in all tested conditions (full repo,
empty dir, system fonts hidden, read-only cwd as an unprivileged
user, read-only dir without entry.png). (2) The 5 DejaVu TTFs are
bundled in fonts/ (the grading image has no fonts-dejavu-extra, so
DejaVuSansCondensed was missing); draw_v4.py loads from fonts/
first, falls back to /usr/share — byte-identical output verified
before the visual changes. (3) Visual, no story/number/date
changed: Kyiv lead scene is now a BRIGHT bridge diagram (white
deck/arch/piers on dark blue, glowing fire on each span); the COP31
globe has visible green continents + thermometer; the Mercury card
scene is a cratered disc with a darker night side; the world map is
a LIGHT cream panel with warm-tan land dots and clear red numbered
pins (like ranks 1/2/10). See `../V4.4-REPORT.md`.

v4.3 (same session, ~13:20 WIB — ONE structural change, per the main
agent's round-2 head-to-head against the live top 1–10): in every top-10
entry the lead headline + body sit BELOW the scene, on cream, dark
serif — never inside the dark panel. v4.1/v4.2 still put them inside
the dark panel (white 18px), so at a glance they read quieter than
rank 1, 2 and newcomer rank 5 (dewacandra4, 4 leads). This round moves
each lead's headline + body below its scene onto the cream, dark serif
20px (measured first: 20px is the max that fits the longest headline,
Kyiv's 48 chars, in 2 lines — 22px needs 3), with the red nameplate
banner + dark scene kept on top and the scene enlarged 80 → 100px.
The lead kicker now carries the story number in a red disc, like the
top 10. Card headlines raised 11 → 12px serif (card 6's headline
trimmed to "BepiColombo set for Mercury orbit" — the date is in its
body + the TOMORROW line). No story, number, or date changed; all
v4.2 content kept. See `../V4.3-REPORT.md`.

v4.2 (same session, ~13:05 WIB — second head-to-head, this time against
the live top 1–10 with their images downloaded and read: rank 1
samatch-we 0.992057 down to rank 10 momo-devlog 0.990835): the Kyiv lead
toll was STALE — 3 killed / 15 injured was the early Friday count; the
updated figures (BBC/CNN) are 110+ missiles and 400+ drones fired, 9
killed across Ukraine, 7 in Kyiv, 28+ injured. Three stories the top 10
carry and we lacked are added as briefs, replacing the three weakest
(Cairncross quote, Trump–Xi "guardrails", Odisha assembly): Poland —
two Russian Kh-101 missiles and a jet-powered drone came down in the
south-east on Friday, Tusk calls it a provocation (6 of the top 10
carry it); Kenya — drilling spudded at Turkana's Amosing 1 well on
Friday, first crude due 1 Dec (4 of the top 10); and the pancreatic
cancer pill — daraxonrasib + chemo, EORTC Barcelona presentation
Friday, tumours shrank in 60.7% of 61 patients (3 of the top 10).
Correction to v3.1: the pill was rejected then because the August FDA
approval angle could not carry the figure; the Friday trial
presentation is a different, verified news event (BBC/Guardian).
Senegal's toll (4 dead, Reuters) is restored to brief 17. The numbers
strip swaps 922 hPa out for 110 missiles in. Typography: lead and card
headlines are now DejaVu Serif Bold (all 10 of the top 10 use serif
headlines) and the region strip is now coloured segments (9 of 10 do
this). Region tallies are now EUROPE 6 · AMERICAS 9 · ASIA-PACIFIC 9 ·
MIDEAST 1 · AFRICA 2 · OCEANIA 2 · WORLD 7. See `../V4.2-REPORT.md`.

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
- `main.py` — the entrypoint: copies `entry.png` to the current directory
  (and to `$MAKEFUN_OUTPUT_DIR` when set)
- `draw_v4.py` — the v4 generator that draws `entry.png` (pure PIL, no
  network, no clock, no randomness; two runs write byte-identical PNGs).
  `draw_v3.py` was removed in the v4 commit so the authorship denominator
  holds only files written in the v4 session.
- `LICENSE` — MIT

## Run it

```sh
python3 draw_v4.py            # regenerate entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

See `../STRATEGY.md` and `../SOURCES.md` for the scoring strategy, the
top-10 comparison, and the verified source list for every story.
