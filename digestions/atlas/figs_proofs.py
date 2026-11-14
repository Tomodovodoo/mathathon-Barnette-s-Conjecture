"""Figures for the two comparison pages: keystep (three written proofs of the nonvanishing step,
recomputed on the running example) and blueprint (the paper's route against the Lean proof)."""
import json
import lib
from lib import *
from figs_chain import DISK, DARCS

U2 = 0.57
CW = 6.6

# ---------------------------------------------------------------------------
# Face paths: for every white face the path in G to the outer face along one fixed tree
# (breadth-first distances from t0, ties by face index), and the corner each black face on it turns round.
_dist = nx.single_source_shortest_path_length(m.G, m.t0)


def face_path(y):
    path, cur = [y], y
    while cur != m.t0:
        cur = min(w for w in m.G[cur] if _dist[w] == _dist[cur] - 1)
        path.append(cur)
    return path


def turns_of(path):
    """Black face on the path -> (corner it turns round, +1 if that corner is on the left of the path, else -1)."""
    out = {}
    for prev, t, nxt in zip(path, path[1:], path[2:]):
        if t not in m.A:
            continue
        f = m.F[t]
        e_in, e_out = set(m.F[prev]) & set(f), set(f) & set(m.F[nxt])
        (v,) = e_in & e_out
        (a_,) = e_in - {v}
        (b_,) = e_out - {v}
        i = f.index(v)
        out[t] = (v, 1 if (f[(i + 1) % 3], f[(i + 2) % 3]) == (a_, b_) else -1)
    return out


PATH = {y: face_path(y) for y in m.white}
TURN = {y: turns_of(PATH[y]) for y in m.white}
assert all(len(set(p_)) == len(p_) and p_[-1] == m.t0 for p_ in PATH.values())


def eta(z, y):
    return sum(sg for t, (v, sg) in TURN[y].items() if z[m.A.index(t)] == v)


def omega_paths(z):
    return sum(eta(z, y) for y in m.white)


def reverse_cycle(a_, b_, cyc):
    on = set(zip(cyc, cyc[1:] + cyc[:1]))
    return (tuple(y_ if (x_, y_) in on else x_ for x_, y_ in zip(a_, b_)),
            tuple(x_ if (x_, y_) in on else y_ for x_, y_ in zip(a_, b_)))


def path_curve(p, path):
    pts, gates = [p.cen[path[0]]], {}
    for f1, f2 in zip(path, path[1:]):
        a_, b_ = sorted(set(m.F[f1]) & set(m.F[f2]))
        pts.append(p.mid(a_, b_))
        gates[len(pts) - 1] = (xy[a_], xy[b_])
        if f2 != m.t0:
            pts.append(p.cen[f2])
    pts.append(pts[-1] * (R + draw.COLLAR * 0.85) / np.hypot(*pts[-1]))
    return p.curve_tex(p.smooth_route(pts, gates))


