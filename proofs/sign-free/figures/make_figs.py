"""Compute and draw the figures of sign-free.tex. Writes fig-*.tex (TikZ bodies) and figdata.json.

Usage: python make_figs.py      (from this folder; needs plantri.exe for the 16-vertex figure)
Every object drawn is computed here and asserted again, from figdata.json alone, by check.py.
"""
import json
import math
import sf

d = json.load(open('running.json'))
lay = json.load(open('layout-running.json'))
RUN = sf.Inst(d['faces'], d['t0'])
PR = {int(k): tuple(v) for k, v in lay['coordinates'].items()}
DATA = {}


# ---------------------------------------------------------------- drawing helpers
def cen(P, f):
    return (sum(P[v][0] for v in f) / 3, sum(P[v][1] for v in f) / 3)


def c(p):
    return '(%.3f,%.3f)' % p


def lerp(p, q, s):
    return (p[0] + s * (q[0] - p[0]), p[1] + s * (q[1] - p[1]))


class Panel:
    def __init__(self, inst, P, width, wedge=0.5, vr=1.3):
        self.I, self.P, self.width, self.wr, self.vr = inst, P, width, wedge, vr
        xs = [p[0] for p in P.values()]
        self.unit = width / (max(xs) - min(xs) + 1.0)
        self.layers = {k: [] for k in ('back', 'mid', 'top', 'lab')}
        I = inst
        r = sorted(I.R)
        self.layers['back'].append('\\draw[bfblack,line width=4.5pt,line join=round] %s--%s--%s--cycle;' % tuple(c(P[v]) for v in r))
        for f in I.A:
            self.layers['back'].append('\\fill[bfblack] %s--%s--%s--cycle;' % tuple(c(P[v]) for v in f))
        for a, b in I.edges:
            self.layers['back'].append('\\draw[bf edge] %s--%s;' % (c(P[a]), c(P[b])))
        for v in range(I.V):
            st = 'bf root' if v in I.R else 'bf vertex'
            self.layers['top'].append('\\path[%s] %s circle[radius=%.1fpt];' % (st, c(P[v]), vr + (0.5 if v in I.R else 0)))

    def add(self, s, layer='mid'):
        self.layers[layer].append(s)

    def darker(self, t, colour='black!38'):
        self.layers['back'].insert(1 + self.I.n, '\\fill[%s] %s--%s--%s--cycle;' % ((colour,) + tuple(c(self.P[v]) for v in self.I.A[t])))

    def outline(self, t, style):
        self.add('\\draw[%s] %s--%s--%s--cycle;' % ((style,) + tuple(c(self.P[v]) for v in self.I.A[t])))

    def wedge(self, t, v, style='bf s'):
        f = self.I.A[t]
        a, b = [w for w in f if w != v]
        P = self.P
        a1 = math.degrees(math.atan2(P[a][1] - P[v][1], P[a][0] - P[v][0]))
        a2 = math.degrees(math.atan2(P[b][1] - P[v][1], P[b][0] - P[v][0]))
        dl = (a2 - a1 + 180) % 360 - 180
        la = math.dist(P[a], P[v])
        lb = math.dist(P[b], P[v])
        r = min(self.wr, 0.42 * la, 0.42 * lb)
        self.add('\\path[%s] %s -- ++(%.1f:%.3f) arc[start angle=%.1f,end angle=%.1f,radius=%.3f] -- cycle;' % (style, c(P[v]), a1, r, a1, a1 + dl, r))

    def label(self, v, text=None, dist=0.5):
        P, I = self.P, self.I
        nb = I.adj[v]
        mx = sum(P[w][0] for w in nb) / len(nb)
        my = sum(P[w][1] for w in nb) / len(nb)
        if v in I.R:
            mx, my = 0.0, 0.0
            ang = math.atan2(P[v][1] - my, P[v][0] - mx)
        else:
            # the widest angular gap between incident edges
            cands = []
            for f in I.white:
                if v in f:
                    a, b = [w for w in f if w != v]
                    a1 = math.atan2(P[a][1] - P[v][1], P[a][0] - P[v][0])
                    a2 = math.atan2(P[b][1] - P[v][1], P[b][0] - P[v][0])
                    dl = (a2 - a1 + math.pi) % (2 * math.pi) - math.pi
                    reach = min(math.dist(P[a], P[v]), math.dist(P[b], P[v]))
                    cands.append((abs(dl) * min(reach, 3.0), a1 + dl / 2))
            ang = max(cands)[1]
        q = (P[v][0] + dist * math.cos(ang), P[v][1] + dist * math.sin(ang))
        self.add('\\node[fill=white,fill opacity=.8,text opacity=1,inner sep=.5pt,rounded corners=1pt] at %s {%s};' % (c(q), text if text is not None else '$%d$' % v), 'lab')

    def ring(self, v, style='draw=black,line width=.8pt', rad=3.4):
        self.add('\\draw[%s] %s circle[radius=%.1fpt];' % (style, c(self.P[v]), rad), 'top')

    def wtree(self, sig):
        P, I = self.P, self.I
        for x in I.X:
            t = sig[x]
            f = I.A[t]
            ends = []
            for w in f:
                if w != x:
                    e = tuple(sorted((x, w)))
                    other = [I.faces[j] for j in I.edge_faces[e] if I.faces[j] != f][0]
                    ends.append(other)
            p = lerp(P[x], cen(P, f), 0.36)
            self.add('\\draw[bf wtree] plot[smooth,tension=.55] coordinates {%s %s %s};' % (c(cen(P, ends[0])), c(p), c(cen(P, ends[1]))), 'mid')
        for f in I.white:
            self.add('\\path[draw=bfW,fill=white,line width=.6pt] %s circle[radius=1.5pt];' % c(cen(P, f)), 'top')

    def arrow(self, a, b, style, bend=0):
        self.add('\\draw[%s] %s to[bend left=%d] %s;' % (style, c(self.P[a]), bend, c(self.P[b])))

    def tex(self, tag=None):
        body = ['\\begin{tikzpicture}[bf,x=%.5f\\textwidth,y=%.5f\\textwidth]' % (self.unit, self.unit)]
        for k in ('back', 'mid', 'top', 'lab'):
            body += self.layers[k]
        if tag:
            ys = [p[1] for p in self.P.values()]
            xs = [p[0] for p in self.P.values()]
            body.append('\\node[anchor=north] at (%.3f,%.3f) {%s};' % ((min(xs) + max(xs)) / 2, min(ys) - 0.95, tag))
        body.append('\\end{tikzpicture}')
        return '\n'.join(body)


