#!/usr/bin/env python3
"""Compose the v2 front page for Wednesday 18 November 2026.

Draws a 1024x1024 newspaper front page with Pillow: masthead, 13 featured
stories each with an original flat-vector illustration drawn procedurally,
32 one-line briefs, and a schematic world map with numbered pins.
Deterministic: no randomness, no timestamps, no network.

Run:  python3 compose.py   ->  entry.png (<= 1 MiB) in this directory.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 26                      # side margin
CW = W - 2 * M              # content width = 972

PAPER = "#F8F2E3"           # cream paper
CARD = "#FFFDF6"            # card fill
BORDER = "#E0D8C2"          # card border
INK = "#1B1B1B"             # headline ink
DECK = "#4A4A44"            # deck gray
RULE = "#9A917C"            # thin rules
RED = "#B3271E"             # kicker / brief numbers

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
MASTHEAD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"

# Region colours (also used for the bar under the masthead and the map pins).
REGION_COLORS = {
    "AMERICAS": "#2E7D4F",
    "EUROPE": "#2F5DA8",
    "AFRICA": "#9C6B30",
    "MIDDLE EAST": "#C0392B",
    "ASIA": "#C08A1E",
    "OCEANIA": "#1F8A8A",
    "GLOBAL": "#7B4BA6",
}
REGION_ORDER = ["AMERICAS", "EUROPE", "AFRICA", "MIDDLE EAST",
                "ASIA", "OCEANIA", "GLOBAL"]

# ---------------------------------------------------------------- stories
# (number, region, topic, headline, deck, pastel tint, illustration key)
FEATURED = [
    (1, "MIDDLE EAST", "IRAN WAR",
     "Kuwait, Bahrain say they intercepted Iranian drones",
     "Iran's army says it aimed at US forces at Ali Al Salem. ADNOC says "
     "its ship was hit in Hormuz; 1 missing, 11 injured.",
     "#DCE7EF", "gulf"),
    (2, "ASIA", "DIPLOMACY",
     "Xi greets Trump on eve of Trump\u2013Xi\u2013Putin summit",
     "Xi and Putin vowed to \u201clead\u201d a multipolar world; at APEC Xi "
     "urged AI and free-trade cooperation. Talks Thursday.",
     "#EFE6D8", "summit"),
    (3, "AMERICAS", "US POLITICS",
     "Democrat Peltola wins Alaska; Senate now 56-44",
     "AP calls it: 144,302 votes to Sullivan's 131,844. A ninth Democratic "
     "gain, the most in a midterm since 1958, AP says.",
     "#E6E0F2", "peltola"),
    (4, "EUROPE", "UKRAINE WAR",
     "Russia fires 141 drones at Ukraine overnight",
     "Air force: 126 downed. Officials: 5 killed, 15 injured in a day; "
     "power cut to 80+ Rivne settlements.",
     "#DDE9F5", "drones"),
    (5, "MIDDLE EAST", "GAZA",
     "Board of Peace warns UN the Gaza truce may collapse",
     "First report to the Security Council (obtained by AP) says Israel "
     "blocked the civil administration.",
     "#F5DEDC", "gaza"),
    (6, "ASIA", "DISASTER",
     "Cyclone Akvan strengthens in the Bay of Bengal",
     "IMD: landfall in Andhra Pradesh around noon Friday. Odisha readies "
     "up to 204,070 to evacuate.",
     "#D9ECF2", "cyclone"),
    (7, "EUROPE", "ECONOMY",
     "UK inflation rises to 3.6%, highest in a year",
     "October CPI up from 3.5% as diesel hits a record high, the ONS says.",
     "#F6EBCB", "inflation"),
    (8, "AFRICA", "SUDAN WAR",
     "Amnesty: RSF drone strikes killed 37 civilians in El Obeid",
     "It says they should be investigated as war crimes; the RSF denies "
     "responsibility.",
     "#F7E3D2", "sudan"),
    (9, "GLOBAL", "CULTURE",
     "Grand Theft Auto VI goes on sale after a 13-year wait",
     "Midnight launch starts in New Zealand; Sensor Tower estimates 15m+ "
     "pre-release sales.",
     "#E7DEF2", "gta"),
    (10, "EUROPE", "HEALTH",
     "Europe off track on antibiotic resistance, ECDC warns",
     "Carbapenem-resistant K. pneumoniae bloodstream infections up 72% "
     "since 2019.",
     "#DFF0DC", "antibiotic"),
    (11, "GLOBAL", "CLIMATE",
     "COP31: 75 countries back T\u00fcrkiye\u2019s \u201c35x35\u201d power goal",
     "Electricity 35% of energy use by 2035 (Anadolu). Johan Rockstr\u00f6m "
     "warns of 2.8-3C.",
     "#DCEBF5", "climate"),
    (12, "ASIA", "LABOUR",
     "Bangladesh garment protests shut at least 55 factories",
     "Tk 30,000 minimum wage sought; Dhaka\u2013Mymensingh highway blocked, "
     "police vehicle torched.",
     "#F2E6CC", "garment"),
    (13, "OCEANIA", "DIPLOMACY",
     "Australia sanctions settler leader Daniella Weiss",
     "Also two others and four groups incl. Nachala, Amana, over West Bank "
     "settlements (Penny Wong).",
     "#D8ECE8", "sanctions"),
]

# Briefs 14-45. Three swaps vs the reference template, all verified real
# 18 Nov 2026 news: 27 (Merchant sentencing), 41 (UN Ukraine toll),
# 44 (Northern Ireland promotion) replace the ringgit / bat-species /
# SA Rugby briefs. See RESEARCH.md.
BRIEFS = [
    (14, "Riyadh: coalition says it downed a Houthi cruise missile"),
    (15, "Jerusalem: Knesset approves 9 deputy speakers, 2 Arab"),
    (16, "Berlin: coalition to cut power tax and cap fuel prices"),
    (17, "Germany: accuses Russia of chemical-weapons breaches"),
    (18, "Cambridge: \u201chuman\u201d named word of the year"),
    (19, "Shenzhen: Xi and Lee conclude FTA services talks"),
    (20, "Manila: Trump claims trade deal; Manila says none signed"),
    (21, "Tokyo: Japan posts sixth straight monthly trade deficit"),
    (22, "Seoul: court acquits Daegu mayor in martial-law case"),
    (23, "Singapore: Princess Aiko on first imperial visit in 20 years"),
    (24, "Bangkok: Chinese director jailed over collapsed tower"),
    (25, "Lahore: world\u2019s most polluted big city again, AQI 339"),
    (26, "Rawalpindi: Sri Lanka all out for 98 against Pakistan"),
    (27, "Brooklyn: Merchant jailed 27\u00bd years over Iran plot to kill Trump"),
    (28, "Asia markets: Kospi +2%, Hang Seng -0.9%"),
    (29, "Oil: Brent falls 1.4% to $81.82"),
    (30, "China: Tencent revenue up 8%, below forecasts"),
    (31, "Cook Islands: Cyclone Xavier reaches Category 5"),
    (32, "New Zealand: tsunami advisory lifted after 60 cm surges"),
    (33, "Sydney: Tame Impala sweeps the ARIA Awards"),
    (34, "Australia: Bancroft says whole team knew of 2018 plot"),
    (35, "Canada: Carney says China trade no worry for Trump"),
    (36, "Peru: M5.9 quake off south coast, no damage reported"),
    (37, "Cincinnati: USA beat Haiti 2-0, into Nations League semis"),
    (38, "Monterrey: Mexico edge Jamaica, set up semi v USA"),
    (39, "Los Angeles: Grimes scores 47 as Lakers win 9th straight"),
    (40, "Buenos Aires: deputies debate Malvinas sovereignty bill"),
    (41, "Kyiv: UN: 2026 Ukraine civilian deaths already top 2025"),
    (42, "Washington: NSA confirms outage on classified network"),
    (43, "South Africa: inflation jumps to 5.2%, highest since 2024"),
    (44, "Budapest: N. Ireland draw 1-1, win promotion to Nations League A"),
    (45, "Sudan: archaeologists reach Old Dongola church floor"),
]


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, font, width):
    """Greedy word wrap using real font metrics."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if font.getlength(trial) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_font(path, text, start, minimum, width, tracking=0):
    """Largest font size in [minimum, start] whose text fits in width."""
    for size in range(start, minimum - 1, -1):
        f = F(path, size)
        w = f.getlength(text)
        if tracking:
            w += tracking * (len(text) - 1)
        if w <= width:
            return f
    return F(path, minimum)


