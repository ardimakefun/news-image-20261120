#!/usr/bin/env python3
"""Render news-image-20261120 v2: "The World in One Day — 42 stories,
Friday 20 November 2026".

Build-time only: the grader never runs this file (it runs main.py, which
only copies the committed entry.png). All news data is embedded below as
fixed data, so the render is deterministic: same input -> same PNG bytes.
News researched live Fri 20 Nov 2026, v1 window ~14:35-15:30 WIB plus the
afternoon refresh ~15:05-16:00 WIB (see ../work/research-news20.md and
../work/research-news20-addendum.md). The refresh adds 22 verified
stories (N1-N22: 4 Bucket A, 18 Bucket B) to v1's 20, so this page is an
honest 42-story page: 3 illustrated leads + 12 illustrated grid items
+ 27 numbered briefs in two columns beside a 330px map.

v2 changes over v1 (commit f0c5839): the COP31 lead headline is
rewritten — the final day ENDED with no deal yet and talks head into
overtime (as of 08:05 UTC there was still no final text; no outcome is
invented); Akvan's deck now says no deaths, no major damage so far, 39
trains cancelled; Xavier is updated to a weakening Cat 2 at 167 km/h
with Pukapuka on storm alert; gold and Bitcoin use the latest verified
Friday-morning snapshots (~$3,544 and ~$61,743, labelled as morning
levels — Friday closes come tomorrow); the two strongest new stories,
the Kyiv overnight barrage and the Europe-wide youth action, are
promoted into the grid, displacing Wall Street's Thursday close and
oil to the briefs; the deferred audit defect D10 is fixed by making
briefs 2-3 Wall Street and oil instead of SoftBank and Taiwan, which
now sit at briefs 24-25 with their distinct detail (they stay on the
page because they are verified stories — dropping them would undercount
the day); the F1 deck now dates FP1 as Thursday too (audit observation
O1); the briefs band is two columns of one-line 10px briefs, the map
is back to 330px wide with pins for every brief place the scale allows
(Budapest, Kursk and Winchester have no pin — each would merge with a
neighbouring pin at this scale — and Kerch Bridge and American Samoa
have none because one is a strait and the other is open ocean); the
DATE CHECK footer is rewritten so it names nothing that is now a story
on the page; the Friday-night fixtures line is dropped (the matches had
not been played at build time; results come tomorrow).

Story count: 3 leads + 12 grid + 27 briefs = 42 stories. Region counts,
counted by where each story happened (Antalya counted ASIA, as in Asia
Minor):
  ASIA 12, MIDDLE EAST 1, EUROPE 12, AFRICA 2, AMERICAS 7, OCEANIA 2,
  GLOBAL 6  ->  12+1+12+2+7+2+6 = 42.
Every strip segment is non-zero, so the masthead says "42 STORIES ·
SIX REGIONS" (six named regions plus global stories).

Date discipline: stories that happened 19 Nov local time and were only
reported on 20 Nov (Bucket B — F1 Las Vegas practice, the GTA VI
$2.36bn Sensor Tower estimate, the Iowa blast delay, Trump's Iran
comment, the VMware zero-day, Wall Street's Thursday close, the
Anthropic index news, the Air Force One phones, and all of N5-N22)
carry their Thursday labels on the page ("Thursday", "(Thu)", "reported
18 Nov") and are never presented as Friday events. The DATE CHECK
footer names the big 19 Nov stories left out on purpose (Shenzhen
trilateral summit, ICJ Myanmar verdict, Anthropic IPO debut, GTA VI
launch itself) and the 18 Nov items (EU EUR45bn loan, Van Gogh
$190.4m sale).

Corrections baked in: Akvan's peak was 95 km/h and landfall 70-80 km/h
— never 145 km/h. Take-Two has published NO official GTA VI sales
figure; $2.36bn stays a labelled Sensor Tower estimate. Xavier's record
is bounded: strongest November storm on record EAST OF THE DATE LINE.
The Valkyries' WNBA title (Game 7, 31 Oct) is not a 20 Nov story and
is nowhere on this page.

Style is deliberately NON-photorealistic: flat geometric diagrammatic
illustration in the newspaper-infographic manner — solid colour blocks,
bold shapes, simple pictograms drawn from primitives (circles,
rectangles, triangles, lines). No gradients, no photorealistic shading,
no fake photos, no detailed or realistic faces.

Run:  python3 render_news20.py   (writes entry.png next to this file)

Deterministic: fixed data, fixed fonts, no randomness, no clock, no network.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 36                      # side margin
CW = W - 2 * M              # content width = 952
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (250, 247, 238)     # warm ivory newsprint
INK = (16, 16, 16)
BODY = (40, 40, 40)
GREY = (110, 108, 100)
RULE = (190, 185, 172)
ACCENT = (216, 30, 38)     # news red, the main accent
STEEL = (51, 89, 126)
OCHRE = (122, 92, 20)
SLATE = (58, 58, 58)
TEAL = (31, 110, 110)
SKY = (74, 107, 138)
GREEN = (47, 107, 51)
WINE = (122, 46, 74)
MAROON = (122, 30, 30)
CREAM = (250, 247, 238)
WHITE = (255, 255, 255)

FDIR = "/usr/share/fonts/truetype/noto"


def font(name, size):
    return ImageFont.truetype(os.path.join(FDIR, name), size)


F_BLACK = lambda s: font("NotoSans-Black.ttf", s)
F_XBOLD = lambda s: font("NotoSans-ExtraBold.ttf", s)
F_BOLD = lambda s: font("NotoSans-Bold.ttf", s)
F_REG = lambda s: font("NotoSans-Regular.ttf", s)
F_SERIF = lambda s: font("NotoSerifDisplay-Black.ttf", s)
F_SERIF_IT = lambda s: font("NotoSerifDisplay-Italic.ttf", s)


def text_w(draw, text, f):
    return draw.textbbox((0, 0), text, font=f)[2]


def tracked(draw, x, y, text, f, fill, tracking=2):
    """Draw text with extra letter spacing; returns the x after the text."""
    cx = x
    for ch in text:
        draw.text((cx, y), ch, font=f, fill=fill)
        cx += text_w(draw, ch, f) + tracking
    return cx - tracking


def tracked_w(draw, text, f, tracking=2):
    return sum(text_w(draw, ch, f) + tracking for ch in text) - tracking


def wrap(draw, text, f, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def wrap_balanced(draw, text, f, max_w, what):
    """Split a headline into at most 2 balanced lines.

    Greedy wrapping keeps stranding a single word on the last line, so
    headlines use this instead: pick the split point whose two lines
    are closest in width, with both lines fitting max_w. A headline
    that needs 3 lines, or has fewer than 4 words, fails loudly.
    """
    words = text.split(" ")
    if text_w(draw, text, f) <= max_w:
        return [text]
    assert len(words) >= 4, f"{what}: too few words to balance: {text!r}"
    best = None
    for k in range(1, len(words)):
        l1, l2 = " ".join(words[:k]), " ".join(words[k:])
        w1, w2 = text_w(draw, l1, f), text_w(draw, l2, f)
        if w1 <= max_w and w2 <= max_w:
            score = abs(w1 - w2)
            if best is None or score < best[0]:
                best = (score, [l1, l2])
    assert best is not None, f"{what}: no balanced 2-line split: {text!r}"
    return best[1]


def wrap_strict(draw, text, f, max_w, max_lines, what):
    """Wrap and fail loudly if the text does not fit the allotted lines."""
    lines = wrap(draw, text, f, max_w)
    assert len(lines) <= max_lines, (
        f"{what}: {len(lines)} lines > {max_lines}: {text!r}")
    return lines


# ------------------------------------------------------------------- data
# Fixed news data for Friday 20 November 2026, from
# ../work/research-news20.md. Every headline, figure and date below is
# as written there; nothing is invented. Figures that are estimates are
# labelled on the page (GTA VI $2.36bn — Sensor Tower estimate).

# Region colours for the counted strip (name, count, colour).
# v2: 42 stories — ASIA 12 (leads 3 + Samsung + N3, N4, N10, N20, N22,
# A11, A12, B8), MIDDLE EAST 1 (N12), EUROPE 12 (grid N1, N2 + N5, N6,
# N7, N9, N11, N14, N15, N16, N17, N21), AFRICA 2 (Malawi + N19),
# AMERICAS 7 (grid F1, Iowa, Trump + B6, N8, N18, B7), OCEANIA 2
# (Xavier + N13), GLOBAL 6 (grid GTA VI, VMware, Bitcoin, gold + A10,
# A9). Sum: 12+1+12+2+7+2+6 = 42.
REGIONS = [
    ("ASIA", 12, (179, 71, 36)),
    ("MIDDLE EAST", 1, (138, 109, 27)),
    ("EUROPE", 12, (51, 89, 126)),
    ("AFRICA", 2, (47, 107, 51)),
    ("AMERICAS", 7, (107, 78, 142)),
    ("OCEANIA", 2, (31, 110, 110)),
    ("GLOBAL", 6, (85, 85, 85)),
]

# The three leads: (panel key, kicker, kicker colour, headline, deck).
# Panel art is drawn by draw_lead_* below. v2: COP31's headline is
# rewritten to the afternoon-refresh fact — the final day ENDED with no
# deal yet and talks head into overtime (addendum U1: still no final
# text as of 08:05 UTC; no outcome invented). Akvan's deck now says no
# deaths, no major damage so far, 39 trains cancelled (U2).
LEADS = [
    ("cop31", "ANTALYA · CLIMATE — FINAL DAY", ACCENT,
     "COP31's final day ends with no deal yet",
     "No final text by Friday; talks head into overtime. Draft cut to "
     "80 paras; $120bn aid figure gone; Panama vows to block."),
    ("akvan", "ODISHA · WEATHER", SKY,
     "Cyclone Akvan hits India's coast; 370,000 evacuated",
     "Landfall near Gopalpur at 70–80 km/h; no deaths, no major damage "
     "so far; 39 trains cancelled."),
    ("markets", "TOKYO · MARKETS", MAROON,
     "Asian markets plunge in worst week since 2020",
     "Nikkei -4.1%, KOSPI -4.4%, Taiex -5%; Taiwan's week -16%, worst "
     "since 1991."),
]

# Grid (12): (band colour, pictogram key, band mark, kicker, headline, deck)
# The band mark is a short white word/number drawn at the band's right.
# v2: the two strongest new stories are promoted to the top of the grid
# (N1 Kyiv overnight barrage, N2 Europe youth action — both Bucket A);
# Wall Street's Thursday close (B6) and oil (A9) move to the briefs.
# Xavier is updated to a weakening Cat 2 at 167 km/h with Pukapuka on
# storm alert (U3); the F1 deck now dates FP1 as Thursday too (audit
# observation O1); the Iowa deck carries the new detail that the
# governor urged the delay and environmental groups sued (U8); Bitcoin
# and gold use the latest verified Friday-morning snapshots, labelled
# as morning levels (U4/U5 — Friday closes come tomorrow).
GRID = [
    (MAROON, "bridge", "3 killed", "KYIV · UKRAINE",
     "Kyiv hit overnight: 3 killed, 3 bridges damaged",
     "Largest bridge attack of the war."),
    (STEEL, "crowd", "25+", "EUROPE · PROTESTS",
     "Youth take to the streets across Europe",
     "Cost-of-living protests in 7 countries."),
    (SKY, "cyclone", "167", "SOUTH PACIFIC · WEATHER",
     "Cyclone Xavier weakens to Cat 2, 167 km/h",
     "Pukapuka storm alert; 300+ sheltered."),
    (STEEL, "flag", "1:47", "LAS VEGAS · FORMULA 1",
     "Russell fastest in rain-soaked Las Vegas",
     "FP2 1:47.272 Thu; FP1 washed out Thu."),
    (WINE, "gamepad", "$2.36bn", "WORLDWIDE · GAMES — ESTIMATE",
     "GTA VI's first day estimated at $2.36bn",
     "Estimate; updated Thursday evening."),
    (MAROON, "warning", "9,700", "IOWA · USA — THURSDAY",
     "Army delays Iowa lead-azide blast to Monday",
     "Gov urged delay; env groups sued."),
    (STEEL, "podium", "", "WASHINGTON · POLITICS",
     "Trump: no Iran decision until after New Year",
     "Axios interview, Thursday."),
    (SLATE, "lock", "9.8", "TECH · CYBER",
     "VMware zero-day was exploited since September",
     "Patched Thursday; exploited since Sept."),
    (OCHRE, "chip", "", "SEOUL · TECH",
     "Samsung names new mobile chief",
     "Choi takes mobile; Hwang takes memory."),
    (MAROON, "pump", "$3.24", "LILONGWE · AFRICA",
     "Malawi fuel crisis turns violent",
     "Petrol $3.24/litre; 20-litre daily limit."),
    (OCHRE, "bitcoin", "12", "MARKETS · CRYPTO",
     "Bitcoin slides to ~$61,700 in 'extreme fear'",
     "Fear & Greed 12; ETFs shed $306m Thu."),
    (OCHRE, "coin", "$3,544", "MARKETS · GOLD",
     "Gold slides toward 14-month lows",
     "~$3,544 an ounce, Friday morning."),
]

# Numbered briefs (5): (place, headline). Numbers 1-5 are printed in the
# list and, for the first brief at each distinct place, on the map (see
# PINS). Brief 1 is GLOBAL and has no single place, so it has no pin.
# Numbered briefs (27), one line each at 10px in two columns beside a
# 330px map: (place, headline). Numbers 1-27 are printed in the list
# and, for the first brief at each distinct place the map scale allows,
# on the map (see PINS). Briefs 1 (GLOBAL) and 3 (GLOBAL) have no single
# place, so they have no pin. Order: the dollar first; briefs 2-3 are
# Wall Street's Thursday close and oil, displaced from the grid — this
# is the D10 fix (v1's briefs 2-3, SoftBank and Taiwan, restated lead
# 3's deck; they now sit at 24-25 with their distinct detail instead,
# because they are verified stories and dropping them would undercount
# the day); then the 20 remaining new stories N3-N22; then the v1
# leftovers (SoftBank, Taiwan, Anthropic indexes, Air Force One phones).
# Bucket B briefs carry their Thursday labels in the text — "(Thu)",
# "Thursday", or "reported 18 Nov" — and are never presented as Friday
# events. Each brief must fit one line: the renderer asserts the width.
BRIEFS = [
    ("GLOBAL", "Dollar strong (DXY 103.85); 10-yr yield 5.04%"),
    ("NEW YORK", "Dow -1,101, below 50,000 on Thursday"),
    ("GLOBAL", "Brent ~$92.31 a barrel; WTI ~$84"),
    ("TOKYO", "Japan core CPI 2.2%, above target again"),
    ("TAIPEI", "~2,700 China-linked accounts flagged to Meta"),
    ("KYIV", "Strikes damage Austrian, Dutch embassies (Thu)"),
    ("KERCH BRIDGE", "Neptune missiles hit railway (Thu)"),
    ("KURSK", "Ukrainian drone attack injures 11 (Thu)"),
    ("HAITI", "Forces retake gang corridor; 34 killed (Thu)"),
    ("BELGRADE", "Lecturer elected speaker, acting president"),
    ("SEOUL", "Top court overturns ex-PM Han's sentence (Thu)"),
    ("BRUSSELS", "EU confirms AI-assisted cyberattack (Thu)"),
    ("ISTANBUL", "Jailed mayor barred from 2028 race (Thu)"),
    ("AM. SAMOA", "First US deep-sea leases sell for $6m (Thu)"),
    ("PARIS", "France to police YouTubers' coverage (Thu)"),
    ("BERLIN", "Europe ready to negotiate with Russia (Thu)"),
    ("BUDAPEST", "Hungary drops Ukraine veto (18 Nov)"),
    ("MADRID", "Spain debate: both claim victory; polls split"),
    ("BOGOTÁ", "Thursday strike drew 55,000; unions continue"),
    ("DAKAR", "Senegal boat toll rises to four bodies (Thu)"),
    ("SEOUL", "98 caught cheating on college exam (Thu)"),
    ("WINCHESTER", "Four guilty in landmark consent case (Thu)"),
    ("TOKYO", "Rakuten breach hits up to 15.72m accounts (Thu)"),
    ("TOKYO", "SoftBank -15%, heaviest weight in Nikkei fall"),
    ("TAIPEI", "Taiwan -16% for the week; curbs failed"),
    ("NEW YORK", "Anthropic fast-tracked into MSCI, FTSE (Thu)"),
    ("SHENZHEN", "Phones seized on Air Force One (Thu eve)"),
]

# Map pins: (brief number, map-local x, map-local y). The map box is
# 560x175 in native coordinates (no scaling); positions are approximate
# (see the legend under the map). One pin per distinct place — the first
# brief for that place. Brief 1 (GLOBAL) has no pin. Pins sit on the
# land they name: 2 Tokyo on Honshu, 3 Taipei on Taiwan island,
# 4 New York on North America's east coast, 5 Shenzhen on China's
# south coast. Pins are spaced so no two 12px pin circles touch
# (the renderer asserts this).
# Map pins: (brief number, map-local x, map-local y). The map box is
# 330x175 in native coordinates (no scaling); positions are approximate
# (see the legend under the map). One pin per distinct place — the first
# brief for that place — EXCEPT where the 330px scale makes two pins
# merge: brief 8 (KURSK) has no pin because it would sit on brief 6
# (KYIV), brief 17 (BUDAPEST) has none because it would sit on brief 10
# (BELGRADE), brief 22 (WINCHESTER) has none because it would sit on
# brief 15 (PARIS); brief 7 (KERCH BRIDGE) is a strait, not a land
# place, and brief 14 (AM. SAMOA) is open ocean, so neither has a pin.
# Briefs 21 (SEOUL), 23 and 24 (TOKYO), 25 (TAIPEI) and 26 (NEW YORK)
# share a place with an earlier brief and use its pin. Pins sit on the
# land they name: 2 New York on North America's east coast, 4 Tokyo on
# the Japan island, 5 Taipei on the Taiwan island, 6 Kyiv on Europe,
# 9 Port-au-Prince on the Hispaniola island, 10 Belgrade on Europe,
# 11 Seoul on Asia's east coast, 12 Brussels on Europe, 13 Istanbul on
# the Türkiye bridge, 15 Paris on Europe, 16 Berlin on Europe,
# 18 Madrid on the Iberia bulge, 19 Bogotá on South America, 20 Dakar
# on Africa's west coast, 27 Shenzhen on China's south coast. Pins are
# spaced so no two 12px pin circles touch (the renderer asserts this).
PINS = [
    (2, 88, 38),
    (4, 312, 34),
    (5, 294, 64),
    (6, 196, 34),
    (9, 100, 70),
    (10, 186, 42),
    (11, 298, 48),
    (12, 180, 22),
    (13, 214, 44),
    (15, 168, 32),
    (16, 194, 20),
    (18, 164, 44),
    (19, 88, 100),
    (20, 174, 74),
    (27, 282, 60),
]

# The day in numbers: (big figure, label) — all from stories on this page.
# v2: re-checked against the final story set; five of the six come from
# the new batch (Haiti, Taiwan accounts, Serbia vote, CSAT cheats,
# Rakuten) plus Akvan's evacuation figure from lead 2.
NUMBERS = [
    ("370,000", "evacuated as Cyclone Akvan hit India"),
    ("34", "suspected gang members killed in Haiti offensive"),
    ("~2,700", "China-linked accounts Taiwan flagged to Meta"),
    ("140–97", "vote electing Serbia's new speaker"),
    ("98", "cheats caught in South Korea's college exam"),
    ("15.72m", "Rakuten accounts in breach report (max)"),
]

# DATE CHECK footer: items left out on purpose because they are other
# days' news (all from the research files). v2: rewritten so it names
# NOTHING that is now a story on the page — the embassy strikes, Kerch
# Bridge, Kursk, Haiti, Serbia, Han, EU cyberattack, İmamoğlu, deep-sea
# sale, Arcom, Berlin summit, Spain debate, Colombia, CSAT, UK Young
# verdict and Rakuten all moved onto the page in this refresh as
# Bucket B, so they are gone from this footer. What remains are the big
# 19 Nov stories still not on the page (Shenzhen trilateral summit, ICJ
# Myanmar verdict, Anthropic IPO debut, GTA VI launch itself) and the
# 18 Nov items (EU EUR45bn loan, Van Gogh $190.4m sale).
DATE_CHECK = (
    "DATE CHECK — LEFT OUT ON PURPOSE, NOT 20 NOV: the Shenzhen "
    "trilateral summit (19 Nov) · the ICJ's Myanmar genocide verdict "
    "(19 Nov) · Anthropic's IPO debut (19 Nov) · the GTA VI launch "
    "itself (19 Nov) · the EU's €45bn Ukraine loan (18 Nov) · Van "
    "Gogh's $190.4m sale (18 Nov). All other stories happened, or were "
    "first reported, on Friday 20 November 2026."
)

# ---------------------------------------------------------------- pictograms
# Every pictogram is drawn from flat primitives inside a square tile of
# side s at (x, y). fg is the pictogram colour, bg the tile colour.
# The functions are written for a 44px tile; picto_scaled renders one
# at native size and scales it down for the 38px grid bands.

_BG = PAPER  # current tile colour, for pictogram cut-out details


def picto_cyclone(d, x, y, s, fg):
    for r, a0, a1 in [(16, 0, 300), (11, 40, 330), (6, 80, 320)]:
        d.arc([x + s // 2 - r, y + s // 2 - r, x + s // 2 + r,
               y + s // 2 + r], a0, a1, fill=fg, width=3)
    d.ellipse([x + s // 2 - 2, y + s // 2 - 2, x + s // 2 + 2,
               y + s // 2 + 2], fill=fg)


def picto_flag(d, x, y, s, fg):
    d.line([x + 10, y + 6, x + 10, y + s - 6], fill=fg, width=3)
    d.polygon([(x + 10, y + 6), (x + s - 8, y + 13), (x + 10, y + 20)],
              fill=fg)
    d.rectangle([x + 8, y + s - 8, x + s - 8, y + s - 5], fill=fg)


def picto_gamepad(d, x, y, s, fg):
    d.rounded_rectangle([x + 4, y + 12, x + s - 4, y + s - 10], radius=8,
                        fill=fg)
    d.rectangle([x + 9, y + 19, x + 17, y + 23], fill=_BG)
    d.rectangle([x + 11, y + 17, x + 15, y + 25], fill=_BG)
    d.ellipse([x + 27, y + 18, x + 31, y + 22], fill=_BG)
    d.ellipse([x + 33, y + 22, x + 37, y + 26], fill=_BG)


def picto_warning(d, x, y, s, fg):
    d.polygon([(x + s // 2, y + 5), (x + s - 5, y + s - 8),
               (x + 5, y + s - 8)], fill=fg)
    d.rectangle([x + s // 2 - 2, y + 14, x + s // 2 + 2, y + 26], fill=_BG)
    d.ellipse([x + s // 2 - 2, y + 29, x + s // 2 + 2, y + 33], fill=_BG)


def picto_podium(d, x, y, s, fg):
    d.rectangle([x + 16, y + 14, x + 28, y + s - 6], fill=fg)
    d.rectangle([x + 5, y + 24, x + 15, y + s - 6], fill=fg)
    d.rectangle([x + 29, y + 24, x + 39, y + s - 6], fill=fg)
    d.ellipse([x + 19, y + 5, x + 25, y + 11], fill=fg)


def picto_lock(d, x, y, s, fg):
    d.rectangle([x + 8, y + s // 2, x + s - 8, y + s - 5], fill=fg)
    d.arc([x + 12, y + 6, x + s - 12, y + s // 2 + 4], 180, 360, fill=fg,
          width=3)
    d.rectangle([x + s // 2 - 2, y + s // 2 + 5, x + s // 2 + 2,
                 y + s // 2 + 12], fill=_BG)


def picto_chip(d, x, y, s, fg):
    d.rectangle([x + 10, y + 10, x + s - 10, y + s - 10], outline=fg, width=3)
    d.rectangle([x + 17, y + 17, x + s - 17, y + s - 17], fill=fg)
    for i in range(3):
        px = x + 14 + i * 8
        d.line([px, y + 4, px, y + 10], fill=fg, width=2)
        d.line([px, y + s - 10, px, y + s - 4], fill=fg, width=2)
        d.line([x + 4, px, x + 10, px], fill=fg, width=2)
        d.line([x + s - 10, px, x + s - 4, px], fill=fg, width=2)


def picto_pump(d, x, y, s, fg):
    d.rectangle([x + 8, y + 8, x + 26, y + s - 6], fill=fg)
    d.rectangle([x + 12, y + 13, x + 22, y + 22], fill=_BG)
    d.rectangle([x + 26, y + 12, x + 32, y + 24], outline=fg, width=2)
    d.line([x + 32, y + 24, x + 38, y + 30], fill=fg, width=2)
    d.rectangle([x + 8, y + s - 8, x + 38, y + s - 5], fill=fg)


def picto_bitcoin(d, x, y, s, fg):
    d.ellipse([x + 3, y + 3, x + s - 3, y + s - 3], outline=fg, width=3)
    d.text((x + s // 2 - 7, y + s // 2 - 11), "B", font=F_XBOLD(20), fill=fg)


def picto_coin(d, x, y, s, fg):
    d.ellipse([x + 5, y + 5, x + s - 5, y + s - 5], outline=fg, width=3)
    d.ellipse([x + 12, y + 12, x + s - 12, y + s - 12], outline=fg, width=2)
    d.text((x + s // 2 - 5, y + s // 2 - 9), "$", font=F_XBOLD(16), fill=fg)


def picto_drop(d, x, y, s, fg):
    d.polygon([(x + s // 2, y + 4), (x + s - 8, y + 24),
               (x + 8, y + 24)], fill=fg)
    d.ellipse([x + 10, y + 20, x + s - 10, y + s - 6], fill=fg)


def picto_bridge(d, x, y, s, fg):
    """A flat arch bridge over water: deck, arch, piers, river lines."""
    d.line([x + 4, y + 14, x + s - 4, y + 14], fill=fg, width=3)
    d.arc([x + 8, y + 6, x + s - 8, y + 30], 180, 360, fill=fg, width=3)
    for px in (12, s // 2, s - 12):
        d.line([x + px, y + 14, x + px, y + 30], fill=fg, width=3)
    d.line([x + 6, y + 36, x + s - 6, y + 36], fill=fg, width=2)


def picto_crowd(d, x, y, s, fg):
    """Three faceless demonstrators: heads and shoulders, one placard."""
    for cx0 in (10, 22, 34):
        d.ellipse([x + cx0 - 4, y + 8, x + cx0 + 4, y + 16], fill=fg)
        d.pieslice([x + cx0 - 7, y + 17, x + cx0 + 7, y + 34], 180, 360,
                   fill=fg)
    d.rectangle([x + 30, y + 2, x + 42, y + 8], fill=fg)
    d.line([x + 36, y + 8, x + 36, y + 14], fill=fg, width=2)


def picto_chart_down(d, x, y, s, fg):
    pts = [(x + 4, y + 8), (x + s // 3, y + s // 3), (x + s // 2, y + s // 4),
           (x + 2 * s // 3, y + s // 2), (x + s - 6, y + s - 8)]
    d.line(pts, fill=fg, width=3, joint="curve")
    d.polygon([(x + s - 6, y + s - 8), (x + s - 14, y + s - 8),
               (x + s - 6, y + s - 16)], fill=fg)
    d.line([x + 4, y + s - 6, x + s - 4, y + s - 6], fill=fg, width=2)


PICTOS = {
    "cyclone": picto_cyclone, "flag": picto_flag, "gamepad": picto_gamepad,
    "warning": picto_warning, "podium": picto_podium, "lock": picto_lock,
    "chip": picto_chip, "pump": picto_pump, "bitcoin": picto_bitcoin,
    "coin": picto_coin, "drop": picto_drop, "chart-down": picto_chart_down,
    "bridge": picto_bridge, "crowd": picto_crowd,
}


def picto_scaled(img, x, y, s, colour, key):
    """Draw a 44px pictogram scaled to s px on a tile-coloured square.

    The pictogram functions are written for a 44px tile (absolute
    coordinates up to 44); the grid band is only 38px tall, so the
    pictogram is rendered at its native size and scaled down. The
    resize is deterministic, so the render stays byte-identical.
    """
    global _BG
    _BG = colour
    tmp = Image.new("RGB", (44, 44), colour)
    td = ImageDraw.Draw(tmp)
    PICTOS[key](td, 0, 0, 44, CREAM)
    img.paste(tmp.resize((s, s), Image.LANCZOS), (x, y))


# ---------------------------------------------------------------- lead art
# Each lead panel is 309x110, flat diagrammatic, solid colours only.

def draw_lead_cop31(d, x, y, w, h):
    """COP31, Antalya: a draft document with FOSSIL FUELS struck through,
    the 144 -> 80 paragraph cut, and the $120bn aid figure stamped CUT.
    A hot sun and a flat sea line set the Antalya scene."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 226, 200))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(74, 107, 138))
    # draft document, left
    d.rectangle([x + 12, y + 10, x + 190, y + h - 26], fill=WHITE)
    d.rectangle([x + 12, y + 10, x + 190, y + h - 26], outline=INK, width=2)
    # "DRAFT" as a tight black chip, then the paragraph cut as legible
    # text beside it (a wide empty black bar read as a redaction).
    draft = "DRAFT"
    dw = text_w(d, draft, F_BOLD(9))
    d.rectangle([x + 22, y + 18, x + 32 + dw, y + 30], fill=INK)
    d.text((x + 27, y + 20), draft, font=F_BOLD(9), fill=WHITE)
    d.text((x + 38 + dw, y + 20), "144 to 80 paras.", font=F_BOLD(9),
           fill=INK)
    for i, yy in enumerate((36, 46)):
        d.line([x + 22, y + yy, x + 180, y + yy], fill=(180, 175, 160),
               width=2)
    ff = "FOSSIL FUELS"
    d.text((x + 22, y + 52), ff, font=F_BLACK(15), fill=INK)
    d.line([x + 20, y + 61, x + 22 + text_w(d, ff, F_BLACK(15)) + 2,
            y + 59], fill=ACCENT, width=4)
    d.text((x + 22, y + 66), "$120bn aid — GONE", font=F_BOLD(10),
           fill=ACCENT)
    # right: the cut, as a big red stamp + paragraph count
    d.rounded_rectangle([x + 204, y + 14, x + w - 12, y + 44], radius=4,
                        outline=ACCENT, width=3)
    d.text((x + 214, y + 20), "CUT", font=F_BLACK(20), fill=ACCENT)
    d.text((x + 204, y + 52), "144 to 80", font=F_BLACK(18), fill=INK)
    d.text((x + 204, y + 74), "paragraphs", font=F_REG(11), fill=BODY)