def write(name, panels, sep='\\hfill'):
    if len(panels) == 2:
        sep = chr(92) + 'hspace{0.04' + chr(92) + 'textwidth}'
    with open(name, 'w') as f:
        f.write(('%\n' + sep + '%\n').join(panels) + '%\n')


def wedges(pan, sig, style='bf s'):
    for x in pan.I.X:
        pan.wedge(sig[x], x, style)


def sig_of(inst, k):
    return dict(zip(inst.X, k))


def in_forest(inst, sig):
    """The 2-factor of sigma (deleted-corner map u), and the arcs x -> u(par(x))."""
    par = inst.parent(sig)
    u = {}
    for i, f in enumerate(inst.A):
        rest = [v for v in f if not (v in sig and sig[v] == i) and not (v in par and par[v] == i)]
        assert len(rest) == 1
        u[i] = rest[0]
    arcs = {x: u[par[x]] for x in inst.X}
    return par, u, arcs


# ---------------------------------------------------------------- data on the running example
I = RUN
s_good = sig_of(I, (2, 1, 4, 0, 7, 9, 3, 5, 6, 8))
T_ORBIT = 1
assert I.is_rainbow(s_good) and I.excess(s_good) == 0
s_img, walk = I.iota(s_good, T_ORBIT)
assert len(walk) == 2 and I.excess(s_img) == 0 and sf.key(I, I.iota(s_img, T_ORBIT)[0]) == sf.key(I, s_good)
sig_a = walk[0][0]                      # a rainbow tree of excess 2
assert I.is_rainbow(sig_a) and I.excess(sig_a) == 2

