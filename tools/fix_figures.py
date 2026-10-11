"""Make every figure show its whole image at every width.

The Framer export draws figures as CSS background images with background-size: cover and a
box whose shape per breakpoint rarely matches the image, so the browser crops the top and
bottom or the sides. This script writes assets/figures.css, which overrides every content
figure on the case study pages so the box always has the image's own aspect ratio and shows
the whole image (background-size: contain).

How a figure is sized depends on its Framer rule, and that can differ per breakpoint:
  width-driven  (width set, height auto or fixed): keep the width, force height auto + aspect-ratio
  height-driven (height: 100% and width: auto, e.g. filmstrip rows): keep the height, force
                width auto + aspect-ratio
So the overrides are emitted inside the same @media blocks the page uses.

Skipped on purpose: home-page card artwork (project cards, Related Links thumbnails) and the
paper-thumbnail Ticker marquees, whose Framer aspect-ratio already equals the image ratio
(verified by the browser audit in wiki/qa.md). Slideshow slides keep the frame height.

Run from anywhere:  python -I tools/fix_figures.py            writes assets/figures.css
                    python -I tools/fix_figures.py --report   inventory only
Also writes tools/out/figure_sizes.json (class -> [w, h]) for the browser audit.
"""
import glob, json, os, re, sys
from html.parser import HTMLParser
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
PAGES = ['index.html'] + sorted(glob.glob('*/index.html'))
VOID = {'img', 'input', 'br', 'meta', 'link', 'hr', 'source', 'wbr', 'area', 'base', 'col', 'embed', 'param', 'track'}


def rd(p): return open(p, encoding='utf-8', newline='').read()


class Walker(HTMLParser):
    """Finds role="img" elements and whether they sit inside a Ticker or a home-page Card."""
    def __init__(self):
        super().__init__(); self.stack = []; self.found = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('role') == 'img' and a.get('class'):
            comps = [s.get('data-component', '') for s in self.stack]
            self.found.append({'classes': a['class'].split(),
                               'ticker': 'Ticker' in comps,
                               'card': any(c in ('Card', 'Card 2') for c in comps)})
        if tag not in VOID: self.stack.append(a)
    def handle_endtag(self, tag):
        if tag not in VOID and self.stack: self.stack.pop()


def css_segments(css):
    """Split a stylesheet into [(media_query or None, body)] at the top level."""
    segs = []; i = 0; n = len(css); base = []
    while i < n:
        j = css.find('@media', i)
        if j < 0: base.append(css[i:]); break
        base.append(css[i:j])
        k = css.find('{', j); depth = 0; m = k
        while m < n:
            if css[m] == '{': depth += 1
            elif css[m] == '}':
                depth -= 1
                if depth == 0: break
            m += 1
        segs.append((css[j:k].strip(), css[k + 1:m]))
        i = m + 1
    return [(None, ''.join(base))] + segs


def rules_in(body):
    return {m.group(1): m.group(2) for m in re.finditer(r'\.([A-Za-z0-9_]+)\{([^}]*)\}', body)}


def driver(decl):
    """'height' if the box is sized by its height (height:100% + width:auto), else 'width'."""
    if decl is None: return None
    h100 = re.search(r'(?<![a-z-])height:100%', decl) is not None
    wauto = re.search(r'(?<![a-z-])width:auto', decl) is not None
    return 'height' if (h100 and wauto) else 'width'


out_base = []; out_media = {}   # media query -> list of rules
sizes = {}; report = []; pinned = set()

for page in PAGES:
    html = rd(page)
    head_css = ''.join(re.findall(r'<style[^>]*>(.*?)</style>', html, flags=re.S))
    segs = css_segments(head_css)
    per_seg = [(mq, rules_in(body)) for mq, body in segs]
    bg = {}
    for _, rules in per_seg:
        for cls, decl in rules.items():
            u = re.search(r"background-image:url\('([^']+)'\)", decl)
            if u and cls not in bg: bg[cls] = u.group(1)
    w = Walker(); w.feed(html)
    for el in w.found:
        cls = next((c for c in el['classes'] if c in bg), None)
        if not cls or cls in pinned: continue
        if page == 'index.html' and el['card']:
            report.append((page, cls, 'skip: home card art')); continue
        path = os.path.normpath(os.path.join(os.path.dirname(page), bg[cls]))
        if not os.path.exists(path):
            report.append((page, cls, f'missing {path}')); continue
        iw, ih = Image.open(path).size
        sizes[cls] = [iw, ih]
        if el['ticker']:
            report.append((page, cls, f'skip: ticker {iw}x{ih}')); continue
        pinned.add(cls)
        common = (f"aspect-ratio:{iw}/{ih};background-size:contain!important;"
                  f"background-repeat:no-repeat!important;background-position:center!important")
        base_driver = driver(per_seg[0][1].get(cls, ''))
        drivers = []
        for mq, rules in per_seg:
            d = driver(rules.get(cls)) or base_driver
            drivers.append(d)
            if d == 'height':
                rule = f".{cls}{{max-width:none!important;{common}}}"
            else:
                rule = f".{cls}{{height:auto!important;min-height:0!important;max-height:none!important;flex-basis:auto!important;{common}}}"
            if mq is None: out_base.append(rule + f" /* {page} {os.path.basename(path)} */")
            else: out_media.setdefault(mq, []).append(rule)
        report.append((page, cls, f'PIN {iw}x{ih} drivers={drivers} {os.path.basename(path)}'))

os.makedirs(os.path.join('tools', 'out'), exist_ok=True)
json.dump(sizes, open(os.path.join('tools', 'out', 'figure_sizes.json'), 'w'), separators=(',', ':'))

if '--report' in sys.argv:
    for p, c, info in report: print(f'{p:22} {c:22} {info}')
    print(len(pinned), 'figure classes pinned')
    sys.exit()

lines = ["/* generated by tools/fix_figures.py: every content figure keeps its image's own aspect ratio",
         "   and shows the whole image at any width. Do not edit by hand; re-run the script. */"]
lines += out_base
for mq, rules in out_media.items():
    lines.append(mq + '{')
    lines += ['  ' + r for r in rules]
    lines.append('}')
lines.append('/* slideshow slides are sized by the frame height; keep that and let width follow the ratio */')
lines.append('.slideshow .slide>[role="img"]{height:100%!important;width:auto!important;flex:0 0 auto!important}')
open('assets/figures.css', 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
print('wrote assets/figures.css:', len(pinned), 'figure classes,', len(out_media), 'media blocks')