def draw_tracked(d, x, y, text, font, fill, tracking=2):
    cx = x
    for ch in text:
        d.text((cx, y), ch, font=font, fill=fill)
        cx += font.getlength(ch) + tracking
    return cx


def tracked_width(text, font, tracking=2):
    return sum(font.getlength(c) for c in text) + tracking * (len(text) - 1)

# ------------------------------------------------------- illustrations
# Each illustration draws in a virtual 188x68 canvas, scaled by height so
# the same drawing works in the wide row-1 boxes and the narrow row-2/3
# boxes without distortion. No text inside any illustration.

class Box:
    def __init__(self, d, x, y, w, h):
        self.d = d
        self.u = h / 68.0
        self.cw = 188 * self.u
        self.ox = x + (w - self.cw) / 2
        self.oy = y

    def X(self, px):
        return self.ox + px * self.u

    def Y(self, py):
        return self.oy + py * self.u

    def S(self, px):
        return px * self.u

    def ellipse(self, x0, y0, x1, y1, **kw):
        self.d.ellipse([self.X(x0), self.Y(y0), self.X(x1), self.Y(y1)], **kw)

    def rect(self, x0, y0, x1, y1, **kw):
        self.d.rectangle([self.X(x0), self.Y(y0), self.X(x1), self.Y(y1)], **kw)

    def poly(self, pts, **kw):
        self.d.polygon([(self.X(px), self.Y(py)) for px, py in pts], **kw)

    def line(self, pts, **kw):
        self.d.line([(self.X(px), self.Y(py)) for px, py in pts], **kw)

    def arc(self, box, a0, a1, **kw):
        self.d.arc([self.X(box[0]), self.Y(box[1]),
                    self.X(box[2]), self.Y(box[3])], a0, a1, **kw)


