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
import figs_chain, figs_algebra, figs_order, figs_scope, figs_proofs      # noqa: F401
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

# 1b. the numbers that page texts quote from the certificates
C = lib.CERT
k = C['keystep']
check(k['height_jump_checks'] == 176 and k['flux_checks'] == 16, 'keystep: number of checked height jumps or cut fluxes changed')
check((k['sigma_paper'], k['primal_coefficient'], k['marked_signed_total'], k['unpaired_objects'], k['marked_objects']) == (18, 9, -9, 9, 43), 'keystep: the three totals changed')
check(abs(k['sigma_paper']) == 2 * k['product_sum'] and abs(k['primal_coefficient']) == k['product_sum'] == abs(k['marked_signed_total']), 'keystep: the three proofs disagree')
b = C['blueprint']
check(b['route_statements'] == 34 and b['counts'] == {'exact': 4, 'form': 25, 'none': 5}, 'blueprint: counts differ from the page text')
check(b['advisory_recount'] == {'exact': 5, 'form': 27, 'none': 2} and len(b['moved_by_recount']) == 3, 'blueprint: recount differs from the page text')
u = C['induction']['unrepaired_lifts']
check(u['rows'] == 466 and u['shape']['two trees, a with v1 and b with v2'] == 466, 'induction: the 466 unrepaired lifts do not share one shape')
check([p['slug'] for p in P] == pages.ORDER, 'page order differs from pages.ORDER')

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
check(doc[len(P) + 1].get_text().lstrip().startswith('Sources'), 'a route page overflowed onto a second page')
check(all(str(k) in doc[0].get_text() for k in range(1, len(P) + 1)) and len(doc[0].get_images(full=True)) + len(doc[0].get_drawings()) > 30 * 20, 'contents page lacks a thumbnail')
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
