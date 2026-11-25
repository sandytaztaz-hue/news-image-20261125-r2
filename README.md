# news-image-20261125-r2

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/sandytaztaz-hue/news-image-20261125-r2/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/sandytaztaz-hue/news-image-20261125-r2/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

Round-2 entry for "Sum up 25 November's world news in one image": a single 1024x1024 broadsheet with 50 stories, every one dated Wednesday 25 November 2026. This round fixes round 1's flaw — every word is now set in clean anti-aliased DejaVu Serif Bold headlines and DejaVu Sans body text, with no pixel font anywhere, every string measured to fit its box, text kept in bands below the art, and no empty area on the page. All 50 stories were checked against reports dated 25 Nov 2026.

SPDX-License-Identifier: MIT

## What is on the page

- Masthead "Wednesday 25 November 2026" with a red tagline strip.
- A red stat strip with 8 big numbers (18th crewed China flight, 3,000 ha Flinders fire, 11 wounded Riyadh, 700,000+ Russians killed, 47,000 women killed 2025, 98% Dec Fed hike odds, $237.5bn Venezuela debt, 3.4% Q3 GDP).
- A UTC timeline ruler, 00:00-24:00, with dated ticks (00:18 Shenzhou lift-off, 01:23 AU CPI, 07:00 Germany GDP, 13:30 US data pile, 15:00 US home sales, 19:00 Beige Book, 20:00 UCL night).
- Lead hero: Shenzhou-24 lifts off from Jiuquan carrying China's first foreign astronaut, Pakistan's Muhammad Zeeshan Ali.
- 15 more hero cards with drawn illustrated scenes, each with headline, body, source and status tag (CONFIRMED / OFFICIAL / REPORTED / FORECAST / SCHEDULED / CLAIM / SPORT / MKT).
- ALSO TODAY: a 34-item numbered list (stories 17-50) in three columns.
- A world map with numbered red pins matching story numbers, a DATE CHECK box listing stories that did not happen on Wednesday (GTA 6, COP31, DR Congo vote, midterm vote, Man Utd comeback, Nepal PM visit), and a sources footer.

## Run it

```python3 main.py```

Writes /output/entry.png. `main.py` uses only the Python standard library, needs no Pillow, and produces byte-identical output on repeat runs. `render.py` (Pillow) regenerates `entry.png` deterministically from code.