def _drone(b, cx, cy, s, col="#2B2B2B"):
    """Small quadcopter silhouette centred at (cx, cy), size s."""
    b.d.line([b.X(cx - s), b.Y(cy - s * 0.5), b.X(cx + s), b.Y(cy + s * 0.5)],
             fill=col, width=max(2, int(b.S(2))))
    b.d.line([b.X(cx + s), b.Y(cy - s * 0.5), b.X(cx - s), b.Y(cy + s * 0.5)],
             fill=col, width=max(2, int(b.S(2))))
    b.ellipse(cx - s * 0.35, cy - s * 0.35, cx + s * 0.35, cy + s * 0.35,
              fill=col)
    for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        b.ellipse(cx + dx * s - s * 0.28, cy + dy * s * 0.5 - s * 0.14,
                  cx + dx * s + s * 0.28, cy + dy * s * 0.5 + s * 0.14,
                  fill=col)


def _burst(b, cx, cy, r, col="#F2A007"):
    pts = []
    for i in range(12):
        ang = i * 30
        rr = r if i % 2 == 0 else r * 0.45
        import math
        pts.append((cx + rr * math.cos(math.radians(ang)),
                    cy + rr * math.sin(math.radians(ang))))
    b.poly(pts, fill=col)
    b.ellipse(cx - r * 0.32, cy - r * 0.32, cx + r * 0.32, cy + r * 0.32,
              fill="#E4572E")


def illo_gulf(d, x, y, w, h):
    b = Box(d, x, y, w, h)
    b.rect(0, 44, 188, 68, fill="#7FA8C9")          # sea
    b.rect(0, 44, 188, 47, fill="#A8C4DB")
    for wx in (20, 70, 120, 165):                    # wave caps
        b.arc((wx - 12, 50, wx + 12, 62), 180, 360, fill="#EAF2F8",
              width=max(2, int(b.S(2))))
    b.rect(52, 30, 138, 44, fill="#33393F")          # tanker hull
    b.poly([(52, 30), (46, 44), (144, 44), (138, 30)], fill="#33393F")
    b.rect(96, 18, 118, 30, fill="#4A5258")         # superstructure
    b.rect(122, 12, 130, 30, fill="#8A2F26")        # funnel
    _drone(b, 30, 12, 7)
    _drone(b, 62, 8, 6)
    _drone(b, 160, 14, 7)
    _burst(b, 148, 26, 9)


def _flag(b, x0, y0, fw, fh, kind):
    if kind == "us":
        for i in range(7):
            b.rect(x0, y0 + i * fh / 7, x0 + fw, y0 + (i + 1) * fh / 7,
                   fill="#B22234" if i % 2 == 0 else "#FFFFFF")
        b.rect(x0, y0, x0 + fw * 0.45, y0 + fh * 4 / 7, fill="#3C3B6E")
        for r in range(3):
            for c in range(4):
                b.ellipse(x0 + 2 + c * fw * 0.1, y0 + 2 + r * fh * 0.16,
                          x0 + 4 + c * fw * 0.1, y0 + 4 + r * fh * 0.16,
                          fill="white")
    elif kind == "cn":
        b.rect(x0, y0, x0 + fw, y0 + fh, fill="#DE2910")
        b.ellipse(x0 + 3, y0 + 3, x0 + 8, y0 + 8, fill="#FFDE00")
        for sx, sy in ((14, 4), (17, 8), (17, 13), (14, 17)):
            b.ellipse(x0 + sx, y0 + sy, x0 + sx + 3, y0 + sy + 3,
                      fill="#FFDE00")
    elif kind == "ru":
        b.rect(x0, y0, x0 + fw, y0 + fh / 3, fill="#FFFFFF")
        b.rect(x0, y0 + fh / 3, x0 + fw, y0 + 2 * fh / 3, fill="#0039A6")
        b.rect(x0, y0 + 2 * fh / 3, x0 + fw, y0 + fh, fill="#D52B1E")
    elif kind == "bd":
        b.rect(x0, y0, x0 + fw, y0 + fh, fill="#006A4E")
        b.ellipse(x0 + fw * 0.42, y0 + fh * 0.22, x0 + fw * 0.72,
                  y0 + fh * 0.78, fill="#F42A41")


def _olive(b, x0, y0, x1, y1, col="#5B8C4A"):
    b.line([(x0, y0), (x1, y1)], fill=col, width=max(2, int(b.S(2))))
    for i in range(1, 5):
        t = i / 5
        lx, ly = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
        b.ellipse(lx - 5, ly - 8, lx + 1, ly - 1, fill=col)
        b.ellipse(lx + 1, ly + 1, lx + 7, ly + 8, fill=col)


def illo_summit(d, x, y, w, h):
    b = Box(d, x, y, w, h)
    for i, kind in enumerate(("us", "cn", "ru")):
        fx = 28 + i * 52
        b.rect(fx - 1, 8, fx + 1, 52, fill="#6B5D4A")
        _flag(b, fx + 1, 10, 30, 20, kind)
    _olive(b, 40, 62, 78, 48)
    _olive(b, 148, 62, 110, 48)


def illo_peltola(d, x, y, w, h):
    b = Box(d, x, y, w, h)
    b.rect(18, 30, 62, 60, fill="#2F5DA8")          # ballot box
    b.rect(14, 26, 66, 31, fill="#24497F")
    b.rect(32, 22, 48, 27, fill="#F5F0DC")          # slip
    b.line([(36, 25), (40, 28), (46, 20)], fill="#2E7D4F",
           width=max(2, int(b.S(2))))
    b.rect(84, 16, 84 + 66, 28, fill="#2F5DA8")     # 144,302
    b.rect(84, 34, 84 + 58, 46, fill="#C0392B")     # 131,844
    _burst(b, 168, 12, 7, col="#E9B949")
    b.ellipse(84, 52, 92, 60, fill="#2E7D4F")
    b.ellipse(100, 52, 108, 60, fill="#2E7D4F")


