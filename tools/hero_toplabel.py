"""Step 2 of the hero pipeline: paint the centred role label.

Adds AI UX RESEARCHER at the top centre of both generated hero layers, straddling the slider
divider. Run after hero_relabel.py: python -I tools/hero_toplabel.py
TOP must stay at 60 or lower; the fixed nav clips anything higher (wiki/hero-pipeline.md).
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
OUT = os.path.join('tools', 'out'); os.makedirs(OUT, exist_ok=True)
IMG = 'assets/images/'
FONT_CLEAN = 'C:/Windows/Fonts/ariblk.ttf'
FONT_SKETCH = 'C:/Windows/Fonts/segoeprb.ttf'
TEXT = 'AI UX RESEARCHER'
CX, TOP = 1440, 60


def fit_font(path, text, target_cap):
    size = 20
    while True:
        f = ImageFont.truetype(path, size)
        bb = f.getbbox('H')
        if bb[3] - bb[1] >= target_cap: return f
        size += 1


def rough_mask(mask, seed=0):
    rng = np.random.default_rng(seed)
    m = np.array(mask).astype(float) / 255
    noise = rng.random(m.shape)
    noise = np.array(Image.fromarray((noise * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0))).astype(float) / 255
    keep = (m > 0.5) & (noise > 0.36)
    out = np.array(Image.fromarray((keep * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.5)))
    return Image.fromarray(out)


for f in ['hero-qual-quant-color.webp', 'hero-qual-quant-sketch.webp']:
    a = np.array(Image.open(IMG + f).convert('L'))
    dark = int((a[20:100, 1100:1780] < 140).sum())
    if dark: raise SystemExit(f'{f}: top band is not clean ({dark} dark px). Re-run hero_relabel.py first.')

# colour layer: clean bold sans, letterspaced
im = Image.open(IMG + 'hero-qual-quant-color.webp').convert('RGBA')
f = fit_font(FONT_CLEAN, TEXT, 25)
d = ImageDraw.Draw(im)
sp = 3
widths = [f.getlength(ch) for ch in TEXT]
total = sum(widths) + sp * (len(TEXT) - 1)
x = CX - total / 2; bb = f.getbbox('H')
for ch, w in zip(TEXT, widths):
    d.text((x, TOP - bb[1]), ch, font=f, fill=(0, 0, 0, 255)); x += w + sp
im.save(IMG + 'hero-qual-quant-color.webp', quality=90, method=6)
im.crop((900, 0, 1980, 240)).save(os.path.join(OUT, 'toplabel_color.png'))

# sketch layer: marker, roughened
im = Image.open(IMG + 'hero-qual-quant-sketch.webp').convert('RGBA')
f = fit_font(FONT_SKETCH, TEXT, 27)
bb = f.getbbox(TEXT); w = bb[2] - bb[0]; h = bb[3] - bb[1]
layer = Image.new('L', (w + 60, h + 40), 0); dl = ImageDraw.Draw(layer)
dl.text((30 - bb[0], 20 - bb[1]), TEXT, font=f, fill=255, stroke_width=1, stroke_fill=255)
layer = rough_mask(layer, seed=11)
im.paste(Image.new('RGBA', layer.size, (74, 75, 75, 255)), (int(CX - w / 2) - 30, TOP - 20), layer)
im.save(IMG + 'hero-qual-quant-sketch.webp', quality=90, method=6)
im.crop((900, 0, 1980, 240)).save(os.path.join(OUT, 'toplabel_sketch.png'))
print('ok, check tools/out/toplabel_*.png, then run og_image.py and bump the hero ?v= in index.html')
