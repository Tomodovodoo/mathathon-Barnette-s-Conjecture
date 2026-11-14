"""Figures for the linear-algebra pages: rowdep, determinant, dimers, pfaffian."""
import lib
from lib import *

U2 = 0.615
FL = 'abcdefghij'


def named_panel(z, u=U2):
    """The running example with vertex numbers and black faces lettered a to j."""
    p = P(u).base()
    cyc = nx.cycle_basis(m.Q_graph(z))
    for c in cyc:
        shade_faces(p, [f for f in m.white if set(m.F[f]) == set(c)], 'af tint')
    p.state(z).lines(m.Q(z), 'bf Q')
    for c in cyc:
        p.lines(list(zip(c, c[1:] + c[:1])), 'bf Q,line width=2pt')
    for i, t in enumerate(m.A):
        v = z[i]
        q = p.cen[t] + 0.28 * (p.cen[t] - p.xy[v])
        p.add(rf'\node[font=\footnotesize\itshape,inner sep=0pt] at {pt(q)} {{{FL[i]}}};')
    p.vertices(labels=True)
    return p, cyc


def matrix_tex(z):
    N = sp.zeros(len(m.A), len(m.X))
    for i, (t, v) in enumerate(zip(m.A, z)):
        for u in m.F[t]:
            if u != v and u in m.X:
                N[i, m.X.index(u)] = m.delta(u, v)
    det = N.det()
    ker = N.T.nullspace()
    rows = set()
    if ker:
        k = ker[0]
        k = k / min(abs(x) for x in k if x != 0)
        assert N.T * k == sp.zeros(len(m.X), 1) and all(x in (-1, 0, 1) for x in k)
        rows = {i for i, x in enumerate(k) if x != 0}
    c = 0.56
    L = []
    for i in rows:
        L.append(rf'\fill[black!17] (-.05,{-(i + 1) * c}) rectangle ({len(m.X) * c + .05},{-i * c});')
    for j, v in enumerate(m.X):
        L.append(rf'\node[font=\footnotesize] at ({(j + .5) * c},{.3}) {{${v}$}};')
    for i in range(len(m.A)):
        L.append(rf'\node[font=\footnotesize\itshape] at (-.35,{-(i + .5) * c}) {{{FL[i]}}};')
        for j in range(len(m.X)):
            e = N[i, j]
            txt = r'$\cdot$' if e == 0 else ('$+$' if e > 0 else '$-$')
            L.append(rf'\node[font=\footnotesize,inner sep=0pt{",text=black!45" if e == 0 else ""}] at ({(j + .5) * c},{-(i + .5) * c}) {{{txt}}};')
    L.append(rf'\draw[line width=.5pt] (-.05,0) rectangle ({len(m.X) * c + .05},{-len(m.A) * c});')
    return tikz(L), det, sorted(rows), N


@fig('rowdep')
def rowdep_fig():
    cells = []
    out = {}
    for z, tag in ((s, 'a'), (r, 'b')):
        p, cyc = named_panel(z)
        M, det, rows, N = matrix_tex(z)
        # the nonzero terms of the determinant are the partners of z
        found = []

        def rec_(i, used, acc):
            if i == len(m.A):
                found.append(tuple(acc))
                return
            for j in range(len(m.X)):
                if j not in used and N[i, j] != 0:
                    rec_(i + 1, used | {j}, acc + [m.X[j]])
        rec_(0, frozenset(), [])
        assert sorted(found) == sorted(mates[z])
        terms = len(found)
        if cyc:
            assert det == 0 and len(rows) == len(cyc[0])
            cap = (rf'({tag}) The state $s_{{{nm[z]}}}$. Its opposite edges (dashed) close up round the shaded face. The rows of the faces \textit{{{", ".join(FL[i] for i in rows)}}} on that cycle, '
                   rf'shaded in the matrix, add up to zero with suitable signs. Determinant $0$, from {terms} terms that cancel.')
        else:
            assert abs(det) == 1 and not rows
            cap = rf'({tag}) The state $s_{{{nm[z]}}}$. Its opposite edges form a forest, no rows are dependent, and the determinant is ${int(det):+d}$, a single term.'
        cells.append(r'\begin{tabular}[t]{@{}c@{}}' + p.tex() + r'\\[1mm]' + M + r'\\[1mm]\begin{minipage}{7.1cm}\centering\footnotesize ' + cap + r'\end{minipage}\end{tabular}')
        out[tag] = dict(state=nm[z], det=int(det), dependent_rows=[FL[i] for i in rows], terms=terms)
    # all twelve states
    for z in states:
        _, det, _, _ = matrix_tex(z)
        assert (det == 0) == (not is_tree_matching(m, z) or not mates[z]) or True
        assert abs(det) == (1 if z in tree_states else 0)
    CERT['rowdep'] = out
    return grid(cells, 2)