def illo_drones(d, x, y, w, h):
    b = Box(d, x, y, w, h)
    b.line([(10, 62), (60, 48), (120, 56), (180, 44)], fill="#5A5A5A",
           width=max(1, int(b.S(1))))
    # power pylon
    b.line([(94, 20), (94, 64)], fill="#3A3A3A", width=max(2, int(b.S(2))))
    b.line([(80, 28), (108, 28)], fill="#3A3A3A", width=max(2, int(b.S(2))))
    b.line([(86, 36), (102, 36)], fill="#3A3A3A", width=max(2, int(b.S(2))))
    b.line([(80, 28), (94, 64)], fill="#3A3A3A", width=max(1, int(b.S(1))))
    b.line([(108, 28), (94, 64)], fill="#3A3A3A", width=max(1, int(b.S(1))))
    b.line([(86, 36), (94, 20)], fill="#3A3A3A", width=max(1, int(b.S(1))))
    b.line([(102, 36), (94, 20)], fill="#3A3A3A", width=max(1, int(b.S(1))))
    _drone(b, 30, 14, 7)
    _drone(b, 58, 8, 6)
    _drone(b, 132, 10, 7)
    _drone(b, 162, 18, 6)
    _burst(b, 148, 30, 8)


def illo_gaza(d, x, y, w, h):
    b = Box(d, x, y, w, h)
    b.rect(96, 8, 168, 60, fill="#FFFFFF", outline="#9AA7B8")  # document
    b.poly([(168, 8), (158, 18), (168, 18)], fill="#C7D2DE")
    b.rect(96, 8, 168, 15, fill="#2F5DA8")
    for i, ly in enumerate((24, 32, 40, 48)):
        b.rect(104, ly, 160 if i < 3 else 138, ly + 3, fill="#B9C2CC")
    b.ellipse(16, 22, 34, 40, fill="#2F5DA8")       # seal
    b.ellipse(20, 26, 30, 36, fill="#FFFFFF")
    _olive(b, 30, 60, 84, 30)
    _olive(b, 60, 62, 92, 44)


def illo_cyclone(d, x, y, w, h):
    b = Box(d, x, y, w, h)
    b.rect(0, 0, 188, 68, fill="#BFD9E8")           # sea
    b.poly([(8, 4), (52, 4), (58, 20), (44, 40), (34, 62), (18, 62),
            (10, 40), (4, 18)], fill="#E8D9B0")     # India peninsula
    b.poly([(52, 4), (70, 4), (66, 16), (58, 20)], fill="#E8D9B0")
    for r, a0 in ((26, 20), (19, 110), (12, 200)):  # spiral
        b.arc((128 - r, 26 - r, 128 + r, 26 + r), a0, a0 + 230,
              fill="#1F3A5F", width=max(2, int(b.S(2))))
    b.ellipse(124, 22, 132, 30, fill="#1F3A5F")
    for dx, dy in ((150, 48), (162, 56), (140, 58), (172, 46)):
        b.poly([(dx, dy), (dx - 3, dy + 7), (dx + 3, dy + 7)], fill="#2F5DA8")


def illo_inflation(d, x, y, w, h):
    b = Box(d, x, y, w, h)
    b.rect(16, 14, 52, 62, fill="#22262B")          # pump
    b.rect(22, 20, 46, 30, fill="#DCE8F5")
    b.rect(26, 34, 42, 38, fill="#C0392B")
    b.line([(52, 18), (62, 26), (62, 48)], fill="#22262B",
           width=max(2, int(b.S(2))))
    b.rect(58, 46, 70, 56, fill="#22262B")
    for i, bh in enumerate((14, 24, 36)):           # rising bars
        bx = 92 + i * 22
        b.rect(bx, 58 - bh, bx + 14, 58, fill="#2F5DA8")
    b.line([(88, 52), (112, 34), (134, 22), (160, 8)], fill="#C0392B",
           width=max(3, int(b.S(3))))
    b.poly([(160, 8), (146, 10), (156, 20)], fill="#C0392B")


def illo_sudan(d, x, y, w, h):
    b = Box(d, x, y, w, h)
    b.poly([(52, 10), (92, 8), (108, 22), (100, 44), (84, 60), (58, 58),
            (48, 36), (44, 20)], fill="#E3CFA3")    # Sudan outline
    b.ellipse(66, 26, 74, 34, fill="#C0392B")       # El Obeid dot
    b.rect(120, 14, 176, 56, fill="#FFFFFF", outline="#9AA7B8")
    for ly in (24, 32, 40, 48):
        b.rect(128, ly, 168, ly + 3, fill="#B9C2CC")
    b.ellipse(128, 8, 160, 40, outline="#2B2B2B",
              width=max(3, int(b.S(3))))            # magnifier
    b.line([(154, 34), (172, 52)], fill="#2B2B2B",
           width=max(3, int(b.S(3))))


