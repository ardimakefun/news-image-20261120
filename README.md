# The World in One Day — 20 stories, Friday 20 November 2026

[![make.fun](https://img.shields.io/badge/make.fun-bounty-blue)](https://make.fun/bounty/news-image-20261120)
[![competition](https://img.shields.io/badge/competition-news--image--20261120-red)](https://make.fun/bounty/news-image-20261120)
[![stories](https://img.shields.io/badge/stories-20-green)](https://make.fun/bounty/news-image-20261120)

A one-page newspaper front page summing up Friday 20 November 2026 in
a single 1024×1024 image: **20 stories** — 3 illustrated leads, 12
illustrated grid items, 5 numbered briefs tied to a world map with
numbered pins, a region-counted strip, a numbers strip, and a DATE
CHECK footer naming the big stories left out because they are other
days' news.

## Why only 20 stories

The page was built on Friday afternoon WIB, before the Western news day
had happened. Only 20 stories were verified by then (see
`../work/research-news20.md`); the rest of the day — the COP31 final
text, the US Friday market close, Friday-night sport, F1 qualifying —
lands in tomorrow morning's refresh, which adds ~24 more briefs into
the same bands. Nothing is padded with unverified or non-20-Nov items.

## The stories

**Leads**

1. **COP31 final day opens with no deal on fossil fuels** (Antalya) —
   draft cut to 80 paragraphs, the $120bn aid figure gone; Panama vows
   to block a text with no oil cap.
2. **Cyclone Akvan hits India's coast; 370,000 evacuated** (Gopalpur,
   Odisha) — landfall 07:30–08:30 IST at 70–80 km/h; no major damage
   so far; 9,341 shelters.
3. **Asian markets plunge in worst week since 2020** — Nikkei −4.1%,
   KOSPI −4.4%, Taiex −5%; Taiwan's week −16%, worst since 1991.

**Grid (12):** Cyclone Xavier (strongest November storm on record east
of the date line, Cat 4, 165 km/h) · Russell fastest in rain-soaked
Las Vegas F1 practice (FP2 1:47.272, Thursday; FP1 washed out) · GTA
VI's first day estimated at $2.36bn (Sensor Tower estimate, updated
Thursday evening — labelled as an estimate) · Army delays Iowa
lead-azide blast to Monday (Thursday-night delay; 9,700 lbs unstable)
· Trump: no Iran decision until after New Year (Axios interview,
Thursday) · VMware zero-day was exploited since September (patched
Thursday; CVE-2026-123890, CVSS 9.8) · Samsung names new mobile chief
· Malawi fuel crisis turns violent · Bitcoin holds near $62,000 in
"extreme fear" (Fear & Greed 12) · Gold slides toward 14-month lows
(~$3,553/oz) · Oil holds high with Hormuz risk high (Brent ~$92.31)
· Thursday's Wall Street sell-off in numbers (Dow −1,101, below
50,000 — the Thursday close Asia woke to, used only as context).

**Briefs (5):** Dollar strong (DXY 103.85); US 10-year yield 5.04% ·
SoftBank −15%, heaviest weight in the Nikkei's fall · Taiwan −16%
for the week; Thursday's short-selling curbs failed to stop the slide
· Anthropic fast-tracked into MSCI (1 Dec) and FTSE (21 Dec),
announced Thursday · Reporters' phones seized on Air Force One
leaving China, Thursday evening.

Below the briefs, a labelled fixtures line — "TONIGHT — FOOTBALL:
Bayern v Köln 19:30 UTC · Athletic v Espanyol 20:00 UTC · Troyes v
Le Havre 19:45 UTC · Al Ahli v Al Nassr 17:30 UTC" — lists
Friday-night football fixtures (not results). It is NOT a story: it
is not counted in the 20-story total, adds nothing to the region
strip, and has no map pin.

## Story-count arithmetic

| Section | Count |
|---|---|
| Leads | 3 |
| Grid | 12 |
| Briefs | 5 |
| **Total** | **20** |

Region strip — counted by where each story happened (Antalya counted
ASIA, as in Asia Minor):

| Region | Stories | Count |
|---|---|---|
| ASIA | COP31, Akvan, Asian markets, Samsung, SoftBank, Taiwan, Air Force One phones | 7 |
| MIDDLE EAST | — | 0 |
| EUROPE | — | 0 |
| AFRICA | Malawi fuel crisis | 1 |
| AMERICAS | F1 Las Vegas, Iowa blast, Trump/Iran, Wall Street close, Anthropic indexes | 5 |
| OCEANIA | Cyclone Xavier | 1 |
| GLOBAL | GTA VI estimate, VMware zero-day, Bitcoin, gold, oil, dollar/yield | 6 |
| **Total** | | **20** |

7 + 0 + 0 + 1 + 5 + 1 + 6 = **20** ✓ — masthead, region strip and
footer all agree. Map pins: one per distinct brief place — brief 2
(Tokyo), 3 (Taipei), 4 (New York), 5 (Shenzhen); brief 1 is GLOBAL and
has no pin. The renderer asserts the pin set and that no two pin
circles touch.

## Date discipline

Stories that happened on 19 Nov local time and were only reported on
20 Nov are worded so they never claim to have happened on 20 Nov
("Thursday evening", "announced Thursday", "reported overnight", and
the GTA VI figure is labelled a Sensor Tower estimate). The DATE CHECK
footer names what was left out on purpose: the Shenzhen trilateral
summit (19 Nov), the ICJ's Myanmar genocide verdict (19 Nov),
Anthropic's IPO debut (19 Nov), the GTA VI launch itself (19 Nov),
the EU's €45bn Ukraine loan (18 Nov), Van Gogh's $190.4m sale
(18 Nov).

Corrections baked in: Akvan's peak was 95 km/h, landfall 70–80 km/h —
never 145 km/h. The Valkyries' WNBA title (Game 7, 31 Oct) is not a
20 Nov story and is nowhere on this page.

## How to run

```sh
python3 render_news20.py   # writes entry.png (1024x1024, ≤1 MiB)
python3 -P -s main.py      # grader entrypoint: copies entry.png to
                           # $MAKEFUN_OUTPUT_DIR/entry.png
```

Deterministic: fixed data, fixed fonts, no clock, no network, no
randomness. Two runs are byte-identical. Standard library + Pillow
only; all pictures are drawn in code (flat diagrammatic style — solid
colours, geometric pictograms, no gradients, no photorealistic
shading, no detailed faces). Map positions are approximate.

## Sources

Reuters, Asia Today, Formula 1, Fiji Met (RSMC Nadi), NordFX, KuCoin,
AP, Al Jazeera, Samsung Newsroom, BleepingComputer, IMD — 20 Nov 2026.
Full source list per story: `../work/research-news20.md`.

## Fix round — audit round 1 (20 Nov, ~15:00 WIB)

Independent audit verdict was NO-GO (1 BLOCKER, 5 MAJOR, 4 LOW). All
ten defects were fixed in `render_news20.py` and re-rendered, except
D10 which is DEFERRED (see below):

- **D1 (BLOCKER):** COP31 headline and masthead subline no longer
  assert an outcome — "final day **opens** with no deal", not "ends
  with". The summit entered its final day with no agreement; the final
  text was due by midnight Antalya Friday.
- **D2:** masthead now reads "20 STORIES · FIVE REGIONS" (the strip
  has MIDDLE EAST 0 and EUROPE 0, so "EVERY CONTINENT" was false).
- **D3:** Xavier is now "strongest Nov storm east of the date line"
  (headline) / "Nov record east of dateline" (deck) — the qualifier
  from the research is on the page.
- **D4:** F1 deck now dates FP2: "FP2 1:47.272, Thursday; FP1 washed
  out." (The audit's exact wording, "FP2 1:47.272 (Thursday
  evening); FP1 washed out Thursday.", is 308px in the 229px grid
  cell and cannot fit on one line; the Thursday label on FP2 — the
  point of the defect — is kept in full.)
- **D5:** briefs band filled — brief type enlarged 11px → 12px and
  the labelled fixtures line added below the briefs (see above); the
  band now runs to just above the DATE CHECK box.
- **D6:** map redrawn in native 560×175 coordinates with a light
  graticule; Japan drawn as an island chain (Hokkaido, Honshu,
  Kyushu), Taiwan as its own island, Europe as a separate polygon
  with a sea gap east of it. Pins sit on the land they name: Tokyo
  on Honshu, Taipei on Taiwan, New York on North America's east
  coast, Shenzhen on China's south coast. Pin numbers still match
  brief numbers; the renderer still asserts no two pins touch.
- **D7:** briefs header is now "ALSO REPORTED ON FRIDAY 20 NOVEMBER
  2026" (briefs 4–5 happened Thursday; their own text says so).
- **D8:** the unexplained black bar after "DRAFT" in the COP31
  illustration is now a tight chip around the word DRAFT, with
  legible text beside it: "144 to 80 paras."
- **D9:** Bitcoin deck now dates the outflow: "ETFs shed $306m Thu."
  (The full "Thursday" spelling is 232px in the 229px cell; "Thu."
  is the same date.)
- **D10 — DEFERRED TO TOMORROW'S REFRESH:** briefs 2–3 (SoftBank
  −15%, Taiwan −16%) still restate figures in lead 3's deck, because
  there are NO other verified brief candidates tonight — all 20
  verified stories are already on the page, and inventing
  replacements is forbidden. The two briefs were reworded to add
  distinct detail from the research instead (SoftBank as the heaviest
  weight in the Nikkei's fall; Taiwan's short-selling curbs failing
  to stop the slide). At refresh, replace these two brief slots with
  genuinely new verified stories when the ~24 new briefs arrive.

## Handover — refresh tomorrow morning (Sat 21 Nov)

Re-check before rebuilding (see "STILL DEVELOPING / RE-CHECK
TOMORROW" in `../work/research-news20.md`): **1.** COP31 final text —
did it close Friday, run into overtime, or collapse? Any fossil-fuel
language back? $120bn restored? CCUS 500m-tonne target kept? Did
Panama block consensus? **2.** Akvan damage assessment — deaths,
injuries, houses/crops/power damage, final rainfall. **3.** Xavier
track — still Cat 4 or weakening? Any land impact on
Suwarrow/Nassau/Pukapuka? **4.** US Friday market close — Dow/S&P/
Nasdaq finals, VIX, Bitcoin and gold closes, Anthropic day-2 price.
**5.** Gold exact level (morning snapshots disagreed $3,553–$3,715).
**6.** F1 Las Vegas FP3 and qualifying. **7.** Friday-night sport
results (NBA 9 games; Bayern–Köln, Athletic–Espanyol, Troyes–Le
Havre, Al Ahli–Al Nassr; NHL). **8.** Trump White House news
conference (Friday). **9.** Spain debate reactions (Sánchez–Feijóo,
19 Nov 22:00). **10.** Colombia strike aftermath. **11.** Senegal
boat search toll. **12.** Iowa detonation — Monday 23 Nov plan holds?
**13.** GTA VI official numbers — has Take-Two published any yet?
**14.** Europe youth action 20 Nov — did it happen, at what scale?
**15.** Any late-breaking 20 Nov story — re-run a full news sweep.

Refresh plan: add ~24 verified stories as briefs (the briefs band goes
back to two columns) — replace briefs 2–3 first (SoftBank, Taiwan;
D10 was deferred because no replacement existed tonight), update the
masthead count and region strip to the new total, re-check the numbers
strip against the new stories, re-audit, and submit before entries
close Sun 22 Nov 07:00 WIB.
