# The World Today - front page for Monday 23 November 2026.
# Draws a newspaper front page with PIL when it is available.
# If PIL cannot be imported at all, copies the pre-rendered
# entry.png bundled beside this file to the output directory.
# No network is used at any point. Output is deterministic.

import os
import shutil
import sys


# ---------------------------------------------------------------- fonts
# Candidate font file names, tried in order for every requested style.
# NEWS_FONT_DIR, when set, replaces the default search directories:
# pointing it at a directory with no fonts exercises the built-in
# fallback, and a missing font must never crash the program.
SERIF_BOLD = ["DejaVuSerif-Bold.ttf", "LiberationSerif-Bold.ttf",
              "NotoSerif-Bold.ttf"]
SERIF = ["DejaVuSerif.ttf", "LiberationSerif-Regular.ttf",
         "NotoSerif-Regular.ttf"]
SANS_BOLD = ["DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf",
             "NotoSans-Bold.ttf"]
SANS = ["DejaVuSans.ttf", "LiberationSans-Regular.ttf",
        "NotoSans-Regular.ttf"]

_DEFAULT_FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/truetype/noto",
    "/usr/share/fonts",
    "/usr/local/share/fonts",
    os.path.expanduser("~/.fonts"),
]


def _font_dirs():
    override = os.environ.get("NEWS_FONT_DIR")
    if override:
        return [override]
    return _DEFAULT_FONT_DIRS


def load_font(names, size):
    """Return a font of the requested size.

    Tries every candidate file in every candidate directory, then
    falls back to PIL's built-in default font so a machine with no
    font files at all still renders the page.
    """
    from PIL import ImageFont
    for directory in _font_dirs():
        for name in names:
            path = os.path.join(directory, name)
            if os.path.isfile(path):
                try:
                    return ImageFont.truetype(path, size)
                except Exception:
                    continue
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def text_w(draw, text, font):
    """Pixel width of text in the given font."""
    left, _top, right, _bottom = draw.textbbox((0, 0), text, font=font)
    return right - left