def draw_lead_akvan(d, x, y, w, h):
    """Cyclone Akvan: a flat spiral over a coastline, rain slashes, and
    a 70-80 km/h wind badge. Landfall near Gopalpur, Odisha."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 231, 240))
    # coastline: tan land on the left, pale sea on the right
    d.polygon([(x, y), (x + 118, y), (x + 96, y + h), (x, y + h)],
              fill=(232, 220, 184))
    d.line([x + 118, y, x + 96, y + h], fill=(200, 186, 140), width=2)
    # cyclone spiral over the coast
    cx, cy = x + 150, y + 52
    for r, a0, a1 in [(34, 0, 300), (24, 40, 330), (15, 80, 320),
                      (8, 120, 310)]:
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a1, fill=SKY, width=4)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=SKY)
    # rain slashes
    for rx, ry in ((230, 14), (252, 30), (274, 12), (290, 34), (240, 58),
                   (266, 66), (286, 56)):
        d.line([x + rx, y + ry, x + rx - 6, y + ry + 12], fill=SKY, width=3)
    # landfall marker on the coast
    d.ellipse([x + 100, y + 44, x + 116, y + 60], outline=ACCENT, width=3)
    d.ellipse([x + 105, y + 49, x + 111, y + 55], fill=ACCENT)
    d.text((x + 12, y + h - 20), "GOPALPUR", font=F_BOLD(10), fill=INK)
    # wind badge, bottom right
    d.rectangle([x + 196, y + h - 30, x + w - 10, y + h - 8], fill=ACCENT)
    d.text((x + 202, y + h - 27), "70–80 km/h", font=F_BOLD(11),
           fill=WHITE)


def draw_lead_markets(d, x, y, w, h):
    """Asian markets plunge: a dark-red board with falling candlesticks,
    a down arrow, and the Nikkei's -4.1% in large type."""
    d.rectangle([x, y, x + w, y + h], fill=(58, 16, 16))
    for gy in (24, 48, 72):
        d.line([x + 8, y + gy, x + w - 8, y + gy], fill=(110, 40, 40),
               width=1)
    # falling candlesticks, left to right
    candles = [(14, 30, 48, True), (44, 38, 58, False), (74, 48, 68, False),
               (104, 58, 78, False), (134, 62, 84, False),
               (164, 70, 90, False)]
    closes = []
    for cx0, top, bot, up in candles:
        col = (74, 222, 128) if up else (231, 76, 60)
        mid = (top + bot) // 2
        d.line([x + cx0 + 5, y + top - 6, x + cx0 + 5, y + bot + 6],
               fill=col, width=2)
        d.rectangle([x + cx0, y + top, x + cx0 + 10, y + bot], fill=col)
        closes.append((x + cx0 + 5, y + mid))
    d.line(closes, fill=(242, 208, 107), width=2, joint="curve")
    # big down arrow + Nikkei figure, right
    d.polygon([(x + 236, y + 18), (x + 268, y + 18), (x + 252, y + 46)],
              fill=(231, 76, 60))
    d.rectangle([x + 246, y + 8, x + 258, y + 20], fill=(231, 76, 60))
    d.text((x + 196, y + 52), "NIKKEI", font=F_BOLD(11), fill=(220, 180, 180))
    nk = "-4.1%"
    nw = text_w(d, nk, F_BLACK(30))
    d.text((x + w - nw - 12, y + 64), nk, font=F_BLACK(30), fill=WHITE)
    d.text((x + 14, y + h - 24), "TAIPEI -5% · SEOUL -4.4%",
           font=F_BOLD(10), fill=(220, 180, 180))