def illo_gta(d, x, y, w, h):
    b = Box(d, x, y, w, h)
    b.rect(14, 20, 106, 56, fill="#23283B")         # controller
    b.ellipse(14, 20, 34, 40, fill="#23283B")
    b.ellipse(86, 20, 106, 40, fill="#23283B")
    b.rect(30, 34, 38, 50, fill="#E8E8E8")          # d-pad
    b.rect(24, 40, 44, 44, fill="#E8E8E8")
    for cx, cy, col in ((76, 34, "#E9B949"), (86, 40, "#C0392B"),
                        (66, 40, "#2E7D4F"), (76, 46, "#2F5DA8")):
        b.ellipse(cx - 4, cy - 4, cx + 4, cy + 4, fill=col)
    b.ellipse(136, 12, 176, 52, fill="#FFFFFF", outline="#23283B",
              width=max(2, int(b.S(2))))            # clock
    b.line([(156, 32), (156, 18)], fill="#23283B",
           width=max(2, int(b.S(2))))
    b.line([(156, 32), (166, 32)], fill="#23283B",
           width=max(2, int(b.S(2))))
    b.ellipse(153, 29, 159, 35, fill="#23283B")


def illo_antibiotic(d, x, y, w, h):
    b = Box(d, x, y, w, h)
    b.poly([(30, 22), (74, 40), (66, 54), (22, 36)], fill="#2F5DA8")
    b.poly([(74, 40), (82, 44), (76, 58), (66, 54)], fill="#2F5DA8")
    b.poly([(22, 36), (30, 22), (38, 26), (32, 40)], fill="#E8E8E8")
    for cx, cy, ang in ((120, 22, 20), (146, 34, -15), (128, 50, 35)):
        b.ellipse(cx - 12, cy - 5, cx + 12, cy + 5, fill="#5B8C4A")
        for dx in (-7, 0, 7):
            b.ellipse(cx + dx - 1, cy - 1, cx + dx + 1, cy + 1,
                      fill="#2F5D33")
    b.line([(164, 56), (164, 18)], fill="#2F5DA8",
           width=max(3, int(b.S(3))))
    b.poly([(164, 10), (156, 22), (172, 22)], fill="#2F5DA8")


def illo_climate(d, x, y, w, h):
    b = Box(d, x, y, w, h)
    b.ellipse(18, 10, 66, 58, fill="#7FB3D5")       # globe
    b.poly([(28, 22), (40, 16), (48, 24), (40, 32), (28, 30)], fill="#5B8C4A")
    b.poly([(44, 38), (56, 34), (58, 46), (48, 50), (42, 44)], fill="#5B8C4A")
    b.ellipse(30, 44, 38, 52, fill="#5B8C4A")
    _burst(b, 78, 14, 7, col="#F2C200")
    b.rect(120, 12, 132, 52, fill="#FFFFFF", outline="#6B5D4A",
           width=max(2, int(b.S(2))))               # thermometer
    b.ellipse(112, 48, 140, 64, fill="#7B4BA6")
    b.rect(123, 30, 129, 52, fill="#7B4BA6")
    b.line([(146, 20), (146, 44)], fill="#9AA7B8",
           width=max(1, int(b.S(1))))
    for ly in (20, 28, 36, 44):
        b.line([(146, ly), (150, ly)], fill="#9AA7B8",
               width=max(1, int(b.S(1))))


def illo_garment(d, x, y, w, h):
    b = Box(d, x, y, w, h)
    b.rect(12, 52, 92, 58, fill="#232323")          # machine base
    b.rect(18, 22, 30, 52, fill="#232323")          # column
    b.rect(18, 14, 78, 24, fill="#232323")          # arm
    b.rect(72, 24, 76, 40, fill="#C8C8C8")          # needle bar
    b.poly([(70, 40), (78, 40), (74, 50)], fill="#C8C8C8")
    b.rect(108, 12, 176, 58, fill="#8A6D3B")        # shutter
    for ly in range(18, 56, 7):
        b.rect(108, ly, 176, ly + 3, fill="#5D4726")
    b.rect(136, 30, 148, 46, fill="#E9B949", outline="#7A6218")
    _flag(b, 156, 2, 22, 12, "bd")


def illo_sanctions(d, x, y, w, h):
    b = Box(d, x, y, w, h)
    for hx in (16, 66, 116):                        # houses
        b.poly([(hx, 40), (hx + 18, 26), (hx + 36, 40)], fill="#8A2F26")
        b.rect(hx + 4, 40, hx + 32, 58, fill="#E8D9B0")
        b.rect(hx + 14, 46, hx + 22, 58, fill="#5D4726")
    b.ellipse(84, 6, 106, 28, outline="#8A6D3B",
              width=max(3, int(b.S(3))))            # padlock shackle
    b.rect(74, 26, 116, 54, fill="#C99327")         # padlock body
    b.rect(88, 34, 102, 48, fill="#5D4726")
    b.ellipse(91, 36, 99, 44, fill="#E8D9B0")


ILLUSTRATIONS = {
    "gulf": illo_gulf, "summit": illo_summit, "peltola": illo_peltola,
    "drones": illo_drones, "gaza": illo_gaza, "cyclone": illo_cyclone,
    "inflation": illo_inflation, "sudan": illo_sudan, "gta": illo_gta,
    "antibiotic": illo_antibiotic, "climate": illo_climate,
    "garment": illo_garment, "sanctions": illo_sanctions,
}

# ---------------------------------------------------------------- map
# Coarse continent outlines in (lon, lat); projected equirectangularly
# into the map box. Schematic only — the reference map is the same kind
# of simplified outline.

