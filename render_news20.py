#!/usr/bin/env python3
"""Render news-image-20261120 v1: "The World in One Day — 20 stories,
Friday 20 November 2026".

Build-time only: the grader never runs this file (it runs main.py, which
only copies the committed entry.png). All news data is embedded below as
fixed data, so the render is deterministic: same input -> same PNG bytes.
News researched live Fri 20 Nov 2026 ~14:35-15:30 WIB from public sources
(see ../work/research-news20.md). Only 20 stories were verified by then —
the Western news day had not happened yet — so this page is an honest
20-story page, not a padded 44. It is built to expand tomorrow morning:
the refresh adds ~24 more briefs into the same bands.

Story count: 3 illustrated leads + 12 illustrated grid items + 5
numbered briefs = 20 stories. Region counts, counted by where each
story happened (Antalya counted ASIA, as in Asia Minor):
  ASIA 7, MIDDLE EAST 0, EUROPE 0, AFRICA 1, AMERICAS 5, OCEANIA 1,
  GLOBAL 6  ->  7+0+0+1+5+1+6 = 20.
The three leads are COP31's final day in Antalya (no deal, fossil fuels
erased), Cyclone Akvan's landfall near Gopalpur (370,000 evacuated) and
the Asian market plunge (worst week since 2020).

Date discipline: stories that happened 19 Nov local time and were only
reported on 20 Nov (Bucket B in the research file — F1 Las Vegas
practice, the GTA VI $2.36bn Sensor Tower estimate, the Iowa blast
delay, Trump's Iran comment, the VMware zero-day, Wall Street's
Thursday close, the Anthropic index news, the Air Force One phones)
are worded so they never claim to have happened on 20 Nov
("Thursday evening", "announced Thursday", "reported overnight", and
the estimate is labelled as an estimate). The DATE CHECK footer names
the big 19 Nov stories left out on purpose (Shenzhen trilateral
summit, ICJ Myanmar verdict, Anthropic IPO debut, GTA VI launch
itself) and the 18 Nov items (EU EUR45bn loan, Van Gogh $190.4m sale).

Corrections baked in: Akvan's peak was 95 km/h and landfall 70-80 km/h
— never 145 km/h. The Valkyries' WNBA title (Game 7, 31 Oct) is not a
20 Nov story and is nowhere on this page.

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
REGIONS = [
    ("ASIA", 7, (179, 71, 36)),
    ("MIDDLE EAST", 0, (138, 109, 27)),
    ("EUROPE", 0, (51, 89, 126)),
    ("AFRICA", 1, (47, 107, 51)),
    ("AMERICAS", 5, (107, 78, 142)),
    ("OCEANIA", 1, (31, 110, 110)),
    ("GLOBAL", 6, (85, 85, 85)),
]

# The three leads: (panel key, kicker, kicker colour, headline, deck).
# Panel art is drawn by draw_lead_* below.
LEADS = [
    ("cop31", "ANTALYA · CLIMATE — FINAL DAY", ACCENT,
     "COP31 final day ends with no deal on fossil fuels",
     "Draft cut to 80 paragraphs, $120bn aid figure gone; Panama vows "
     "to block a text with no oil cap."),
    ("akvan", "ODISHA · WEATHER", SKY,
     "Cyclone Akvan hits India's coast; 370,000 evacuated",
     "Landfall near Gopalpur at 70–80 km/h; no major damage so far; "
     "9,341 shelters."),
    ("markets", "TOKYO · MARKETS", MAROON,
     "Asian markets plunge in worst week since 2020",
     "Nikkei -4.1%, KOSPI -4.4%, Taiex -5%; Taiwan's week -16%, worst "
     "since 1991."),
]

# Grid (12): (band colour, pictogram key, band mark, kicker, headline, deck)
# The band mark is a short white word/number drawn at the band's right.
GRID = [
    (SKY, "cyclone", "165", "SOUTH PACIFIC · WEATHER",
     "Cyclone Xavier: strongest November storm on record",
     "Cat 4, 165 km/h; record Nov storm."),
    (STEEL, "flag", "1:47", "LAS VEGAS · FORMULA 1",
     "Russell fastest in rain-soaked Las Vegas",
     "FP2 1:47.272; FP1 washed out Thursday."),
    (WINE, "gamepad", "$2.36bn", "WORLDWIDE · GAMES — ESTIMATE",
     "GTA VI's first day estimated at $2.36bn",
     "Estimate; updated Thursday evening."),
    (MAROON, "warning", "9,700", "IOWA · USA",
     "Army delays Iowa lead-azide blast to Monday",
     "Thursday-night delay; 9,700 lbs unstable."),
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
     "Bitcoin holds near $62,000 in 'extreme fear'",
     "Fear & Greed 12; ETFs shed $306m."),
    (OCHRE, "coin", "$3,553", "MARKETS · GOLD",
     "Gold slides toward 14-month lows",
     "~$3,553 an ounce as the dollar rallies."),
    (STEEL, "drop", "$92", "MARKETS · ENERGY",
     "Oil holds high with Hormuz risk high",
     "Brent ~$92.31 a barrel; WTI ~$84."),
    (OCHRE, "chart-down", "-1,101", "NEW YORK · MARKETS — THURSDAY",
     "Thursday's Wall Street sell-off in numbers",
     "Dow -1,101, below 50,000."),
]

# Numbered briefs (5): (place, headline). Numbers 1-5 are printed in the
# list and, for the first brief at each distinct place, on the map (see
# PINS). Brief 1 is GLOBAL and has no single place, so it has no pin.
BRIEFS = [
    ("GLOBAL", "Dollar strong (DXY 103.85); US 10-year yield 5.04%"),
    ("TOKYO", "SoftBank -15% leads Tokyo's tech rout"),
    ("TAIPEI", "Taiwan's worst week since 1991 (-16%)"),
    ("NEW YORK", "Anthropic fast-tracked into MSCI (1 Dec) and FTSE "
     "(21 Dec), announced Thursday"),
    ("SHENZHEN", "Reporters' phones seized on Air Force One leaving "
     "China, Thursday evening"),
]

# Map pins: (brief number, map-local x, map-local y). The map box is
# 560x175; positions are approximate (see the legend under the map).
# One pin per distinct place — the first brief for that place. Brief 1
# (GLOBAL) has no pin. Pins are spaced so no two 12px pin circles touch
# (the renderer asserts this).
PINS = [
    (2, 519, 44),
    (3, 502, 62),
    (4, 153, 40),
    (5, 462, 58),
]

# The day in numbers: (big figure, label) — all from stories on this page.
NUMBERS = [
    ("370,000", "evacuated as Cyclone Akvan hit India"),
    ("-4.1%", "Nikkei's Friday fall; worst week since 2020"),
    ("~$2.36bn", "GTA VI estimated first-day sales (Sensor Tower)"),
    ("9,341", "shelters housing Akvan evacuees"),
    ("12", "Crypto Fear & Greed — 'Extreme Fear'"),
    ("$92.31", "Brent crude a barrel, holding high"),
]

# DATE CHECK footer: items left out on purpose because they are other
# days' news (all from the research file).
DATE_CHECK = (
    "DATE CHECK — LEFT OUT ON PURPOSE, NOT 20 NOV: the Shenzhen "
    "trilateral summit (19 Nov) · the ICJ's Myanmar genocide verdict "
    "(19 Nov) · Anthropic's IPO debut (19 Nov) · the GTA VI launch "
    "itself (19 Nov; the $2.36bn figure on this page is a Sensor Tower "
    "estimate) · the EU's €45bn Ukraine loan (18 Nov) · Van Gogh's "
    "$190.4m sale (18 Nov). All other stories happened, or were first "
    "reported, on Friday 20 November 2026."
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
    d.rectangle([x + 22, y + 18, x + 110, y + 30], fill=INK)
    d.text((x + 27, y + 20), "DRAFT", font=F_BOLD(9), fill=WHITE)
    d.text((x + 118, y + 20), "80 paras.", font=F_BOLD(9), fill=INK)
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
# Schematic world map drawn in code from polygons — flat tan land on
# pale-blue ocean, no external assets. Base polygons are written in a
# 330-wide coordinate space (the proven v7 map) and scaled horizontally
# to the wider 560px box; the vertical space is unchanged at 175px.

MAP_W, MAP_H = 560, 175
MAP_SX = MAP_W / 330.0

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
    # Europe
    [(162, 26), (180, 14), (200, 18), (206, 30), (196, 42),
     (180, 48), (168, 40)],
    # UK
    [(158, 24), (164, 20), (166, 28), (160, 30)],
    # Africa
    [(166, 60), (192, 54), (212, 64), (210, 88), (200, 118),
     (188, 108), (176, 84)],
    # Asia
    [(212, 18), (258, 8), (306, 16), (322, 32), (300, 50),
     (282, 64), (264, 56), (246, 44), (224, 34)],
    # India
    [(250, 58), (262, 60), (258, 88), (248, 84)],
    # Japan
    [(308, 28), (314, 26), (316, 40), (310, 44)],
    # Australia
    [(272, 128), (300, 124), (310, 136), (296, 150), (276, 144)],
]


def draw_map(d, x, y, w, h):
    """Schematic world map: flat tan continents on pale ocean, numbered
    red pins tied to the briefs list. Positions approximate."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 231, 240))
    land = (232, 220, 184)
    edge = (200, 186, 140)
    for poly in CONTINENTS:
        pts = [(x + px * MAP_SX, y + py) for px, py in poly]
        d.polygon(pts, fill=land, outline=edge)
    # SE Asia islands: three small dots
    for ix, iy in ((282, 78), (292, 84), (276, 88)):
        d.ellipse([x + ix * MAP_SX - 5, y + iy - 3, x + ix * MAP_SX + 5,
                   y + iy + 3], fill=land, outline=edge)
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
    assert total == 20, f"story total {total} != 20"
    assert sum(n for _, n, _ in REGIONS) == 20, (
        f"region counts sum to {sum(n for _, n, _ in REGIONS)} != 20")
    # Pins: one per distinct brief place — briefs 2 (TOKYO), 3 (TAIPEI),
    # 4 (NEW YORK), 5 (SHENZHEN). Brief 1 (GLOBAL) has no pin.
    assert {n for n, _, _ in PINS} == {2, 3, 4, 5}, (
        "map pins must be one per distinct brief place")
    for i, (n1, x1, y1) in enumerate(PINS):
        for n2, x2, y2 in PINS[i + 1:]:
            assert (x1 - x2) ** 2 + (y1 - y2) ** 2 > 12 ** 2, (
                f"map pins {n1} and {n2} touch")

    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    y = 8
    tracked(d, M, y, "THE WORLD IN ONE DAY", F_BOLD(13), ACCENT, tracking=3)
    right = "20 STORIES · EVERY CONTINENT"
    tracked(d, W - M - tracked_w(d, right, F_BOLD(13), 3), y, right,
            F_BOLD(13), GREY, tracking=3)
    y = 24
    title = "Friday 20 November 2026"
    assert text_w(d, title, F_SERIF(54)) <= CW, "masthead title too wide"
    d.text((M, y), title, font=F_SERIF(54), fill=INK)
    y = 86
    sub = ("COP31's final day ends without a deal · Cyclone Akvan hits "
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
    # Only 5 briefs tonight, so the map gets the room: a 560px-wide map
    # at left, the 5 briefs in ONE column at right (up to 2 lines each,
    # 34px per brief). Tomorrow's refresh adds ~24 more briefs into the
    # same band — the column then goes back to two columns.
    y = 735
    tracked(d, M, y, "WHERE IT HAPPENED", F_BOLD(12), ACCENT, tracking=2)
    briefs_x = M + MAP_W + 16
    briefs_w = W - M - briefs_x
    tracked(d, briefs_x, y, "ALSO ON FRIDAY 20 NOVEMBER 2026",
            F_BOLD(12), ACCENT, tracking=2)
    map_y = 751
    draw_map(d, M, map_y, MAP_W, MAP_H)
    d.rectangle([M, map_y, M + MAP_W, map_y + MAP_H], outline=INK, width=2)
    legend = ("One pin per place — first brief for that place; "
              "positions approximate.")
    assert text_w(d, legend, F_REG(9)) <= MAP_W, "map legend too wide"
    d.text((M, map_y + MAP_H + 3), legend, font=F_REG(9), fill=GREY)
    assert len(BRIEFS) == 5, f"briefs must be 5, have {len(BRIEFS)}"
    for idx, (place, head) in enumerate(BRIEFS):
        by = map_y + idx * 34
        num = str(idx + 1)
        nw = text_w(d, num, F_BOLD(11))
        d.text((briefs_x, by), num, font=F_BOLD(11), fill=ACCENT)
        tx = briefs_x + nw + 5
        tw = briefs_w - nw - 5
        # Place in bold on the first line, headline wraps to 2 lines.
        first = f"{place} — "
        fw = text_w(d, first, F_BOLD(11))
        assert fw < tw, f"brief {idx + 1} place too wide"
        lines = wrap(d, head, F_REG(11), tw - fw)
        assert len(lines) <= 2, f"brief {idx + 1} too long: {head!r}"
        d.text((tx, by), first, font=F_BOLD(11), fill=INK)
        d.text((tx + fw, by), lines[0], font=F_REG(11), fill=BODY)
        if len(lines) > 1:
            d.text((tx, by + 14), lines[1], font=F_REG(11), fill=BODY)
    assert map_y + 4 * 34 + 28 <= 938, "briefs overflow"

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
    src = ("Sources: Reuters, Asia Today, Formula 1, Fiji Met, NordFX, "
           "KuCoin, AP, Al Jazeera, Samsung, BleepingComputer — 20 Nov "
           "2026. Pictures drawn in code; map positions approximate.")
    assert text_w(d, src, F_REG(10)) <= CW, "sources line too wide"
    d.text((M, 1004), src, font=F_REG(10), fill=GREY)

    img.save(OUT, format="PNG")
    print(f"saved {OUT} {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