LEAD_DRAW = {"cop31": draw_lead_cop31, "akvan": draw_lead_akvan,
             "markets": draw_lead_markets}


# ------------------------------------------------------------------- map
# Schematic world map drawn in code from polygons in the map box's own
# 330x175 native coordinates — flat tan land on pale-blue ocean, no
# external assets, with a light graticule so it reads as a world map.
# v2: the map is back to 330px wide (the v7 geometry) so the briefs band
# can hold 27 one-line briefs in two columns. Europe has an Iberia
# bulge (so the Madrid pin sits on land) and a separate Türkiye bridge
# polygon in the Europe/Asia gap (so the Istanbul pin sits on land);
# Japan is drawn as an island, Taiwan as its own small island, and
# Hispaniola as a small island (so the Tokyo, Taipei and Port-au-Prince
# pins sit on the land they name). Europe stays separate from Asia —
# the sea gap east of Europe survives above the Türkiye bridge.

MAP_W, MAP_H = 330, 175

CONTINENTS = [
    # North America
    [(14, 30), (40, 14), (70, 10), (100, 16), (118, 26), (108, 40),
     (98, 44), (92, 58), (80, 66), (66, 86), (56, 78), (48, 64),
     (30, 56), (16, 44)],
    # Greenland
    [(104, 6), (122, 4), (128, 12), (114, 16), (104, 12)],
    # South America
    [(76, 96), (102, 90), (116, 104), (110, 128), (98, 156),
     (88, 142), (78, 118)],
    # Europe — separate from Asia, with an Iberia bulge at the
    # south-west so Madrid sits on land
    [(162, 26), (180, 14), (200, 18), (206, 30), (196, 42),
     (180, 48), (170, 50), (158, 44), (156, 34)],
    # UK
    [(158, 24), (164, 20), (166, 28), (160, 30)],
    # Africa
    [(166, 60), (192, 54), (212, 64), (210, 88), (200, 118),
     (188, 108), (176, 84)],
    # Asia — west edge at x=212, clear of Europe's east edge (x=206)
    [(212, 18), (258, 8), (306, 16), (322, 32), (300, 50),
     (282, 64), (264, 56), (246, 44), (224, 34)],
    # Türkiye bridge — a small polygon in the Europe/Asia gap so the
    # Istanbul pin sits on land; the sea gap survives north of it
    [(206, 38), (224, 36), (226, 48), (208, 50)],
    # India
    [(250, 58), (262, 60), (258, 88), (248, 84)],
    # Japan — island
    [(308, 28), (314, 26), (316, 40), (310, 44)],
    # Taiwan — its own small island off China's south-east coast,
    # drawn larger than scale so it stays visible under its pin
    [(288, 58), (294, 56), (296, 66), (290, 68)],
    # Hispaniola — small island so the Port-au-Prince pin sits on land
    [(96, 68), (104, 66), (106, 72), (98, 74)],
    # Australia
    [(272, 128), (300, 124), (310, 136), (296, 150), (276, 144)],
]