# Figure 1: two rainbow trees with their trees on the white faces
panels = []
for sig, tag in ((sig_a, '(a)'), (s_good, '(b)')):
    assert I.w_tree([(sig[x], x) for x in I.X])
    p = Panel(I, PR, 0.47)
    ld = I.load(sig)
    for t in range(I.n):
        if ld[t] == 2:
            p.darker(t)
        if ld[t] == 0:
            p.outline(t, 'bf Q')
    wedges(p, sig)
    p.wtree(sig)
    for v in range(I.V):
        p.label(v)
    panels.append(p.tex(tag))
write('fig-rainbow.tex', panels)
DATA['rainbow'] = {'a': {str(x): I.A[sig_a[x]] for x in I.X}, 'b': {str(x): I.A[s_good[x]] for x in I.X}, 'load_a': I.load(sig_a)}

# Figure 2: the digraph G_u of the 2-factor of sig_a, and the in-forest of sig_a
par, u, arcs = in_forest(I, sig_a)
assert any(all(u[i] == g[i] for i in range(I.n)) for g in I.two_factors())
panels = []
p = Panel(I, PR, 0.42)
for i, f in enumerate(I.A):
    for v in f:
        if v != u[i]:
            p.arrow(v, u[i], 'bf arc')
for v in range(I.V):
    p.label(v)
panels.append(p.tex('(a)'))
p = Panel(I, PR, 0.42)
for i, f in enumerate(I.A):
    for v in f:
        if v != u[i]:
            p.arrow(v, u[i], 'bf Qdir' if par[v] == i else 'bf arc faint')
wedges(p, sig_a)
for v in range(I.V):
    p.label(v)
panels.append(p.tex('(b)'))
write('fig-digraph.tex', panels)
DATA['digraph'] = {'u': {str(I.A[i]): u[i] for i in range(I.n)}, 'sigma': DATA['rainbow']['a'], 'forest': {str(x): arcs[x] for x in I.X},
                   'all_arcs': sorted([v, u[i]] for i, f in enumerate(I.A) for v in f if v != u[i])}


# Figure 3: one exchange, with the cycle Gamma in the spoke graph
def gamma(inst, sig, x):
    """Vertices of the cycle of F_sigma + (sigma(x), x), from x to the centre of sigma(x) in F_sigma."""
    rem = {(sig[y], y) for y in inst.X}
    nb = {}
    for s in inst.spokes:
        if s not in rem:
            nb.setdefault(inst.V + s[0], []).append(s[1])
            nb.setdefault(s[1], []).append(inst.V + s[0])
    prev = {x: None}
    stack = [x]
    while stack:
        a = stack.pop()
        for b in nb[a]:
            if b not in prev:
                prev[b] = a
                stack.append(b)
    path = [inst.V + sig[x]]
    while path[-1] != x:
        path.append(prev[path[-1]])
    return path[::-1]


best = None
for x in I.X:
    g = gamma(I, sig_a, x)
    if I.V + I.n not in g and (best is None or len(g) > len(best[1])) and len(g) <= 8:
        best = (x, g)
x_ex, g_ex = best
t_new = I.alt(sig_a, x_ex)
assert g_ex[1] == I.V + t_new        # the cycle leaves x through the spoke of the new face
sig_b = dict(sig_a)
sig_b[x_ex] = t_new
assert I.is_rainbow(sig_b)


def hpos(P, inst, v):
    return P[v] if v < inst.V else cen(P, inst.black[v - inst.V])


