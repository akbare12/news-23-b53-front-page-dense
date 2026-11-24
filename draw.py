"""news-23 b53 front-page-dense: draw THE WORLD TODAY, Monday 23 November 2026.
1024x1024 front page, 31 stories. PIL only in draw.py; main.py is stdlib-only.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FD = "/usr/share/fonts/truetype/dejavu/"

def font(name, size):
    return ImageFont.truetype(FD + name, size)

SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (212, 175, 55)
RED = (178, 34, 34)
DARKRED = (139, 0, 0)
TEAL = (0, 128, 128)
NAVY = (16, 42, 90)
CREAM = (250, 246, 230)
LIGHTGREY = (238, 238, 238)
GREY = (120, 120, 120)
DARKGREY = (70, 70, 70)
GREEN = (46, 139, 87)
PURPLE = (107, 63, 160)
ORANGE = (204, 119, 34)

def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def chip(draw, x, y, text, fill):
    f = SANS_B(9)
    w = draw.textlength(text, font=f) + 8
    draw.rounded_rectangle([x, y, x + w, y + 13], radius=2, fill=fill)
    draw.text((x + 4, y + 2), text, font=f, fill=WHITE)
    return w

img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)

# ---------- masthead ----------
d.rectangle([0, 0, W, 48], fill=BLACK)
d.text((12, 7), "THE WORLD TODAY", font=SERIF_B(33), fill=WHITE)
d.text((W - 12 - d.textlength("MONDAY 23 NOVEMBER 2026", font=SANS_B(19)), 13),
       "MONDAY 23 NOVEMBER 2026", font=SANS_B(19), fill=GOLD)

# ---------- kicker ----------
d.text((12, 50), "AI rout hits Asia  ·  UN chief urges AI rules  ·  US lead over China at record low  ·  Anthropic IPO $107.3B",
       font=SANS_B(13), fill=RED)

# ---------- number strip: 2 rows x 5 cols ----------
nums = [
    ("-3.3%", "KOSPI", RED), ("5.3", "US-CHINA POWER GAP", NAVY),
    ("11,762", "EBOLA CASES, DRC", GREEN), ("10T won", "SEOUL STABILISATION FUND", ORANGE),
    ("2%", "BILLIONAIRE TAX IN PARIS", PURPLE),
    ("$450M", "SKUBAL DEAL", PURPLE), ("165", "RUSSIAN MISSILES IN A WEEK", RED),
    ("12,000", "CLEARED IN MANCHESTER", NAVY), ("264 kg", "EXPLOSIVES SEIZED IN LEBANON", ORANGE),
    ("$107.3B", "ANTHROPIC IPO — LARGEST", PURPLE),
]
cell_w = (W - 24) // 5
for i, (val, lab, col) in enumerate(nums):
    row, c = divmod(i, 5)
    x = 12 + c * cell_w
    y = 66 + row * 23
    d.text((x, y), val, font=SANS_B(18), fill=col)
    d.text((x, y + 16), lab, font=SANS_B(8), fill=DARKGREY)

# ---------- region bar ----------
regions = [("ASIA-PACIFIC 7", TEAL, 200), ("AMERICAS 8", NAVY, 205),
           ("MIDDLE EAST 6", ORANGE, 195), ("EUROPE 5", PURPLE, 155),
           ("AFRICA 3", RED, 130), ("WORLD 2", (90, 90, 90), 115)]
x = 0
for name, col, wdt in regions:
    d.rectangle([x, 122, x + wdt, 140], fill=col)
    d.text((x + 6, 127), name, font=SANS_B(11), fill=WHITE)
    x += wdt
# total = 1000; pad remainder
d.rectangle([x, 122, W, 140], fill=(90, 90, 90))

# ---------- UTC strip ----------
d.rectangle([0, 141, W, 157], fill=BLACK)
d.text((8, 145), "THE DAY IN UTC   ~00:00 Kospi dives   ~06:30 Guterres opens   ~09:00 Power Index   ~12:00 Paris 2% tax   ~15:00 Kyiv missiles   ~18:00 IPO $97.17",
       font=SANS(10), fill=WHITE)
d.text((W - 8 - d.textlength("~ APPROX", font=SANS(10)), 145), "~ APPROX", font=SANS(10), fill=GOLD)

# ---------- hero scenes ----------
# scene 1: Kospi chart
sx, sy, sw, sh = 8, 160, 330, 138
d.rectangle([sx, sy, sx + sw, sy + sh], fill=(10, 20, 50))
d.text((sx + 8, sy + 6), "-3.3%", font=SANS_B(30), fill=(255, 80, 60))
pts = [(sx + 10, sy + 78), (sx + 45, sy + 66), (sx + 80, sy + 74), (sx + 115, sy + 58),
       (sx + 150, sy + 68), (sx + 185, sy + 52), (sx + 220, sy + 62), (sx + 255, sy + 48),
       (sx + 290, sy + 56), (sx + 320, sy + 44)]
d.line(pts, fill=(255, 140, 60), width=2)
for px, py in pts:
    d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=GOLD)
# skyline
import random
random.seed(23)
bx = sx + 6
while bx < sx + sw - 14:
    bw = random.randint(14, 26)
    bh = random.randint(18, 40)
    d.rectangle([bx, sy + sh - 16 - bh, bx + bw, sy + sh - 16], fill=(25, 45, 80))
    for wy in range(sy + sh - 14 - bh + 3, sy + sh - 18, 8):
        for wx in range(bx + 3, bx + bw - 3, 7):
            if random.random() < 0.5:
                d.rectangle([wx, wy, wx + 3, wy + 4], fill=GOLD)
    bx += bw + 3
d.rectangle([sx, sy + sh - 16, sx + sw, sy + sh], fill=BLACK)
d.text((sx + 6, sy + sh - 14), "KOSPI 4,708.54  ·  -161 PTS", font=SANS_B(10), fill=WHITE)

# scene 2: Guterres
sx2 = 346
d.rectangle([sx2, sy, sx2 + sw, sy + sh], fill=TEAL)
d.text((sx2 + 10, sy + 8), "150 DELEGATES", font=SANS_B(26), fill=GOLD)
d.text((sx2 + 10, sy + 38), "BACK A RISK", font=SANS_B(26), fill=WHITE)
d.text((sx2 + 10, sy + 68), "FRAMEWORK", font=SANS_B(26), fill=WHITE)
# globe
cx, cy, r = sx2 + sw - 52, sy + 100, 34
d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE, width=2)
d.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r], outline=WHITE, width=1)
d.line([cx - r, cy, cx + r, cy], fill=WHITE, width=1)
d.arc([cx - r, cy - r // 2, cx + r, cy + r // 2], 0, 360, fill=WHITE, width=1)
d.rectangle([sx2, sy + sh - 16, sx2 + sw, sy + sh], fill=BLACK)
d.text((sx2 + 6, sy + sh - 14), "UN  ·  BRIDGETOWN", font=SANS_B(10), fill=WHITE)

# scene 3: Power index bars
sx3 = 684
d.rectangle([sx3, sy, sx3 + sw, sy + sh], fill=CREAM)
d.text((sx3 + 10, sy + 6), "NARROWEST SINCE 2018", font=SANS_B(12), fill=BLACK)
d.text((sx3 + sw - 10 - d.textlength("GAP 5.3", font=SANS_B(12)), sy + 6), "GAP 5.3", font=SANS_B(12), fill=(150, 110, 0))
bars = [("US", 78.9, NAVY, 40), ("CHINA", 73.6, RED, 140), ("INDIA", 40.5, (190, 150, 40), 240)]
base = sy + sh - 18
for name, val, col, bx in bars:
    bh = int(val * 0.95)
    d.rectangle([sx3 + bx, base - bh, sx3 + bx + 70, base], fill=col)
    d.text((sx3 + bx + 8, base - bh - 16), str(val), font=SANS_B(14), fill=BLACK)
    d.text((sx3 + bx + 10, base - 16), name, font=SANS_B(11), fill=WHITE)
d.rectangle([sx3, sy + sh - 16, sx3 + sw, sy + sh], fill=BLACK)
d.text((sx3 + 6, sy + sh - 14), "ASIA POWER INDEX 2026", font=SANS_B(10), fill=WHITE)

# ---------- hero headlines (gap below scene caption strips) ----------
heroes = [
    (8, "1", "AI ROUT HITS ASIA",
     "Kospi closes -3.3% to 4,708.54, sheds 161 pts; intraday -5.8%. Samsung -3.1%, SK Hynix -2.5%.",
     "KOREA EXCHANGE"),
    (346, "2", "GUTERRES: REGULATE AI BEFORE IT'S TOO LATE",
     "UN chief urges global AI safety rules at the Bridgetown summit; 150 delegates back a risk framework.",
     "UNITED NATIONS"),
    (684, "3", "US LEAD OVER CHINA AT RECORD LOW",
     "Asia Power Index 2026: US 78.9, China 73.6 — gap 5.3, narrowest since 2018. India third at 40.5.",
     "LOWY INSTITUTE"),
]
for hx, num, head, body, src in heroes:
    # red number circle
    d.ellipse([hx, 306, hx + 20, 326], fill=RED)
    d.text((hx + 6, 309), num, font=SANS_B(12), fill=WHITE)
    lines = wrap(d, head, SANS_B(17), sw - 26)
    y = 304
    for ln in lines[:2]:
        d.text((hx + 26, y), ln, font=SANS_B(17), fill=BLACK)
        y += 20
    by = 348
    for ln in wrap(d, body, SANS(11), sw - 6)[:2]:
        d.text((hx, by), ln, font=SANS(11), fill=DARKGREY)
        by += 14
    d.text((hx, 376), src, font=SANS(9), fill=GREY)
    chip(d, hx + sw - 78, 374, "REPORTED", NAVY)

# ---------- MORE OF THE DAY bar ----------
d.rectangle([0, 394, W, 412], fill=BLACK)
d.text((8, 398), "MORE OF THE DAY  —  10 STORIES", font=SANS_B(12), fill=WHITE)

# ---------- 10 cards: 5 cols x 2 rows ----------
cards = [
    ("AMERICAS", TEAL, "BESSENT: NVIDIA ANSWERS", "Treasury chief wants China answers.", "Reuters", "REPORTED"),
    ("FBI", RED, "FBI PROBES NCIC HACK", "Hackers hit police NCIC database.", "AP", "REPORTED"),
    ("WHITE HOUSE", ORANGE, "TRUMP: IRAN STRIKES MAY RESUME", "Strikes may resume in New Year.", "Reuters", "REPORTED"),
    ("MARKETS", NAVY, "US FUTURES JUMP 3%", "Holiday rally lifts futures 3%.", "Bloomberg", "REPORTED"),
    ("SPORT", DARKRED, "SKUBAL'S $450M METS DEAL", "Nine-year deal, largest ever.", "AP", "REPORTED"),
    ("SPORT", DARKRED, "TOM JACKSON DIES AT 75", "Broncos LB, ESPN voice, dies.", "ESPN", "REPORTED"),
    ("LEGAL", PURPLE, "STATES SUE SPACEX", "Ten states challenge AI claims.", "AP", "REPORTED"),
    ("TECH", TEAL, "ANTHROPIC IPO: $107.3B", "Raised at $83; closes $97.17.", "WSJ", "REPORTED"),
    ("EUROPE", PURPLE, "POLAND: 3 MISSILES CROSSED AIRSPACE", "Kyiv: three Kh-101s crossed.", "AP", "CLAIM"),
    ("SPACE", (90, 90, 90), "RUSSIAN NUCLEAR SATELLITE", "Intel: satellite may carry a nuke.", "Reuters", "CLAIM"),
]
cw = (W - 16) // 5
chh = 62
for i, (cat, col, head, body, src, tag) in enumerate(cards):
    row, c = divmod(i, 5)
    x = 8 + c * cw
    y = 416 + row * (chh + 4)
    d.rectangle([x, y, x + cw - 4, y + 13], fill=col)
    d.text((x + 4, y + 1), cat, font=SANS_B(9), fill=WHITE)
    num = str(i + 1)
    d.text((x + cw - 4 - 12 - d.textlength(num, font=SANS_B(9)), y + 1), num, font=SANS_B(9), fill=WHITE)
    hl = wrap(d, head, SANS_B(10), cw - 12)
    hy = y + 15
    for ln in hl[:2]:
        d.text((x + 2, hy), ln, font=SANS_B(10), fill=BLACK)
        hy += 12
    d.text((x + 2, y + chh - 22), body, font=SANS(10), fill=DARKGREY)
    d.text((x + 2, y + chh - 11), src, font=SANS(9), fill=GREY)
    chip(d, x + cw - 4 - 66, y + chh - 12, tag, NAVY if tag == "REPORTED" else RED)

# ---------- map + ALSO ----------
d.rectangle([0, 548, W, 566], fill=BLACK)
d.text((8, 552), "WHERE IT HAPPENED", font=SANS_B(12), fill=WHITE)
d.text((318, 552), "ALSO ON MONDAY", font=SANS_B(12), fill=WHITE)

# map area
mx, my, mw, mh = 8, 570, 300, 250
d.rectangle([mx, my, mx + mw, my + mh], fill=(235, 242, 235))
for gx in range(mx, mx + mw, 20):
    d.line([gx, my, gx, my + mh], fill=(215, 225, 215), width=1)
for gy in range(my, my + mh, 20):
    d.line([mx, gy, mx + mw, gy], fill=(215, 225, 215), width=1)
# stylised land blobs
d.ellipse([mx + 10, my + 20, mx + 130, my + 130], fill=(150, 200, 140))
d.ellipse([mx + 90, my + 90, mx + 210, my + 200], fill=(150, 200, 140))
d.ellipse([mx + 180, my + 10, mx + 295, my + 110], fill=(150, 200, 140))
d.ellipse([mx + 150, my + 180, mx + 240, my + 245], fill=(150, 200, 140))
pins = [(1, 250, 610), (2, 92, 742), (3, 240, 592), (4, 70, 630), (5, 92, 606),
        (6, 196, 612), (7, 62, 596), (8, 48, 652), (9, 68, 676), (10, 82, 716),
        (11, 176, 578), (12, 192, 586), (13, 208, 572)]
for n, px, py in pins:
    d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=WHITE, width=1)
    d.text((px - 3 if n < 10 else px - 6, py - 6), str(n), font=SANS_B(9), fill=WHITE)
d.text((mx + 2, my + mh - 46), "Pins 1–13: 1 Seoul · 2 Bridgetown · 3 Beijing", font=SANS(9), fill=BLACK)
d.text((mx + 2, my + mh - 34), "4 Washington · 5 New York · 6 Tehran · 7 Chicago", font=SANS(9), fill=BLACK)
d.text((mx + 2, my + mh - 22), "8 SF · 9 Denver · 10 Austin · 11 Warsaw · 12 Kyiv · 13 Moscow", font=SANS(9), fill=BLACK)

# ALSO list, 2 columns x 9
also = [
    "14. Paris: 100+ back 2% billionaire tax",
    "15. Manchester: 12,000 cleared",
    "16. Zelenskyy: 165 missiles in a week",
    "17. COP31: the day after pact rejected",
    "18. Benghazi: UN demands port probe",
    "19. Israel unity talks resume",
    "20. Gaza: two killed in Israeli strike",
    "21. West Bank settler attacks",
    "22. Iran war: no deal in sight",
    "23. Lebanon seizes 264 kg explosives",
    "24. Bahrain: strike hits plant, 2 hurt",
    "25. Sudan: defences down drones",
    "26. DRC: fighting traps Ebola teams",
    "27. Bangladesh: Hasina jailed if she returns",
    "28. Seoul minister quits in exam row",
    "29. SK Telecom -7.3% as hype cools",
    "30. China eases margin rules",
    "31. Seoul readies 10T-won fund",
]
for i, item in enumerate(also):
    col, row = divmod(i, 9)
    x = 318 + col * 352
    y = 572 + row * 27
    d.text((x, y), item, font=SANS(12), fill=BLACK)

# ---------- DATE CHECK ----------
dy = 830
d.rectangle([8, dy, W - 8, dy + 78], outline=RED, width=2)
d.text((14, dy + 4), "DATE CHECK", font=SANS_B(13), fill=RED)
d.text((W - 14 - d.textlength("READ 23 NOV 2026, 23:59 UTC — STORIES DATED 23 NOV ONLY", font=SANS_B(9)), dy + 6),
       "READ 23 NOV 2026, 23:59 UTC — STORIES DATED 23 NOV ONLY", font=SANS_B(9), fill=RED)
left = "LEFT OUT — NOT 23 NOV: Democrats reach 258 seats (22 Nov) · Sparta II fire (22 Nov) · El Chapo Isidro captured (22 Nov) · EU–Indonesia pact (21 Nov) · Nigeria boat (21 Nov) · ICJ Myanmar ruling (19 Nov)"
ly = dy + 24
for ln in wrap(d, left, SANS(11), W - 32)[:2]:
    d.text((14, ly), ln, font=SANS(11), fill=BLACK)
    ly += 15
d.text((14, ly + 2), "NOT YET: Dymer search continues (14 missing) · 4 House races uncalled · COP32 venue not set · WHO evacuating trapped Ebola staff",
       font=SANS(11), fill=BLACK)

# ---------- footer ----------
d.text((8, 916), "Sources: Reuters · AP · Bloomberg · AFP · Yonhap · BBC · WSJ · NYT · ESPN · Lowy Institute (Asia Power Index 2026).", font=SANS(9), fill=GREY)
d.text((8, 930), "CHIPS: REPORTED = confirmed by wires · CLAIM = one side's claim, not independently confirmed · ONGOING = still developing", font=SANS(9), fill=GREY)
d.text((8, 944), "All times UTC. Figures as reported 23 Nov 2026. Scenes are drawn illustrations, not photographs.", font=SANS(9), fill=GREY)

# ---------- bottom bar ----------
d.rectangle([0, 962, W, H], fill=BLACK)
d.text((W // 2 - d.textlength("THE WORLD TODAY  —  Monday 23 November 2026  ·  31 stories  ·  6 regions", font=SANS_B(14)) // 2, 976),
       "THE WORLD TODAY  —  Monday 23 November 2026  ·  31 stories  ·  6 regions", font=SANS_B(14), fill=GOLD)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, "PNG")
print("saved", out, os.path.getsize(out), "bytes")