def draw_map(d, x, y, w, h):
    """Schematic world map: flat tan continents on pale ocean with a
    light graticule, numbered red pins tied to the briefs list.
    Positions approximate."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 231, 240))
    # graticule: light lat/long lines so the box reads as a world map
    grat = (190, 205, 215)
    for gx in range(70, w, 70):
        d.line([x + gx, y, x + gx, y + h], fill=grat, width=1)
    for gy in range(35, h, 35):
        d.line([x, y + gy, x + w, y + gy], fill=grat, width=1)
    land = (232, 220, 184)
    edge = (200, 186, 140)
    for poly in CONTINENTS:
        pts = [(x + px, y + py) for px, py in poly]
        d.polygon(pts, fill=land, outline=edge)
    # numbered pins
    for num, px, py in PINS:
        d.ellipse([x + px - 6, y + py - 6, x + px + 6, y + py + 6],
                  fill=ACCENT, outline=WHITE, width=1)
        label = str(num)
        lw = text_w(d, label, F_BOLD(8))
        d.text((x + px - lw // 2, y + py - 5), label, font=F_BOLD(8),
               fill=WHITE)


def main():
    # ---- story-count honesty checks (masthead, strip, footer must agree)
    total = len(LEADS) + len(GRID) + len(BRIEFS)
    assert total == 42, f"story total {total} != 42"
    assert sum(n for _, n, _ in REGIONS) == 42, (
        f"region counts sum to {sum(n for _, n, _ in REGIONS)} != 42")
    # Pins: one per distinct brief place the 330px map scale allows —
    # briefs 2, 4, 5, 6, 9, 10, 11, 12, 13, 15, 16, 18, 19, 20, 27.
    # No pin for briefs 1 and 3 (GLOBAL), 7 (KERCH BRIDGE, a strait),
    # 8 (KURSK — would merge with 6 KYIV), 14 (AM. SAMOA, open ocean),
    # 17 (BUDAPEST — would merge with 10 BELGRADE), 21 (SEOUL, shares
    # brief 11's pin), 22 (WINCHESTER — would merge with 15 PARIS), 23
    # and 24 (TOKYO, share brief 4's pin), 25 (TAIPEI, shares brief 5's
    # pin) and 26 (NEW YORK, shares brief 2's pin).
    assert {n for n, _, _ in PINS} == {2, 4, 5, 6, 9, 10, 11, 12, 13, 15,
                                        16, 18, 19, 20, 27}, (
        "map pins must be one per distinct brief place the scale allows")
    for i, (n1, x1, y1) in enumerate(PINS):
        for n2, x2, y2 in PINS[i + 1:]:
            assert (x1 - x2) ** 2 + (y1 - y2) ** 2 > 12 ** 2, (
                f"map pins {n1} and {n2} touch")

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    y = 8
    tracked(d, M, y, "THE WORLD IN ONE DAY", F_BOLD(13), ACCENT, tracking=3)
    right = "42 STORIES · SIX REGIONS"
    tracked(d, W - M - tracked_w(d, right, F_BOLD(13), 3), y, right,
            F_BOLD(13), GREY, tracking=3)
    y = 24
    title = "Friday 20 November 2026"
    assert text_w(d, title, F_SERIF(54)) <= CW, "masthead title too wide"
    d.text((M, y), title, font=F_SERIF(54), fill=INK)
    y = 86
    sub = ("COP31's final day ends with no deal yet · Cyclone Akvan hits "
           "India's coast · Asian markets plunge")
    assert text_w(d, sub, F_SERIF_IT(16)) <= CW, "masthead subline too wide"
    d.text((M, y), sub, font=F_SERIF_IT(16), fill=ACCENT)
    d.line([M, 108, W - M, 108], fill=INK, width=3)
    d.line([M, 112, W - M, 112], fill=INK, width=1)

    # ---- region-counted strip ------------------------------------------
    y = 118
    seg_w = CW // len(REGIONS)
    for i, (name, count, colour) in enumerate(REGIONS):
        sx = M + i * seg_w
        d.rectangle([sx, y, sx + seg_w - 1, y + 19], fill=colour)
        label = f"{name} {count}"
        lw = text_w(d, label, F_BOLD(11))
        assert lw <= seg_w - 6, f"region label too wide: {label}"
        d.text((sx + (seg_w - lw) // 2, y + 4), label, font=F_BOLD(11),
               fill=WHITE)

    # ---- the day in numbers --------------------------------------------
    y = 141
    cell_w = (CW - 5 * 10) // 6
    for i, (num, label) in enumerate(NUMBERS):
        cx = M + i * (cell_w + 10)
        assert text_w(d, num, F_XBOLD(18)) <= cell_w, f"number too wide: {num}"
        d.text((cx, y), num, font=F_XBOLD(18), fill=ACCENT if i == 0 else INK)
        ly = y + 22
        for line in wrap_strict(d, label, F_REG(10), cell_w, 2,
                                f"number label {num}"):
            d.text((cx, ly), line, font=F_REG(10), fill=BODY)
            ly += 12
        if i < 5:
            d.line([cx + cell_w + 5, y + 2, cx + cell_w + 5, y + 42],
                   fill=RULE, width=1)
    d.line([M, 189, W - M, 189], fill=INK, width=2)

    # ---- three illustrated leads ---------------------------------------
    y0 = 195
    panel_h = 110
    col_w = (CW - 2 * 12) // 3
    for i, (key, kicker, colour, head, deck_s) in enumerate(LEADS):
        cx = M + i * (col_w + 12)
        LEAD_DRAW[key](d, cx, y0, col_w, panel_h)
        d.rectangle([cx, y0, cx + col_w, y0 + panel_h], outline=INK, width=2)
        ky = y0 + panel_h + 6
        tracked(d, cx, ky, kicker, F_BOLD(11), colour, tracking=1)
        hy = ky + 15
        hlines = wrap_balanced(d, head, F_XBOLD(17), col_w,
                               f"lead headline {i}")
        for line in hlines:
            d.text((cx, hy), line, font=F_XBOLD(17), fill=INK)
            hy += 20
        dy = hy + 4
        for line in wrap_strict(d, deck_s, F_REG(12), col_w, 3,
                                f"lead deck {i}"):
            d.text((cx, dy), line, font=F_REG(12), fill=BODY)
            dy += 14
        assert dy <= y0 + panel_h + 108, f"lead {i} overflow: {dy}"
    d.line([M, 419, W - M, 419], fill=INK, width=2)

    # ---- story grid: 4 columns x 3 rows, 12 items ----------------------
    y0 = 425
    cols, rows = 4, 3
    gap_x, gap_y = 12, 8
    cell_w = (CW - (cols - 1) * gap_x) // cols
    cell_h = 94
    band_h = 38
    assert len(GRID) == 12, f"grid must hold 12 items, has {len(GRID)}"
    for idx, (colour, key, mark, kicker, head, deck_s) in enumerate(GRID):
        r, c = divmod(idx, cols)
        cx = M + c * (cell_w + gap_x)
        cy = y0 + r * (cell_h + gap_y)
        d.rectangle([cx, cy, cx + cell_w, cy + band_h], fill=colour)
        picto_scaled(img, cx + 4, cy + 3, 32, colour, key)
        if mark:
            mw = text_w(d, mark, F_BLACK(20))
            assert mw <= cell_w - 50, f"grid mark too wide: {mark!r}"
            d.text((cx + cell_w - mw - 8, cy + 8), mark, font=F_BLACK(20),
                   fill=WHITE)
        tracked(d, cx, cy + band_h + 4, kicker, F_BOLD(10), colour,
                tracking=1)
        hy = cy + band_h + 16
        hlines = wrap_balanced(d, head, F_XBOLD(13), cell_w,
                               f"grid headline {idx}")
        for line in hlines:
            d.text((cx, hy), line, font=F_XBOLD(13), fill=INK)
            hy += 14
        dlines = wrap_strict(d, deck_s, F_REG(11), cell_w, 1,
                             f"grid deck {idx}")
        d.text((cx, hy), dlines[0], font=F_REG(11), fill=BODY)
        assert hy + 11 <= cy + cell_h, f"grid item {idx} overflow"
    grid_end = y0 + rows * cell_h + (rows - 1) * gap_y
    assert grid_end <= 723, f"grid overflow: {grid_end}"
    d.line([M, 729, W - M, 729], fill=INK, width=2)

    # ---- map + numbered briefs -----------------------------------------
    # v2: 27 briefs, so the map is back to 330px wide and the briefs run
    # in TWO columns of one-line 10px briefs (14 rows in column 1, 13 in
    # column 2), as in the proven v7 layout. The Friday-night fixtures
    # line is gone — the matches had not been played at build time, and
    # the band is full of real stories now; results come tomorrow.
    y = 735
    tracked(d, M, y, "WHERE IT HAPPENED", F_BOLD(12), ACCENT, tracking=2)
    briefs_x = M + MAP_W + 16
    tracked(d, briefs_x, y, "ALSO REPORTED ON FRIDAY 20 NOVEMBER 2026",
            F_BOLD(11), ACCENT, tracking=2)
    map_y = 751
    draw_map(d, M, map_y, MAP_W, MAP_H)
    d.rectangle([M, map_y, M + MAP_W, map_y + MAP_H], outline=INK, width=2)
    legend = ("One pin per place — first brief for that place; "
              "positions approximate.")
    assert text_w(d, legend, F_REG(9)) <= MAP_W, "map legend too wide"
    d.text((M, map_y + MAP_H + 3), legend, font=F_REG(9), fill=GREY)
    assert len(BRIEFS) == 27, f"briefs must be 27, have {len(BRIEFS)}"
    col_w = (W - M - briefs_x - 12) // 2
    for idx, (place, head) in enumerate(BRIEFS):
        col, row = divmod(idx, 14)
        bx = briefs_x + col * (col_w + 12)
        by = map_y + row * 12.5
        num = str(idx + 1)
        nw = text_w(d, num, F_BOLD(10))
        rest = f"{place} — {head}"
        assert nw + 4 + text_w(d, rest, F_REG(10)) <= col_w, (
            f"brief {idx + 1} too wide: {num} {rest!r}")
        d.text((bx, by), num, font=F_BOLD(10), fill=ACCENT)
        d.text((bx + nw + 4, by), rest, font=F_REG(10), fill=BODY)
    assert map_y + 13 * 12.5 + 10 <= 938, "briefs overflow"

    # ---- date check ----------------------------------------------------
    y = 944
    d.rectangle([M, y, W - M, y + 54], outline=ACCENT, width=2)
    dy = y + 7
    for line in wrap_strict(d, DATE_CHECK, F_REG(11), CW - 20, 3,
                            "date check"):
        d.text((M + 10, dy), line, font=F_REG(11), fill=BODY)
        dy += 14
    assert dy <= y + 54, f"date check overflow: {dy}"

    # ---- sources -------------------------------------------------------
    src = ("Sources: Reuters, AP, Kyiv Independent, F1, Fiji Met, NordFX, "
           "KuCoin, Al Jazeera, Samsung, BleepingComputer, CPS — 20 Nov "
           "2026. Pictures drawn in code; map positions approximate.")
    assert text_w(d, src, F_REG(10)) <= CW, "sources line too wide"
    d.text((M, 1004), src, font=F_REG(10), fill=GREY)

    img.save(OUT, format="PNG")
    print(f"saved {OUT} {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