@fig('keystep')
def keystep_fig():
    n_, mm = len(m.A), min(len(d['W']) for d in group_data)
    assert mm == 2 and all(len(d['W']) == 2 for d in group_data)
    # --- main paper, Lemma 4.6: reversing a clockwise cycle of D raises the height at y by one exactly when y is inside
    triples = 0
    for a_, b_ in pairs:
        for c in m.directed_cycles(m.D(a_, b_)):
            k = m.disk(c)
            a2, b2 = reverse_cycle(a_, b_, c)
            assert m.is_pair(a2, b2) and eps(a2, b2) == -eps(a_, b_)
            for y in m.white:
                jump = eta(b2, y) - eta(b_, y)
                assert jump == (1 if y in k['white'] else 0) * (-1 if k['ccw'] else 1)
                triples += 1
    om = {z: omega_paths(z) for z in states}
    shift = {om[z] - vol[sid[z]] for z in states}
    assert len(shift) == 1                                       # total height = volume of page 'heights', up to one constant
    Sigma = sum(eps(a_, b_) * om[b_] ** mm for a_, b_ in pairs)
    prodsum = sum(math.prod(d['W']) for d in group_data)
    assert prodsum == abs(lead_coeff) == 9
    assert Sigma == (-1) ** ((n_ - mm) // 2) * math.factorial(mm) * prodsum          # Proposition 4.8
    # the sum over good states only gives the same number (Lemma 4.5)
    assert Sigma == sum(eps(mates[z][0], z) * om[z] ** mm for z in tree_states)
    # --- primal note: lay all paths on G. One flow, one unit from each white vertex to t0
    flow = Counter()
    for y, path in PATH.items():
        for f1, f2 in zip(path, path[1:]):
            flow[f1, f2] += 1
    net = {}
    for (f1, f2), k in flow.items():
        v_ = k - flow.get((f2, f1), 0)
        if v_ > 0:
            net[f1, f2] = v_
    assert all(flow.get((f2, f1), 0) == 0 for (f1, f2) in flow)   # tree paths never run against each other
    div = Counter()
    for (f1, f2), k in net.items():
        div[f1] += k
        div[f2] -= k
    assert all(div[w] == 1 for w in m.white) and div[m.t0] == -len(m.white) and all(div[t] == 0 for t in m.A)
    # flux out of the shore of every cycle of every cover = number of white vertices inside
    fluxes = 0
    for a_, b_ in pairs:
        for c in m.directed_cycles(m.D(a_, b_)):
            k = m.disk(c)
            inside = set(k['faces'])
            out_ = sum(v_ for (f1, f2), v_ in net.items() if f1 in inside and f2 not in inside)
            in_ = sum(v_ for (f1, f2), v_ in net.items() if f2 in inside and f1 not in inside)
            assert out_ - in_ == k['W']
            fluxes += 1
    # the same weight read in G: the summed turn signs are local potentials of this flow
    K = {(t, v): sum(sg for y in m.white for t2, (v2, sg) in TURN[y].items() if (t2, v2) == (t, v)) for t in m.A for v in m.F[t]}
    for t in m.A:
        for f_, g_ in it.permutations(m.F[t], 2):
            other = next(x for x in m.dual[und(f_, g_)] if x != t)
            out_t = net.get((t, other), 0) - net.get((other, t), 0)
            assert K[t, g_] - K[t, f_] == m.delta(f_, g_) * out_t
    Z = sp.Poly(sp.expand(sum(eps(a_, b_) * sp.prod([1 + xs * K[t, v] for t, v in zip(m.A, b_)]) for a_, b_ in pairs)), xs)
    assert Z.nth(0) == 0 and Z.nth(1) == 0 and Z.nth(2) == (-1) ** ((n_ - mm) // 2) * prodsum      # primal note, (6.4)
    # --- bijective note, path marks: a token of s is a white face and a step of its path that turns at the wedge of s
    def tokens(z):
        return [(y, t, sg) for y in m.white for t, (v, sg) in TURN[y].items() if z[m.A.index(t)] == v]

    def sigma(a_, b_, marks):
        return (-1) ** (m.J(a_, b_) // 2 + sum((1 + sg) // 2 for _, _, sg in marks))
    total, nobj = 0, 0
    for a_, b_ in pairs:
        for M_ in it.combinations(tokens(b_), mm):
            total += sigma(a_, b_, M_)
            nobj += 1
    # the unpaired objects: a white face inside each cycle, marked at the first step of its path that turns at a corner on the cycle
    fixed = []
    for d in group_data:
        a0, b0 = d['pairs'][0]
        cycs = [k['cycle'] for k in d['cycles']]
        for choice in it.product(*[k['white'] for k in d['cycles']]):
            a_, b_ = a0, b0
            marks = []
            for cyc, y in zip(cycs, choice):
                faces_on = {m.black_face(u_, v_) for u_, v_ in zip(cyc, cyc[1:] + cyc[:1])}
                steps = [(t, v, sg) for t, (v, sg) in TURN[y].items() if t in faces_on and v in cyc]
                t1, v1, sg1 = steps[0]                      # dicts keep the path order
                if b_[m.A.index(t1)] != v1:
                    cur = next(c for c in m.directed_cycles(m.D(a_, b_)) if set(c) == set(cyc))
                    a_, b_ = reverse_cycle(a_, b_, cur)
                assert b_[m.A.index(t1)] == v1
                marks.append((y, t1, sg1))
            assert m.is_pair(a_, b_) and len(set(marks)) == mm
            fixed.append((a_, b_, tuple(marks)))
    assert len(fixed) == prodsum == 9 and len({sigma(*f_) for f_ in fixed}) == 1
    common = sigma(*fixed[0])
    assert total == common * prodsum                              # all other marked objects cancel in pairs
    # --- drawing
    y = next(w for w in m.white if sorted(m.F[w]) == [1, 8, 9])
    assert y in DISK['white'] and DISK['ccw'] and DISK['h'] == 7
    r_cw, s_cw = reverse_cycle(r, s, DISK['cycle'])
    eta_cw, eta_ccw = eta(s_cw, y), eta(s, y)
    assert eta_ccw - eta_cw == 1

    def turn_signs(p, yy, only=None):
        for t, (v, sg) in TURN[yy].items():
            if only is None or t in only:
                q = xy[v] + 0.5 * (p.cen[t] - xy[v])
                p.label(q, rf'${"+" if sg > 0 else "-"}$', 'fill=white,draw=black,circle,inner sep=.3pt,line width=.5pt,minimum size=9pt')
    # (a) heights along one face path
    p = P(U2).base()
    shade_faces(p, [y], 'af tint')
    p.state(s).arrows(DARCS)
    p.add(WT_HEAVY + r'\draw[bf wtree,-{Stealth[length=4.5pt,width=4pt]}] ' + path_curve(p, PATH[y]) + ';')
    turn_signs(p, y)
    p.label(p.cen[y] + np.array([0.05, -0.05]), r'$y$', 'af lab')
    a = cell(p.vertices().tex(), rf'(a) Main paper. The path from the white face $y$ (hatched) to the outer face turns round one corner in each black face: $+$ if the corner is on its left, $-$ if on its right. '
             rf'The height of $s$ at $y$ adds the signs at corners with a wedge, here ${eta_ccw}$. With the long cycle of $D$ reversed it is ${eta_cw}$, one less, because $y$ is inside.', CW)
    # (b) the same paths as one flow in G
    p = P(U2).base(shade=False)
    shade_faces(p, DISK['faces'], 'af soft')
    p.graphG(dots=False)
    inside = set(DISK['faces'])
    for (f1, f2), v_ in sorted(net.items()):
        cut = (f1 in inside) != (f2 in inside)
        p.add(rf'\draw[draw=black,line width={0.7 + 0.28 * v_:.2f}pt,shorten >=2.6pt,-{{Stealth[length=4.6pt,width=4.2pt]}}] {p.dual_path((f1, f2))};')
    for (f1, f2), v_ in sorted(net.items()):
        cut = (f1 in inside) != (f2 in inside)
        te = m.cross[und(f1, f2)]
        q = p.mid(*te) * (0.93 if m.t0 in (f1, f2) else 1)
        p.add(rf'\node[font=\scriptsize{",draw=black,line width=.6pt" if cut else ""},fill=white,inner sep=.9pt] at {pt(q)} {{${v_}$}};')
    p.dotsG(2.0)
    cutflow = sum(v_ for (f1, f2), v_ in net.items() if f1 in inside and f2 not in inside)
    assert cutflow == DISK['W'] == 6 and not any(f2 in inside and f1 not in inside for (f1, f2) in net)     # no unit re-enters this shore
    b = cell(p.tex(), rf'(b) Primal note. Lay all {len(m.white)} paths on $G$: one flow, a unit from every white vertex to $t_0$. Numbers count units. '
             rf'The boxed numbers leave the tinted shore of the long cycle and add up to {cutflow}, one unit for each white vertex inside.', CW)
    # (c) one unpaired marked object on the same cover
    fa, fb, fm = next(f_ for f_ in fixed if {und(u_, v_) for u_, v_ in zip(f_[0], f_[1])} == {und(u_, v_) for u_, v_ in zip(r, s)} and y in [mk[0] for mk in f_[2]])
    p = P(U2).base()
    shade_faces(p, [mk[0] for mk in fm], 'af tint')
    p.state(fb).arrows(m.D(fa, fb))
    for (yy, t1, sg1) in fm:
        p.add(WT_HEAVY + r'\draw[bf wtree,-{Stealth[length=4.5pt,width=4pt]}] ' + path_curve(p, PATH[yy]) + ';')
    p.vertices()
    for (yy, t1, sg1) in fm:
        v1 = TURN[yy][t1][0]
        q = xy[v1] + 0.34 * (p.cen[t1] - xy[v1])
        p.add(rf'\draw[af halo,line width=3.4pt] {pt(q)} circle[radius=5.2pt];\draw[line width=1.5pt] {pt(q)} circle[radius=5.2pt];')
    per_cover = [math.prod(d['W']) for d in group_data]
    c = cell(p.tex(), rf'(c) Bijective note. Pick a white face inside each cycle of a cover and ring the first corner on that cycle where its path turns. '
             rf'Orient the cycle so that this corner carries the wedge of $s$. Such objects have no partner. The two covers give ${per_cover[0]}+{per_cover[1]}={prodsum}$ of them, all of one sign.', CW)
    sg_ = lambda v_: ('+' if v_ > 0 else '-') + str(abs(v_))
    led = (r'\begin{minipage}[b][6.9cm][c]{6.6cm}\footnotesize\renewcommand{\arraystretch}{1.3}\begin{tabular}{@{}>{\raggedright\arraybackslash}p{1.45cm}>{\raggedright\arraybackslash}p{3.6cm}r@{}}\toprule '
           r'\textbf{Proof} & \textbf{What it adds up} & \textbf{Here}\\\midrule '
           rf'main paper & $\sum\varepsilon(r,s)\,\omega(s)^{mm}$ over pairs, $\omega$ the total height & ${sg_(Sigma)}$\\'
           rf'primal note & lowest coefficient of $\sum\varepsilon\prod(1+a\,z)$, weights $a$ from the flow & ${sg_(int(Z.nth(2)))}$\\'
           rf'bijective note & pairs carrying {mm} marks, counted with sign & ${sg_(total)}$\\\bottomrule\end{{tabular}}\par\smallskip '
           rf'Each number is ${prodsum}=6\cdot1+3\cdot1$ up to the factor ${mm}!$ and a sign: white faces inside the cycles of the two covers. '
           r'The flow in (b) is the sum of the paths in (a), so its weights are the heights added over all white faces. '
           rf'A mark in (c) is one term of a height. (d) All three were recomputed here on the running example with the same paths, {nobj} marked objects in all.\end{{minipage}}')
    CERT['keystep'] = dict(paths={str(k): v for k, v in PATH.items()}, turns={str(k): {str(t): list(x) for t, x in v.items()} for k, v in TURN.items()},
                           height_jump_checks=triples, omega_minus_volume=shift.pop(), sigma_paper=Sigma, min_cycles=mm, product_sum=prodsum,
                           flow={f'{a_}->{b_}': v_ for (a_, b_), v_ in net.items()}, flux_checks=fluxes, primal_coefficient=int(Z.nth(2)),
                           marked_objects=nobj, marked_signed_total=total, unpaired_objects=len(fixed), unpaired_sign=common,
                           drawn=dict(y=y, eta_clockwise=eta_cw, eta_counterclockwise=eta_ccw, cut_flow=cutflow))
    return grid([a, b, c, led], 2)


# ---------------------------------------------------------------------------
BP_SHORT = {
    'thm:main': '1.1 cycle avoiding $e$', 'lem:dual': '2.1 dual triangulation', 'txt:two-faces': 'two faces, one side', 'lem:connected': '2.2 connected',
    'eq:counts': '(2.3) counts', 'def:selection': '2.4 selection', 'lem:duality.2': '2.5(2) no cycle', 'lem:duality.1': '2.5(1) cycle and cut',
    'prop:target.1': '2.6(1) to a cycle', 'prop:target.2': '2.6(2) two trees', 'def:state': '3.2 state', 'def:good': '3.4 good state',
    'lem:good': '3.5 spanning tree', 'lem:Y': '3.6 tree and selection', 'lem:outdegree': '3.7 outdegree', 'txt:inside': 'inside of a cycle',
    'lem:disk': '3.8 disk identity', 'prop:recover': '3.9 recovery', 'def:pair': '4.1 pair', 'lem:partner': '4.2 partner', 'txt:D': 'cycles of $D$',
    'lem:reversals': '4.3 two reversals', 'txt:delta': 'local sign $\\delta$', 'lem:sign': '4.4 sign', 'lem:cancel': '4.5 cancellation', 'txt:heights': 'heights on paths',
    'lem:height': '4.6 height jump', 'lem:difference': '4.7 finite difference', 'prop:good': '4.8 pair to good state', 'txt:flow': 'max-flow step',
    'eq:hall': '(5.1) capacity', 'prop:pair': '5.2 a pair exists', 'lem:cap': '6.1 caps', 'thm:T': '6.2 selection with $e_0$'}
# The fill is the blueprint's own status. The independent rebuild of the later Lean version
# (research/2026-11-14_astra_lean-check/) left those statuses unchanged and gave an advisory recount;
# the statements that recount moves are marked with a dot.


@fig('blueprint')
def blueprint_fig():
    bp = json.loads((ROOT / 'proofs/blueprint/blueprint.json').read_text(encoding='utf8'))
    node = {n_['id']: n_ for n_ in bp['nodes']}
    sk = bp['analysis']['skeleton']
    assert len(sk) == 34 and set(sk) == set(BP_SHORT)
    kind = {'checked-exact': 'exact', 'checked-form': 'form', 'refereed': 'none'}
    cat = {i: kind[node[i]['status']] for i in sk}
    assert Counter(cat.values()) == {'exact': 4, 'form': 25, 'none': 5}
    assert bp['analysis']['status_counts_skeleton'] == {'checked-form': 25, 'refereed': 5, 'checked-exact': 4}
    assert sorted(i for i in sk if cat[i] == 'none') == sorted(['lem:connected', 'prop:target.2', 'lem:outdegree', 'lem:sign', 'lem:difference'])
    rc = json.loads((ROOT / 'research/2026-11-14_astra_lean-check/recount.json').read_text(encoding='utf8'))
    rk = {'exact': 'exact', 'after translation': 'form', 'no counterpart': 'none'}
    cat2 = {row['id']: rk[row['category']] for row in rc['rows']}
    assert set(cat2) == set(sk) and Counter(cat2.values()) == {'exact': 5, 'form': 27, 'none': 2}
    moved = sorted(i for i in sk if cat2[i] != cat[i])
    assert moved == ['lem:difference', 'lem:outdegree', 'lem:sign']
    assert (cat2['lem:difference'], cat2['lem:sign'], cat2['lem:outdegree']) == ('exact', 'form', 'form')
    assert sorted(i for i in sk if cat2[i] == 'none') == ['lem:connected', 'prop:target.2']
    counts, counts2 = Counter(cat.values()), Counter(cat2.values())
    uses = nx.DiGraph()
    uses.add_nodes_from(sk)
    uses.add_edges_from((e['dst'], e['src']) for e in bp['edges'] if e['type'] == 'uses' and e['src'] in cat and e['dst'] in cat)
    assert nx.is_directed_acyclic_graph(uses) and uses.number_of_edges() == 67
    assert all(nx.has_path(uses, i, 'thm:main') for i in sk)          # every route statement feeds the theorem
    red = nx.transitive_reduction(uses)
    col_of = lambda i: {2: 0, 3: 1, 4: 2, 5: 3, 6: 3, 1: 3}[node[i]['section']]
    cols = [[i for i in sk if col_of(i) == k] for k in range(4)]
    cols[3] = ['eq:hall', 'txt:flow', 'prop:pair', 'lem:cap', 'thm:T', 'thm:main']
    assert sorted(sum(cols, [])) == sorted(sk)
    assert all(col_of(a_) <= col_of(b_) for a_, b_ in uses.edges())    # the paper never uses a later section
    cw, nw, nh, dy = 3.72, 3.05, 0.5, 0.74
    pos = {}
    for k, colm in enumerate(cols):
        off = 0 if k < 3 else 2.2
        for j, i in enumerate(colm):
            pos[i] = (k * cw, -(j + off) * dy)
    L = []
    heads = ['Section 2: the dual', 'Section 3: states', 'Section 4: signed sum', 'Sections 5, 6 and 1']
    for k, h in enumerate(heads):
        L.append(rf'\node[font=\footnotesize\bfseries,anchor=south] at ({k * cw},{0.48 - (0 if k < 3 else 2.2 * dy)}) {{{h}}};')
    for a_, b_ in sorted(red.edges()):
        (x1, y1), (x2, y2) = pos[a_], pos[b_]
        if x1 == x2:
            dd = min(.5, .22 + .07 * abs(y1 - y2))
            L.append(rf'\draw[black!55,line width=.45pt,-{{Stealth[length=3pt,width=2.6pt]}}] ({x1 - nw / 2},{y1}) .. controls ({x1 - nw / 2 - dd},{y1}) and ({x2 - nw / 2 - dd},{y2}) .. ({x2 - nw / 2},{y2});')
        else:
            L.append(rf'\draw[black!55,line width=.45pt,-{{Stealth[length=3pt,width=2.6pt]}}] ({x1 + nw / 2},{y1}) to[out=0,in=180,looseness=.55] ({x2 - nw / 2},{y2});')
    style = {'exact': 'fill=black!78,text=white,draw=black,line width=.6pt', 'form': 'fill=black!13,draw=black,line width=.6pt',
             'none': 'fill=white,draw=black,line width=.9pt,dash pattern=on 2.2pt off 1.4pt'}
    for i in sk:
        x, y_ = pos[i]
        L.append(rf'\node[{style[cat[i]]},rounded corners=1.2pt,minimum width={nw}cm,minimum height={nh}cm,inner sep=1pt,font=\footnotesize] at ({x},{y_}) {{{BP_SHORT[i]}}};')
        if i in moved:
            L.append(rf'\fill[white,draw=black,line width=.7pt] ({x + nw / 2 - .02},{y_ + nh / 2 - .02}) circle[radius=3.1pt];\fill ({x + nw / 2 - .02},{y_ + nh / 2 - .02}) circle[radius=1.2pt];')
    # legend and count bar under the last column
    ly = -(max(len(c_) for c_ in cols) - 1) * dy - .85
    lxs = [-nw / 2, 1.1, 5.6, 9.2]
    leg = [('exact', rf'{counts["exact"]} exact'), ('form', rf'{counts["form"]} after a translation'),
           ('none', rf'{counts["none"]} no counterpart')]
    for j, (k_, txt_) in enumerate(leg):
        L.append(rf'\node[{style[k_]},rounded corners=1.2pt,minimum width=.62cm,minimum height=.36cm,inner sep=0pt] at ({lxs[j] + .31},{ly}) {{}};'
                 rf'\node[font=\footnotesize,anchor=west,inner sep=1pt] at ({lxs[j] + .7},{ly}) {{{txt_}}};')
    if moved:
        L.append(rf'\fill[white,draw=black,line width=.7pt] ({lxs[3] + .2},{ly}) circle[radius=3.1pt];\fill ({lxs[3] + .2},{ly}) circle[radius=1.2pt];'
                 rf'\node[font=\footnotesize,anchor=west,inner sep=1pt] at ({lxs[3] + .42},{ly}) {{better in the recount}};')
    chart = tikz(L)
    tot = len(sk)
    wu = 14.4 / tot
    B = [rf'\fill[black!78] (0,0) rectangle ({counts["exact"] * wu},.5);', rf'\fill[black!13] ({counts["exact"] * wu},0) rectangle ({(counts["exact"] + counts["form"]) * wu},.5);',
         rf'\draw[line width=.7pt] (0,0) rectangle ({tot * wu},.5);', rf'\draw[line width=.7pt] ({counts["exact"] * wu},0) -- ++(0,.5) ({(counts["exact"] + counts["form"]) * wu},0) -- ++(0,.5);']
    for k in range(1, tot):
        B.append(rf'\draw[line width=.3pt,black!50] ({k * wu},0) -- ({k * wu},.11);')
    B.append(rf'\node[font=\footnotesize,text=white] at ({counts["exact"] * wu / 2},.25) {{{counts["exact"]}}};')
    B.append(rf'\node[font=\footnotesize] at ({(counts["exact"] + counts["form"] / 2) * wu},.25) {{{counts["form"]} after a translation that is not machine-checked}};')
    B.append(rf'\node[font=\footnotesize] at ({(tot - counts["none"] / 2) * wu},.25) {{{counts["none"]}}};')
    bar = tikz(B)
    capa = (r'\begin{minipage}{14.4cm}\centering\footnotesize (a) The ' + str(tot) + r' statements on the main paper\textquotesingle s route to its theorem, by section. An arrow runs from a statement to one that uses it '
            rf'({red.number_of_edges()} arrows, after dropping those implied by others). Dark: the Lean proof has a declaration that says the same. Grey: it has one after a translation. Dashed: none. Dot: the {len(moved)} statements that a later Lean version covers better, which gives {counts2["exact"]}, {counts2["form"]} and {counts2["none"]}.\end{{minipage}}')
    capb = (r'\begin{minipage}{14.4cm}\centering\footnotesize (b) The same count as one bar, a box for each statement.\end{minipage}')
    led = (r'\begin{minipage}{14.4cm}\footnotesize\renewcommand{\arraystretch}{1.3}\begin{tabular}{@{}>{\raggedright\arraybackslash}p{3.6cm}>{\raggedright\arraybackslash}p{10.4cm}@{}}\toprule '
           r'\textbf{The paper says} & \textbf{The Lean proof says instead}\\\midrule '
           r'a triangulation drawn on the sphere, inside and outside of a cycle & a graph with an algebraic dual, and a set of faces cut off from the root\\'
           r'a sign $\pm1$, the product of local signs & a power of $i$; the later Lean version works with the sign and relates the two\\'
           r'heights along paths of faces & weights from a flow\\'
           r'a cycle that avoids a given edge & a cycle; avoiding an edge is proved for the algebraic dual and not restated for the drawn graph\\\bottomrule\end{tabular}\end{minipage}')
    CERT['blueprint'] = dict(route_statements=tot, counts=dict(counts), no_counterpart=sorted(i for i in sk if cat[i] == 'none'), exact=sorted(i for i in sk if cat[i] == 'exact'),
                             uses=uses.number_of_edges(), drawn_arrows=red.number_of_edges(), advisory_recount=dict(counts2), moved_by_recount=moved,
                             source='proofs/blueprint/blueprint.json')
    return (r'\begin{tabular}{@{}c@{}}' + chart + vs('2mm') + capa + vs('4mm') + bar + vs('1.5mm') + capb + vs('4mm') + led + r'\end{tabular}')