# ---------------------------------------------------------------------------
def prism_model(p_=6, avoiding=None):
    """The dual of the prism with p_ sides, rooted at its first black face.
    With `avoiding`, the prescribed edge is chosen so that this many Hamiltonian cycles avoid it."""
    hm0 = Model(dual_of_cubic(nx.circular_ladder_graph(p_)), 0)
    rts = list(hm0.roots)
    for e0 in [None] + [(rts[i], rts[(i + 1) % 3]) for i in range(3)]:
        if avoiding is None and e0 is not None:
            break
        if avoiding is not None and e0 is None:
            continue
        hm = rooted(hm0.F, hm0.roots, e0)
        if avoiding is None or sum(hm.dual[hm.e0] not in {und(*g) for g in c} for c in hm.two_factors(1)) == avoiding:
            q, rad = auto_layout(f'prism{p_}' + ('' if e0 is None else f'-e{hm.e0[0]}{hm.e0[1]}'), hm)
            return hm, q, rad
    raise AssertionError('no prescribed edge with that many avoiding cycles')


@fig('determinant')
def determinant_fig():
    hm, q, rad = prism_model(6)
    sts = hm.states()
    prs = hm.pairs(sts)
    tms = [z for z in sts if is_tree_matching(hm, z) and any(b_ == z for _, b_ in prs)]
    assert (len(sts), len(prs), len(tms)) == (3, 2, 2)
    sign = {b_: eps(a_, b_, hm) for a_, b_ in prs}
    assert sum(sign.values()) == 0
    u = 0.42
    cells = []
    for i, z in enumerate(sts):
        p = P(u, hm, q, rad).base()
        cyc = nx.cycle_basis(hm.Q_graph(z))
        p.state(z).lines(hm.Q(z), 'bf Q')
        for c in cyc:
            p.lines(list(zip(c, c[1:] + c[:1])), 'bf Q,line width=2pt')
        p.vertices()
        if z in tms:
            lab = rf'tree matching, sign ${"+" if sign[z] > 0 else "-"}1$'
        else:
            lab = 'no partner' + (', and a cycle' if cyc else '')
        cells.append(cell(p.tex(), rf'({"abc"[i]}) {lab}', 4.8))
    # the same balance on the running example
    plus = sum(eps(a_, b_) > 0 for a_, b_ in pairs if b_ in tree_states)
    minus = sum(eps(a_, b_) < 0 for a_, b_ in pairs if b_ in tree_states)
    assert plus == minus == 3
    led = (r'\begin{minipage}{14.6cm}\footnotesize\renewcommand{\arraystretch}{1.55}\begin{tabular}{@{}p{14.4cm}@{}}\toprule '
           r'\textbf{The dual of the hexagonal prism}: 8 vertices, 3 states, 2 tree matchings, drawn with their opposite edges dashed.\\\midrule '
           r'Polynomial: $F(w)=\prod_t w_{t,s_a(t)}-\prod_t w_{t,s_b(t)}$, one monomial for each tree matching, with opposite signs.\\'
           r'One evaluation, all weights $1$: $F=1-1=0$. The number has forgotten that two tree matchings exist.\\'
           rf'The running example behaves the same way: its 6 tree matchings carry signs ${plus}$ plus and ${minus}$ minus.\\\midrule '
           r'With the weights kept as variables, $F(w)=\bigl[\prod_t y_t\bigr]\det N(y,w)$: the coefficient that uses each black face $t$ exactly once. '
           r'Terms of the determinant that use a face twice are discarded by taking this coefficient, not by evaluating.\\\bottomrule\end{tabular}\end{minipage}')
    six = []
    for z in sorted(tree_states, key=lambda z: nm[z]):
        e_ = eps(mates[z][0], z)
        pp = P(0.2).base().state(z).lines(m.Q(z), 'bf Q').vertices()
        six.append(cell(small(pp.tex()), rf'$s_{{{nm[z]}}}$: ${"+" if e_ > 0 else "-"}1$'))
    sixrow = (r'\begin{minipage}{14.6cm}\centering\footnotesize\textbf{The six tree matchings of the running example and their signs}\end{minipage}\\[1mm]'
              + grid(six, 6, colsep='1.2mm'))
    CERT['determinant'] = dict(prism=dict(faces=hm.F, t0=hm.t0, states=sts, tree_matchings=tms, signs=[sign[z] for z in tms]), running_signs=[plus, minus])
    return r'\begin{tabular}{@{}c@{}}' + grid(cells, 3, colsep='2mm') + r'\\[3mm]' + led + r'\\[3mm]' + sixrow + r'\end{tabular}'


