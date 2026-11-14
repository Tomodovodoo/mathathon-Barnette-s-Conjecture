"""Figures for order and optimisation: lattice, pairlattice, canonical, matroids, lp."""
import ast
import lib
from lib import *
from scipy.optimize import linprog

U2 = 0.615


def potentials(mod):
    """Heights of every state of a rooted triangulation, lowest state at zero."""
    sp_ = [(t, v) for t in mod.A for v in mod.F[t]]
    ix = {e: i for i, e in enumerate(sp_)}
    inn = [w for w in mod.white if all(mod.black_face(u, v) != mod.t0 for u, v in zip(mod.F[w], mod.F[w][1:] + mod.F[w][:1]))]
    C = sp.zeros(len(sp_), len(inn))
    for j, w in enumerate(inn):
        f = mod.F[w]
        for u, v in zip(f, f[1:] + f[:1]):
            t = mod.black_face(u, v)
            C[ix[t, v], j] += 1
            C[ix[t, u], j] -= 1
    sts = mod.states()
    vec = lambda z: sp.Matrix([int(z[mod.A.index(t)] == v) for t, v in sp_])
    hh = []
    for z in sts:
        h = list(C.gauss_jordan_solve(vec(z) - vec(sts[0]))[0])
        assert all(q.q == 1 for q in h)
        hh.append(tuple(map(int, h)))
    lo = tuple(min(h[j] for h in hh) for j in range(len(inn)))
    return sts, inn, [tuple(a - b for a, b in zip(h, lo)) for h in hh]


def kind(z):
    if z in tree_states:
        return 'tree'
    return 'cyclic' if mates[z] else 'alone'


# ---------------------------------------------------------------------------
@fig('lattice')
def lattice_fig():
    u = 0.25
    d = 11.6 * u
    ranks = defaultdict(list)
    for z in states:
        ranks[vol[sid[z]]].append(z)
    assert max(len(v) for v in ranks.values()) == 2
    px, py = 3.3, 1.97
    side = {}
    g = state_order
    for k in sorted(ranks):
        zs = ranks[k]
        below = lambda z: [side[states[i]] for i, j in g.edges() if states[j] == z and states[i] in side]
        if len(zs) == 1:
            b = below(zs[0])
            side[zs[0]] = round(sum(b) / len(b)) if b else 0
        else:
            zs.sort(key=lambda z: (sum(below(z)) / max(1, len(below(z))), nm[z]))
            side[zs[0]], side[zs[1]] = 0, 1
    pos = {z: ((k % 2) * px + 2 * px * side[z], k * py) for k in ranks for z in ranks[k]}
    pre, L = '', []
    for i, z in enumerate(states):
        p = P(u).base()
        shade_faces(p, [w for w, v in zip(inner, hs[sid[z]]) if v > 0], 'af tint')
        p.state(z).vertices()
        pre += rf'\newsavebox\lb{chr(97 + i)}\sbox\lb{chr(97 + i)}{{{small(p.tex())}}}'
    for i, j in g.edges():
        (x1, y1), (x2, y2) = pos[states[i]], pos[states[j]]
        L.append(rf'\draw[line width=1.1pt,black!75] ({x1},{y1}) -- ({x2},{y2});')
    for i, z in enumerate(states):
        x, y = pos[z]
        L.append(rf'\node[inner sep=0pt,fill=white,circle,minimum size={d - .1}cm] at ({x},{y}) {{}};\node[inner sep=0pt] at ({x},{y}) {{\usebox\lb{chr(97 + i)}}};')
        k = kind(z)
        if k == 'tree':
            L.append(rf'\draw[line width=1.8pt] ({x},{y}) circle[radius={d / 2 - .02}];')
        elif k == 'cyclic':
            L.append(rf'\draw[line width=1.8pt,dash pattern=on 4pt off 3pt] ({x},{y}) circle[radius={d / 2 - .02}];')
        right = side[z] == 1 or (len(ranks[vol[sid[z]]]) == 1 and x > 2 * px)
        tag = {'tree': 'good state', 'cyclic': r'partner, $Q$ has a cycle', 'alone': 'no partner'}[k]
        ext = r'\\lowest' if nm[z] == 0 else (r'\\highest' if nm[z] == len(states) - 1 else '')
        ext = ext.replace(r'\\', ', ')
        L.append(rf'\node[font=\footnotesize,anchor=north,align=center,inner sep=1.2pt,fill=white] at ({x},{y - d / 2 - .04}) {{$s_{{{nm[z]}}}$, volume {vol[sid[z]]}{ext}\\{tag}}};')
    CERT['lattice'] = dict(kinds={nm[z]: kind(z) for z in states}, covers=[[nm[states[i]], nm[states[j]]] for i, j in g.edges()])
    return pre + tikz(L)


