"""Repaint the caption line of the "four themes" figure on mllmjudge/.

  python -I tools/fig_themes_caption.py

The Framer export (0OpibaTk6UPCRnv5HyRc0G2jgMQ.webp) has its caption baked in and said
"8 Adobe CC designers (3 junior, 3 mid, 2 senior)", which contradicted the page text and the
card footers (10 designers). This writes a derived file, mllm-themes-10-designers.webp, with the
caption strip repainted. The source image is never edited (CLAUDE.md rule 3).
"""
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'assets', 'images', '0OpibaTk6UPCRnv5HyRc0G2jgMQ.webp')
OUT = os.path.join(ROOT, 'assets', 'images', 'mllm-themes-10-designers.webp')
CAPTION = ('Four themes coded from think-aloud transcripts across 10 Adobe CC designers '
           'over three RITE rounds on usertesting.com.')
FONTS = [
    '/System/Library/Fonts/Helvetica.ttc',
    '/System/Library/Fonts/HelveticaNeue.ttc',
    r'C:\Windows\Fonts\arial.ttf',
    '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
]
STRIP_BOTTOM = 44      # caption occupies y 0..44; the cards start at about y 52
TEXT_X, TEXT_Y, SIZE = 8, 9, 22

im = Image.open(SRC).convert('RGB')
bg = im.getpixel((im.width - 4, 4))
# darkest pixel in the old caption is the ink colour
strip = im.crop((0, 0, im.width, STRIP_BOTTOM))
ink = min(strip.getdata(), key=sum)
font = ImageFont.truetype(next(p for p in FONTS if os.path.exists(p)), SIZE)
d = ImageDraw.Draw(im)
d.rectangle((0, 0, im.width, STRIP_BOTTOM), fill=bg)
d.text((TEXT_X, TEXT_Y), CAPTION, font=font, fill=ink)
im.save(OUT, 'WEBP', quality=92, method=6)
print('wrote', OUT, im.size, 'bg', bg, 'ink', ink)