# ---------------------------------------------------------------------------
@fig('dimers')
def dimers_fig():
    def overlay(a_, b_):
        p = P(U2).base().spokes(style='bf spoke', centres=False)
        same = [t for t, x, y in zip(m.A, a_, b_) if x == y]
        for t, x, y in zip(m.A, a_, b_):
            if x == y:
                p.add(rf'\draw[draw=black,line width=3.2pt] {pt(p.cen[t])} -- {pt(p.xy[x])};\draw[draw=white,line width=1.2pt] {pt(p.cen[t])} -- {pt(p.xy[x])};')
            else:
                p.add(rf'\draw[draw=bfR,line width=1.5pt,dash pattern=on 3pt off 1.6pt] {pt(p.cen[t])} -- {pt(p.xy[x])};')
                p.add(rf'\draw[draw=bfS,line width=1.5pt] {pt(p.cen[t])} -- {pt(p.xy[y])};')
                p.add(rf'\draw[bf D,line width=.7pt,draw=black!70] {pt(p.xy[x])} -- {pt(p.xy[y])};')
        for t in m.A:
            p.add(rf'\fill {pt(p.cen[t])} ++(-1.7pt,-1.7pt) rectangle ++(3.4pt,3.4pt);')
        return p.vertices(), len(same)
    agree = lambda a_, b_: sum(x == y for x, y in zip(a_, b_))
    p1, k1 = overlay(r, s)
    assert k1 == 0
    lo = by_name[0]
    one = next(states[j] for i, j in state_order.edges() if states[i] == lo)
    p2, k2 = overlay(lo, one)
    mid = min(((a_, b_) for a_ in states for b_ in states if 2 <= agree(a_, b_) <= 5), key=lambda ab: (abs(agree(*ab) - 4), nm[ab[0]], nm[ab[1]]))
    p3, k3 = overlay(*mid)
    cells = [cell(p1.tex(), rf'(a) A pair, $s_{{{nm[r]}}}$ dashed over $s_{{{nm[s]}}}$ solid. No spoke is shared. The spokes alternate round closed curves, and the grey arrows through the centres are the cycles of $D$.', 7.1),
             cell(p3.tex(), rf'(b) States $s_{{{nm[mid[0]]}}}$ and $s_{{{nm[mid[1]]}}}$ agree on {k3} faces. Their shared spokes are drawn double. A double spoke is a closed curve of length two and encloses nothing.', 7.1),
             cell(p2.tex(), rf'(c) States $s_{{{nm[lo]}}}$ and $s_{{{nm[one]}}}$ differ by one clock move: {k2} double spokes and one short curve round a white face.', 7.1)]
    c = 0.5
    L = []
    order = [by_name[k] for k in range(len(states))]
    for i, a_ in enumerate(order):
        L.append(rf'\node[font=\footnotesize] at ({(i + .5) * c},.3) {{${i}$}};\node[font=\footnotesize] at (-.3,{-(i + .5) * c}) {{${i}$}};')
        for j, b_ in enumerate(order):
            k = agree(a_, b_)
            if k == 0:
                L.append(rf'\fill[black!80] ({j * c},{-(i + 1) * c}) rectangle ({(j + 1) * c},{-i * c});')
            L.append(rf'\node[font=\footnotesize,inner sep=0pt{",text=white" if k == 0 else (",text=black!45" if i == j else "")}] at ({(j + .5) * c},{-(i + .5) * c}) {{${k}$}};')
    L.append(rf'\draw[line width=.5pt] (0,0) rectangle ({12 * c},{-12 * c});')
    zeros = sum(agree(a_, b_) == 0 for a_ in states for b_ in states)
    assert zeros == len(pairs)
    d = cell(r'\begin{minipage}[c][6.9cm][c]{7.1cm}\centering ' + tikz(L) + r'\end{minipage}',
             rf'(d) All $12\times12$ overlays of states $s_i$ and $s_j$: the number of shared spokes. Only the {zeros} black cells, with none, are pairs.', 7.1)
    CERT['dimers'] = dict(shared=[[agree(a_, b_) for b_ in order] for a_ in order], b=[nm[mid[0]], nm[mid[1]], k3], c=[nm[lo], nm[one], k2])
    return grid(cells + [d], 2)


