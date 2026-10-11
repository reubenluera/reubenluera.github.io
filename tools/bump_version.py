"""Cache-bust helper and text checks for all seven pages.

  python -I tools/bump_version.py --check            report versions, em dashes, footer link counts
  python -I tools/bump_version.py --css v9           set base.css?v=v9 on every page
  python -I tools/bump_version.py --js v9            set site.js?v=v9 on every page
  python -I tools/bump_version.py --og 3             set og.jpg?v=3 on every page
  python -I tools/bump_version.py --hero 4           set hero-qual-quant-*.webp?v=4 on index.html

Files are read and written with newline='' so CRLF / LF endings survive untouched.
"""
import glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
PAGES = ['index.html'] + sorted(glob.glob('*/index.html'))


def rd(p): return open(p, encoding='utf-8', newline='').read()
def wr(p, s): open(p, 'w', encoding='utf-8', newline='').write(s)


def check():
    for f in PAGES:
        t = rd(f)
        css = sorted(set(re.findall(r'base\.css\?v=(\w+)', t)))
        js = sorted(set(re.findall(r'site\.js\?v=(\w+)', t)))
        og = sorted(set(re.findall(r'og\.jpg\?v=(\w+)', t)))
        footers = re.findall(r'<p>Gallery</p></div><div class="[^"]+">(.*?)</div></div>', t)
        links = [v.count('<a ') for v in footers]
        print(f'{f:22} css={css} js={js} og={og} emdash={t.count(chr(0x2014))} fffd={t.count(chr(0xfffd))} footer_links={links}')
    for f in ['assets/base.css', 'assets/site.js']:
        t = rd(f); print(f'{f:22} emdash={t.count(chr(0x2014))}')


def setver(pattern, new, files):
    for f in files:
        t = rd(f); t2 = re.sub(pattern, new, t)
        if t2 != t: wr(f, t2); print('updated', f)


args = sys.argv[1:]
if not args or args[0] == '--check':
    check()
elif args[0] == '--css':
    setver(r'base\.css\?v=\w+', f'base.css?v={args[1]}', PAGES)
elif args[0] == '--js':
    setver(r'site\.js\?v=\w+', f'site.js?v={args[1]}', PAGES)
elif args[0] == '--og':
    setver(r'og\.jpg\?v=\w+', f'og.jpg?v={args[1]}', PAGES)
elif args[0] == '--hero':
    setver(r'(hero-qual-quant-(?:color|sketch)\.webp)\?v=\w+', rf'\1?v={args[1]}', ['index.html'])
else:
    print(__doc__)
