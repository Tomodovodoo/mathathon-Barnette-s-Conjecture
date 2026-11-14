"""Generate the TikZ figures of paper/draft-B that are drawn on the running example.

Run from the repository root:
    python research/2026-11-14_opus_manuscript-B/figs.py

Reads paper/figures/running.json and layout-running.json (read only) and writes
paper/draft-B/figures/fig-*.tex (tikzpicture bodies; the document sets the
scale). Every drawn object is recomputed here and asserted against the numbers
in example.txt.
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'paper/draft-B/figures'
OUT.mkdir(parents=True, exist_ok=True)
data = json.load(open(ROOT / 'paper/figures/running.json'))
lay = json.load(open(ROOT / 'paper/figures/layout-running.json'))
F = [tuple(f) for f in data['faces']]
t0 = data['t0']
xy = {int(k): tuple(v) for k, v in lay['coordinates'].items()}
R = lay['R']
ang = {int(k): v for k, v in lay['root_angles'].items()}
roots = list(F[t0])
V = sorted(xy)
left = {}
for i, f in enumerate(F):
    for a, b in zip(f, f[1:] + f[:1]):
        left[a, b] = i
E = sorted({tuple(sorted(k)) for k in left})
black = [0, 2, 4, 7, 9, 11, 13, 15, 17, 19, 21]
white = [i for i in range(len(F)) if i not in black]
A = [t for t in black if t != t0]
outer_edges = {tuple(sorted((a, b))) for a, b in zip(F[t0], F[t0][1:] + F[t0][:1])}
e0 = tuple(sorted(data['e0']))


def fmt(p):
    return f'({p[0]:.3f},{p[1]:.3f})'


def arcmid(e):
    a, b = e
    x, y = ang[a], ang[b]
    # the arc not containing the third root
    (c,) = [r for r in roots if r not in e]
    z = ang[c]
    lo, hi = sorted((x, y))
    mid = (lo + hi) / 2
    if lo < z < hi:
        mid += 180
    return (R * math.cos(math.radians(mid)), R * math.sin(math.radians(mid))), mid


def edge_mid(e):
    e = tuple(sorted(e))
    if e in outer_edges:
        return arcmid(e)[0]
    a, b = e
    return ((xy[a][0] + xy[b][0]) / 2, (xy[a][1] + xy[b][1]) / 2)


def arc_cmd(e):
    a, b = tuple(sorted(e))
    _, mid = arcmid(e)
    sa, sb = ang[a], ang[b]
    # go from a to b through mid
    def norm(t):
        return t % 360
    # choose start/end so that the arc passes through mid
    s, t = sa, sb
    if not (min(s, t) < mid < max(s, t)):
        if s < t:
            s += 360
        else:
            t += 360
    return f'{fmt(xy[a])} arc[start angle={s:.1f}, end angle={t:.1f}, radius={R}]'


def centre(i):
    f = F[i]
    if i == t0:
        return (0.0, -5.75)
    rs = [v for v in f if v in roots]
    if len(rs) == 2:
        (v,) = [v for v in f if v not in roots]
        m, _ = arcmid(tuple(sorted(rs)))
        return (0.62 * m[0] + 0.38 * xy[v][0], 0.62 * m[1] + 0.38 * xy[v][1])
    return (sum(xy[v][0] for v in f) / 3, sum(xy[v][1] for v in f) / 3)


def base(lines, shade_black=True, labels=False):
    lines.append(r'\fill[gray!22, even odd rule] (0,0) circle (5.55) (0,0) circle (5);')
    if shade_black:
        for t in A:
            a, b, c = F[t]
            lines.append(rf'\fill[gray!22] {fmt(xy[a])}--{fmt(xy[b])}--{fmt(xy[c])}--cycle;')
    for e in E:
        if e in outer_edges:
            lines.append(rf'\draw[gray!70, line width=0.4pt] {arc_cmd(e)};')
        else:
            lines.append(rf'\draw[gray!70, line width=0.4pt] {fmt(xy[e[0]])}--{fmt(xy[e[1]])};')


def vertices(lines, labels=False, label_set=None):
    for v in V:
        if v in roots:
            lines.append(rf'\draw[fill=white, line width=0.6pt] {fmt(xy[v])} circle (0.16);')
        else:
            lines.append(rf'\fill {fmt(xy[v])} circle (0.09);')
    if labels:
        for v in (label_set or V):
            x, y = xy[v]
            # push label away from the centre of mass of neighbours
            nb = [w for e in E if v in e for w in e if w != v]
            mx = sum(xy[w][0] for w in nb) / len(nb)
            my = sum(xy[w][1] for w in nb) / len(nb)
            dx, dy = x - mx, y - my
            norm = math.hypot(dx, dy) or 1
            if v in roots:
                dx, dy, norm = x, y, math.hypot(x, y)
                p = (x + 0.75 * dx / norm, y + 0.75 * dy / norm)
            else:
                p = (x + 0.42 * dx / norm, y + 0.42 * dy / norm)
            lines.append(rf'\node[font=\footnotesize, inner sep=0pt] at {fmt(p)} {{${v}$}};')


def wedge(lines, t, v, style):
    """sector at corner v of triangle t"""
    a, b = [w for w in F[t] if w != v]
    x, y = xy[v]
    th1 = math.degrees(math.atan2(xy[a][1] - y, xy[a][0] - x))
    th2 = math.degrees(math.atan2(xy[b][1] - y, xy[b][0] - x))
    d = (th2 - th1) % 360
    if d > 180:
        th1, th2 = th2, th1
        d = 360 - d
    rho = 0.55
    lines.append(rf'\draw[{style}] {fmt((x, y))} -- ++({th1:.1f}:{rho}) arc[start angle={th1:.1f}, delta angle={d:.1f}, radius={rho}] -- cycle;')


S_WEDGE = 'fill=sblue, draw=sblue, line width=0.3pt'
R_WEDGE = 'fill=white, draw=rorange, line width=0.7pt'

# the displayed pair (#6 in example.txt) and its cancellation partner (#5)
r6 = dict(zip(A, (6, 2, 8, 1, 3, 10, 11, 7, 12, 9)))
s6 = dict(zip(A, (1, 3, 7, 2, 9, 11, 6, 12, 8, 10)))
r5 = dict(zip(A, (6, 2, 1, 9, 3, 10, 11, 7, 12, 8)))


def third(t, a, b):
    (c,) = [v for v in F[t] if v not in (a, b)]
    return c


def Q(s):
    return {t: tuple(v for v in F[t] if v != s[t]) for t in A}


def arrow(lines, a, b, style, shorten=0.13):
    lines.append(rf'\draw[{style}, shorten >={shorten}cm, shorten <={shorten}cm] {fmt(xy[a])}--{fmt(xy[b])};')


def write(name, lines):
    (OUT / f'{name}.tex').write_text('\n'.join(lines) + '\n', encoding='utf8')
    print('wrote', name)


# ---------------------------------------------------------------- cancellation
def cancel_panel(r, s, title):
    lines = []
    base(lines)
    qcyc_faces = [7, 9, 21]
    cyc = [8, 1, 9]
    # tint the white face enclosed by the Q_s cycle
    lines.append(rf'\fill[rorange!18] {fmt(xy[8])}--{fmt(xy[1])}--{fmt(xy[9])}--cycle;')
    q = Q(s)
    for t in A:
        a, b = q[t]
        if t in qcyc_faces:
            # directed from r(t) to the third corner u(t)
            u = third(t, r[t], s[t])
            arrow(lines, r[t], u, 'rorange, line width=1.1pt, dash pattern=on 3pt off 1.5pt, -{Stealth[length=4.5pt]}')
        else:
            lines.append(rf'\draw[rorange, line width=1.0pt, dash pattern=on 3pt off 1.5pt] {fmt(xy[a])}--{fmt(xy[b])};')
    for t in A:
        wedge(lines, t, r[t], R_WEDGE)
        wedge(lines, t, s[t], S_WEDGE)
    vertices(lines, labels=True, label_set=[1, 8, 9])
    return lines


write('fig-cancel-a', cancel_panel(r6, s6, 'a'))
write('fig-cancel-b', cancel_panel(r5, s6, 'b'))

# ---------------------------------------------------------------- white faces inside D-cycles
lines = []
base(lines)
long_cyc = [6, 1, 2, 3, 9, 10, 11]      # ccw
tri = [8, 7, 12]                         # cw
inside_long = [6, 8, 10, 16, 18, 20]
inside_tri = [18]
for w in inside_long:
    a, b, c = F[w]
    col = 'sblue!45' if w in inside_tri else 'sblue!18'
    lines.append(rf'\fill[{col}] {fmt(xy[a])}--{fmt(xy[b])}--{fmt(xy[c])}--cycle;')
# re-draw edges on top of tint
for e in E:
    if e not in outer_edges:
        lines.append(rf'\draw[gray!70, line width=0.4pt] {fmt(xy[e[0]])}--{fmt(xy[e[1]])};')
for cyc in (long_cyc, tri):
    for a, b in zip(cyc, cyc[1:] + cyc[:1]):
        arrow(lines, a, b, 'sblue, line width=1.1pt, -{Stealth[length=4.5pt]}')
# spoke route of the triangle cycle: tail -> centre -> head, for faces supplying it
for a, b in zip(tri, tri[1:] + tri[:1]):
    t = [f for f in A if a in F[f] and b in F[f]][0]
    c = centre(t)
    lines.append(rf'\draw[black, line width=0.6pt, densely dotted] {fmt(xy[a])}--{fmt(c)}--{fmt(xy[b])};')
    lines.append(rf'\fill {fmt(c)} rectangle +(0.001,0.001);')
    lines.append(rf'\fill[black] ({c[0]-0.07:.3f},{c[1]-0.07:.3f}) rectangle ({c[0]+0.07:.3f},{c[1]+0.07:.3f});')
for w in inside_long:
    if w in inside_tri:
        continue
    p = centre(w)
    lines.append(rf'\node[font=\scriptsize, text=sblue!70!black] at {fmt(p)} {{$\circ$}};')
vertices(lines, labels=True, label_set=long_cyc + tri)
write('fig-whitefaces', lines)

# ---------------------------------------------------------------- recovery
s = r6                                   # the good state: second state of the forest pair (s6, r6)
q = Q(s)
a0, b0 = e0
(c0,) = [v for v in roots if v not in e0]
S = {tuple(sorted(e)) for e in q.values()} | {tuple(sorted((a0, c0))), tuple(sorted((b0, c0)))}
assert len(S) == len(V) - 1
Yedges = [e for e in E if e not in S]
assert len(Yedges) == len(F) - 1
# root Y at t0
adj = {i: [] for i in range(len(F))}
for e in Yedges:
    i, k = left[e], left[e[1], e[0]]
    adj[i].append((k, e)); adj[k].append((i, e))
parent = {t0: None}
order = [t0]
for x in order:
    for y, e in adj[x]:
        if y not in parent:
            parent[y] = (x, e); order.append(y)
assert len(order) == len(F)
P = {parent[y][1] for y in white}
expected_P = {(0, 2), (0, 4), (0, 6), (1, 9), (3, 9), (5, 11), (6, 7), (7, 8), (9, 10), (10, 11), (11, 12)}
assert P == expected_P, P


def draw_Y(lines, directed=False):
    for e in Yedges:
        i, k = left[e], left[e[1], e[0]]
        m = edge_mid(e)
        if i == t0 or k == t0:
            other = k if i == t0 else i
            lines.append(rf'\draw[ygreen, line width=0.8pt, dash pattern=on 2.5pt off 1pt on 0.6pt off 1pt] {fmt(centre(other))}--{fmt(m)}--{fmt(centre(t0))};')
        else:
            lines.append(rf'\draw[ygreen, line width=0.8pt, dash pattern=on 2.5pt off 1pt on 0.6pt off 1pt] {fmt(centre(i))}--{fmt(m)}--{fmt(centre(k))};')
    for i in range(len(F)):
        p = centre(i)
        if i in black:
            lines.append(rf'\fill[ygreen!60!black] ({p[0]-0.1:.3f},{p[1]-0.1:.3f}) rectangle ({p[0]+0.1:.3f},{p[1]+0.1:.3f});')
        else:
            lines.append(rf'\draw[ygreen!60!black, fill=white, line width=0.6pt] {fmt(p)} circle (0.12);')


lines = []
base(lines)
for e in S:
    if e in outer_edges:
        lines.append(rf'\draw[black, line width=1.5pt] {arc_cmd(e)};')
    else:
        lines.append(rf'\draw[black, line width=1.5pt] {fmt(xy[e[0]])}--{fmt(xy[e[1]])};')
draw_Y(lines)
for t in A:
    wedge(lines, t, s[t], S_WEDGE)
vertices(lines)
lines.append(rf'\node[font=\footnotesize, anchor=west] at ({centre(t0)[0]+0.2:.3f},{centre(t0)[1]:.3f}) {{$t_0$}};')
write('fig-recover-a', lines)

lines = []
base(lines)
draw_Y(lines)
for e in P:
    if e in outer_edges:
        lines.append(rf'\draw[black, line width=1.5pt] {arc_cmd(e)};')
    else:
        lines.append(rf'\draw[black, line width=1.5pt] {fmt(xy[e[0]])}--{fmt(xy[e[1]])};')
# arrows black face -> child along Y (child is a white face)
for y in white:
    par, e = parent[y]
    m = edge_mid(e)
    pc = centre(par)
    yc = centre(y)
    if par == t0:
        continue
    lines.append(rf'\draw[ygreen!60!black, line width=0.9pt, -{{Stealth[length=4pt]}}, shorten >=0.13cm] {fmt(m)}--{fmt(yc)};')
for t in A:
    wedge(lines, t, s[t], S_WEDGE)
vertices(lines)
lines.append(rf'\node[font=\footnotesize, anchor=west] at ({centre(t0)[0]+0.2:.3f},{centre(t0)[1]:.3f}) {{$t_0$}};')
write('fig-recover-b', lines)

print('P =', sorted(P))
