"""Check the built atlas. Run after build.py, from the repository root:

    python digestions/atlas/verify.py

It re-runs every figure function (and with it every assertion on a drawn
object), then checks the texts, the figure sizes, the TeX log and the PDF.
Writes audit.json. Exits non-zero on the first failed check.
"""
import sys, json, re, hashlib
sys.dont_write_bytecode = True
from pathlib import Path
O = Path(__file__).resolve().parent
sys.path.insert(0, str(O))
import fitz
import lib
import figs_chain, figs_algebra, figs_order, figs_scope      # noqa: F401
import pages

TW = 15.92
fails = []


def check(ok, msg):
    if not ok:
        fails.append(msg)
        print('FAIL', msg)


P = pages.PAGES
num = {p['slug']: i + 1 for i, p in enumerate(P)}
lib.NUM.update(num)

# 1. every drawn object: the figure functions carry the assertions
for p in P:
    check(p['slug'] in lib.FIGS, f'no figure for {p["slug"]}')
    lib.FIGS[p['slug']]()
check(set(lib.CERT) >= {p['slug'] for p in P if p['slug'] not in ('chain', 'sum')}, 'a figure wrote no certificate')

# 2. texts: length, no internal tags, no file paths, no dashes used as punctuation
TAGS = re.compile(r'PROVED-HERE|\bLIT\b|COMPUTED|CONJECTURE|HUNCH|REFUTED|\bT[1-4]\b')
PATHS = re.compile(r'[\w-]+/[\w./-]+|\.(py|md|json|tex|txt)\b')
words = {}
for p in P:
    body = re.sub(r'\$[^$]*\$', 'x', re.sub(r'\\[a-zA-Z]+', ' ', p['text'] + ' ' + p['status']))
    n = len(body.split())
    words[p['slug']] = n
    check(80 <= n <= 150, f'{p["slug"]}: {n} words')
    raw = p['text'] + ' ' + p['status'] + ' ' + p['title']
    check(not TAGS.search(raw), f'{p["slug"]}: internal status tag in the text')
    check(not PATHS.search(raw), f'{p["slug"]}: file path in the text')
    check('---' not in raw and '—' not in raw and '–' not in raw, f'{p["slug"]}: dash used as punctuation')
    check(p['sources'], f'{p["slug"]}: no sources')
    for q in p['see']:
        check(q in num, f'{p["slug"]}: dangling cross-reference {q}')
figtex = ''.join((O / 'figs' / f'{num[p["slug"]]:02d}-{p["slug"]}.tex').read_text(encoding='utf8') for p in P)
check(not TAGS.search(figtex), 'internal status tag inside a figure')

# 3. figures: one vector PDF per page, width between 0.75 and 0.95 of the text width
sizes = {}
for p in P:
    f = O / 'figs' / f'{num[p["slug"]]:02d}-{p["slug"]}.pdf'
    check(f.exists(), f'missing {f.name}')
    d = fitz.open(f)
    w = d[0].rect.width / 72 * 2.54
    sizes[p['slug']] = round(w / TW, 3)
    check(0.75 <= w / TW <= 0.95, f'{p["slug"]}: figure width {w / TW:.3f} of the text width')
    check(not d[0].get_images(), f'{p["slug"]}: raster image in a figure')
    d.close()

# 4. the TeX log: no errors, no overfull box beyond 2pt
log = (O / 'atlas.log').read_text(errors='replace')
check('! ' not in log, 'TeX error in atlas.log')
over = [float(x) for x in re.findall(r'Overfull \\[hv]box \(([\d.]+)pt too', log)]
check(all(x <= 2 for x in over), f'overfull boxes: {over}')
check('undefined' not in log.lower() or 'There were undefined references' not in log, 'undefined references')

# 5. the PDF: contents, one page per route, sources; every route page has its figure and fits
doc = fitz.open(O / 'atlas.pdf')
check(len(doc) >= len(P) + 2, 'too few pages')
check(len(doc) <= len(P) + 3, 'a route page overflowed onto a second page')
for i, p in enumerate(P, 1):
    text = doc[i].get_text()
    check(text.lstrip().startswith(str(i)), f'page {i} does not start with its number')
    check('See also' in text, f'page {i}: the page does not end on the same sheet')
    check(len(doc[i].get_drawings()) > 20, f'page {i}: no figure')
    used = max(b[3] for b in doc[i].get_text('blocks')) - min(b[1] for b in doc[i].get_text('blocks'))
check((O / 'pages').exists() and len(list((O / 'pages').glob('*.pdf'))) == len(doc), 'per-page PDFs missing')

sha = lambda f: hashlib.sha256(f.read_bytes()).hexdigest()[:16]
(O / 'audit.json').write_text(json.dumps(dict(
    command='python digestions/atlas/verify.py', passed=not fails, failures=fails, pages=len(doc), routes=len(P),
    words=words, figure_width_over_textwidth=sizes, overfull_pt=over,
    toolkit_sha256={f.name: sha(f) for f in sorted((O / 'toolkit').glob('*')) if f.is_file()}), indent=1), encoding='utf8')
print('checked', len(P), 'routes,', len(doc), 'pages:', 'all checks passed' if not fails else f'{len(fails)} failures')
sys.exit(1 if fails else 0)
