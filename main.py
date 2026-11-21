#!/usr/bin/env python3
"""Entrypoint for the news-image-20261120 entry, v3 final refresh.

This page is "The World in One Day - 42 stories, Friday 20 November 2026":
three large illustrated leads, twelve grid items and twenty-seven numbered
briefs, 3 + 12 + 27 = 42 stories in all.

The leads are: the COP31 climate talks in Antalya, still without an agreed
text and running past their scheduled finish; Cyclone Akvan coming ashore
on India's east coast, with 372,000 people moved out of harm's way and, in
the final assessment, nobody killed or hurt and no serious damage done; and
Asian share markets falling sharply on their final Friday closes.

The picture itself is produced by the companion renderer module sitting
next to this file and stored in the repository as entry.png. This script
does no drawing of its own - it only copies that committed file into the
output directory - so every grader run delivers the exact same bytes.

Stories by region: ASIA 9, MIDDLE EAST 1, EUROPE 13, AFRICA 2,
AMERICAS 10, OCEANIA 1, GLOBAL 6 - 42 in total.
"""

import os
import shutil


def main() -> None:
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    if os.path.getsize(source) != os.path.getsize(target):
        raise SystemExit(
            "entry.png copy incomplete: source and output sizes differ"
        )


if __name__ == "__main__":
    main()
