#!/usr/bin/env python3
"""Render the 25 November 2026 world-news front page (1024x1024 PNG).

Fresh code written for this entry. Uses Pillow + system DejaVu fonts.
Run: python3 render.py  ->  writes entry.png next to this file.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
NAVY = (15, 42, 74)
NAVY2 = (23, 58, 96)
RED = (178, 34, 34)
INK = (20, 20, 20)
GREY = (90, 90, 88)
RULE = (150, 140, 120)
SKY = (178, 205, 225)
SEA = (46, 92, 128)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIFB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def para(draw, xy, text, fnt, width, fill=INK, leading=None):
    x, y = xy
    lh = leading or int(fnt.size * 1.32)
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def centre(draw, y, text, fnt, fill, cx=W // 2):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size


def draw_sea_scene(d, x0, y0, x1, y1):
    """Flat illustration: two Russian ships hit by Ukrainian sea drones."""
    d.rectangle([x0, y0, x1, y1], fill=SKY)
    d.ellipse([x1 - 78, y0 + 14, x1 - 34, y0 + 58], fill=(250, 214, 120))
    for cx, cy in [(x0 + 60, y0 + 26), (x0 + 150, y0 + 44)]:
        d.ellipse([cx, cy, cx + 66, cy + 20], fill=(235, 240, 244))
        d.ellipse([cx + 16, cy - 10, cx + 56, cy + 12], fill=(235, 240, 244))
    horizon = y0 + int((y1 - y0) * 0.50)
    d.rectangle([x0, horizon, x1, y1], fill=SEA)
    d.polygon([(x0, horizon), (x0 + 150, horizon - 24), (x0 + 260, horizon),
               (x0 + 430, horizon - 16), (x1, horizon - 8), (x1, horizon)],
              fill=(96, 128, 110))
    for wy in range(horizon + 16, y1 - 6, 22):
        for wx in range(x0 + 8, x1 - 30, 46):
            d.arc([wx, wy, wx + 30, wy + 12], 180, 360, fill=(210, 228, 240), width=2)
    # --- cargo ship Sparta II, on fire (left) ---
    sx, sy = x0 + 40, horizon + 26
    d.polygon([(sx, sy), (sx + 210, sy), (sx + 188, sy + 36), (sx + 18, sy + 36)],
              fill=(122, 32, 28))
    d.rectangle([sx + 30, sy - 26, sx + 150, sy], fill=(176, 62, 48))
    d.rectangle([sx + 158, sy - 44, sx + 182, sy], fill=(230, 228, 220))
    d.rectangle([sx + 164, sy - 58, sx + 170, sy - 44], fill=(90, 90, 90))
    d.ellipse([sx + 84, sy - 78, sx + 128, sy - 40], fill=(70, 70, 70))
    d.ellipse([sx + 98, sy - 96, sx + 122, sy - 62], fill=(100, 100, 100))
    d.polygon([(sx + 96, sy - 26), (sx + 110, sy - 52), (sx + 124, sy - 26)],
              fill=(240, 140, 30))
    d.polygon([(sx + 104, sy - 26), (sx + 112, sy - 42), (sx + 120, sy - 26)],
              fill=(250, 210, 60))
    lf = font(SANSB, 14)
    d.text((sx + 22, sy + 10), "SPARTA II", font=lf, fill=(255, 255, 255))
    # --- warship Merkury sinking, bow up (right) ---
    wx0, wy0 = x1 - 216, horizon + 22
    d.polygon([(wx0, wy0), (wx0 + 170, wy0 - 30), (wx0 + 188, wy0 - 10),
               (wx0 + 70, wy0 + 34), (wx0 + 8, wy0 + 34)], fill=(74, 84, 92))
    d.rectangle([wx0 + 92, wy0 - 56, wx0 + 128, wy0 - 30], fill=(96, 106, 114))
    d.rectangle([wx0 + 104, wy0 - 70, wx0 + 108, wy0 - 56], fill=(60, 66, 72))
    d.polygon([(wx0 + 146, wy0 - 30), (wx0 + 156, wy0 - 48), (wx0 + 166, wy0 - 30)],
              fill=(240, 140, 30))
    d.ellipse([wx0 + 132, wy0 - 64, wx0 + 172, wy0 - 32], fill=(90, 90, 90))
    d.text((wx0 + 16, wy0 + 6), "MERKURY", font=lf, fill=(255, 255, 255))
    # --- sea drones ---
    for dx, dy in [(x0 + 210, y0 + 30), (x0 + 330, y0 + 56), (x1 - 120, y0 + 28)]:
        d.ellipse([dx - 5, dy - 3, dx + 5, dy + 3], fill=(30, 30, 30))
        d.line([dx - 12, dy - 6, dx + 12, dy - 6], fill=(30, 30, 30), width=2)
        d.line([dx, dy + 3, dx, dy + 12], fill=(30, 30, 30), width=1)
    d.rectangle([x0, y0, x1, y1], outline=NAVY, width=2)


def draw_courthouse(d, x, y, s):
    d.polygon([(x, y), (x + 54 * s, y), (x + 27 * s, y - 18 * s)], fill=NAVY2)
    d.rectangle([x + 4 * s, y, x + 50 * s, y + 4 * s], fill=NAVY2)
    for cx in (10, 22, 34):
        d.rectangle([x + cx * s, y + 4 * s, x + (cx + 4) * s, y + 34 * s], fill=NAVY2)
    d.rectangle([x, y + 34 * s, x + 54 * s, y + 40 * s], fill=NAVY2)


def draw_tower(d, x, y, s):
    d.rectangle([x + 14 * s, y - 58 * s, x + 40 * s, y], fill=NAVY2)
    d.polygon([(x + 14 * s, y - 58 * s), (x + 40 * s, y - 58 * s),
               (x + 27 * s, y - 74 * s)], fill=NAVY2)
    for ry in range(-50, -4, 10):
        for rx in (18, 28):
            d.rectangle([x + rx * s, y + ry * s, x + (rx + 5) * s, y + (ry + 5) * s],
                        fill=(250, 214, 120))
    d.polygon([(x + 48 * s, y - 66 * s), (x + 56 * s, y - 52 * s),
               (x + 64 * s, y - 66 * s), (x + 56 * s, y - 80 * s)], fill=(240, 140, 30))
    d.ellipse([x + 44 * s, y - 70 * s, x + 68 * s, y - 46 * s], outline=(240, 140, 30), width=2)


def draw_jet(d, x, y, s):
    d.polygon([(x, y), (x + 52 * s, y - 6 * s), (x + 52 * s, y + 2 * s),
               (x + 14 * s, y + 10 * s), (x + 4 * s, y + 22 * s)], fill=NAVY2)
    d.polygon([(x + 18 * s, y - 2 * s), (x + 30 * s, y - 16 * s),
               (x + 34 * s, y - 2 * s)], fill=NAVY2)
    for r in (16, 24):
        d.arc([x + 56 * s - r, y - r, x + 56 * s + r, y + r], -60, 60,
              fill=RED, width=3)


def draw_shield(d, x, y, s):
    d.polygon([(x + 27 * s, y - 40 * s), (x + 54 * s, y - 30 * s),
               (x + 54 * s, y + 4 * s), (x + 27 * s, y + 22 * s),
               (x, y + 4 * s), (x, y - 30 * s)], fill=NAVY2)
    d.rectangle([x + 17 * s, y - 10 * s, x + 37 * s, y + 10 * s], fill=(250, 214, 120))
    d.arc([x + 21 * s, y - 22 * s, x + 33 * s, y - 8 * s], 180, 360,
          fill=(250, 214, 120), width=3)


def story(d, x, y, colw, icon, headline, body, icon_dy=30):
    """One supporting story: icon left of a 2-line headline, body below."""
    icon(d, x + 2, y + icon_dy)
    hy = para(d, (x + 76, y), headline, font(SERIFB, 19), colw - 76, leading=24)
    return para(d, (x, y + 64), body, font(SANS, 15), colw, leading=20)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36
    R = W - M

    # ---- masthead ----
    d.rectangle([0, 0, W, 118], fill=NAVY)
    centre(d, 12, "THE WORLD TODAY", font(SERIFB, 62), (250, 244, 224))
    centre(d, 82, "WEDNESDAY, 25 NOVEMBER 2026  ·  WORLD NEWS IN ONE PAGE  ·  No. 329",
           font(SANSB, 16), (200, 214, 230))

    # ---- breaking banner ----
    d.rectangle([M, 130, R, 160], fill=RED)
    centre(d, 136, "BREAKING NEWS — UKRAINE STRIKES RUSSIAN SHIPS IN TWO SEAS",
           font(SANSB, 17), (255, 255, 255))

    # ---- lead headline ----
    y = 172
    y = para(d, (M, y),
             "ZELENSKYY: WE HIT THEM\nAT SEA — IN THE BALTIC\nAND OFF LIBYA",
             font(SERIFB, 38), R - M, leading=46)
    d.line([M, y + 8, R, y + 8], fill=RULE, width=2)

    # ---- lead illustration + prose ----
    iy = y + 20
    draw_sea_scene(d, M, iy, 600, iy + 220)
    px = 620
    y = para(d, (px, iy),
             "Ukraine confirmed it used sea drones to hit the sanctioned "
             "Russian cargo ship Sparta II in the Gulf of Finland — and sank "
             "the corvette Merkury off Libya.",
             font(SERIFB, 18), R - px, leading=24)
    y = para(d, (px, y + 8),
             "President Zelenskyy called both vessels legitimate military "
             "targets carrying weapons, a claim not independently verified. "
             "Norway urged caution; Putin vowed a response.",
             font(SANS, 15), R - px, leading=21)

    # ---- supporting stories, two columns ----
    colw = (R - M - 28) // 2
    sy = iy + 220 + 14
    d.line([M, sy, R, sy], fill=RULE, width=2)
    sy += 14
    story(d, M, sy, colw,
          lambda dd, x, y: draw_courthouse(dd, x, y, 0.7),
          "HUAWEI CONVICTED IN U.S. TRIAL",
          "A Brooklyn jury found the Chinese telecom giant guilty on 10 of "
          "12 counts — conspiracy to steal trade secrets and bank fraud over "
          "its hidden business in Iran. It was acquitted of racketeering.")
    story(d, M + colw + 28, sy, colw,
          lambda dd, x, y: draw_tower(dd, x, y, 0.6),
          "HOUTHIS HIT RIYADH'S TALLEST TOWER",
          "A Houthi drone struck the PIF Tower in Riyadh for the second time "
          "in five days, wounding 11 people, Saudi civil defence said, as the "
          "Yemen war's reach into the Gulf deepens.", icon_dy=52)

    # ---- second supporting row ----
    sy2 = sy + 168
    d.line([M, sy2, R, sy2], fill=RULE, width=2)
    sy2 += 14
    story(d, M, sy2, colw,
          lambda dd, x, y: draw_jet(dd, x, y, 0.8),
          "RUSSIAN DRONE ENTERS POLISH SKIES",
          "A Russian drone briefly crossed into Poland during an attack on "
          "Ukraine, days after three missiles landed there. NATO is sending "
          "early-warning aircraft; Warsaw summoned Moscow's ambassador.")
    story(d, M + colw + 28, sy2, colw,
          lambda dd, x, y: draw_shield(dd, x, y, 0.7),
          "U.S. SPY AGENCIES HIT BY CYBER BREACH",
          "The CIA and the Office of the Director of National Intelligence "
          "suffered a breach involving some unclassified information, a "
          "source told Reuters, exposing gaps at the top of U.S. intelligence.")

    # ---- also today strip ----
    ay = sy2 + 158
    d.rectangle([M, ay, R, ay + 74], fill=NAVY)
    centre(d, ay + 8, "ALSO TODAY", font(SANSB, 15), (250, 214, 120))
    para(d, (M + 14, ay + 30),
         "Nepal shaken by a 5.6 quake  ·  England level the T20 series "
         "in Australia  ·  Sensex falls 1,484 points  ·  Trump pardons "
         "Thanksgiving turkeys Freedom and Feathers",
         font(SANS, 14), R - M - 28, fill=(235, 238, 242), leading=19)

    # ---- footer ----
    centre(d, ay + 82, "Compiled from Reuters, Bloomberg, AP and BBC  ·  Wednesday, 25 November 2026",
           font(SANS, 12), GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