# ---------------------------------------------------------------------------
@fig('pairlattice')
def pairlattice_fig():
    vecs = [svec(d['pairs'][0][0]) + svec(d['pairs'][0][1]) for d in group_data]
    for d, v in zip(group_data, vecs):
        assert all(svec(a_) + svec(b_) == v for a_, b_ in d['pairs'])
    h = heights(vecs[0] - vecs[1])
    assert all(x >= 0 for x in h) or all(x <= 0 for x in h)          # the two covers are comparable
    hi, lo = (0, 1) if all(x >= 0 for x in h) else (1, 0)
    hh = [abs(x) for x in h]
    cells = []
    trees = []
    for i, d in enumerate(group_data):
        a_, b_ = d['pairs'][0]
        p = P(U2).base()
        for t in m.A:
            unused = next(v for v in m.F[t] if v not in (a_[m.A.index(t)], b_[m.A.index(t)]))
            p.wedge(t, unused, 'bf r')
        p.lines(m.D(a_, b_), 'bf detour').vertices()
        nt = sum(m.Q_is_forest(q) for _, q in d['pairs'])
        trees.append(nt)
        where = 'upper' if i == hi else 'lower'
        cells.append(cell(p.tex(), rf'({"ab"[i]}) Cover $D_{{{i + 1}}}$, the {where} node. Heavy blue lines: its two cycles, without direction. Outlined wedge: the one corner each black face does not use. {nt} of its 4 orientations are good pairs.', 7.1))
    # (c) what changes between the two covers
    sym = [e for e, x1, x2 in zip(spokes, vecs[0], vecs[1]) if x1 != x2]
    p = P(U2).base()
    shade_faces(p, [w for w, x in zip(inner, hh) if x], 'af tint')
    p.spokes(style='bf spoke', centres=False)
    for t, v in sym:
        st = 'af bold' if vecs[hi][sindex[t, v]] > vecs[lo][sindex[t, v]] else 'af half'
        p.add(rf'\draw[{st}] {pt(p.cen[t])} -- {pt(p.xy[v])};')
    for t in m.A:
        p.add(rf'\fill {pt(p.cen[t])} ++(-1.7pt,-1.7pt) rectangle ++(3.4pt,3.4pt);')
    for w, x in zip(inner, hh):
        if x:
            facelabel(p, w, rf'${x}$')
    p.vertices()
    H = nx.Graph([(('t', t), ('v', v)) for t, v in sym])
    assert all(dg == 2 for _, dg in H.degree())
    c = cell(p.tex(), rf'(c) The step between them, drawn on the spokes. Bold spokes are used only by the upper cover, dashed ones only by the lower. They alternate round a closed curve ({nx.number_connected_components(H)} in all), and the cover rises by one over the shaded white faces ({sum(hh)} in all).', 7.1)
    L = [r'\node[draw,line width=1.6pt,circle,minimum size=1.5cm,font=\footnotesize] (hi) at (0,2.6) {$D_{' + str(hi + 1) + r'}$};',
         r'\node[draw,line width=1.6pt,circle,minimum size=1.5cm,font=\footnotesize] (lo) at (0,0) {$D_{' + str(lo + 1) + r'}$};',
         r'\draw[line width=1.1pt,black!75] (lo) -- (hi);',
         rf'\node[af note,anchor=west] at (1.1,2.6) {{highest cover\\{trees[hi]} good pairs}};',
         rf'\node[af note,anchor=west] at (1.1,0) {{lowest cover\\{trees[lo]} good pairs}};',
         r'\node[af note,anchor=north west,text width=6.7cm] at (-2.6,-1.25) {(d) The whole lattice of this example has two nodes, each with four orientations. '
         r'A bold ring means that some orientation is a good pair. On larger triangulations the lattice is large and the two extreme nodes can both lack a good pair. '
         r'The smallest such example has 18 vertices.};']
    CERT['pairlattice'] = dict(upper=hi + 1, lower=lo + 1, height_difference=hh, tree_orientations=trees)
    return grid(cells + [c, r'\begin{minipage}[c][6.9cm][c]{7.1cm}\centering ' + tikz(L) + r'\end{minipage}'], 2)


