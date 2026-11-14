"""Label fixes for proofs/involutions/figures/{marked,second,paths}.tex.

The committed .tex files are the source of these figures (see proofs/involutions/README.md),
so this script edits them in place. It is idempotent: a file that is already fixed is left alone.

1. marked.tex (zoom panel) and second.tex (both panels): a white-face label drawn as a circle
   on its own point covered the blue cycle edges round a small face. The point becomes a green
   dot, and the circled label moves to the nearest place where it keeps WANT points from every
   drawn segment, vertex and label; a thin leader joins the two. Same device as w_3 in first.tex.
2. paths.tex: normal-size text and wider spacing (the figure used 8 cm of a 15.9 cm block).

Run from anywhere: python fix_involutions.py
"""
import math
import re
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
F = ROOT / 'proofs/involutions/figures'
B = chr(92)
PT = 0.03515          # cm per TeX point
WANT, MIN = 1.5, 0.5  # pt of clearance wanted, and the least accepted
NUM = r'(-?\d+\.?\d*)'
WIDTH = {'bf edge': .4, 'bf spoke': .4, 'bf D': 1.1, 'bf kept': 1.1}
LOG = []


def obstacles(body, unit, skip):
    """Sample discs (x, y, r) in layout units for everything drawn in one tikzpicture."""
    u = lambda p: p * PT / unit
    obs = []
    seg = re.compile(r'\\draw\[(.*?)\] \(' + NUM + ',' + NUM + r'\) -- \(' + NUM + ',' + NUM + r'\);')
    for st, x0, y0, x1, y1 in seg.findall(body):
        p, q = np.array([float(x0), float(y0)]), np.array([float(x1), float(y1)])
        w = WIDTH.get(st, .7)
        for t in np.linspace(0, 1, int(np.hypot(*(q - p)) / u(1)) + 2):
            obs.append((*(p + t * (q - p)), u(w / 2)))
        if st == 'bf D':                                   # arrowhead
            e = (p - q) / np.hypot(*(p - q))
            obs.append((*(q + u(4.5) * e), u(3.0)))
    for x, y, r in re.findall(r'\(' + NUM + ',' + NUM + r'\) circle\[radius=' + NUM + r'pt\]', body):
        obs.append((float(x), float(y), u(float(r) + .3)))
    node = re.compile(r'\\node\[(.*?)\] at \(' + NUM + ',' + NUM + r'\) \{\$(\w)_\{(\d+)\}\$\};')
    for st, x, y, letter, idx in node.findall(body):
        if (letter, idx) == skip:
            continue
        hw, hh = u(4 + 2 * len(idx) + 1.5), u(5.5)
        for a in np.linspace(-hw, hw, 7):
            for b in np.linspace(-hh, hh, 5):
                obs.append((float(x) + a, float(y) + b, 0))
    return np.array(obs)


def fix_panel(body, name, k):
    m = re.search(r'x=' + NUM + 'cm', body)
    unit = float(m.group(1))
    u = lambda p: p * PT / unit
    bb = re.search(r'use as bounding box\] \(' + NUM + ',' + NUM + r'\) rectangle \(' + NUM + ',' + NUM + r'\)', body)
    x0, y0, x1, y1 = map(float, bb.groups())
    node = re.compile(r'\\node\[draw=bfW,circle,fill=white,inner sep=1pt,font=\\footnotesize\] at \(' + NUM + ',' + NUM + r'\) \{\$w_\{(\d+)\}\$\};')
    for x, y, idx in node.findall(body):
        line = node.search(body, body.index('at (%s,%s) {$w_{%s}$}' % (x, y, idx)) - 80).group(0)
        o = np.array([float(x), float(y)])
        obs = obstacles(body.replace(line, ''), unit, ('w', idx))
        rad = u(math.hypot(3.6 + 2.0 * len(idx), 3.4) + 1.4)     # radius of the circled label
        clear = lambda c: float(np.min(np.hypot(obs[:, 0] - c[0], obs[:, 1] - c[1]) - obs[:, 2]) - rad) / u(1)
        here = clear(o)
        if here >= MIN:
            LOG.append((name, k, 'w_' + idx, 'kept', round(here, 2), 0.0))
            continue
        best = None
        for d in np.arange(4, 60, .5):
            for th in np.arange(0, 360, 5):
                c = o + u(d) * np.array([math.cos(math.radians(th)), math.sin(math.radians(th))])
                if not (x0 + rad < c[0] < x1 - rad and y0 + rad < c[1] < y1 - rad):
                    continue
                cl = clear(c)
                if best is None or cl > best[0]:
                    best = (cl, d, c)
            if best and best[0] >= WANT:
                break
        cl, d, c = best
        assert cl >= MIN, (name, idx, cl)
        e = (c - o) / np.hypot(*(c - o))
        end = c - rad * e
        new = (B + 'draw[bfW,line width=.5pt] (%.3f,%.3f) -- (%.3f,%.3f);\n' % (*end, *o)
               + B + 'fill[bfW] (%.3f,%.3f) circle[radius=1.3pt];\n' % tuple(o)
               + B + 'node[draw=bfW,circle,fill=white,inner sep=1pt,font=' + B + 'footnotesize] at (%.3f,%.3f) {$w_{%s}$};' % (*c, idx))
        body = body.replace(line, new)
        LOG.append((name, k, 'w_' + idx, 'moved', round(cl, 2), float(d)))
    return body


def zoom(name):
    s = (F / name).read_text(encoding='utf-8')
    parts = s.split(B + 'begin{tikzpicture}')
    out = [parts[0]]
    for k, body in enumerate(parts[1:]):
        # the overview panel of marked.tex (x=0.42cm) carries no labels
        out.append(fix_panel(body, name, k))
    (F / name).write_text((B + 'begin{tikzpicture}').join(out), encoding='utf-8', newline='\n')


def paths():
    s = (F / 'paths.tex').read_text(encoding='utf-8')
    old = B + 'begin{tikzpicture}[bf,x=1.6cm,y=1cm]'
    if old not in s:
        LOG.append(('paths.tex', 0, '', 'already fixed', None, None))
        return
    s = s.replace(old, B + 'begin{tikzpicture}[bf,x=2.3cm,y=1.15cm,every node/.append style={font=' + B + 'normalsize,inner sep=1.6pt}]')
    s = s.replace('-0.55) {', '-0.62) {').replace('-2.35) {', '-2.42) {')
    (F / 'paths.tex').write_text(s, encoding='utf-8', newline='\n')
    LOG.append(('paths.tex', 0, '', 'normalsize text, x=2.3cm', None, None))


if __name__ == '__main__':
    zoom('marked.tex')
    zoom('second.tex')
    paths()
    for row in LOG:
        print(row)
