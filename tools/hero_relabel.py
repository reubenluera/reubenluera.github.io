"""Step 1 of the hero pipeline: repaint the side labels.

Reads the two Framer-exported hero layers, erases DESIGN / RESEARCH by cloning background,
and paints QUALITATIVE / QUANTITATIVE in each layer's own style. Writes
assets/images/hero-qual-quant-color.webp and hero-qual-quant-sketch.webp, plus check crops
in tools/out/. Run from anywhere: python -I tools/hero_relabel.py
See wiki/hero-pipeline.md for the measurements.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
OUT = os.path.join('tools', 'out'); os.makedirs(OUT, exist_ok=True)
IMG = 'assets/images/'
FONT_CLEAN = 'C:/Windows/Fonts/ariblk.ttf'      # Arial Black
FONT_SKETCH = 'C:/Windows/Fonts/segoeprb.ttf'   # Segoe Print Bold


def best_shift(a, box, period, direction, nmax=40):
    """Shift (multiple of the pattern period) whose source rows match the bands around the box."""
    x0, y0, x1, y1 = box
    bands = [(max(0, y0 - 30), y0), (y1, y1 + 8)]
    best = None
    for k in range(4, nmax):
        s = k * period * direction; sx0 = x0 + s; sx1 = x1 + s
        if sx0 < 0 or sx1 > a.shape[1]: continue
        if sx1 > x0 - 20 and sx0 < x1 + 20: continue          # must not overlap the box
        src_g = a[y0:y1, sx0:sx1, :3].mean(axis=2)
        if (src_g < 140).sum() > 20: continue                  # source must be clean background
        err = 0
        for by0, by1 in bands:
            d = a[by0:by1, x0:x1, :3].astype(float); src = a[by0:by1, sx0:sx1, :3].astype(float)
            err += np.abs(d - src).mean()
        if best is None or err < best[0]: best = (err, s)
    if best is None: raise SystemExit(f'no clean background found for box {box}')
    return best


def erase(a, box, period, direction):
    err, s = best_shift(a, box, period, direction)
    x0, y0, x1, y1 = box
    a[y0:y1, x0:x1] = a[y0:y1, x0 + s:x1 + s]
    return err, s


def fit_font(path, text, target_cap, max_w):
    size = 40
    while True:
        f = ImageFont.truetype(path, size)
        bb = f.getbbox('H'); cap = bb[3] - bb[1]
        if cap >= target_cap or f.getlength(text) >= max_w: return f
        size += 1


def draw_clean(im, text, cx, top, font, color=(0, 0, 0, 255)):
    d = ImageDraw.Draw(im)
    bb = font.getbbox(text); w = bb[2] - bb[0]; x = int(cx - w / 2) - bb[0]
    d.text((x, top - bb[1]), text, font=font, fill=color)
    y = top + (bb[3] - bb[1]) + 8
    d.rectangle((int(cx - w / 2), y, int(cx + w / 2), y + 3), fill=color)


def rough_mask(mask, seed=0):
    """Give a text mask a marker / pencil texture."""
    rng = np.random.default_rng(seed)
    m = np.array(mask).astype(float) / 255
    noise = rng.random(m.shape)
    noise = np.array(Image.fromarray((noise * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))).astype(float) / 255
    keep = (m > 0.5) & (noise > 0.38)
    out = np.array(Image.fromarray((keep * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)))
    return Image.fromarray(out)


def draw_sketch(im, text, cx, top, font, color=(74, 75, 75)):
    bb = font.getbbox(text); w = bb[2] - bb[0]; h = bb[3] - bb[1]
    layer = Image.new('L', (w + 60, h + 40), 0); d = ImageDraw.Draw(layer)
    d.text((30 - bb[0], 20 - bb[1]), text, font=font, fill=255, stroke_width=2, stroke_fill=255)
    layer = rough_mask(layer, seed=hash(text) & 0xffff)
    im.paste(Image.new('RGBA', layer.size, color + (255,)), (int(cx - w / 2) - 30, top - 20), layer)
    bx0 = int(cx - w / 2) - 6; bx1 = int(cx + w / 2) + 6; by = top + h + 22
    br = Image.new('L', (bx1 - bx0 + 20, 40), 0); d = ImageDraw.Draw(br)
    d.line((10, 20, bx1 - bx0 + 10, 20), fill=255, width=4)
    d.line((10, 8, 10, 32), fill=255, width=4); d.line((bx1 - bx0 + 10, 8, bx1 - bx0 + 10, 32), fill=255, width=4)
    br = rough_mask(br, seed=7)
    im.paste(Image.new('RGBA', br.size, color + (255,)), (bx0 - 10, by - 20), br)


# colour layer
im = Image.open(IMG + 'bkZpxj8grx5v3QcIPHdwYG9sw0o.webp').convert('RGBA'); a = np.array(im)
print('color erase L', erase(a, (840, 96, 1160, 172), 38, -1))
print('color erase R', erase(a, (1650, 96, 2080, 172), 38, +1))
im = Image.fromarray(a)
f = fit_font(FONT_CLEAN, 'QUANTITATIVE', 41, 560)
draw_clean(im, 'QUALITATIVE', 994, 109, f); draw_clean(im, 'QUANTITATIVE', 1861, 110, f)
im.save(IMG + 'hero-qual-quant-color.webp', quality=90, method=6)
im.crop((700, 40, 2200, 280)).save(os.path.join(OUT, 'relabel_color.png'))

# sketch layer
im = Image.open(IMG + 'gERBzf4G8UwGf737LFgkQbapKiY.webp').convert('RGBA'); a = np.array(im)
print('sketch erase L', erase(a, (840, 100, 1160, 212), 46, -1))
print('sketch erase R', erase(a, (1650, 100, 2080, 212), 46, +1))
im = Image.fromarray(a)
f = fit_font(FONT_SKETCH, 'QUANTITATIVE', 44, 560)
draw_sketch(im, 'QUALITATIVE', 1000, 113, f); draw_sketch(im, 'QUANTITATIVE', 1845, 114, f)
im.save(IMG + 'hero-qual-quant-sketch.webp', quality=90, method=6)
im.crop((700, 40, 2200, 280)).save(os.path.join(OUT, 'relabel_sketch.png'))
print('ok, check tools/out/relabel_*.png, then run hero_toplabel.py')