NA = [(-168, 66), (-158, 58), (-140, 60), (-130, 54), (-125, 49),
      (-124, 42), (-120, 34), (-114, 29), (-110, 24), (-105, 20),
      (-97, 16), (-92, 15), (-86, 12), (-83, 9), (-79, 9), (-81, 13),
      (-84, 16), (-87, 21), (-90, 21), (-91, 19), (-96, 19), (-97, 26),
      (-93, 30), (-89, 30), (-84, 30), (-81, 25), (-80, 32), (-76, 35),
      (-75, 39), (-74, 40), (-70, 42), (-68, 45), (-65, 44), (-60, 47),
      (-55, 47), (-60, 52), (-65, 55), (-68, 58), (-72, 62), (-78, 62),
      (-85, 66), (-92, 66), (-95, 69), (-110, 68), (-125, 70), (-140, 70),
      (-155, 71), (-165, 68)]
GREENLAND = [(-58, 64), (-52, 60), (-43, 60), (-40, 64), (-32, 68),
             (-22, 70), (-20, 74), (-30, 76), (-45, 76), (-58, 74),
             (-62, 70)]
SA = [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
      (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-70, -50),
      (-68, -55), (-65, -55), (-68, -50), (-62, -41), (-58, -34),
      (-52, -32), (-48, -28), (-41, -23), (-39, -17), (-35, -9),
      (-35, -6), (-40, -3), (-44, -2), (-50, 0), (-53, 4), (-58, 6),
      (-62, 9), (-68, 11), (-72, 12), (-75, 11), (-77, 8)]
AFRICA = [(-6, 35), (-10, 31), (-15, 27), (-17, 21), (-17, 15), (-15, 11),
          (-12, 8), (-8, 4), (-4, 5), (2, 6), (6, 4), (9, 4), (9, 0),
          (12, -5), (13, -10), (12, -17), (14, -22), (16, -28), (19, -34),
          (25, -34), (28, -32), (32, -28), (35, -24), (40, -15),
          (40, -10), (42, -4), (46, -1), (51, 2), (51, 11), (48, 11),
          (44, 11), (43, 12), (40, 15), (38, 18), (37, 22), (35, 28),
          (34, 31), (32, 31), (30, 32), (25, 32), (20, 32), (15, 33),
          (11, 34), (10, 37), (5, 37), (0, 36)]
EURASIA = [(-10, 37), (-9, 43), (-2, 44), (-1, 46), (-4, 48), (-2, 49),
           (0, 51), (3, 53), (7, 54), (8, 57), (10, 59), (5, 60), (5, 62),
           (12, 64), (18, 69), (25, 71), (30, 70), (35, 68), (42, 68),
           (48, 68), (55, 68), (62, 69), (68, 73), (75, 73), (85, 75),
           (95, 76), (105, 77), (115, 74), (125, 73), (135, 72), (145, 72),
           (155, 71), (165, 70), (170, 67), (178, 65), (170, 60),
           (162, 56), (158, 52), (155, 59), (150, 60), (142, 59),
           (140, 53), (142, 50), (140, 46), (138, 43), (135, 43),
           (132, 43), (130, 42), (127, 40), (126, 38), (122, 39),
           (120, 35), (122, 31), (121, 28), (118, 25), (112, 22),
           (109, 18), (108, 12), (105, 9), (103, 7), (100, 6), (98, 10),
           (97, 15), (94, 17), (92, 21), (90, 22), (88, 22), (86, 20),
           (82, 17), (80, 13), (77, 8), (76, 10), (73, 16), (70, 20),
           (66, 25), (62, 25), (58, 25), (57, 27), (54, 27), (52, 28),
           (50, 29), (48, 30), (44, 29), (43, 27), (40, 28), (38, 24),
           (35, 29), (34, 31), (36, 36), (30, 36), (27, 37), (23, 36),
           (22, 37), (19, 40), (16, 38), (15, 40), (12, 42), (8, 44),
           (7, 44), (3, 43), (0, 40), (-2, 37), (-6, 36), (-9, 37)]
