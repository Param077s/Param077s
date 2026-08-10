#!/usr/bin/env python3
"""
Render a photo as an ASCII-art SVG.

The glyph grid is baked in at generation time — no script, no external
reference — so GitHub's SVG sanitiser leaves it alone and nothing is fetched
when someone views the profile.

Usage:
    python3 make_portrait.py SOURCE OUT.svg [--cols 120] [--crop l,t,r,b]
                            [--gamma 1.0] [--ramp dense|soft] [--light]
"""

import argparse
import sys

from PIL import Image, ImageEnhance, ImageOps

# Light glyphs on a dark panel: more ink = brighter. Index 0 is the darkest
# part of the photo, the last entry the brightest.
RAMPS = {
    "soft":  " .·:-=+*csS#%@",
    "dense": " .'`^\",:;!i~+?][}{1tfjxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@",
}

# A monospace cell is about 0.55 as wide as it is tall; sampling has to
# compensate or the portrait comes out stretched vertically.
CELL_RATIO = 0.55


def build_grid(img, cols, ramp, gamma, invert):
    w, h = img.size
    rows = max(1, int(cols * (h / w) * CELL_RATIO))

    g = img.convert("L")
    g = ImageOps.autocontrast(g, cutoff=1)
    g = ImageEnhance.Contrast(g).enhance(1.15)
    g = g.resize((cols, rows), Image.LANCZOS)

    px = g.load()
    n = len(ramp) - 1
    lines = []
    for y in range(rows):
        row = []
        for x in range(cols):
            v = px[x, y] / 255.0
            if invert:
                v = 1.0 - v
            v = v ** gamma
            row.append(ramp[min(n, max(0, round(v * n)))])
        lines.append("".join(row).rstrip())
    return lines


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def to_svg(lines, cols, light, label):
    FS = 10                      # font-size
    LH = FS                      # line-height: square-ish blocks read best
    CW = FS * CELL_RATIO
    PAD = 20
    W = int(cols * CW + 2 * PAD)
    H = int(len(lines) * LH + 2 * PAD)

    bg, fg = ("#f6f8fa", "#1f2328") if light else ("#0d1117", "#e6edf3")

    body = "\n".join(
        f'<text x="{PAD}" y="{PAD + (i + 1) * LH}">{esc(l)}</text>'
        for i, l in enumerate(lines) if l.strip()
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(label)}">
<style>
  text {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace;
          font-size: {FS}px; letter-spacing: 0; white-space: pre; fill: {fg}; }}
</style>
<rect width="{W}" height="{H}" rx="12" fill="{bg}"/>
{body}
</svg>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--cols", type=int, default=120)
    ap.add_argument("--crop", help="l,t,r,b in pixels")
    ap.add_argument("--gamma", type=float, default=1.0)
    ap.add_argument("--ramp", choices=list(RAMPS), default="soft")
    ap.add_argument("--light", action="store_true", help="dark glyphs on a light panel")
    ap.add_argument("--invert", dest="invert", action="store_true", default=None,
                    help="map dark photo areas to dense glyphs (right for a dark subject on a light ground)")
    ap.add_argument("--no-invert", dest="invert", action="store_false")
    ap.add_argument("--label", default="ASCII portrait")
    a = ap.parse_args()

    img = Image.open(a.src)
    if a.crop:
        img = img.crop(tuple(int(v) for v in a.crop.split(",")))

    # Which end of the ramp gets the ink. Defaults to matching the panel, but
    # a dark subject on a light ground needs it forced the other way.
    invert = a.light if a.invert is None else a.invert
    lines = build_grid(img, a.cols, RAMPS[a.ramp], a.gamma, invert=invert)
    svg = to_svg(lines, a.cols, a.light, a.label)

    with open(a.out, "w") as f:
        f.write(svg)
    print(f"{a.out}: {a.cols}x{len(lines)} chars, {len(svg)} bytes")


if __name__ == "__main__":
    main()