def wrap(draw, text, font, max_width):
    """Word-wrap text into lines that fit max_width pixels."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if text_w(draw, trial, font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_centered(draw, cx, y, text, font, fill):
    """Draw text centred on x=cx, return its height in pixels."""
    width = text_w(draw, text, font)
    draw.text((cx - width // 2, y), text, font=font, fill=fill)
    _l, top, _r, bottom = draw.textbbox((0, 0), text, font=font)
    return bottom - top


def draw_wrapped(draw, x, y, text, font, fill, max_width, spacing=4):
    """Draw word-wrapped text; return the y just below the last line."""
    for line in wrap(draw, text, font, max_width):
        draw.text((x, y), line, font=font, fill=fill)
        _l, top, _r, bottom = draw.textbbox((0, 0), line, font=font)
        y += (bottom - top) + spacing
    return y


# ------------------------------------------------------------- colours
PAPER = (247, 243, 234)
INK = (18, 18, 18)
RED = (179, 32, 44)
GREY = (90, 88, 82)
RULE = (150, 145, 132)
GREEN = (34, 139, 34)
DARK_GREEN = (18, 90, 40)
GOLD = (201, 162, 39)
BLUE = (28, 68, 128)
SKY = (120, 170, 220)


# ------------------------------------------------- pictorial illustrations
def draw_chip(draw, x, y, w, h):
    """A green computer chip with circuit traces and a rising arrow."""
    draw.rectangle([x, y, x + w, y + h], fill=(16, 60, 34),
                   outline=DARK_GREEN, width=3)
    pin = 8
    for i in range(5):
        px = x + 18 + i * ((w - 36) // 4)
        draw.rectangle([px, y - pin, px + 10, y], fill=GREEN)
        draw.rectangle([px, y + h, px + 10, y + h + pin], fill=GREEN)
    for i in range(5):
        py = y + 18 + i * ((h - 36) // 4)
        draw.rectangle([x - pin, py, x, py + 10], fill=GREEN)
        draw.rectangle([x + w, py, x + w + pin, py + 10], fill=GREEN)
    cx, cy = x + w // 2, y + h // 2
    draw.rectangle([cx - 52, cy - 36, cx + 52, cy + 36],
                   fill=(24, 110, 52), outline=(120, 220, 140), width=2)
    label = load_font(SANS_BOLD, 22)
    lw = text_w(draw, "NVDA", label)
    draw.text((cx - lw // 2, cy - 12), "NVDA", font=label,
              fill=(255, 255, 255))
    # rising arrow across the chip
    pts = [(x + 8, y + h - 18), (x + w // 3, y + h - 52),
           (x + w // 2, y + h - 34), (x + w - 14, y + 14)]
    draw.line(pts, fill=(140, 255, 150), width=6, joint="curve")
    ax, ay = x + w - 14, y + 14
    draw.polygon([(ax, ay - 16), (ax + 16, ay + 2), (ax - 2, ay + 16)],
                 fill=(140, 255, 150))


def draw_bank(draw, x, y, w, h):
    """A bank building struck through by a red ban slash."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 226, 210),
                   outline=RULE, width=2)
    bx, by = x + w // 2, y + h // 2
    draw.polygon([(bx - 78, by - 42), (bx, by - 66), (bx + 78, by - 42)],
                 fill=BLUE)
    for i in range(-2, 3):
        cx = bx + i * 30
        draw.rectangle([cx - 7, by - 34, cx + 7, by + 40], fill=(240, 240, 235),
                       outline=BLUE, width=2)
    draw.rectangle([bx - 92, by + 40, bx + 92, by + 52], fill=BLUE)
    draw.rectangle([bx - 100, by + 52, bx + 100, by + 62], fill=BLUE)
    # red slash across the whole scene
    draw.line([(x + 10, y + h - 12), (x + w - 10, y + 12)], fill=RED, width=10)
    draw.ellipse([x + w - 62, y + h - 62, x + w - 14, y + h - 14],
                 outline=RED, width=6)
    dollar = load_font(SANS_BOLD, 30)
    dw = text_w(draw, "$", dollar)
    draw.text((x + w - 38 - dw // 2, y + h - 52), "$", font=dollar, fill=RED)


def draw_ball(draw, x, y, w, h):
    """A football beside a gold trophy cup."""
    cx, cy = x + w // 3, y + h // 2
    r = min(w, h) // 3
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255),
                 outline=INK, width=3)
    draw.polygon([(cx - 12, cy - 8), (cx + 12, cy - 8), (cx + 18, cy + 12),
                  (cx, cy + 24), (cx - 18, cy + 12)], fill=INK)
    for dx, dy in [(-r + 8, -r + 20), (r - 8, -r + 20), (-r + 6, r - 26),
                   (r - 6, r - 26), (0, -r + 4)]:
        draw.line([(cx, cy), (cx + dx, cy + dy)], fill=INK, width=2)
    tx = x + int(w * 0.68)
    ty = y + h // 2
    draw.polygon([(tx - 34, ty - 44), (tx + 34, ty - 44), (tx + 22, ty + 6),
                  (tx - 22, ty + 6)], fill=GOLD, outline=(120, 90, 10), width=2)
    draw.rectangle([tx - 8, ty + 6, tx + 8, ty + 26], fill=GOLD)
    draw.rectangle([tx - 26, ty + 26, tx + 26, ty + 34], fill=GOLD)
    draw.arc([tx - 48, ty - 44, tx - 18, ty - 8], 90, 270, fill=GOLD, width=5)
    draw.arc([tx + 18, ty - 44, tx + 48, ty - 8], 270, 90, fill=GOLD, width=5)
    draw.ellipse([tx - 7, ty - 58, tx + 7, ty - 44], fill=GOLD)