# ---------------------------------------------------------------------------
@fig('canonical')
def canonical_fig():
    ct = (ROOT / 'research/2026-11-14_fable_route-combinatorics/data/counterexamples.txt').read_text()
    cf = ast.literal_eval(ct.split('faces (counterclockwise):\n')[1].splitlines()[0].strip())
    cm0 = Model(cf, 8)
    cs = (0, 4, 1, 5, 8, 9, 11, 6, 10)
    assert cm0.is_state(cs) and not cm0.Q_is_forest(cs)
    cm = rooted(cf, cm0.roots)
    assert cm.A == cm0.A and len(cm.V) == 12
    q, rad = auto_layout('canonical-12', cm)
    sts, inn, hh = potentials(cm)
    prs = cm.pairs(sts)
    partnered = {b_ for _, b_ in prs}
    v = {z: sum(h) for z, h in zip(sts, hh)}
    top = max(partnered, key=lambda z: v[z])
    bot = min(partnered, key=lambda z: v[z])
    assert cs in (top, bot) and cs in partnered
    assert all(all(a <= b for a, b in zip(hh[sts.index(z)], hh[sts.index(top)])) for z in partnered)   # top is above every partnered state
    which = 'highest' if cs == top else 'lowest'
    tms = [z for z in sts if z in partnered and cm.Q_is_forest(z)]
    assert tms and len(sts) == 9 and len(prs) == 10

    def panel(z, lab):
        p = P(U2, cm, q, rad).base()
        cyc = nx.cycle_basis(cm.Q_graph(z))
        for c in cyc:
            fs = [i for i in range(len(cm.F)) if set(cm.F[i]) == set(c)]
            shade_faces(p, [f for f in fs if f in cm.white], 'af tint')
        p.state(z).lines(cm.Q(z), 'bf Q')
        for c in cyc:
            p.lines(list(zip(c, c[1:] + c[:1])), 'bf Q,line width=2pt')
        for w, x in zip(inn, hh[sts.index(z)]):
            facelabel(p, w, rf'$\mathbf{{{x}}}$')
        return cell(p.vertices().tex(), lab, 7.1)
    near = max(tms, key=lambda z: v[z]) if which == 'highest' else min(tms, key=lambda z: v[z])
    ncyc = len(nx.cycle_basis(cm.Q_graph(cs))[0])
    assert ncyc == 3 and any(set(cm.F[f]) == set(nx.cycle_basis(cm.Q_graph(cs))[0]) for f in cm.white)     # the cycle is the boundary of a white face
    a = panel(cs, rf'(a) A 12-vertex triangulation, different from the running example. This is its {which} state that has a partner. Bold numbers are heights, volume {v[cs]}. Its opposite edges contain a cycle of length {ncyc} (heavy dashes).')
    b = panel(near, rf'(b) The nearest good state, volume {v[near]}. The rule had to pass over it.')
    # (c) all nine states in volume order, each drawn
    order = sorted(sts, key=lambda z: (v[z], sts.index(z)))
    kinds = ['good' if z in tms else ('cycle' if z in partnered else 'alone') for z in order]
    assert kinds.count('good') == 8 and kinds.count('cycle') == 1 and kinds.count('alone') == 0
    assert all(is_tree_matching(cm, z) for z in tms)
    thumbs = []
    for z, k in zip(order, kinds):
        p = P(0.238, cm, q, rad).base()
        cyc = nx.cycle_basis(cm.Q_graph(z))
        for c in cyc:
            shade_faces(p, [f for f in cm.white if set(cm.F[f]) == set(c)], 'af tint')
        p.state(z).lines(cm.Q(z), 'bf Q')
        for c in cyc:
            p.lines(list(zip(c, c[1:] + c[:1])), 'bf Q,line width=2pt')
        tag = ' (a)' if z == cs else (' (b)' if z == near else '')
        thumbs.append(cell(small(p.vertices().tex()), rf'volume {v[z]}, ' + ('good' if k == 'good' else r'\textbf{cycle}') + tag))
    strip = (r'\begin{minipage}{14.4cm}\centering\footnotesize (c) All nine states of this triangulation by volume, with their opposite edges dashed. '
             rf'Every state has a partner. Eight are good and one has a cycle, and that one is the {which}. '
             r'Mirror the triangulation and the order turns over, so the same state defeats the other extreme.\end{minipage}')
    CERT['canonical'] = dict(faces=cm.F, t0=cm.t0, state=cs, extreme=which, volumes=[v[z] for z in order], kinds=kinds, tree_matchings=len(tms), cycle_length=ncyc)
    return (r'\begin{tabular}{@{}c@{}}' + grid([a, b], 2) + vs('3mm') + grid(thumbs[:5], 5, colsep='1.5mm') + vs('2mm') + grid(thumbs[5:], 4, colsep='1.5mm')
            + vs('2.5mm') + strip + r'\end{tabular}')

