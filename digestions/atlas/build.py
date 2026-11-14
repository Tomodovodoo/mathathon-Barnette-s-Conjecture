"""Build the route atlas. Run from the repository root:

    python digestions/atlas/build.py            # everything
    python digestions/atlas/build.py lattice    # only figures whose slug contains 'lattice', then the atlas

Steps: compute and assert every drawn object (lib.py, figs_*.py), write one
standalone TikZ file per figure in figs/, compile the changed ones, write
atlas.tex from pages.py, compile it twice, split it into pages/NN-slug.pdf,
and render every page to PNG in renders/.
"""
import sys, subprocess, hashlib, json, os, re, shutil
sys.dont_write_bytecode = True
from pathlib import Path
O = Path(__file__).resolve().parent
sys.path.insert(0, str(O))
import fitz
import lib
import figs_chain, figs_algebra, figs_order, figs_scope       # noqa: F401  (they register figures)
import pages

FD = O / 'figs'
FD.mkdir(exist_ok=True)
ENV = dict(os.environ, TEXINPUTS=f'{O};{O / "toolkit"};')
only = sys.argv[1:]
PAGES = pages.PAGES
num = {p['slug']: i + 1 for i, p in enumerate(PAGES)}
lib.NUM.update(num)


def latex(tex, cwd):
    res = subprocess.run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error', tex.name], cwd=cwd, env=ENV,
                         capture_output=True, text=True, errors='replace')
    if res.returncode:
        print(res.stdout[-3000:])
        raise SystemExit(f'pdflatex failed on {tex.name}')


widths = {}
for p in PAGES:
    slug = p['slug']
    name = f'{num[slug]:02d}-{slug}'
    tex = FD / f'{name}.tex'
    if slug not in lib.FIGS:
        raise SystemExit(f'no figure for page {slug}')
    if only and not any(o in slug for o in only) and tex.with_suffix('.pdf').exists():
        continue
    body = lib.FIGS[slug]()
    src = ('\\documentclass[10pt,border=1pt]{standalone}\n\\usepackage{amsmath,amssymb,booktabs}\n\\usepackage{atlas-figs}\n\\begin{document}%\n'
           + body + '%\n\\end{document}\n')
    for old in FD.glob(f'*-{slug}.*'):
        if not old.name.startswith(name + '.'):
            old.unlink()
    if not tex.exists() or tex.read_text(encoding='utf8') != src or not tex.with_suffix('.pdf').exists():
        tex.write_text(src, encoding='utf8')
        latex(tex, FD)
        print('figure', name)
for p in PAGES:
    name = f'{num[p["slug"]]:02d}-{p["slug"]}'
    d = fitz.open(FD / f'{name}.pdf')
    widths[p['slug']] = (round(d[0].rect.width / 72 * 2.54, 2), round(d[0].rect.height / 72 * 2.54, 2))
    d.close()

(O / 'computed.json').write_text(json.dumps(lib.plain(lib.CERT), indent=1), encoding='utf8')

# ---------------------------------------------------------------------------
HEAD = r'''\documentclass[10pt,a4paper]{article}
\usepackage[left=1in,right=1in,top=19mm,bottom=24mm,footskip=11mm]{geometry}
\usepackage[T1]{fontenc}
\usepackage{lmodern,amsmath,amssymb,graphicx,booktabs,longtable,array,url}
\usepackage[hidelinks]{hyperref}
\frenchspacing\raggedbottom\setlength{\parindent}{0pt}\emergencystretch=2em
\newcommand{\routetitle}[3]{\noindent{\Large\bfseries #1\quad #2}\hfill{\small #3}\par\vspace{1mm}\hrule\vspace{0mm}}
\newcommand{\figcap}[1]{\par\smallskip{\centering\begin{minipage}{.94\textwidth}\small\centering #1\end{minipage}\par}}
\begin{document}
'''


def srctex(text):
    r"""Wrap path-like words in \path so they break and need no escaping."""
    words = []
    for w in text.split(' '):
        core = w.rstrip(',;)')
        tail = w[len(core):]
        lead = '(' if core.startswith('(') else ''
        core = core[len(lead):]
        if '/' in core or '_' in core or re.search(r'[.](py|md|json|pdf|txt)$', core):
            words.append(lead + r'\path{' + core + '}' + tail)
        else:
            words.append(w)
    return ' '.join(words)


def see(p):
    return ', '.join(f'{num[q]} ({pages.SHORT[q]})' for q in p['see'] if q in num)