panels = []
for sig, tag in ((sig_a, '(a)'), (sig_b, '(b)')):
    p = Panel(I, PR, 0.42)
    rem = {(sig[y], y) for y in I.X}
    cyc_edges = {frozenset((g_ex[i], g_ex[i + 1])) for i in range(len(g_ex) - 1)} | {frozenset((g_ex[0], g_ex[-1]))}
    for (i, v) in I.spokes:
        if i == I.n:
            continue
        on = frozenset((v, I.V + i)) in cyc_edges
        if (i, v) in rem:
            if on:
                p.add('\\draw[bf cut] %s--%s;' % (c(PR[v]), c(cen(PR, I.A[i]))))
            continue
        p.add('\\draw[%s] %s--%s;' % ('bf kept' if on else 'bf spoke', c(PR[v]), c(cen(PR, I.A[i]))))
    for i in range(I.n):
        p.add('\\path[fill=black!70] %s circle[radius=1pt];' % c(cen(PR, I.A[i])), 'top')
    wedges(p, sig)
    p.ring(x_ex)
    for v in range(I.V):
        p.label(v)
    panels.append(p.tex(tag))
write('fig-exchange.tex', panels)
DATA['exchange'] = {'sigma': DATA['rainbow']['a'], 'x': x_ex, 'old_face': I.A[sig_a[x_ex]], 'new_face': I.A[t_new],
                    'gamma': [v if v < I.V else list(I.A[v - I.V]) for v in g_ex]}

# Figure 4: one orbit of the involution iota_t
seq = [(s_good, None, None)] + [(w[0], w[1], w[2]) for w in walk] + [(s_img, None, None)]
tags = ['$s$', '$S_1$', '$S_2$', "$s'=\\iota_t(s)$"]
panels = []
moved = set()
for (sig, tt, a), tag in zip(seq, tags):
    p = Panel(I, PR, 0.238, wedge=0.75, vr=1.0)
    ld = I.load(sig)
    for t in range(I.n):
        if ld[t] == 2:
            p.darker(t)
    p.outline(T_ORBIT, 'bf Q')
    wedges(p, sig)
    if a is not None:
        p.ring(a, rad=3.0)
        res = [x for x in I.X if sig[x] == tt and x != a][0]
        p.add('\\draw[draw=black,line width=.8pt] %s +(-2.6pt,-2.6pt) rectangle +(2.6pt,2.6pt);' % c(PR[res]), 'top')
        moved |= {a, res}
    panels.append((p, tag))
moved.add([x for x in I.X if s_good[x] == T_ORBIT][0])
for p, tag in panels:
    for v in sorted(moved):
        p.label(v, dist=0.8)
write('fig-orbit.tex', [p.tex(tag) for p, tag in panels])
DATA['orbit'] = {'t': I.A[T_ORBIT], 's': DATA['rainbow']['b'], 'image': {str(x): I.A[s_img[x]] for x in I.X},
                 'walk': [{'sigma': {str(x): I.A[w[0][x]] for x in I.X}, 'face': I.A[w[1]], 'arrival': w[2]} for w in walk]}

# ---------------------------------------------------------------- Figure 5: the 16-vertex cover without a good state
rot = sf.plantri(16)[27]
fs = sf.faces_of(rot)
J = sf.Inst(fs, fs.index((0, 1, 2)))
factors = J.two_factors()
bad = [u for u in factors if not any(J.good_state(s) for s in J.states_in(u))]
assert len(bad) == 1
ub = bad[0]
cyc = J.factor_cycles(ub)
assert len(cyc) == 1 and len(cyc[0]) == 13
st = J.states_in(ub)
assert len(st) == 2
n_good_total = len({tuple(sorted(s.items())) for u in factors for s in J.states_in(u) if J.good_state(s)})
n_rb_in = 0
for bits in range(1 << J.n):
    used = {x: [i for i in J.at[x] if ub[i] != x] for x in J.X}
    sg = {x: used[x][(bits >> j) & 1] for j, x in enumerate(J.X)}
    if J.is_rainbow(sg):
        n_rb_in += 1
        assert J.excess(sg) > 0


