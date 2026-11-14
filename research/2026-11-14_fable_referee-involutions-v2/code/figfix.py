"""One-time label and crossing fixes for proofs/involutions/figures/marked.tex and first.tex.
Not idempotent: it was run once on the files of commit d4cd3f1.
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
F = ROOT / 'proofs/involutions/figures'
B = chr(92)
def cross_pt(w, c, v, d=(-0.5, 0.866)):
    ex, ey = v[0] - c[0], v[1] - c[1]
    cr = lambda a, b, c_, d_: a * d_ - b * c_
    tau = cr(c[0] - w[0], c[1] - w[1], ex, ey) / cr(d[0], d[1], ex, ey)
    return (w[0] + tau * d[0], w[1] + tau * d[1])
x50 = cross_pt((-0.112, -1.905), (-2.067, -1.144), (-0.335, -0.716))
x67 = cross_pt((-0.849, -0.317), (-0.926, 0.145), (-1.535, -0.215))
dot = lambda p: B + 'draw[black,line width=.6pt,fill=black] (%.3f,%.3f) circle[radius=2.2pt];' % p
s = (F / 'marked.tex').read_text()
head, zoom = s.split(B + 'end{tikzpicture}' + B + 'qquad')
zoom = zoom.replace('at (-1.201,-0.930) {$t_{0}$};', 'at (-1.750,-1.320) {$t_{0}$};')
zoom = zoom.replace('at (-1.230,-0.035) {$t_{7}$};', 'at (-1.020,0.380) {$t_{7}$};')
zoom = zoom.replace('densely dashed,thin]', 'densely dashed,line width=.7pt]')
zoom = zoom.replace(B + 'end{tikzpicture}', dot(x50) + '\n' + dot(x67) + '\n' + B + 'end{tikzpicture}')
(F / 'marked.tex').write_text(head + B + 'end{tikzpicture}' + B + 'qquad' + zoom, newline='\n')
s = (F / 'first.tex').read_text()
assert s.count('at (-2.097,0.039) {$t_{0}$};') == 2
s = s.replace('at (-2.097,0.039) {$t_{0}$};', 'at (-3.050,0.350) {$t_{0}$};')
s = s.replace('at (-1.263,0.469) {$w_{3}$};', 'at (-0.550,1.250) {$w_{3}$};' + '\n' + B + 'draw[bfW,line width=.5pt] (-0.95,0.87) -- (-1.263,0.469);' + '\n' + B + 'fill[bfW] (-1.263,0.469) circle[radius=1.3pt];')
(F / 'first.tex').write_text(s, newline='\n')
print(x50, x67)