out = [HEAD, r'\thispagestyle{empty}\setcounter{page}{0}',
       r'\noindent{\LARGE\bfseries An atlas of proof routes for Barnette\textquotesingle s conjecture}\par\medskip',
       r'\noindent ' + pages.INTRO + r'\par\vfill']
cols = 5
cells = []
for p in PAGES:
    name = f'{num[p["slug"]]:02d}-{p["slug"]}'
    cells.append(r'\begin{minipage}[t]{2.95cm}\centering\includegraphics[width=2.75cm,height=2.35cm,keepaspectratio]{figs/' + name + r'.pdf}\\[.3mm]'
                 r'\footnotesize\raggedright\hyperlink{r' + str(num[p['slug']]) + r'}{\textbf{' + str(num[p['slug']]) + r'}\ ' + pages.SHORT[p['slug']].capitalize() + r'}\end{minipage}')
rows = [' & '.join(cells[i:i + cols]) for i in range(0, len(cells), cols)]
out.append(r'\noindent\begin{tabular}{@{}' + 'c@{\\hspace{2.9mm}}' * (cols - 1) + 'c@{}}\n' + '\\\\[2.2mm]\n'.join(rows) + '\n\\end{tabular}\\par\\vfill')
for p in PAGES:
    k = num[p['slug']]
    name = f'{k:02d}-{p["slug"]}'
    out.append(r'\clearpage\hypertarget{r' + str(k) + r'}{}\routetitle{' + str(k) + '}{' + p['title'] + '}{' + p['group'] + '}')
    out.append(r'\vfill{\centering\includegraphics{figs/' + name + r'.pdf}\par}')
    if p.get('caption'):
        out.append(r'igcap{' + p['caption'] + '}')
    out.append(r'\vfill\vfill ' + p['text'] + r'\par\smallskip ' + p['status'] + r'\par\vfill')
    out.append(r'{\small\textbf{See also}\quad ' + see(p) + r'.\par}')
out.append(r'\clearpage\noindent{\Large\bfseries Sources}\par\vspace{1mm}\hrule\medskip')
out.append(r'{\small ' + pages.SOURCES_INTRO + r'\par}\medskip')
out.append(r'{\footnotesize\setlength{\tabcolsep}{3pt}\begin{longtable}{@{}r>{\raggedright\arraybackslash}p{3.6cm}>{\raggedright\arraybackslash}p{11.2cm}@{}}\toprule')
out.append(r'& Page & Sources and computation\\\midrule\endhead')
for p in PAGES:
    src = '; '.join(srctex(s_) for s_ in p['sources'])
    out.append(f'{num[p["slug"]]} & {pages.SHORT[p["slug"]].capitalize()} & {src}\\\\[.6mm]')
out.append(r'\bottomrule\end{longtable}}')
out.append(r'\end{document}')
(O / 'atlas.tex').write_text('\n'.join(out) + '\n', encoding='utf8')
latex(O / 'atlas.tex', O)
latex(O / 'atlas.tex', O)

# split and render
PD = O / 'pages'
RD = O / 'renders'
for d in (PD, RD):
    shutil.rmtree(d, ignore_errors=True)
    d.mkdir()
doc = fitz.open(O / 'atlas.pdf')
names = ['00-contents'] + [f'{num[p["slug"]]:02d}-{p["slug"]}' for p in PAGES]
overflow = len(doc) > len(PAGES) + 3
if overflow:
    print('WARNING: some page overflowed; pages are named by position')
    names = [f'p{i:02d}' for i in range(len(doc))]
else:
    names += [f'{len(PAGES) + 1 + i:02d}-sources' + (f'-{i + 1}' if i else '') for i in range(len(doc) - len(names))]
for i, nm in enumerate(names):
    one = fitz.open()
    one.insert_pdf(doc, from_page=i, to_page=i)
    one.save(PD / f'{nm}.pdf')
    doc[i].get_pixmap(dpi=110).save(RD / f'{nm}.png')
(O / 'manifest.json').write_text(json.dumps(dict(
    command='python digestions/atlas/build.py',
    pages=[dict(n=num[p['slug']], slug=p['slug'], title=p['title'], figure_cm=widths[p['slug']],
                words=len(re.sub(r'\$[^$]*\$', 'x', re.sub(r'\\[a-zA-Z]+', ' ', p['text'] + ' ' + p['status'])).split())) for p in PAGES],
    pdf_pages=len(doc)), indent=1), encoding='utf8')
print('atlas.pdf', len(doc), 'pages')
if overflow:
    raise SystemExit('a page overflowed')
