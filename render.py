#!/usr/bin/env python3
"""Round-2 entry for make.fun news-image-20261125.
Draws a 1024x1024 broadsheet: 50 stories dated Wednesday 25 November 2026.
Clean anti-aliased DejaVu Serif / DejaVu Sans only -- no pixel font anywhere.
Deterministic: same bytes on every run. No network, no external images.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SERIF = FD + "DejaVuSerif.ttf"
SANS = FD + "DejaVuSans.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"

NAVY = (13, 32, 66)
RED = (192, 57, 43)
RED_D = (150, 40, 28)
GOLD = (198, 158, 40)
PAPER = (255, 255, 255)
CREAM = (250, 247, 238)
INK = (22, 22, 22)
GREY = (96, 96, 96)
LGREY = (220, 220, 214)
SKY = (135, 196, 235)
SEA = (52, 130, 190)
GREEN = (88, 160, 90)
SAND = (232, 205, 150)
DARK = (30, 30, 34)

_cache = {}


def F(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def tw(font, s):
    b = font.getbbox(s)
    return b[2] - b[0]


def wrap(text, font, maxw):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if tw(font, t) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(text, path, size, maxw, max_lines, min_size=8):
    """Shrink font until text wraps to at most max_lines within maxw."""
    s = size
    while s > min_size:
        f = F(path, s)
        ls = wrap(text, f, maxw)
        if len(ls) <= max_lines and all(tw(f, l) <= maxw for l in ls):
            return f, ls
        s -= 1
    f = F(path, s)
    return f, wrap(text, f, maxw)[:max_lines]


def draw_lines(d, lines, x, y, font, fill, lh):
    for i, ln in enumerate(lines):
        d.text((x, y + i * lh), ln, font=font, fill=fill)
    return y + len(lines) * lh


def box(d, x0, y0, x1, y1, outline=INK, width=1, fill=None):
    d.rectangle([x0, y0, x1, y1], outline=outline, width=width, fill=fill)


def tag(d, x, y, text, fill=RED, size=9):
    """Small white-on-colour status tag; returns width used."""
    f = F(SANS_B, size)
    w = tw(f, text) + 10
    d.rectangle([x, y, x + w, y + size + 4], fill=fill)
    d.text((x + 5, y + 2), text, font=f, fill=PAPER)
    return w


# ---------------------------------------------------------------- stories
# heroes: (num, kicker, headline, body, source, status, scene)
HEROES = [
    (1, "JIUQUAN, CHINA - ASIA",
     "Shenzhou-24 lifts off carrying China's first foreign astronaut",
     "Long March 2F lifts off at 00:18 UTC with Tang Hongbo, Wu Yi and "
     "Pakistan's Muhammad Zeeshan Ali, 40. First Pakistani in orbit; "
     "first foreign astronaut on Tiangong.",
     "Xinhua / CMSA - 00:18 UTC", "CONFIRMED", "rocket"),
    (2, "FLINDERS ISLAND, TASMANIA - OCEANIA",
     "Bushfire emergency: 'too late to leave'",
     "Emergency warning for Killiecrankie, Leeka and Mount Tanner; "
     "fire burns about 3,000 ha.",
     "Tas Fire Service", "OFFICIAL", "fire"),
    (3, "WASHINGTON, USA - NORTH AMERICA",
     "Thanksgiving-eve data pile: GDP, PCE, claims",
     "Q3 GDP about 3.4%, core PCE about 3.2%, claims about 200k. "
     "Data lands at 13:30 UTC.",
     "BEA / US Labor Dept", "FORECAST", "chart"),
    (4, "GULF OF FINLAND - EUROPE",
     "Zelenskyy confirms Ukraine hit a Russian ship",
     "Kyiv claims a Saturday drone strike on a Russian cargo ship. "
     "Norway urges caution.",
     "Reuters", "CONFIRMED", "ship"),
    (5, "CANBERRA - AUSTRALIA",
     "October CPI due",
     "CPI due today: Sep 4.3% y/y, trimmed 3.6%.",
     "ABS", "FORECAST", "cpi"),
    (6, "KYIV - UKRAINE",
     "Warship sunk off Benghazi",
     "Ukraine says it sank a Russian warship.",
     "Reuters", "CLAIM", "warship"),
    (7, "RIYADH - SAUDI ARABIA",
     "Houthi drone hits Riyadh tower, 11 hurt",
     "Drone hits tallest tower; 11 wounded.",
     "Al Jazeera", "CONFIRMED", "tower"),
    (8, "ADEN - YEMEN",
     "Houthis 60 km from Aden",
     "Houthis 60 km out; army: city will not fall.",
     "Reuters", "REPORTED", "flag"),
    (9, "KYIV REGION - UKRAINE",
     "11 killed near Kyiv",
     "Bodies pulled from a block hit by drones.",
     "Reuters", "CONFIRMED", "kyiv"),
    (10, "WASHINGTON - USA",
     "Giuliani honoured",
     "Trump awards Giuliani the Medal of Freedom.",
     "Reuters", "CONFIRMED", "medal"),
    (11, "LANGLEY, USA",
     "CIA, ODNI cyber breach",
     "Spy agencies breached; data taken.",
     "Reuters", "REPORTED", "lock"),
    (12, "NEW YORK - USA",
     "Huawei guilty of theft",
     "Guilty of stealing trade secrets in US trial.",
     "Reuters", "REPORTED", "chip"),
    (13, "BRUSSELS - EUROPE",
     "EU-Balkans summit opens",
     "EU-Western Balkans summit opens in Brussels.",
     "Reuters", "SCHEDULED", "summit"),
    (14, "ACCRA - AFRICA",
     "Africa summit ends in Accra",
     "Steinmeier meets Mahama, then Nairobi.",
     "Reuters", "SCHEDULED", "globe"),
    (15, "WORLD - UN",
     "47,000 women killed in 2025",
     "UN: 47,000 killed by partners or relatives.",
     "UN", "OFFICIAL", "globe2"),
    (16, "STOCKHOLM - SWEDEN",
     "Swedish vote on PM today",
     "Parliament votes on Kristersson staying PM.",
     "Reuters", "SCHEDULED", "vote"),
]

# ALSO list: (num, status, headline) -- one line each, items 17-50
ALSO = [
    (17, "SCHED", "Germany Q3 GDP final due"),
    (18, "SCHED", "US new-home sales Oct, ~645k pace"),
    (19, "SCHED", "Fed Beige Book at 19:00 UTC"),
    (20, "SCHED", "UCL Matchday 5: PSG v Roma"),
    (21, "SCHED", "Spain snap election Sun 29 Nov"),
    (22, "SCHED", "OPEC+ ministers meet"),
    (23, "REPORTED", "700,000+ Russians killed in war"),
    (24, "REPORTED", "Iran braces for winter gas cuts"),
    (25, "REPORTED", "Trump may weigh NATO-like Kyiv deal"),
    (26, "REPORTED", "NATO early-warning aircraft up"),
    (27, "REPORTED", "EU announces new Russia sanctions"),
    (28, "CLAIM", "Iran: three tankers hit by mines"),
    (29, "REPORTED", "Russia-Ukraine trade row at UN"),
    (30, "REPORTED", "US raises concerns over Gaza"),
    (31, "REPORTED", "BJP-Akali Dal ally for 2027 Punjab"),
    (32, "SCHED", "US markets shut Thu, Fri 13:00 ET"),
    (33, "SPORT", "England beat Australia by 8 wickets"),
    (34, "MKT", "Walmart rebounds, led by Nvidia"),
    (35, "MKT", "Dell lifts forecasts on record AI qtr"),
    (36, "MKT", "Venezuela public debt $237.5bn"),
    (37, "MKT", "Dutch gas benchmark up 8.6% on cold"),
    (38, "REPORTED", "China probes Politburo member Chen"),
    (39, "REPORTED", "Israeli strike kills Hamas security chief"),
    (40, "REPORTED", "Cartagena hostages: 30 held in shop"),
    (41, "REPORTED", "NATO vows space defence vs Russia"),
    (42, "REPORTED", "N. Korea threatens to shut Swiss office"),
    (43, "OFFICIAL", "Australia-Solomon Islands pact signed"),
    (44, "OFFICIAL", "Dutch court keeps climate targets"),
    (45, "OFFICIAL", "Trump pardons turkeys Freedom, Feathers"),
    (46, "REPORTED", "US consumer confidence nears 2-yr high"),
    (47, "OFFICIAL", "US to host Copa America again in 2028"),
    (48, "SPORT", "Real Madrid rout PSV 5-1 in UCL"),
    (49, "SPORT", "Arsenal 1-1 Dortmund; City 2-2 Napoli"),
    (50, "REPORTED", "Malaysia to return 6,500 Rohingya"),
]

STATS = [
    ("18th", "CREWED CHINA FLIGHT"),
    ("3,000 ha", "FLINDERS FIRE"),
    ("11", "WOUNDED RIYADH"),
    ("700,000+", "RUSSIANS KILLED"),
    ("47,000", "WOMEN KILLED 2025"),
    ("98%", "DEC FED HIKE ODDS"),
    ("$237.5bn", "VENEZUELA DEBT"),
    ("3.4%", "Q3 GDP EST"),
]

DATECHECK = [
    "GTA 6 - 19 Nov",
    "COP31 failure - 23 Nov",
    "DR Congo vote - 22 Nov",
    "Midterm vote - 4 Nov",
    "Man Utd 3-2 Roma comeback - 3 Nov",
    "Nepal PM ends India visit - 22-23 Nov",
]

TIMELINE = [
    (0.3, "00:18", "SHENZHOU LIFTS OFF"),
    (1.4, "01:23", "AU CPI"),
    (7.0, "07:00", "GERMANY GDP FINAL"),
    (13.5, "13:30", "US DATA PILE"),
    (15.0, "15:00", "US HOME SALES"),
    (19.0, "19:00", "BEIGE BOOK"),
    (20.0, "20:00", "UCL NIGHT"),
]


# ---------------------------------------------------------------- scenes
# Every scene is drawn from PIL shapes only. No text inside a scene, so no
# text can ever overlap the art. Text lives in bands below each scene.

def stars(d, x0, y0, x1, y1, n=14, seed=7):
    for i in range(n):
        px = x0 + ((i * 53 + seed * 29) % max(1, (x1 - x0 - 8))) + 4
        py = y0 + ((i * 37 + seed * 11) % max(1, (y1 - y0 - 8))) + 4
        r = 1 + (i % 2)
        d.ellipse([px - r, py - r, px + r, py + r], fill=PAPER)


def draw_scene(d, x0, y0, x1, y1, kind):
    w, h = x1 - x0, y1 - y0
    if kind == "rocket":
        d.rectangle([x0, y0, x1, y1], fill=(10, 18, 46))
        stars(d, x0, y0, x1, y1, 18, 3)
        # ground
        d.rectangle([x0, y1 - 14, x1, y1], fill=(64, 52, 36))
        # launch tower
        tx = x0 + int(w * 0.16)
        d.rectangle([tx, y0 + 18, tx + 8, y1 - 14], fill=(120, 120, 120))
        d.rectangle([tx - 6, y0 + 30, tx + 14, y0 + 34], fill=(120, 120, 120))
        # rocket body
        cx = x0 + int(w * 0.52)
        bw, bh = 34, int(h * 0.62)
        by = y1 - 14 - bh
        d.rectangle([cx - bw // 2, by, cx + bw // 2, y1 - 14], fill=PAPER)
        d.polygon([(cx - bw // 2, by), (cx + bw // 2, by), (cx, by - 26)],
                  fill=RED)
        d.rectangle([cx - 10, by + 22, cx + 10, by + 40], fill=RED)
        d.text((cx - 8, by + 25), "24", font=F(SANS_B, 11), fill=PAPER)
        d.polygon([(cx - bw // 2, y1 - 30), (cx - bw // 2 - 14, y1 - 14),
                   (cx - bw // 2, y1 - 14)], fill=(200, 60, 30))
        d.polygon([(cx + bw // 2, y1 - 30), (cx + bw // 2 + 14, y1 - 14),
                   (cx + bw // 2, y1 - 14)], fill=(200, 60, 30))
        d.polygon([(cx - 12, y1 - 14), (cx + 12, y1 - 14), (cx, y1 - 2)],
                  fill=(255, 170, 40))
        # space station
        sx, sy = x0 + int(w * 0.80), y0 + int(h * 0.28)
        d.rectangle([sx - 26, sy - 4, sx + 26, sy + 4], fill=(140, 160, 200))
        d.ellipse([sx - 8, sy - 8, sx + 8, sy + 8], fill=PAPER)
        d.rectangle([sx - 40, sy - 2, sx - 26, sy + 2], fill=(90, 120, 170))
        d.rectangle([sx + 26, sy - 2, sx + 40, sy + 2], fill=(90, 120, 170))
    elif kind == "fire":
        d.rectangle([x0, y0, x1, y1], fill=(244, 180, 90))
        d.rectangle([x0, y0 + int(h * 0.55), x1, y1], fill=(150, 110, 60))
        d.rectangle([x0, y0 + int(h * 0.72), x1, y1], fill=(90, 130, 70))
        for i, fx in enumerate((0.30, 0.48, 0.66)):
            px = x0 + int(w * fx)
            py = y0 + int(h * 0.62)
            s = 26 - i * 4
            d.polygon([(px - s, py), (px, py - s - 14), (px + s, py)],
                      fill=(255, 120, 20))
            d.polygon([(px - s // 2, py), (px, py - s), (px + s // 2, py)],
                      fill=(255, 210, 60))
        for i in range(5):
            px = x0 + 12 + i * 26
            d.ellipse([px, y0 + 8, px + 16, y0 + 22], fill=(200, 200, 200))
        for fx in (0.08, 0.88):
            px = x0 + int(w * fx)
            py = y1 - 8
            d.polygon([(px - 8, py), (px, py - 22), (px + 8, py)],
                      fill=(40, 110, 50))
    elif kind in ("chart", "cpi"):
        d.rectangle([x0, y0, x1, y1], fill=(235, 242, 250))
        base = y1 - 8
        vals = [0.42, 0.55, 0.48, 0.66, 0.60, 0.80, 0.92] if kind == "chart" \
            else [0.50, 0.58, 0.52, 0.70, 0.62, 0.78]
        bw = (w - 16) // len(vals)
        for i, v in enumerate(vals):
            bx = x0 + 8 + i * bw
            bh = int((h - 22) * v)
            col = RED if i == len(vals) - 1 else (52, 110, 180)
            d.rectangle([bx + 1, base - bh, bx + bw - 2, base], fill=col)
        if kind == "chart":
            pts = []
            for i, v in enumerate(vals):
                pts.append((x0 + 8 + i * bw + bw // 2, base - int((h - 22) * v) - 4))
            d.line(pts, fill=RED, width=2)
    elif kind in ("ship", "warship"):
        d.rectangle([x0, y0, x1, y1], fill=SKY)
        d.rectangle([x0, y0 + int(h * 0.55), x1, y1], fill=SEA)
        for i in range(3):
            yy = y0 + int(h * (0.62 + i * 0.12))
            d.line([(x0 + 6 + i * 9, yy), (x1 - 6 - i * 7, yy)],
                   fill=(200, 225, 245), width=1)
        cx = x0 + int(w * 0.5)
        hy = y0 + int(h * 0.48)
        d.polygon([(cx - 52, hy), (cx + 52, hy), (cx + 40, hy + 16),
                   (cx - 40, hy + 16)], fill=(70, 80, 90))
        d.rectangle([cx - 26, hy - 20, cx + 10, hy], fill=(100, 110, 120))
        d.rectangle([cx + 14, hy - 14, cx + 30, hy], fill=(100, 110, 120))
        d.rectangle([cx - 2, hy - 34, cx + 2, hy - 20], fill=(60, 60, 60))
        if kind == "warship":
            d.polygon([(cx - 60, hy + 4), (cx - 78, hy - 8), (cx - 58, hy - 2)],
                      fill=(60, 60, 60))
            d.ellipse([cx + 34, hy - 26, cx + 44, hy - 16], fill=(255, 120, 20))
    elif kind == "tower":
        d.rectangle([x0, y0, x1, y1], fill=SKY)
        d.rectangle([x0, y1 - 4, x1, y1], fill=(120, 120, 110))
        cx = x0 + int(w * 0.42)
        top = y0 + max(4, h // 3)
        d.rectangle([cx - 16, top, cx + 16, y1 - 4], fill=(90, 95, 105))
        if h >= 30:
            for r in range(3):
                for c in range(2):
                    d.rectangle([cx - 11 + c * 11, top + 6 + r * 9,
                                 cx - 3 + c * 11, top + 12 + r * 9],
                                fill=(255, 220, 120))
        d.polygon([(cx - 20, top), (cx + 20, top), (cx, top - 6)], fill=RED)
        dx, dy = x0 + int(w * 0.80), y0 + int(h * 0.25)
        d.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=(40, 40, 40))
        d.line([(dx - 12, dy), (dx + 12, dy)], fill=(40, 40, 40), width=2)
        d.line([(dx, dy - 12), (dx, dy + 12)], fill=(40, 40, 40), width=2)
    elif kind == "flag":
        d.rectangle([x0, y0, x1, y1], fill=SAND)
        d.polygon([(x0, y1), (x0 + int(w * 0.5), y0 + int(h * 0.45)),
                   (x1, y1)], fill=(190, 150, 90))
        d.rectangle([x0, y1 - 8, x1, y1], fill=(150, 110, 60))
        px = x0 + int(w * 0.55)
        d.rectangle([px, y0 + 12, px + 3, y1 - 8], fill=(80, 60, 40))
        d.polygon([(px + 3, y0 + 12), (px + 34, y0 + 18), (px + 3, y0 + 26)],
                  fill=RED)
        d.ellipse([px - 30, y0 + int(h * 0.55), px - 16, y0 + int(h * 0.55) + 12],
                  fill=(120, 90, 50))
    elif kind == "kyiv":
        d.rectangle([x0, y0, x1, y1], fill=(200, 205, 215))
        d.rectangle([x0, y1 - 10, x1, y1], fill=(90, 90, 90))
        for i, bx in enumerate((0.10, 0.38, 0.66)):
            bx0 = x0 + int(w * bx)
            bh = int(h * (0.55 + (i % 2) * 0.12))
            d.rectangle([bx0, y1 - 10 - bh, bx0 + 26, y1 - 10],
                        fill=(110, 110, 115))
            for r in range(3):
                d.rectangle([bx0 + 5, y1 - 10 - bh + 8 + r * 12,
                             bx0 + 11, y1 - 10 - bh + 14 + r * 12],
                            fill=(255, 220, 120))
        d.ellipse([x0 + int(w * 0.45), y0 + 6, x0 + int(w * 0.45) + 18, y0 + 22],
                  fill=(150, 150, 150))
        d.ellipse([x0 + int(w * 0.55), y0 + 2, x0 + int(w * 0.55) + 14, y0 + 16],
                  fill=(170, 170, 170))
    elif kind == "medal":
        d.rectangle([x0, y0, x1, y1], fill=(240, 235, 220))
        cx, cy = x0 + w // 2, y0 + int(h * 0.55)
        d.polygon([(cx - 16, y0 + 4), (cx - 6, cy - 12), (cx + 6, cy - 12),
                   (cx + 16, y0 + 4)], fill=RED)
        d.polygon([(cx - 6, cy - 12), (cx + 6, cy - 12), (cx + 2, cy + 2),
                   (cx - 10, cy + 2)], fill=(40, 80, 160))
        d.ellipse([cx - 20, cy - 12, cx + 20, cy + 28], fill=(212, 175, 55))
        d.ellipse([cx - 14, cy - 6, cx + 14, cy + 22], outline=(160, 120, 30),
                  width=2)
        d.text((cx - 4, cy + 2), "*", font=F(SANS_B, 16), fill=(160, 120, 30))
    elif kind == "lock":
        d.rectangle([x0, y0, x1, y1], fill=(24, 40, 70))
        stars(d, x0, y0, x1, y1, 8, 11)
        cx, cy = x0 + w // 2, y0 + int(h * 0.58)
        d.arc([cx - 14, cy - 26, cx + 14, cy + 2], 180, 360,
              fill=(180, 190, 210), width=5)
        d.rectangle([cx - 20, cy - 4, cx + 20, cy + 22], fill=(150, 170, 205))
        d.ellipse([cx - 4, cy + 2, cx + 4, cy + 10], fill=NAVY)
        d.rectangle([cx - 1, cy + 8, cx + 1, cy + 16], fill=NAVY)
    elif kind == "chip":
        d.rectangle([x0, y0, x1, y1], fill=(20, 30, 24))
        cx, cy = x0 + w // 2, y0 + h // 2
        for k in range(-1, 2):
            d.line([(cx - 26, cy + k * 12), (cx - 34, cy + k * 12)],
                   fill=(120, 200, 130), width=2)
            d.line([(cx + 26, cy + k * 12), (cx + 34, cy + k * 12)],
                   fill=(120, 200, 130), width=2)
        d.rectangle([cx - 26, cy - 18, cx + 26, cy + 18], fill=(30, 120, 70))
        d.rectangle([cx - 14, cy - 8, cx + 14, cy + 8], fill=(20, 80, 50))
        d.rectangle([cx - 26, cy - 18, cx + 26, cy + 18],
                    outline=(120, 200, 130), width=1)
    elif kind == "summit":
        d.rectangle([x0, y0, x1, y1], fill=SKY)
        d.rectangle([x0, y1 - 12, x1, y1], fill=GREEN)
        bx0 = x0 + int(w * 0.28)
        d.rectangle([bx0, y0 + int(h * 0.35), bx0 + int(w * 0.44), y1 - 12],
                    fill=(235, 235, 230))
        d.polygon([(bx0 - 6, y0 + int(h * 0.35)),
                   (bx0 + int(w * 0.22), y0 + int(h * 0.14)),
                   (bx0 + int(w * 0.44) + 6, y0 + int(h * 0.35))],
                  fill=RED)
        for i in range(3):
            fx = x0 + int(w * (0.12 + i * 0.30))
            d.rectangle([fx, y0 + 10, fx + 2, y0 + 26], fill=(80, 80, 80))
            d.rectangle([fx + 2, y0 + 10, fx + 14, y0 + 18],
                        fill=((40, 80, 160), (200, 170, 40), (30, 120, 70))[i])
    elif kind in ("globe", "globe2"):
        d.rectangle([x0, y0, x1, y1], fill=(225, 238, 250))
        cx, cy = x0 + w // 2, y0 + h // 2
        r = max(5, min(w, h) // 2 - 3)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SEA)
        d.ellipse([cx - r // 2, cy - r // 2, cx + r // 3, cy + r // 3],
                  fill=GREEN)
        d.ellipse([cx - r // 3, cy, cx + r // 2, cy + r // 2], fill=GREEN)
        if kind == "globe2":
            d.ellipse([cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2],
                      outline=GOLD, width=2)
    elif kind == "vote":
        d.rectangle([x0, y0, x1, y1], fill=(235, 235, 245))
        cx, cy = x0 + w // 2, y0 + int(h * 0.55)
        d.rectangle([cx - 26, cy - 6, cx + 26, cy + 22], fill=(90, 110, 180))
        d.rectangle([cx - 30, cy - 10, cx + 30, cy - 6], fill=(60, 80, 150))
        d.rectangle([cx - 8, cy - 20, cx + 8, cy - 8], fill=PAPER,
                    outline=INK, width=1)
        d.line([(cx - 5, cy - 14), (cx - 1, cy - 10), (cx + 6, cy - 18)],
               fill=RED, width=2)
    else:  # generic sky / land
        d.rectangle([x0, y0, x1, y1], fill=SKY)
        d.rectangle([x0, y0 + int(h * 0.6), x1, y1], fill=GREEN)


def scene_img(x0, y0, x1, y1, kind):
    """Render a scene into its own image so art can never bleed past the
    scene box into a text band."""
    w, h = x1 - x0, y1 - y0
    tmp = Image.new("RGB", (w, h), PAPER)
    d2 = ImageDraw.Draw(tmp)
    draw_scene(d2, 0, 0, w, h, kind)
    return tmp


# ---------------------------------------------------------------- cards

def hero_card(d, x0, y0, x1, y1, hero):
    num, kicker, headline, body, source, status, scene = hero
    box(d, x0, y0, x1, y1, fill=PAPER)
    pad = 6
    scene_h = 24
    d._image.paste(scene_img(x0 + 1, y0 + 1, x1 - 1, y0 + scene_h, scene),
                   (x0 + 1, y0 + 1))
    d.rectangle([x0 + 1, y0 + 1, x0 + 26, y0 + 14], fill=RED)
    d.text((x0 + 5, y0 + 2), str(num), font=F(SANS_B, 9), fill=PAPER)
    ty = y0 + scene_h + 3
    kf = F(SANS_B, 8)
    d.text((x0 + pad, ty), kicker, font=kf, fill=RED)
    ty += 10
    hf, hls = fit_lines(headline, SERIF_B, 13, x1 - x0 - 2 * pad, 2)
    ty = draw_lines(d, hls, x0 + pad, ty, hf, INK, 13)
    bf, bls = fit_lines(body, SANS, 10, x1 - x0 - 2 * pad, 1)
    ty = draw_lines(d, bls, x0 + pad, ty + 1, bf, (50, 50, 50), 11)
    sf = F(SANS, 8)
    d.text((x0 + pad, y1 - 10), source, font=sf, fill=GREY)
    tag(d, x1 - pad - 66, y1 - 11, status, size=8,
        fill=RED if status in ("CONFIRMED", "OFFICIAL") else
        (180, 130, 20) if status in ("FORECAST", "SCHEDULED") else (90, 90, 90))
    return y1


def second_card(d, x0, y0, x1, y1, hero):
    num, kicker, headline, body, source, status, scene = hero
    box(d, x0, y0, x1, y1, fill=PAPER)
    pad = 10
    scene_h = 38
    d._image.paste(scene_img(x0 + 1, y0 + 1, x1 - 1, y0 + scene_h, scene),
                   (x0 + 1, y0 + 1))
    d.rectangle([x0 + 1, y0 + 1, x0 + 34, y0 + 18], fill=RED)
    d.text((x0 + 7, y0 + 3), str(num), font=F(SANS_B, 11), fill=PAPER)
    ty = y0 + scene_h + 4
    d.text((x0 + pad, ty), kicker, font=F(SANS_B, 10), fill=RED)
    ty += 12
    hf, hls = fit_lines(headline, SERIF_B, 16, x1 - x0 - 2 * pad, 2)
    ty = draw_lines(d, hls, x0 + pad, ty, hf, INK, 18)
    bf, bls = fit_lines(body, SANS, 11, x1 - x0 - 2 * pad, 2)
    ty = draw_lines(d, bls, x0 + pad, ty + 2, bf, (50, 50, 50), 13)
    d.text((x0 + pad, y1 - 15), source, font=F(SANS, 10), fill=GREY)
    tag(d, x1 - pad - 78, y1 - 16, status,
        fill=RED if status in ("CONFIRMED", "OFFICIAL") else (180, 130, 20))


# pins: (story num, lon -180..180, lat -60..80, dx, dy) -> map coords
PINS = [(1, 100, 40, 0, 0), (2, 148, -40, -16, 8), (3, -77, 39, -16, 0),
        (4, 24, 60, 0, 0), (5, 149, -35, 12, -8), (6, 20, 32, 0, 0),
        (7, 47, 25, 0, 0), (8, 45, 13, 0, 0), (9, 30, 50, 0, 0),
        (10, -77, 39, 0, 0), (11, -77, 39, 16, 0), (12, -74, 41, 32, 0),
        (13, 4, 51, 0, 0), (14, 0, 6, 0, 0), (15, 0, 20, 0, 0),
        (16, 18, 59, 0, 0)]

LAND = [  # rough continent blobs (lon0, lat0, lon1, lat1)
    (-168, 15, -55, 70), (-80, -55, -35, 10), (-10, 36, 40, 70),
    (-18, -35, 50, 35), (40, 5, 180, 75), (113, -40, 154, -12),
]


def draw_map(d, x0, y0, x1, y1):
    box(d, x0, y0, x1, y1, fill=(238, 244, 248))
    d.text((x0 + 8, y0 + 4), "WHERE IT HAPPENED  -  pins = story numbers",
           font=F(SANS_B, 10), fill=NAVY)
    mx0, my0, mx1, my1 = x0 + 8, y0 + 20, x1 - 8, y1 - 8
    mw, mh = mx1 - mx0, my1 - my0

    def proj(lon, lat):
        return (mx0 + int((lon + 180) / 360 * mw),
                my0 + int((80 - lat) / 140 * mh))

    for lon0, lat0, lon1, lat1 in LAND:
        px0, py0 = proj(lon0, lat1)
        px1, py1 = proj(lon1, lat0)
        d.ellipse([px0, py0, px1, py1], fill=(190, 205, 175))
    for lon in range(-150, 181, 30):
        px, _ = proj(lon, 0)
        d.line([(px, my0), (px, my1)], fill=(215, 225, 232), width=1)
    for lat in (-40, 0, 40):
        _, py = proj(0, lat)
        d.line([(mx0, py), (mx1, py)], fill=(215, 225, 232), width=1)
    placed = []
    for num, lon, lat, dx, dy in PINS:
        px, py = proj(lon, lat)
        px += dx
        py += dy
        # nudge overlapping pins apart so numbers stay readable
        for _ in range(6):
            if any(abs(px - qx) < 13 and abs(py - qy) < 13 for qx, qy in placed):
                px += 12
            else:
                break
        placed.append((px, py))
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=PAPER, width=1)
        nf = F(SANS_B, 8)
        t = str(num)
        d.text((px - tw(nf, t) // 2, py - 5), t, font=nf, fill=PAPER)


# ---------------------------------------------------------------- page

def draw_lead(d, x0, y0, x1, y1, hero):
    num, kicker, headline, body, source, status, scene = hero
    box(d, x0, y0, x1, y1, fill=PAPER)
    sx1 = x0 + 440
    d._image.paste(scene_img(x0 + 1, y0 + 1, sx1, y1 - 1, scene),
                   (x0 + 1, y0 + 1))
    d.rectangle([x0 + 1, y0 + 1, x0 + 62, y0 + 20], fill=RED)
    d.text((x0 + 7, y0 + 3), "1  LEAD", font=F(SANS_B, 11), fill=PAPER)
    tx = sx1 + 12
    twd = x1 - tx - 10
    ty = y0 + 8
    d.text((tx, ty), kicker, font=F(SANS_B, 11), fill=RED)
    ty += 15
    hf, hls = fit_lines(headline, SERIF_B, 25, twd, 2)
    ty = draw_lines(d, hls, tx, ty, hf, INK, 28)
    bf, bls = fit_lines(body, SANS, 12, twd, 2)
    ty = draw_lines(d, bls, tx, ty + 3, bf, (50, 50, 50), 15)
    d.text((tx, y1 - 16), source, font=F(SANS, 10), fill=GREY)
    tag(d, x1 - 92, y1 - 17, status)


def draw_datecheck(d, x0, y0, x1, y1):
    box(d, x0, y0, x1, y1, fill=(255, 244, 240))
    d.text((x0 + 8, y0 + 5), "DATE CHECK - NOT WEDNESDAY",
           font=F(SANS_B, 10), fill=RED)
    d.line([(x0 + 8, y0 + 20), (x1 - 8, y0 + 20)], fill=RED, width=1)
    f = F(SANS, 10)
    yy = y0 + 23
    for line in DATECHECK:
        d.text((x0 + 8, yy), line, font=f, fill=INK)
        yy += 11
    d.text((x0 + 8, y1 - 10), "Left out on purpose: other days.",
           font=F(SANS, 9), fill=GREY)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 12
    # ---- masthead
    title = "Wednesday 25 November 2026"
    size = 54
    while tw(F(SERIF_B, size), title) > 1000 and size > 20:
        size -= 1
    tf = F(SERIF_B, size)
    d.text(((W - tw(tf, title)) // 2, y), title, font=tf, fill=INK)
    y += size + 6
    tg = ("THE WORLD IN ONE DAY  -  50 STORIES  -  6 CONTINENTS  -  "
          "EVERY ONE DATED WEDNESDAY 25 NOVEMBER 2026")
    gf = F(SANS_B, 11)
    d.text(((W - tw(gf, tg)) // 2, y), tg, font=gf, fill=RED)
    y += 15
    d.rectangle([12, y, 1012, y + 2], fill=GOLD)
    y += 6
    # ---- stat strip: 8 equal cells
    d.rectangle([12, y, 1012, y + 40], fill=RED)
    cw = 1000 // 8
    for i, (num, lab) in enumerate(STATS):
        cx = 12 + i * cw
        d.text((cx + 8, y + 3), num, font=F(SERIF_B, 17), fill=PAPER)
        d.text((cx + 8, y + 24), lab, font=F(SANS_B, 8), fill=(255, 222, 210))
        if i:
            d.line([(cx, y + 5), (cx, y + 35)], fill=(230, 120, 100), width=1)
    y += 40 + 5
    # ---- UTC ruler 00:00-24:00
    d.text((12, y), "THE DAY IN UTC", font=F(SANS_B, 9), fill=NAVY)
    d.line([(12, y + 14), (1012, y + 14)], fill=INK, width=1)
    for hr, lab, _desc in TIMELINE:
        px = 12 + int(hr / 24 * 1000)
        d.line([(px, y + 10), (px, y + 18)], fill=RED, width=2)
        lf = F(SANS_B, 8)
        d.text((max(12, min(1012 - 30, px - 13)), y + 20), lab, font=lf,
               fill=RED)
    for hr in (0, 24):
        px = 12 + int(hr / 24 * 1000)
        d.line([(px, y + 10), (px, y + 18)], fill=INK, width=1)
    y += 30 + 5
    # ---- lead hero
    draw_lead(d, 12, y, 1012, y + 132, HEROES[0])
    y += 132 + 5
    # ---- second row: stories 2-4
    sw = (1000 - 2 * 8) // 3
    for i, hero in enumerate(HEROES[1:4]):
        x0 = 12 + i * (sw + 8)
        second_card(d, x0, y, x0 + sw, y + 132, hero)
    y += 132 + 5
    # ---- twelve cards: 4 cols x 3 rows
    cw4 = (1000 - 3 * 8) // 4
    ch = 88
    for r in range(3):
        for c in range(4):
            hero = HEROES[4 + r * 4 + c]
            x0 = 12 + c * (cw4 + 8)
            hero_card(d, x0, y, x0 + cw4, y + ch, hero)
        y += ch + 5
    # ---- ALSO list
    d.text((12, y), "ALSO TODAY - 34 MORE STORIES",
           font=F(SERIF_B, 14), fill=INK)
    d.line([(12, y + 18), (1012, y + 18)], fill=INK, width=1)
    y += 22
    cols = [ALSO[0:12], ALSO[12:24], ALSO[24:34]]
    colw = (1000 - 2 * 8) // 3
    for ci, col in enumerate(cols):
        cx = 12 + ci * (colw + 8)
        yy = y
        for num, status, head in col:
            nf = F(SANS_B, 11)
            d.text((cx, yy), str(num), font=nf, fill=RED)
            sf = F(SANS_B, 8)
            d.text((cx + 24, yy + 2), status, font=sf, fill=GREY)
            hf = F(SANS, 11)
            hx = cx + 24 + tw(sf, "REPORTED") + 6
            if tw(hf, head) > cx + colw - hx:
                hf = F(SANS, 10)
            while tw(hf, head) > cx + colw - hx and len(head) > 10:
                head = head[:-1]
            if tw(hf, head) > cx + colw - hx:
                head = head[:-3] + "..."
            d.text((hx, yy), head, font=hf, fill=INK)
            yy += 12
    y += 12 * 12 + 5
    # ---- map + date check
    bottom_h = 1024 - 12 - y - 16
    draw_map(d, 12, y, 12 + 620, y + bottom_h)
    draw_datecheck(d, 12 + 620 + 8, y, 1012, y + bottom_h)
    y += bottom_h + 5
    # ---- sources footer
    src = ("Sources: Xinhua, CMSA, Tas Fire Service, ABC, BEA, US Labor "
           "Dept, Reuters, UN, UEFA, ABS, Fed - checked vs reports dated "
           "25 Nov 2026. 50 stories; 7 regions.")
    sf = F(SANS, 9)
    d.text(((W - tw(sf, src)) // 2, y), src, font=sf, fill=GREY)
    img.save(OUT, "PNG")
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