# ---------------------------------------------------------------------------
def rooted_forest(mod, edges):
    g = nx.MultiGraph()
    g.add_nodes_from(mod.V)
    g.add_edges_from(edges)
    return (nx.number_of_edges(g) == len(mod.X) and nx.is_forest(nx.Graph(g)) and nx.Graph(g).number_of_edges() == len(edges)
            and all(len(set(c) & set(mod.roots)) == 1 for c in nx.connected_components(g)))


@fig('matroids')
def matroids_fig():
    U2 = 0.585          # this page is full: smaller panels leave room under the text
    X = set(m.X)
    opp = lambda t, v: tuple(u for u in m.F[t] if u != v)
    # face + forest, vertex condition dropped
    ff = []
    for z in it.product(*[[v for v in m.F[t] if v in X] for t in m.A]):
        if rooted_forest(m, [opp(t, v) for t, v in zip(m.A, z)]):
            ff.append(z)
    assert sum(m.is_state(z) for z in ff) == len(tree_states)
    bad1 = [z for z in ff if not m.is_state(z)]
    w1 = min(bad1, key=lambda z: (sum(c > 1 for c in Counter(z).values()), z))
    # vertex + forest, face condition dropped
    faces_at = {v: [t for t in m.A if v in m.F[t]] for v in m.X}
    vf = []
    for ch in it.product(*[faces_at[v] for v in m.X]):
        if rooted_forest(m, [opp(t, v) for t, v in zip(ch, m.X)]):
            vf.append(ch)
    bij = [ch for ch in vf if len(set(ch)) == len(ch)]
    assert len(bij) == len(tree_states)
    bad3 = [ch for ch in vf if len(set(ch)) < len(ch)]
    w3 = min(bad3, key=lambda ch: (sum(c > 1 for c in Counter(ch).values()), ch))
    # (a)
    p = P(U2).base().state(w1).lines([opp(t, v) for t, v in zip(m.A, w1)], 'bf Q').vertices()
    rep = [v for v, c in Counter(w1).items() if c > 1]
    mis = sorted(X - set(w1))
    for v in rep:
        ring(p, v, '5pt', 'line width=1.3pt')
    for v in mis:
        ring(p, v, '5pt', 'line width=1.1pt,dash pattern=on 2pt off 1.5pt')
    a = cell(p.tex(), rf'(a) Drop \emph{{every vertex once}}. One wedge per black face, and the dashed edges form three trees at the roots, but the ringed vertex carries {Counter(w1)[rep[0]]} wedges and the dashed-ringed vertex none. There are {len(bad1)} such choices.', 7.1)
    # (b)
    p = P(U2).base()
    cyc = nx.cycle_basis(m.Q_graph(s))[0]
    shade_faces(p, [i for i in m.white if set(m.F[i]) == set(cyc)], 'af tint')
    p.state(s).lines(m.Q(s), 'bf Q').lines(list(zip(cyc, cyc[1:] + cyc[:1])), 'bf Q,line width=2pt').vertices()
    nb = sum(not m.Q_is_forest(z) for z in states)
    nj = sum(m.Q_is_forest(z) and not is_tree_matching(m, z) for z in states)
    assert (nb, nj) == (1, 5) and len(states) - nb - nj == len(tree_states)
    b = cell(p.tex(), rf'(b) Drop \emph{{trees at the roots}}. A true state, one wedge per face and per vertex, whose dashed edges close up round the shaded face. Among the 12 states, {nb} has such a cycle. In {nj} more a tree of dashed edges holds two roots, so only {len(tree_states)} pass.', 7.1)
    # (c)
    p = P(U2).base()
    cnt = Counter(w3)
    shade_faces(p, [t for t in m.A if cnt[t] == 0], 'af tintb')
    for t, v in zip(w3, m.X):
        p.wedge(t, v, 'bf s')
    p.lines([opp(t, v) for t, v in zip(w3, m.X)], 'bf Q').vertices()
    c = cell(p.tex(), rf'(c) Drop \emph{{one wedge per face}}. Every vertex has its wedge and the dashed edges form three trees at the roots, but one black face holds two wedges and the dotted face none. There are {len(bad3)} such choices.', 7.1)
    led = (r'\begin{minipage}[c][6.9cm][c]{7.1cm}\centering\footnotesize\renewcommand{\arraystretch}{1.5}\begin{tabular}{@{}lr@{}}\toprule '
           r'\textbf{Conditions kept, running example} & \textbf{choices}\\\midrule '
           rf'one wedge per face, trees at the roots & {len(ff)}\\'
           rf'one wedge per face, every vertex once & {len(states)}\\'
           rf'every vertex once, trees at the roots & {len(vf)}\\\midrule '
           rf'all three: good states & {len(tree_states)}\\\bottomrule\end{{tabular}}\par\medskip '
           r'\begin{minipage}{6.8cm}\footnotesize \emph{Trees at the roots}: the opposite edges form three trees, one at each root. Merge the three roots into one vertex and this says that the edges form a spanning tree. Any two of the conditions can be met together by a fast, standard algorithm. No such algorithm is known for all three.\end{minipage}\end{minipage}')
    CERT['matroids'] = dict(face_forest=len(ff), states=len(states), vertex_forest=len(vf), all_three=len(tree_states),
                            witness_a=w1, witness_c=w3)
    return grid([a, b, c, led], 2)


