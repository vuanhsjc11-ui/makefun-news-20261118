#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news poster and write entry.png.

Deterministic: no clock, no network, no randomness. Facts are the short
labels researched for this entry; URLs live in SOURCES.md.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = Path(__file__).resolve().parent / "entry.png"

FONT = "/usr/share/fonts/truetype/macos/Inter-Bold.ttf"
FONT_MED = "/usr/share/fonts/truetype/macos/Inter-SemiBold.ttf"
FONT_REG = "/usr/share/fonts/truetype/macos/Inter-Regular.ttf"

INK = (22, 24, 28)
PAPER = (244, 239, 230)
WHITE = (255, 252, 247)
NAVY = (16, 28, 48)
RED = (178, 36, 32)
GOLD = (212, 164, 74)
CREAM = (232, 224, 208)
MUTED = (92, 86, 76)
SLATE = (70, 84, 96)


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def wrap(text: str, face: ImageFont.FreeTypeFont, width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for word in text.split():
        trial = word if not current else f"{current} {word}"
        if face.getlength(trial) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(draw, xy, lines, face, fill, leading):
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=face, fill=fill)
        y += leading
    return y


def rounded(draw, box, radius, fill):
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def main() -> None:
    image = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(image)

    f_date = font(FONT, 62)
    f_kicker = font(FONT_MED, 18)
    f_lead = font(FONT, 46)
    f_fact = font(FONT_MED, 22)
    f_small = font(FONT_REG, 18)
    f_card_k = font(FONT_MED, 16)
    f_card_h = font(FONT, 32)
    f_card_b = font(FONT_MED, 20)
    f_brand = font(FONT_MED, 18)
    f_meta = font(FONT, 15)

    # Mast
    draw.rectangle((0, 0, W, 56), fill=NAVY)
    draw.text((32, 16), "WORLD NEWS", font=f_brand, fill=WHITE)
    right = "ONE DAY  ·  SIX FRONTS"
    draw.text((W - 32 - f_brand.getlength(right), 16), right, font=f_brand, fill=GOLD)

    # Date header required by the brief
    draw.text((32, 74), "18 November 2026", font=f_date, fill=INK)
    draw.rectangle((32, 152, 292, 160), fill=RED)
    draw.text((32, 170), "Wednesday", font=f_small, fill=MUTED)

    # Lead slab: headlines on the left, the sequence on the right.
    lead = (32, 208, 992, 468)
    rounded(draw, lead, 18, NAVY)
    draw.rectangle((32, 208, 46, 468), fill=RED)
    draw.text((64, 226), "ASIA  ·  THE DAY’S LEAD", font=f_kicker, fill=GOLD)
    draw.text((64, 258), "Trump in Manila.", font=f_lead, fill=WHITE)
    draw.text((64, 314), "Putin meets Xi.", font=f_lead, fill=WHITE)
    draw.text((64, 384), "Malacañang: the alliance has", font=f_fact, fill=CREAM)
    draw.text((64, 412), "“never been better.”", font=f_fact, fill=WHITE)

    panel = (700, 232, 968, 444)
    rounded(draw, panel, 12, (28, 44, 70))
    draw.text((720, 248), "TODAY", font=f_kicker, fill=GOLD)
    draw.text((720, 276), "Manila", font=font(FONT, 22), fill=WHITE)
    draw.text((720, 302), "Trump and Marcos", font=f_small, fill=CREAM)
    draw.text((720, 332), "Shenzhen", font=font(FONT, 22), fill=WHITE)
    draw.text((720, 358), "Xi and Putin meet", font=f_small, fill=CREAM)
    draw.text((720, 388), "THURSDAY", font=f_kicker, fill=GOLD)
    draw.text((720, 414), "First meeting of the three", font=f_small, fill=WHITE)

    # Six fronts
    cards = [
        (
            RED,
            "UNITED STATES",
            "Peltola wins Alaska",
            "Unseats Sen. Dan Sullivan. Ninth Democratic Senate flip, after two weeks of counting.",
        ),
        (
            (20, 110, 104),
            "SECURITY",
            "Not a cyber attack",
            "Rubio: “zero evidence” this week’s outages are linked. Flights, banks, Apple, Microsoft, NSA.",
        ),
        (
            (22, 78, 140),
            "TECHNOLOGY",
            "Nvidia sales double",
            "Quarterly sales $115.8bn. Board will not reinstate Huang. Shares +4.8% after hours.",
        ),
        (
            (140, 96, 32),
            "MARKETS",
            "Asia mostly lower",
            "Nikkei −0.6% to 58,520. Japan’s October trade gap ¥476.5bn, up 58%, out today.",
        ),
        (
            (92, 48, 120),
            "SPORT",
            "Japan 2–1 Paraguay",
            "Hajime Moriyasu’s last match, in Singapore in the small hours of 18 November.",
        ),
        (
            (48, 52, 58),
            "WAR  ·  17 NOV",
            "Kerch road arch down",
            "Ukraine’s strike dropped the Crimea bridge span. The Kremlin says it will rebuild.",
        ),
    ]

    grid_top = 488
    gap = 14
    card_w = 310
    card_h = 248
    origin_x = 32
    for index, (color, kicker, title, body) in enumerate(cards):
        col = index % 3
        row = index // 3
        x = origin_x + col * (card_w + gap)
        y = grid_top + row * (card_h + gap)
        rounded(draw, (x, y, x + card_w, y + card_h), 16, WHITE)
        draw.rectangle((x, y, x + card_w, y + 8), fill=color)
        draw.text((x + 18, y + 22), kicker, font=f_card_k, fill=color)
        title_lines = wrap(title, f_card_h, card_w - 36)
        y_text = draw_lines(draw, (x + 18, y + 50), title_lines, f_card_h, INK, 38)
        body_lines = wrap(body, f_card_b, card_w - 36)
        draw_lines(draw, (x + 18, y_text + 8), body_lines[:4], f_card_b, SLATE, 26)

    # Footer rule, large enough to survive a shrink
    draw.rectangle((32, 998, 992, 1002), fill=RED)
    note = "BBC  ·  AP  ·  REUTERS  ·  KYODO  ·  GMA"
    draw.text((32, 1004), note, font=f_meta, fill=MUTED)

    image.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} {OUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()