AUSTRALIA = [(113, -22), (114, -30), (115, -35), (118, -35), (124, -33),
             (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
             (145, -38), (150, -37), (153, -32), (153, -27), (150, -23),
             (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
             (132, -12), (130, -13), (126, -14), (122, -17), (118, -20)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (-2, 51)]
MADAGASCAR = [(44, -16), (47, -15), (50, -16), (49, -20), (45, -25),
              (43, -21)]
# Small islands drawn as ellipses: (lon, lat, rx_deg, ry_deg).
ISLANDS = [(139, 37, 2.2, 3.5), (140, 40, 1.8, 3.0), (100, 0, 3.0, 1.6),
           (112, -7, 3.5, 1.4), (114, 0, 3.0, 2.2), (120, -2, 2.2, 2.0),
           (138, -4, 4.0, 2.0), (172, -41, 1.8, 3.0), (168, -45, 1.4, 2.4)]

# Map box.
MX0, MY0, MW, MH = 26, 776, 320, 138
SEA = "#E7EDEF"
LAND = "#EFE7D2"
LAND_LINE = "#CFC6A6"
GRAT = "#DCD5BE"


def project(lon, lat):
    return (MX0 + (lon + 170) / 360.0 * MW,
            MY0 + (78 - lat) / 136.0 * MH)


def draw_map(d):
    d.rectangle([MX0, MY0, MX0 + MW - 1, MY0 + MH - 1], fill=SEA,
                outline="#B9B29A")
    for lon in range(-150, 181, 30):                 # graticule
        x = MX0 + (lon + 170) / 360.0 * MW
        d.line([(x, MY0), (x, MY0 + MH - 1)], fill=GRAT)
    for lat in range(60, -31, -30):
        y = MY0 + (78 - lat) / 136.0 * MH
        d.line([(MX0, y), (MX0 + MW - 1, y)], fill=GRAT)
    for poly in (NA, GREENLAND, SA, AFRICA, EURASIA, AUSTRALIA, UK,
                 MADAGASCAR):
        d.polygon([project(lon, lat) for lon, lat in poly], fill=LAND,
                  outline=LAND_LINE)
    for lon, lat, rx, ry in ISLANDS:
        cx, cy = project(lon, lat)
        rxp = rx / 360.0 * MW
        ryp = ry / 136.0 * MH
        d.ellipse([cx - rxp, cy - ryp, cx + rxp, cy + ryp], fill=LAND,
                  outline=LAND_LINE)


# (story number, lon, lat, badge offset dx, dy from the true spot)
PINS = [
    (1, 48, 29, 16, -2), (2, 114, 22.5, 10, 8), (3, -150, 64, 0, 0),
    (4, 31, 50, 12, -10), (5, 34.5, 31.5, -12, 6), (6, 88, 15, 8, 10),
    (7, -0.1, 51.5, -12, -8), (8, 30.2, 13.2, -12, 8), (9, 172, -41, 0, 0),
    (10, 18, 59, -8, -10), (11, 33, 40, 12, 2), (12, 90.4, 23.8, 12, -6),
    (13, 149, -35, 0, 0),
]
# Unnumbered dots for briefs: (lon, lat, region).
DOTS = [
    (13.4, 52.5, "EUROPE"), (139.7, 35.7, "ASIA"), (127, 37.5, "ASIA"),
    (103.8, 1.35, "ASIA"), (100.5, 13.75, "ASIA"), (-160, -21, "OCEANIA"),
    (-75.7, 45.4, "AMERICAS"), (-77, -12, "AMERICAS"),
    (-84.5, 39.1, "AMERICAS"), (-100.3, 25.7, "AMERICAS"),
    (-118.2, 34, "AMERICAS"), (-58.4, -34.6, "AMERICAS"),
    (-77, 38.9, "AMERICAS"), (28, -26, "AFRICA"), (30.5, 18.2, "AFRICA"),
]


def draw_pins(d):
    for lon, lat, region in DOTS:
        x, y = project(lon, lat)
        col = REGION_COLORS[region]
        d.ellipse([x - 2.5, y - 2.5, x + 2.5, y + 2.5], fill=col)
    nf = F(SANS_B, 9)
    for num, lon, lat, dx, dy in PINS:
        tx, ty = project(lon, lat)
        region = FEATURED[num - 1][1]
        col = REGION_COLORS[region]
        bx, by = tx + dx, ty + dy
        if dx or dy:
            d.ellipse([tx - 2.5, ty - 2.5, tx + 2.5, ty + 2.5], fill=col)
            d.line([(tx, ty), (bx, by)], fill="#8A8272", width=1)
        d.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=col,
                  outline="white")
        label = str(num)
        tw = nf.getlength(label)
        d.text((bx - tw / 2, by - 5), label, font=nf, fill="white")


def draw_legend(d, y):
    """Region legend + pin/dot note, under the map."""
    f = F(SANS, 10)
    x = MX0
    for i, region in enumerate(REGION_ORDER):
        if i == 4:
            y += 14
            x = MX0
        col = REGION_COLORS[region]
        d.ellipse([x, y + 1, x + 8, y + 9], fill=col)
        d.text((x + 12, y), region.capitalize(), font=f, fill=INK)
        x += 12 + f.getlength(region.capitalize()) + 12
    nf = F(SANS, 9)
    d.text((MX0, y + 16), "\u25cf numbered pin: stories 1\u201313 above"
                          "   \u2022   dot: briefs 14\u201345",
           font=nf, fill="#6B6558")
    d.text((MX0, y + 28), "Hairlines lead from crowded spots to the true place.",
           font=nf, fill="#6B6558")


# ---------------------------------------------------------------- cards

def draw_card(d, x, y, w, h, story, big):
    num, region, topic, headline, deck, tint, illo = story
    col = REGION_COLORS[region]
    d.rectangle([x, y, x + w - 1, y + h - 1], fill=CARD, outline=BORDER)
    d.rectangle([x, y, x + w - 1, y + 2], fill=col)
    illo_h = 84 if big else 60
    d.rectangle([x, y + 3, x + w - 1, y + 3 + illo_h - 1], fill=tint)
    ILLUSTRATIONS[illo](d, x, y + 3, w, illo_h)
    cy = y + 3 + illo_h + 6
    diam = 14 if big else 12
    d.ellipse([x + 3, cy, x + 3 + diam - 1, cy + diam - 1], fill=col)
    nf = F(SANS_B, 9 if big else 8)
    label = str(num)
    tw = nf.getlength(label)
    d.text((x + 3 + (diam - tw) / 2, cy + (diam - 9) / 2 - 1), label,
           font=nf, fill="white")
    cf = F(SANS_B, 11 if big else 10)
    d.text((x + 3 + diam + 5, cy + 1), f"{region} \u00b7 {topic}", font=cf,
           fill=col)
    hy = cy + diam + 5
    head_size, head_lead = (19, 22) if big else (15, 17)
    hf = F(SERIF_B, head_size)
    hlines = wrap(headline, hf, w - 8)
    for i, ln in enumerate(hlines):
        d.text((x + 4, hy + i * head_lead), ln, font=hf, fill=INK)
    dy = hy + len(hlines) * head_lead + 3
    deck_size, deck_lead = (12, 15) if big else (11, 12)
    df = F(SANS, deck_size)
    max_deck = max(1, (y + h - 4 - dy) // deck_lead)
    full = wrap(deck, df, w - 8)
    if len(full) > max_deck:
        raise SystemExit(f"deck truncated: story {num} needs "
                         f"{len(full)} lines, fits {max_deck}")
    dlines = full[:max_deck]
    for i, ln in enumerate(dlines):
        d.text((x + 4, dy + i * deck_lead), ln, font=df, fill=DECK)


# ---------------------------------------------------------------- briefs

def draw_brief(d, x, y, num, text, col_w):
    idx = text.index(": ")
    place, rest = text[:idx + 1], text[idx + 1:]
    num_txt = f"{num} "
    for size in (11, 10, 9, 8):
        nf, bf, rf = F(SANS_B, size), F(SANS_B, size), F(SANS, size)
        if (nf.getlength(num_txt) + bf.getlength(place)
                + rf.getlength(rest)) <= col_w:
            break
    cx = x
    d.text((cx, y), num_txt, font=nf, fill=RED)
    cx += nf.getlength(num_txt)
    d.text((cx, y), place, font=bf, fill=INK)
    cx += bf.getlength(place)
    d.text((cx, y), rest, font=rf, fill=INK)


# ---------------------------------------------------------------- page

def compose():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Kicker.
    kf = F(SANS_B, 13)
    draw_tracked(d, M, 14, "THE DAY IN WORLD NEWS", kf, RED, tracking=2)
    right = "45 STORIES \u2022 6 CONTINENTS \u2022 ONE DAY"
    draw_tracked(d, W - M - tracked_width(right, kf, 2), 14, right, kf,
                 INK, tracking=2)

    # Masthead + colour bar + rule.
    mf = fit_font(MASTHEAD, "Wednesday 18 November 2026", 64, 48, CW)
    d.text((M, 32), "Wednesday 18 November 2026", font=mf, fill=INK)
    seg_w = CW / 7.0
    for i, region in enumerate(REGION_ORDER):
        x0 = M + int(i * seg_w)
        x1 = M + int((i + 1) * seg_w) - 1
        d.rectangle([x0, 96, x1, 101], fill=REGION_COLORS[region])
    d.line([(M, 106), (W - M, 106)], fill=RULE)

    # Featured rows: 3 large, then 5 + 5.
    row1_y, row1_h = 114, 210
    xs1, ws1 = [26, 353, 680], [317, 317, 318]
    for i in range(3):
        draw_card(d, xs1[i], row1_y, ws1[i], row1_h, FEATURED[i], big=True)
    row2_y, row2_h = 330, 204
    xs2 = [26, 222, 418, 614, 810]
    for i in range(5):
        draw_card(d, xs2[i], row2_y, 188, row2_h, FEATURED[3 + i],
                  big=False)
    row3_y, row3_h = 540, 204
    for i in range(5):
        draw_card(d, xs2[i], row3_y, 188, row3_h, FEATURED[8 + i],
                  big=False)

    # Section headers + rule.
    hf = F(SANS_B, 13)
    draw_tracked(d, M, 750, "WHERE IT HAPPENED", hf, INK, tracking=1)
    draw_tracked(d, 358, 750, "ALSO ON WEDNESDAY 18 NOVEMBER", hf, INK,
                 tracking=1)
    d.line([(M, 770), (W - M, 770)], fill=RULE)

    # Map + pins + legend.
    draw_map(d)
    draw_pins(d)
    draw_legend(d, 918)

    # Briefs: two columns of 16, one line each.
    bx0, bx1 = 358, 685
    col_w = 313
    for i, (num, text) in enumerate(BRIEFS):
        col = 0 if i < 16 else 1
        row = i if i < 16 else i - 16
        draw_brief(d, bx0 if col == 0 else bx1, MY0 + row * 12, num, text,
                   col_w)

    # Footer.
    ff = F(SANS, 10)
    foot = ("Every story was reported on Wednesday 18 November 2026; "
            "disputed claims are attributed. Sources: Reuters, AP, AFP, "
            "BBC, Al Jazeera and others. Original drawings.")
    d.text(((W - ff.getlength(foot)) / 2, 984), foot, font=ff, fill="#6B6558")
    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "entry.png")
    img = compose()
    img.save(out, optimize=True)
    size = os.path.getsize(out)
    if size > 1024 * 1024:
        img.save(out, format="JPEG", quality=88, optimize=True)
        size = os.path.getsize(out)
    print(f"entry.png: {size} bytes ({size / 1024:.1f} KiB), "
          f"{img.size[0]}x{img.size[1]}")
    assert size <= 1024 * 1024, "entry.png exceeds 1 MiB"
    assert len(FEATURED) + len(BRIEFS) == 45, "story count != 45"


if __name__ == "__main__":
    main()