# ---------------------------------------------------------------------------
@fig('lp')
def lp_fig():
    U2 = 0.585          # this page is full: smaller panels leave room under the text
    choices = [(t, v) for t in m.A for v in m.F[t] if v in m.X]
    qedges = [tuple(0 if u in m.roots else 1 + m.X.index(u) for u in m.F[t] if u != v) for t, v in choices]
    Aeq = np.array([[int(tt == t) for tt, v in choices] for t in m.A] + [[int(vv == v) for t, vv in choices] for v in m.X], float)
    Aub, rhs = [], []
    for mask in range(1, 1 << (len(m.X) + 1)):
        if mask.bit_count() < 2:
            continue
        row = [int((mask >> u & 1) and (mask >> v & 1)) for u, v in qedges]
        if any(row):
            Aub.append(row)
            rhs.append(mask.bit_count() - 1)
    Aub, rhs = np.array(Aub, float), np.array(rhs, float)
    rng = np.random.default_rng(714)
    lpx = None
    for trial in range(250):
        sol = linprog(rng.normal(size=len(choices)), A_ub=Aub, b_ub=rhs, A_eq=Aeq, b_eq=np.ones(2 * len(m.A)), bounds=(0, 1), method='highs')
        assert sol.success
        if any(abs(v - round(v)) > 1e-7 for v in sol.x):
            lpx = sol.x
            break
    assert lpx is not None
    exact = [sp.Rational(float(v)).limit_denominator(1000) for v in lpx]
    assert all(v in (0, sp.Rational(1, 2), 1) for v in exact)
    assert sp.Matrix(Aeq.astype(int)) * sp.Matrix(exact) == sp.ones(2 * len(m.A), 1)
    assert all(sum(int(v) * z for v, z in zip(row, exact)) <= int(y) for row, y in zip(Aub, rhs))
    active = list(Aeq) + [row for row, y in zip(Aub, rhs) if abs(row @ lpx - y) < 1e-8]
    active += [np.eye(len(lpx))[i] for i, v in enumerate(lpx) if min(abs(v), abs(v - 1)) < 1e-8]
    assert sp.Matrix(np.array(active).astype(int)).rank() == len(lpx)        # a vertex of the polytope
    val = dict(zip(choices, exact))
    half = [c for c in choices if val[c] == sp.Rational(1, 2)]
    full = [c for c in choices if val[c] == 1]
    # the two states it averages
    Hh = nx.Graph([(('t', t), ('v', v)) for t, v in half])
    assert all(dg == 2 for _, dg in Hh.degree()) and nx.number_connected_components(Hh) == 1
    z1 = [z for z in states if all(z[m.A.index(t)] == v for t, v in full) and all(val[t, v] > 0 for t, v in zip(m.A, z))]
    assert len(z1) == 2 and all(sp.Rational(int(z1[0][i] == v) + int(z1[1][i] == v), 2) == val[t, v] for i, t in enumerate(m.A) for v in m.F[t] if v in m.X)
    p = P(U2).base().spokes(style='bf spoke', centres=False)
    for t, v in full:
        p.add(rf'\draw[af bold] {pt(p.cen[t])} -- {pt(p.xy[v])};')
    for t, v in half:
        p.add(rf'\draw[af half] {pt(p.cen[t])} -- {pt(p.xy[v])};')
    for t in m.A:
        p.add(rf'\fill {pt(p.cen[t])} ++(-1.7pt,-1.7pt) rectangle ++(3.4pt,3.4pt);')
    a = cell(p.vertices().tex(), rf'(a) A corner point of the relaxed problem. Bold spokes have weight $1$, dashed spokes weight $\tfrac12$, thin spokes $0$. Every centre and every vertex still receives total weight $1$. The {len(half)} half spokes form one closed curve.', 7.1)
    cells = [a]
    for i, z in enumerate(z1):
        p = P(U2).base()
        cyc = nx.cycle_basis(m.Q_graph(z))
        for c in cyc:
            shade_faces(p, [f for f in m.white if set(m.F[f]) == set(c)], 'af tint')
        p.state(z).lines(m.Q(z), 'bf Q')
        for c in cyc:
            p.lines(list(zip(c, c[1:] + c[:1])), 'bf Q,line width=2pt')
        txt = 'Its opposite edges contain a cycle.' if cyc else 'Its opposite edges form a forest.'
        cells.append(cell(p.vertices().tex(), rf'({"bc"[i]}) The point is half of this state $s_{{{nm[z]}}}$ plus half of the other. {txt}', 7.1))
    ncy = [len(nx.cycle_basis(m.Q_graph(z))) for z in z1]
    led = (r'\begin{minipage}[c][6.9cm][c]{7.1cm}\footnotesize\renewcommand{\arraystretch}{1.5}\begin{tabular}{@{}p{6.9cm}@{}}\toprule '
           r'\textbf{The relaxed problem}\\\midrule '
           rf'{len(choices)} weights between $0$ and $1$, one per black face and non-root corner.\\'
           r'Each face and each vertex gets total weight $1$.\\'
           rf'Merge the three roots into one vertex. For every set of the resulting vertices, the opposite edges inside it weigh at most its size minus one ({len(Aub)} conditions, all checked exactly).\\\midrule '
           rf'The point in (a) meets all of them and is a corner of the feasible region, yet it is not a state. So an optimal solution of the relaxed problem need not be a state, and any rounding rule needs a further argument.\\\bottomrule\end{{tabular}}\end{{minipage}}')
    CERT['lp'] = dict(choices=choices, x=exact, half=half, averaged_states=[nm[z] for z in z1], cycles=ncy, inequalities=len(Aub), trial=trial + 1)
    return grid(cells + [led], 2)