def draw_exam(draw, x, y, w, h):
    """An exam paper, a pencil and a crossed-out AI badge."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 226, 210),
                   outline=RULE, width=2)
    px, py = x + 22, y + 8
    pw, ph = 108, 92
    draw.rectangle([px, py, px + pw, py + ph], fill=(255, 255, 255),
                   outline=INK, width=2)
    for i in range(4):
        ly = py + 24 + i * 18
        draw.line([(px + 12, ly), (px + pw - 12, ly)], fill=GREY, width=2)
    draw.rectangle([px + 12, py + 8, px + 44, py + 18], fill=RED)
    # pencil leaning on the paper, kept inside the illustration box
    draw.polygon([(px + pw + 14, py + 4), (px + pw + 30, py + 4),
                  (px + pw + 30, py + 76), (px + pw + 22, py + 90),
                  (px + pw + 14, py + 76)], fill=(240, 180, 60),
                 outline=INK)
    draw.polygon([(px + pw + 22, py + 90), (px + pw + 14, py + 76),
                  (px + pw + 30, py + 76)], fill=(250, 230, 190),
                 outline=INK)
    # AI badge with a red cross
    bx, by = x + w - 92, y + h - 78
    draw.ellipse([bx, by, bx + 68, by + 68], fill=BLUE)
    ai = load_font(SANS_BOLD, 26)
    aw = text_w(draw, "AI", ai)
    draw.text((bx + 34 - aw // 2, by + 18), "AI", font=ai,
              fill=(255, 255, 255))
    draw.line([(bx - 6, by - 6), (bx + 74, by + 74)], fill=RED, width=7)
    draw.line([(bx - 6, by + 74), (bx + 74, by - 6)], fill=RED, width=7)


def draw_arena(draw, x, y, w, h):
    """A concert arena dome, stage lights and a fleeing crowd."""
    draw.rectangle([x, y, x + w, y + h], fill=(20, 24, 48),
                   outline=RULE, width=2)
    cx = x + w // 2
    draw.pieslice([cx - 90, y + 26, cx + 90, y + 206], 180, 360,
                  fill=(70, 90, 140), outline=(150, 170, 220), width=2)
    draw.rectangle([cx - 90, y + 118, cx + 90, y + 128], fill=(150, 170, 220))
    for lx in (cx - 60, cx, cx + 60):
        draw.line([(lx, y + 118), (lx - 26, y + h - 44)], fill=(255, 220, 90),
                  width=3)
        draw.line([(lx, y + 118), (lx + 26, y + h - 44)], fill=(255, 220, 90),
                  width=3)
    # crowd dots streaming out of the doors
    for i, (dx, dy) in enumerate([(-70, 0), (-40, 8), (-10, 0), (20, 8),
                                  (50, 0), (78, 8), (-88, 18), (88, 18)]):
        draw.ellipse([cx + dx - 6, y + h - 34 + dy, cx + dx + 6,
                      y + h - 22 + dy], fill=(255, 255, 255))
    # warning triangle
    tx, ty = x + w - 58, y + 14
    draw.polygon([(tx, ty + 40), (tx + 22, ty), (tx + 44, ty + 40)],
                 fill=(255, 200, 0), outline=INK)
    bang = load_font(SANS_BOLD, 26)
    bw = text_w(draw, "!", bang)
    draw.text((tx + 22 - bw // 2, ty + 12), "!", font=bang, fill=INK)


# ------------------------------------------------------------------ page
def render():
    from PIL import Image, ImageDraw

    width, height = 1024, 1024
    img = Image.new("RGB", (width, height), PAPER)
    draw = ImageDraw.Draw(img)

    masthead = load_font(SERIF_BOLD, 74)
    date_font = load_font(SANS_BOLD, 34)
    lead_head = load_font(SERIF_BOLD, 40)
    head_font = load_font(SERIF_BOLD, 27)
    sub_font = load_font(SANS, 18)
    lead_sub = load_font(SANS, 20)
    foot_font = load_font(SANS, 16)

    margin = 28
    # --- masthead
    draw.line([(margin, 14), (width - margin, 14)], fill=INK, width=4)
    draw_centered(draw, width // 2, 26, "THE WORLD TODAY", masthead, INK)
    draw.line([(margin, 112), (width - margin, 112)], fill=INK, width=3)
    # --- red date band
    draw.rectangle([margin, 122, width - margin, 172], fill=RED)
    draw_centered(draw, width // 2, 134, "MONDAY, 23 NOVEMBER 2026",
                  date_font, (255, 255, 255))
    # --- lead story: Nvidia
    lead_top = 186
    lead_bottom = 452
    draw.rectangle([margin, lead_top, width - margin, lead_bottom],
                   outline=RULE, width=2)
    draw.line([(margin, lead_top + 8), (width - margin, lead_top + 8)],
              fill=RED, width=4)
    hx = margin + 24
    hy = lead_top + 26
    hy = draw_wrapped(draw, hx, hy, "HUANG IS BACK AT NVIDIA",
                      lead_head, INK, 560, spacing=2)
    hy += 6
    hy = draw_wrapped(draw, hx, hy,
                      "Shares soar 31% as the board reinstates its founder "
                      "as chief executive, igniting a global AI rally.",
                      lead_sub, GREY, 560, spacing=3)
    draw_chip(draw, width - margin - 300, lead_top + 34, 276, 190)
    draw.text((width - margin - 296, lead_bottom - 34), "+31% IN A DAY",
              font=load_font(SANS_BOLD, 22), fill=GREEN)

    # --- four smaller stories in a 2 x 2 grid
    stories = [
        ("US CUTS IRAN'S 'LAST LIFELINE'",
         "Sweeping sanctions hit the shadow banks moving billions for Tehran.",
         draw_bank, (235, 222, 196)),
        ("UK TO HOST 2035 WOMEN'S WORLD CUP",
         "FIFA confirms England, Scotland, Wales and Northern Ireland.",
         draw_ball, (235, 222, 196)),
        ("MINISTER QUITS OVER AI EXAM CHEAT",
         "Seoul's education chief takes blame for cheating chaos.",
         draw_exam, (235, 222, 196)),
        ("12,000 FLEE ARENA IN GAS SCARE",
         "Mystery substance released at a Don Toliver concert in Manchester.",
         draw_arena, (235, 222, 196)),
    ]
    grid_top = 466
    cell_w = (width - 2 * margin - 16) // 2
    cell_h = 252
    for i, (headline, sub, art, _box) in enumerate(stories):
        col = i % 2
        row = i // 2
        x0 = margin + col * (cell_w + 16)
        y0 = grid_top + row * (cell_h + 14)
        x1 = x0 + cell_w
        y1 = y0 + cell_h
        draw.rectangle([x0, y0, x1, y1], outline=RULE, width=2)
        draw.line([(x0, y0 + 6), (x1, y0 + 6)], fill=RED, width=3)
        art(draw, x0 + 14, y0 + 16, cell_w - 28, 108)
        ty = y0 + 134
        ty = draw_wrapped(draw, x0 + 14, ty, headline, head_font, INK,
                          cell_w - 28, spacing=2)
        draw_wrapped(draw, x0 + 14, ty + 4, sub, sub_font, GREY,
                     cell_w - 28, spacing=2)

    # --- footer
    draw.line([(margin, 992), (width - margin, 992)], fill=RULE, width=2)
    draw_centered(draw, width // 2, 1000,
                  "Five stories from Monday 23 November 2026  |  "
                  "Sources: Reuters, FIFA, CNN",
                  foot_font, GREY)
    return img


# ------------------------------------------------------------- entrypoint
def _bundled_png():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")

    try:
        from PIL import Image  # noqa: F401  (probe only)
    except Exception:
        bundled = _bundled_png()
        if not os.path.isfile(bundled):
            print("error: PIL is not installed and no bundled entry.png "
                  "was found beside main.py", file=sys.stderr)
            return 1
        shutil.copyfile(bundled, out_path)
        print("PIL unavailable; copied bundled entry.png to " + out_path)
        return 0

    img = render()
    img.save(out_path, format="PNG")
    print("wrote " + out_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
