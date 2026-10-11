"""Step 3 of the hero pipeline: rebuild the share image (assets/og.jpg, 1200 by 630).

Left half of the colour layer, right half of the sketch layer, a dark gradient on the bottom
third, name and caption. Run after hero_toplabel.py: python -I tools/og_image.py
Then bump og.jpg?v= on all seven pages (tools/bump_version.py --og N).
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
IMG = 'assets/images/'
NAME = 'Reuben Luera'
CAPTION = 'AI UX Researcher  |  HP, Adobe Research, Amazon Fire TV'
FONT_NAME = 'C:/Windows/Fonts/ariblk.ttf'
FONT_CAPTION = 'C:/Windows/Fonts/segoeuib.ttf'

col = Image.open(IMG + 'hero-qual-quant-color.webp').convert('RGB')
skt = Image.open(IMG + 'hero-qual-quant-sketch.webp').convert('RGB')
cw = int(962 * 1200 / 630); cx = 1440; x0 = cx - cw // 2
im = Image.new('RGB', (cw, 962))
im.paste(col.crop((x0, 0, cx, 962)), (0, 0))
im.paste(skt.crop((cx, 0, x0 + cw, 962)), (cx - x0, 0))
im = im.resize((1200, 630), Image.LANCZOS)

grad = Image.new('L', (1, 630), 0); px = grad.load()
for y in range(630):
    t = max(0, (y - 330) / 300); px[0, y] = int(200 * t ** 1.3)
im = Image.composite(Image.new('RGB', (1200, 630), (11, 20, 36)), im, grad.resize((1200, 630)))

d = ImageDraw.Draw(im)
d.text((64, 478), NAME, font=ImageFont.truetype(FONT_NAME, 64), fill=(255, 255, 255))
d.text((66, 566), CAPTION, font=ImageFont.truetype(FONT_CAPTION, 28), fill=(236, 240, 248))
im.save('assets/og.jpg', quality=88)
print('wrote assets/og.jpg', im.size)