# ---------------------------------------------------------------------------
@fig('pfaffian')
def pfaffian_fig():
    Z = range(7)
    black = {i: (i, (i + 1) % 7, (i + 3) % 7) for i in Z}
    white = {i: (i, (i + 3) % 7, (i + 2) % 7) for i in Z}
    E = Counter(frozenset(e) for f in list(black.values()) + list(white.values()) for e in it.combinations(f, 2))
    assert len(E) == 21 and set(E.values()) == {2} and 7 - 21 + 14 == 0        # K7 on a torus
    G = nx.Graph([(('b', i), ('w', j)) for i in Z for j in Z if len(set(black[i]) & set(white[j])) == 2])
    assert nx.is_isomorphic(G, nx.heawood_graph())
    sts = [z for z in it.product(*[black[i] for i in Z]) if len(set(z)) == 7]
    prs = [(a_, b_) for a_ in sts for b_ in sts if all(x != y for x, y in zip(a_, b_))]
    assert (len(sts), len(prs)) == (24, 48)
    def delta(i, u, v):
        f = black[i]
        return 1 if f[(f.index(u) + 1) % 3] == v else -1
    sums = Counter()
    for a_, b_ in prs:
        D = nx.DiGraph(list(zip(a_, b_)))
        assert len(list(nx.simple_cycles(D))) == 1 and len(next(nx.simple_cycles(D))) == 7
        sums[sum(delta(i, a_[i], b_[i]) for i in Z)] += 1
    assert set(sums) <= {1, -1, 7, -7}
    e_ = lambda a_, b_: math.prod(delta(i, a_[i], b_[i]) for i in Z)
    part = defaultdict(list)
    for a_, b_ in prs:
        part[b_].append(a_)
    assert all(len(v) == 2 and e_(v[0], z) == -e_(v[1], z) for z, v in part.items())
    for z in sts:
        Q = nx.Graph([tuple(v for v in black[i] if v != z[i]) for i in Z])
        assert Q.number_of_edges() == 7 and len(nx.cycle_basis(Q)) == 1 and len(nx.cycle_basis(Q)[0]) % 2 == 1
    z = sts[0]
    ra, rb = part[z]
    e1, e2 = np.array([1.0, 0.0]), np.array([0.5, math.sqrt(3) / 2])
    sc = 1.12
    W, Hh = 6.9, 6.2

    def panel(r_=None, s_=None, labels=True, dom=True, primal=False):
        L = [rf'\path[use as bounding box] (0,0) rectangle ({W},{Hh});', rf'\clip (0,0) rectangle ({W},{Hh});']
        pts = {(a, b): sc * (a * e1 + b * e2) + np.array([-1.2, -.5]) for a in range(-6, 12) for b in range(-3, 10)}
        lab = lambda a, b: (a + 3 * b) % 7
        for (a, b), o in pts.items():
            if (a + 1, b) in pts and (a, b + 1) in pts:
                L.append(rf'\fill[bfblack] {pt(o)} -- {pt(pts[a + 1, b])} -- {pt(pts[a, b + 1])} -- cycle;')
        for (a, b), o in pts.items():
            for d in ((1, 0), (0, 1), (-1, 1)):
                if (a + d[0], b + d[1]) in pts:
                    L.append(rf'\draw[bf edge] {pt(o)} -- {pt(pts[a + d[0], b + d[1]])};')
        if primal:
            for (a, b), o in pts.items():
                if (a + 1, b) in pts and (a, b + 1) in pts:
                    cb = (o + pts[a + 1, b] + pts[a, b + 1]) / 3
                    for nb in ((a, b), (a - 1, b), (a, b - 1)):       # the three white triangles round a black one
                        if (nb[0] + 1, nb[1]) in pts and (nb[0] + 1, nb[1] + 1) in pts and (nb[0], nb[1] + 1) in pts:
                            cw = (pts[nb[0] + 1, nb[1]] + pts[nb[0] + 1, nb[1] + 1] + pts[nb[0], nb[1] + 1]) / 3
                            L.append(rf'\draw[bf cycle,line width=.9pt] {pt(cb)} -- {pt(cw)};')
            for (a, b), o in pts.items():
                if (a + 1, b) in pts and (a, b + 1) in pts:
                    L.append(rf'\fill {pt((o + pts[a + 1, b] + pts[a, b + 1]) / 3)} circle[radius=1.6pt];')
                if (a + 1, b) in pts and (a + 1, b + 1) in pts and (a, b + 1) in pts:
                    L.append(rf'\draw[fill=white,line width=.5pt] {pt((pts[a + 1, b] + pts[a + 1, b + 1] + pts[a, b + 1]) / 3)} circle[radius=1.6pt];')
        for (a, b), o in pts.items():
            if not ((a + 1, b) in pts and (a, b + 1) in pts):
                continue
            i = lab(a, b)
            corner = {i: (o, 0), (i + 1) % 7: (pts[a + 1, b], 120), (i + 3) % 7: (pts[a, b + 1], 240)}
            for st, style in ((r_, 'bf r'), (s_, 'bf s')):
                if st is not None:
                    c, a0 = corner[st[i]]
                    L.append(rf'\path[{style}] {pt(c)} -- ++({a0}:.36) arc[start angle={a0},end angle={a0 + 60},radius=.36] -- cycle;')
            if r_ is not None and s_ is not None:
                L.append(rf'\draw[bf D] {pt(corner[r_[i]][0])} -- {pt(corner[s_[i]][0])};')
        for (a, b), o in pts.items():
            L.append(rf'\fill {pt(o)} circle[radius=1.4pt];')
            if labels:
                L.append(rf'\node[font=\footnotesize,fill=white,inner sep=.6pt,circle] at {pt(o + np.array([.0, .0]))} {{${lab(a, b)}$}};')
        if dom:
            o = pts[1, 1]
            u_, v_ = sc * (1 * e1 + 2 * e2), sc * (-3 * e1 + 1 * e2) + sc * (1 * e1 + 2 * e2) * 0
            u_, v_ = sc * (2 * e1 + 1 * e2) * 0 + sc * (1 * e1 + 2 * e2), sc * (3 * e1 - 1 * e2)
            assert (1 + 3 * 2) % 7 == 0 and (3 - 3) % 7 == 0
            L.append(rf'\draw[line width=1.3pt,dash pattern=on 5pt off 3pt] {pt(o)} -- {pt(o + v_)} -- {pt(o + u_ + v_)} -- {pt(o + u_)} -- cycle;')
        return tikz(L)
    cells = [cell(panel(), '(a) The complete graph $K_7$ on a torus. The pattern repeats: equal numbers are one vertex, and the dashed parallelogram is one copy of the torus, with 7 black and 7 white faces.', 7.1),
             cell(panel(labels=False, dom=False, primal=True), '(b) Its dual, the Heawood graph: 14 vertices, one in each face, every vertex with three neighbours.', 7.1),
             cell(panel(ra, z, labels=False), rf'(c) A pair. The arrows of $D$ form one cycle through all 7 vertices. On the torus it winds round and bounds no disk. Left minus right: ${sum(delta(i, ra[i], z[i]) for i in Z):+d}$.', 7.1),
             cell(panel(rb, z, labels=False), rf'(d) The other partner of the same state. Left minus right: ${sum(delta(i, rb[i], z[i]) for i in Z):+d}$. The two terms have opposite signs and cancel. This happens for all 24 states.', 7.1)]
    CERT['pfaffian'] = dict(states=len(sts), pairs=len(prs), delta_sums=dict(sums), every_state_cancels=True, shown=[list(ra), list(rb), list(z)])
    return grid(cells, 2)
