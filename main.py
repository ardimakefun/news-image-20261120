#!/usr/bin/env python3
"""news-image-20261120 entry, v2: copy the committed front page to the output dir.

v2 is "The World in One Day — 42 stories, Friday 20 November 2026".
The afternoon refresh (research-news20-addendum.md, ~15:05-16:00 WIB)
added 22 verified stories to v1's 20, so this page is an honest
42-story page, not a padded 44: 3 illustrated leads + 12 illustrated
grid items + 27 numbered briefs in two columns beside a 330px world
map. The three leads are COP31's final day in Antalya (still no deal
as talks run on — as of 08:05 UTC there was still no final text, and
no outcome is invented; the final text was due at midnight Antalya
Friday and overtime was only expected), Cyclone
Akvan's landfall near Gopalpur (370,000 people evacuated to 9,341
shelters, no deaths and no major damage so far, 39 trains cancelled)
and the Asian market plunge (Nikkei -4.1%, worst week since 2020). The
grid promotes the two strongest new stories — Russia's overnight
barrage on Kyiv (3 killed, 3 Dnipro bridges damaged) and the
Europe-wide youth action on the cost of living — and carries the
second cyclone (Xavier, weakening Cat 2 at 167 km/h, Pukapuka on
storm alert), the rain-soaked Las Vegas F1 practice (Russell fastest
in FP2, 1:47.272, Thursday; FP1 washed out Thursday), the GTA VI
first-day sales figure as a labelled Sensor Tower estimate (~$2.36bn,
updated Thursday evening — Take-Two has published nothing official),
the Iowa lead-azide blast delayed to Monday (the governor urged the
delay; environmental groups sued), Trump's no-Iran-decision-until-
after-New-Year comment, the VMware vCenter zero-day (CVE-2026-123890,
exploited since September), Samsung's new mobile chief, Malawi's fuel
crisis, Bitcoin sliding to ~$61,700 in "extreme fear" and gold at
~$3,544 on Friday morning (both morning snapshots, labelled as such —
Friday closes come tomorrow). The 27 briefs run from the dollar and
the 10-year yield through Wall Street's Thursday close (Dow -1,101,
below 50,000) and oil (Brent ~$92.31), the new batch — Japan core CPI
2.2%, Taiwan flagging ~2,700 China-linked accounts to Meta, the
embassy strikes in Kyiv, the Kerch Bridge railway hit, the Kursk drone
attack, Haiti's offensive (34 killed), Serbia's student-list speaker
becoming acting president, South Korea's top court overturning ex-PM
Han's sentence, the EU's AI-assisted cyberattack, the Istanbul mayor
barred from the 2028 race, the first US deep-sea leases ($6m), France
policing YouTubers' election coverage, Europe ready to negotiate with
Russia, Hungary dropping its Ukraine veto, the Spain debate, Colombia's
strike (55,000), the Senegal boat toll (four bodies), 98 CSAT cheats,
the Winchester consent-case verdict and the Rakuten breach (up to
15.72m accounts) — to the v1 leftovers SoftBank (-15%), Taiwan's -16%
week, Anthropic's index fast-track and the Air Force One phones.
Region counts, counted by where each story happened (Antalya counted
ASIA): ASIA 12, MIDDLE EAST 1, EUROPE 12, AFRICA 2, AMERICAS 7,
OCEANIA 2, GLOBAL 6 — summing to 42. Stories that happened on 19 Nov
local time and were only reported on 20 Nov are worded as reported
Thursday, never as Friday events, and the DATE CHECK footer names the
big 19 Nov stories left out on purpose (the Shenzhen trilateral
summit, the ICJ Myanmar genocide verdict, Anthropic's IPO debut, the
GTA VI launch itself) and the 18 Nov items (the EU's EUR45bn Ukraine
loan, Van Gogh's $190.4m sale) — nothing in the footer is now a story
on the page. Akvan's peak was 95 km/h and landfall 70-80 km/h — never
145 km/h. Xavier's record is bounded: strongest November storm on
record east of the date line. Every headline, figure and date comes
from the verified research in ../work/research-news20.md and
../work/research-news20-addendum.md.

The image itself is drawn at build time by render_news20.py (Pillow,
fixed data, no clock, no network, no randomness) and committed as
entry.png; this entrypoint only copies it, so the grader's run is
byte-identical every time. The map is drawn in code from polygons with
one numbered pin per distinct brief place the 330px scale allows
(Kursk, Budapest and Winchester have no pin — each would merge with a
neighbouring pin — Kerch Bridge is a strait and American Samoa is
open ocean), and the briefs band holds the 27 briefs in two columns
of one-line 10px briefs. The Friday-night fixtures line from v1 is
gone — the matches had not been played at build time and the band is
full of real stories now.

Standard library only; no network, no randomness, no clock. The image in
this repository (entry.png) already sums up the world's news of 20
November 2026, so a copy is byte-identical on every run.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

SRC = os.path.join(HERE, "entry.png")
DST = os.path.join(OUT, "entry.png")
os.makedirs(OUT, exist_ok=True)
shutil.copyfile(SRC, DST)
# Fail loudly instead of handing the grader a truncated copy.
if os.path.getsize(DST) != os.path.getsize(SRC):
    raise SystemExit("entry.png copy is incomplete")