def tutte(inst, rounds=120):
    V = inst.V
    r = sorted(inst.R)
    P = {r[0]: (-4.33, -2.5), r[1]: (4.33, -2.5), r[2]: (0.0, 5.0)}
    for v in inst.X:
        P[v] = (0.0, 0.0)
    w = {e: 1.0 for e in inst.edges}
    for rnd in range(rounds):
        for it in range(400):
            for v in inst.X:
                sw = sx = sy = 0.0
                for z in inst.adj[v]:
                    ww = w[tuple(sorted((v, z)))]
                    sw += ww
                    sx += ww * P[z][0]
                    sy += ww * P[z][1]
                P[v] = (sx / sw, sy / sw)
        L = {e: math.dist(P[e[0]], P[e[1]]) for e in inst.edges}
        mean = sum(L.values()) / len(L)
        for e in inst.edges:
            w[e] *= (L[e] / mean) ** 0.7
    return P


P16 = tutte(J)


def q_cycle(inst, s, r):
    """The directed cycle of Q_s oriented r(t) -> u(t)."""
    nxt = {}
    for i, f in enumerate(inst.A):
        uu = [v for v in f if v != s[i] and v != r[i]][0]
        nxt[r[i]] = uu
    for x in inst.X:
        seen = []
        y = x
        while y in nxt and y not in seen:
            seen.append(y)
            y = nxt[y]
        if y in seen:
            return nxt, seen[seen.index(y):]
    return nxt, None


panels = []
qc = []
# (a) the cover: one edge r(t)s(t) in every face, and both states
p = Panel(J, P16, 0.325, wedge=0.42, vr=1.0)
for i, f in enumerate(J.A):
    a, b = st[0][i], st[1][i]
    p.add('\\draw[bfS,line width=1.1pt] %s--%s;' % (c(P16[a]), c(P16[b])))
for v in range(J.V):
    p.label(v, dist=0.45)
panels.append(p.tex('(a)'))
for (s, r), tag in (((st[0], st[1]), '(b)'), ((st[1], st[0]), '(c)')):
    nxt, cy = q_cycle(J, s, r)
    assert cy is not None and not J.good_state(s)
    qc.append(cy)
    p = Panel(J, P16, 0.325, wedge=0.42, vr=1.0)
    for i in range(J.n):
        p.wedge(i, s[i])
    on = set(zip(cy, cy[1:] + cy[:1]))
    for a, b in nxt.items():
        p.arrow(a, b, 'bf Qdir,line width=1.5pt' if (a, b) in on else 'bf Qdir,line width=.7pt,opacity=.75')
    panels.append(p.tex(tag))
write('fig-badcover.tex', panels)
DATA['badcover'] = {'plantri_index': 27, 'V': 16, 'outer_face': [0, 1, 2], 'faces': fs, 'u': {str(J.A[i]): ub[i] for i in range(J.n)},
                    'states': [{str(J.A[i]): s[i] for i in range(J.n)} for s in st], 'q_cycles': qc,
                    'covers_in_this_rooting': len(factors), 'good_states_in_this_rooting': n_good_total,
                    'rainbow_trees_inside_the_cover': n_rb_in, 'coordinates': {str(v): [round(z, 3) for z in P16[v]] for v in P16}}
DATA['running'] = {'faces': d['faces'], 't0': d['t0'], 'rainbow_trees': len(I.rainbow_trees()), 'two_factors': len(I.two_factors())}
json.dump(DATA, open('figdata.json', 'w'), indent=1)
print('exchange at', x_ex, 'gamma', DATA['exchange']['gamma'])
print('bad cover: covers', len(factors), 'good states', n_good_total, 'rainbow inside', n_rb_in, 'q cycles', qc)
print('orbit moved', sorted(moved))
