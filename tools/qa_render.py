"""Full-page renders for the QA pass (wiki/qa.md).

  python -I tools/qa_render.py http://localhost:8765/ http://localhost:8765/mllmjudge/

For each URL renders a 1280px-wide and a 375px-wide full-page PNG with headless Edge (or Chrome
if EDGE is not found), then cuts each into 1150px-tall slices scaled to 900px wide under
tools/out/. Uses a fresh profile directory per run, because a second headless instance on the
same profile silently writes nothing.
"""
import os, random, subprocess, sys
from PIL import Image
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'tools', 'out'); os.makedirs(OUT, exist_ok=True)
CANDIDATES = [
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/usr/bin/google-chrome', '/usr/bin/chromium',
]
BROWSER = next((p for p in CANDIDATES if os.path.exists(p)), None)
if not BROWSER: raise SystemExit('no Edge or Chrome found; edit CANDIDATES')

urls = sys.argv[1:] or ['http://localhost:8765/']
for url in urls:
    slug = url.rstrip('/').split('/')[-1] or 'home'
    for width, height in [(1280, 6000), (375, 7000)]:
        png = os.path.join(OUT, f'{slug}_{width}.png')
        prof = os.path.join(OUT, f'profile-{random.randint(1, 10**6)}')
        subprocess.run([BROWSER, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run',
                        f'--user-data-dir={prof}', f'--window-size={width},{height}',
                        f'--screenshot={png}', url + ('&' if '?' in url else '?') + f'qa={random.randint(1, 10**6)}'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=90)
        if not os.path.exists(png): print('render failed', url, width); continue
        im = Image.open(png); W, H = im.size
        a = np.array(im.convert('L')); rows = np.where(a.min(axis=1) < 250)[0]
        bottom = int(rows.max() + 1) if len(rows) else H
        n = 0
        for y in range(0, bottom, 1150):
            c = im.crop((0, y, W, min(y + 1150, bottom)))
            c = c.resize((900, int(c.height * 900 / W)), Image.LANCZOS)
            c.save(os.path.join(OUT, f'{slug}_{width}_s{n}.png')); n += 1
        print(f'{url} @ {width}: content height {bottom}, {n} slices in tools/out/')
