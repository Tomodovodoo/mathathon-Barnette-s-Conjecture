"""Rebuild proofs/involutions/figures/second.tex: a token move of the second map (object 2 -> object 6).

    python research/2026-11-14_fable_referee-involutions-v2/code/figure2.py
The base drawing (triangulation, arrows of D, selected spokes of pair 0) is the left panel of the
previous second.tex, read from git commit d4cd3f1. Tokens and crossings come from running.py:
object 2 = pair 0 with tokens 5:0 and 16:11, image object 6 = pair 0 with tokens 5:7 and 16:11.
"""
import subprocess, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
old = subprocess.run(['git', 'show', 'd4cd3f1:proofs/involutions/figures/second.tex'], capture_output=True, text=True, cwd=ROOT).stdout
panel = old.split(r'\end{tikzpicture}')[0].splitlines()
base = [l for l in panel[2:] if 'bf kept' not in l and 'bfW' not in l and not l.startswith(r'\node')]
V = {0: (-4.330, -2.500), 1: (-1.535, -0.215), 2: (-2.215, -0.099), 3: (-1.908, 0.944), 4: (0.0, 5.0), 5: (4.330, -2.500),
     6: (-0.335, -0.716), 7: (-0.677, -0.021), 8: (-0.565, 0.672), 9: (-1.086, 1.376), 10: (-0.293, 1.953),
     11: (0.477, 0.764), 12: (-0.275, 0.175)}
bary = lambda f: tuple(sum(V[v][i] for v in f) / 3 for i in (0, 1))
W = {5: bary((0, 6, 5)), 16: bary((6, 12, 11))}
D = (-0.5, 0.866)                                  # image of the vertical direction of the exact layout
SP = {0: (bary((0, 1, 6)), V[6]), 7: (bary((1, 8, 7)), V[1]), 11: (bary((3, 4, 9)), V[9])}   # centre -> s(t), pair 0
for t, (c, v) in SP.items():                       # each must be a drawn spoke of the old panel
    assert any('bf spoke' in l and '(%.3f,%.3f) -- (%.3f,%.3f)' % (c + v) in l for l in base), t
def hit(w, t):
    (cx, cy), (vx, vy) = SP[t]; ex, ey = vx - cx, vy - cy
    wx, wy = W[w]; cr = lambda a, b, c, d: a * d - b * c
    tau = cr(cx - wx, cy - wy, ex, ey) / cr(D[0], D[1], ex, ey)
    mu = cr(wx - cx, wy - cy, D[0], D[1]) / cr(ex, ey, D[0], D[1])
    assert tau > 0 and 0 < mu < 1
    return (wx + tau * D[0], wy + tau * D[1])
X = {(5, 0): hit(5, 0), (5, 7): hit(5, 7), (16, 11): hit(16, 11)}
pt = lambda p: '(%.3f,%.3f)' % p
def make(tokens):
    out = [r'\begin{tikzpicture}[baseline=(current bounding box.center),bf,x=1.4cm,y=1.4cm]',
           r'\path[use as bounding box] (-2.6,-2.25) rectangle (1.0,2.75);\clip (-2.6,-2.25) rectangle (1.0,2.75);'] + base
    for w in (5, 16):
        end = (W[w][0] + 7 * D[0], W[w][1] + 7 * D[1])
        out.append(r'\draw[bfW,densely dashed,line width=.7pt] %s -- %s;' % (pt(W[w]), pt(end)))
    for (w, t) in tokens:
        out.append(r'\draw[bf kept] %s -- %s;' % (pt(SP[t][0]), pt(SP[t][1])))
    for key, p in X.items():
        style = 'fill=black' if key in tokens else 'fill=white'
        out.append(r'\draw[black,line width=.6pt,%s] %s circle[radius=2.2pt];' % (style, pt(p)))
    for w, anchor in ((5, 'west'), (16, 'west')):
        out.append(r'\node[draw=bfW,circle,fill=white,inner sep=1pt,font=\footnotesize] at %s {$w_{%d}$};' % (pt(W[w]), w))
    lab = {0: ((-1.75, -1.32), 't_0'), 7: ((-1.02, 0.38), 't_7'), 11: ((-0.72, 2.50), 't_{11}')}
    for t, (p, name) in lab.items():
        out.append(r'\node[fill=white,font=\footnotesize,inner sep=.6pt] at %s {$%s$};' % (pt(p), name))
    out.append(r'\end{tikzpicture}')
    return '\n'.join(out)
tex = make([(5, 0), (16, 11)]) + r'\quad$\longleftrightarrow$\quad' + make([(5, 7), (16, 11)]) + '\n'
(ROOT / 'proofs/involutions/figures/second.tex').write_text(tex, newline='\n')
print('crossings', {k: tuple(round(x, 3) for x in v) for k, v in X.items()})
