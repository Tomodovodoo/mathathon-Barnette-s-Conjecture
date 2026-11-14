"""Figures for trees, cutting, induction and scope: rainbow, trinity, cuts,
induction, earlier, produced, hypotheses, families, open."""
import json
import lib
from lib import *
from figs_algebra import prism_model

U2 = 0.615
FL = 'abcdefghij'


def state_panel(mod, q, rad, z, u, wedges=True):
    p = P(u, mod, q, rad).base()
    cyc = nx.cycle_basis(mod.Q_graph(z))
    for c in cyc:
        shade_faces(p, [f for f in mod.white if set(mod.F[f]) == set(c)], 'af tint')
    p.state(z).lines(mod.Q(z), 'bf Q')
    for c in cyc:
        p.lines(list(zip(c, c[1:] + c[:1])), 'bf Q,line width=2pt')
    return p, cyc


# ---------------------------------------------------------------------------
@fig('rainbow')
def rainbow_fig():
    cand = {}
    for t in m.A:
        f = m.F[t]
        for v in f:
            cand[t, v] = tuple(m.white_face(v, u) for u in f if u != v)
    sel = set(zip(m.A, r))
    WT = nx.Graph(rec['white_tree'])
    swap = None
    for (t, v), (u, w) in cand.items():
        if (t, v) in sel or v not in m.X:
            continue
        path = nx.shortest_path(WT, u, w)
        for g in zip(path, path[1:]):
            rem = next(k for k in sel if und(*cand[k]) == und(*g))
            if rem[0] != t and rem[1] == v:
                tr = WT.copy()
                tr.remove_edge(*g)
                tr.add_edge(u, w)
                assert nx.is_tree(tr)
                swap = (t, v, rem)
                break
        if swap:
            break
    assert swap
    t_add, v_add, rem = swap
    new = (sel - {rem}) | {(t_add, v_add)}
    assert Counter(v for t, v in new) == Counter(m.X)                    # still one passage at every non-root vertex
    cnt = Counter(t for t, v in new)
    assert cnt[t_add] == 2 and cnt[rem[0]] == 0

    def draw(selection, marks=False):
        p = P(U2).base().add(WT_HEAVY)
        if marks:
            shade_faces(p, [t_add], 'af tint')
            shade_faces(p, [rem[0]], 'af tintb')
        for t, v in sorted(selection):
            u, w = cand[t, v]
            fake = {'chosen': {t: {'parent': u, 'child': w}}}
            p.add(r'\draw[bf wtree] ' + p.curve_tex(p.white_curves(fake, t, v)) + ';')
            p.add(rf'\draw[bf cut] {pt(p.cen[t])} -- {pt(p.xy[v])};')
        for w in m.white:
            p.add(rf'\draw[draw=bfW,fill=white,line width=.8pt] {pt(p.cen[w])} circle[radius=2pt];')
        for i, t in enumerate(m.A):
            used = [v for tt, v in selection if tt == t]
            far = p.cen[t] if not used else p.cen[t] + 0.3 * (p.cen[t] - p.xy[used[0]])
            p.add(rf'\node[font=\footnotesize\itshape,inner sep=0pt] at {pt(far)} {{{FL[i]}}};')
        return p.vertices()
    a = cell(draw(sel).tex(), r'(a) A good state as a tree on the white faces (small circles). Each green curve crosses one deleted spoke (dotted), inside a black face. The ten black faces \textit{a} to \textit{j} are each crossed once.', 7.1)
    ia, ir = m.A.index(t_add), m.A.index(rem[0])
    b = cell(draw(new, True).tex(), rf'(b) One exchange at vertex ${v_add}$: its passage moves from face \textit{{{FL[ir]}}} (dotted fill) to face \textit{{{FL[ia]}}} (hatched). Still a tree with one passage at every vertex, but \textit{{{FL[ia]}}} is crossed twice and \textit{{{FL[ir]}}} not at all.', 7.1)
    Hs = m.spoke_graph()
    kept = []
    for k_, selection in enumerate((sel, new)):
        Hk = Hs.copy()
        Hk.remove_edges_from((('t', t), ('v', v)) for t, v in selection)
        assert nx.is_tree(Hk)
        pk = P(U2).base().spokes(deleted=list(selection), outer=True).vertices()
        kept.append(pk.tex())
    c = cell(kept[0], r'(c) The same good state on the spokes. Delete the dotted spokes and the bold rest is a spanning tree: each black centre has lost one spoke.', 7.1)
    d = cell(kept[1], rf'(d) After the exchange the bold spokes are still a spanning tree, but the centre of \textit{{{FL[ia]}}} has lost two spokes and that of \textit{{{FL[ir]}}} none.', 7.1)
    CERT['rainbow'] = dict(add=[t_add, v_add], remove=list(rem), counts_after=[cnt[t] for t in m.A])
    return grid([a, b, c, d], 2)


# ---------------------------------------------------------------------------
@fig('trinity')
def trinity_fig():
    def wspokes(p, style):
        for w in m.white:
            for v in m.F[w]:
                p.add(rf'\draw[{style}] {pt(p.cen[w])} -- {pt(p.xy[v])};')
        return p

    def wdots(p):
        for w in m.white:
            p.add(rf'\draw[draw=bfW,fill=white,line width=.8pt] {pt(p.cen[w])} circle[radius=2pt];')
        return p
    H = m.spoke_graph()
    assert H.number_of_edges() == 3 * len(m.black) == 33 and m.G.number_of_edges() == 33
    nK = len(m.V) + len(m.F)
    eK = 3 * len(m.F) + m.G.number_of_edges()
    assert nK - eK + 2 * eK // 3 == 2                                     # K is a sphere triangulation
    p = P(U2).base(shade=False).graphG('bf cycle,line width=.8pt', dots=False)
    wspokes(p, 'bf wtree,line width=1.1pt').spokes(style='bf kept,line width=.8pt', outer=True, kept='bf kept,line width=.8pt')
    wdots(p).vertices()
    a = cell(p.tex(), rf'(a) All three at once: {nK} points and {eK} joins. Squares are black centres, small circles white centres, dots the vertices of $T$. The edges of $T$ are thin grey.', 7.1)
    p = P(U2).base().spokes(style='bf kept', outer=True, kept='bf kept').vertices()
    b = cell(p.tex(), r'(b) Without the white centres: the spoke graph. States, pairs and the spanning tree of page 8 live here.', 7.1)
    p = wdots(wspokes(P(U2).base(), 'bf wtree,line width=1.5pt')).vertices()
    c = cell(p.tex(), r'(c) Without the black centres: the same construction on the white faces.', 7.1)
    p = P(U2).base(shade=False).graphG('bf cycle,line width=.9pt', dots=False).dotsG(2.0)
    d = cell(p.tex(), r'(d) Without the vertices of $T$: the cubic graph $G$, where the Hamiltonian cycle lives.', 7.1)
    CERT['trinity'] = dict(points=nK, joins=eK)
    return grid([a, b, c, d], 2)


# ---------------------------------------------------------------------------
def partitions(mod):
    out = []
    for cyc in mod.two_factors(1):
        blocked = {und(*mod.cross[und(*g)]) for g in cyc}
        f = mod.T.copy()
        f.remove_edges_from(blocked)
        parts = [sorted(c) for c in nx.connected_components(f)]
        assert len(parts) == 2 and all(nx.is_tree(mod.T.subgraph(c)) for c in parts)
        out.append((parts, sorted(e for e in mod.E if e not in blocked)))
    return out


@fig('cuts')
def cuts_fig():
    T, q, rad, cap = gl['T'], gl['xy'], gl['R'], list(gl['cap'])
    parts = partitions(T)
    def word(ps, cyc):
        w = tuple(int(v in ps[0]) for v in cyc)
        return min(w, tuple(1 - x for x in w))
    by3 = defaultdict(list)
    for ps, Pe in parts:
        by3[word(ps, cap)].append((ps, Pe))
    assert len(by3) == 3 and all(sum(w) in (1, 2) for w in by3)
    u3 = 0.415
    top = []
    for w, lst in sorted(by3.items()):
        ps, Pe = lst[0]
        p = P(u3, T, q, rad).base().lines(Pe, 'bf P')
        p.lines(list(zip(cap, cap[1:] + cap[:1])), 'draw=bfR,line width=2.4pt,dash pattern=on 4pt off 2pt')
        p.vertices(classes=ps)
        top.append(cell(small(p.tex()), rf'{len(lst)} of the {len(parts)} cycles', 4.7))
    # a separating 4-cycle of the running example
    best = None
    for c4 in it.permutations(m.V, 4):
        if c4[0] != min(c4) or c4[1] > c4[3] or set(c4) & set(m.roots):
            continue
        if all(m.T.has_edge(a_, b_) for a_, b_ in zip(c4, c4[1:] + c4[:1])) and not m.T.has_edge(c4[0], c4[2]) and not m.T.has_edge(c4[1], c4[3]):
            g = m.T.copy()
            g.remove_nodes_from(c4)
            comps = list(nx.connected_components(g))
            if len(comps) == 2 and min(map(len, comps)) >= 2:
                if best is None or min(map(len, comps)) > best[1]:
                    best = (list(c4), min(map(len, comps)))
    assert best
    c4 = best[0]
    rparts = partitions(m)
    # the two sides of the 4-cycle: inside is the side without roots
    g = m.T.copy()
    g.remove_nodes_from(c4)
    sides = sorted(map(set, nx.connected_components(g)), key=lambda U: bool(U & set(m.roots)))
    assert len(sides) == 2 and not sides[0] & set(m.roots)
    cutedges = {und(a_, b_) for a_, b_ in zip(c4, c4[1:] + c4[:1])}

    def joins(U, side):
        """Blocks of cut vertices that the tree on U joins inside one open side (cut edges excluded)."""
        sub = nx.Graph(m.T.subgraph(set(U) & (side | set(c4))))
        sub.remove_edges_from([e for e in list(sub.edges()) if und(*e) in cutedges])
        return tuple(sorted(tuple(sorted(set(cc) & set(c4), key=c4.index)) for cc in nx.connected_components(sub) if len(set(cc) & set(c4)) > 1))

    by4, bysig = defaultdict(list), defaultdict(list)
    for ps, Pe in rparts:
        if c4[0] not in ps[0]:
            ps = ps[::-1]
        w = word(ps, c4)
        sig = tuple(joins(U, side) for side in sides for U in ps)        # (inside disks, inside squares, outside disks, outside squares)
        by4[w].append((ps, Pe))
        bysig[w, sig].append((ps, Pe))
    alt = min((0, 1, 0, 1), (1, 0, 1, 0))
    assert len(by4) == 5 and len(bysig) == 6 and sum(map(len, bysig.values())) == len(rparts) == 28
    assert sorted(len(v_) for (w, _), v_ in bysig.items() if w == alt) == [4, 8]         # the alternating word hides two different connections
    assert all(len([1 for (w2, _) in bysig if w2 == w]) == 1 for w in by4 if w != alt)
    u4 = 0.36
    letters = dict(zip(c4, 'abcd'))
    bot = []
    for (w, sig), lst in sorted(bysig.items(), key=lambda kv: (-len(by4[kv[0][0]]), kv[0][0], -len(kv[1]))):
        ps, Pe = lst[0]
        p = P(u4).base()
        shade_faces(p, [f for f in range(len(m.F)) if f in m.white and set(m.F[f]) <= sides[0] | set(c4)], 'af tint')
        p.lines(Pe, 'bf P')
        p.lines(list(zip(c4, c4[1:] + c4[:1])), 'draw=bfR,line width=2pt,dash pattern=on 3pt off 1.6pt')
        p.vertices(classes=ps)
        cen4 = sum(xy[v] for v in c4) / 4
        for v in c4:
            d = xy[v] - cen4
            p.label(xy[v] + 0.95 * d / np.hypot(*d), rf'\textit{{{letters[v]}}}', 'af lab')
        txt = lambda blocks: ' and '.join(', '.join(rf'\textit{{{letters[v]}}}' for v in b_) for b_ in blocks)
        parts_ = []
        for name, (dk, sq) in (('inside', sig[:2]), ('outside', sig[2:])):
            bits = ([f'the disk tree joins {txt(dk)}'] if dk else []) + ([f'the square tree joins {txt(sq)}'] if sq else [])
            if bits:
                parts_.append(f'{name} ' + ', '.join(bits))
        how = r'\\ '.join(parts_) if parts_ else r'joined along the cycle only,\\ nothing through either side'
        split = ''.join(letters[v] for v in c4 if v in ps[0]) + ' / ' + ''.join(letters[v] for v in c4 if v not in ps[0])
        bot.append(cell(small(p.tex()), rf'\textbf{{{len(lst)} of {len(rparts)}}}, split \textit{{{split}}}\\ {how}', 4.6))

    hd = lambda t: r'\begin{minipage}[t]{14.4cm}\centering\footnotesize\textbf{' + t + r'}\end{minipage}\\[2.5mm]'
    CERT['cuts'] = dict(triangle=cap, triangle_patterns={str(k): len(v) for k, v in by3.items()}, four_cycle=c4,
                        four_patterns={str(k): len(v) for k, v in by4.items()}, hamiltonian_cycles=len(rparts),
                        four_signatures=[dict(word=w, joins_inside_outside=sig, cycles=len(v_)) for (w, sig), v_ in bysig.items()])
    return (r'\begin{tabular}{@{}c@{}}' + hd(rf'A separating triangle (heavy dashes), 9 vertices: the {len(by3)} ways two trees can meet it')
            + grid(top, 3, colsep='3mm') + r'\\\noalign{\vskip 4mm}'
            + hd(rf'A separating cycle \textit{{abcd}} of length four in the running example (inside hatched): {len(by4)} splits of its vertices occur among {len(rparts)} cycles, in {len(bysig)} ways. '
                 r'``Joined\textquotedblright{} lists the cut vertices that a tree connects through that side, not along the cycle')
            + grid(bot, 3, colsep='3mm', rowsep='2mm') + r'\end{tabular}')

# ---------------------------------------------------------------------------
@fig('induction')
def induction_fig():
    found = None
    for x in m.X:
        if m.T.degree(x) != 4 or any(x in m.F[f] and f == m.t0 for f in range(len(m.F))):
            continue
        fs = [f for f in range(len(m.F)) if x in m.F[f]]
        # cyclic order of the neighbours
        nxt = {m.F[f][(m.F[f].index(x) + 1) % 3]: m.F[f][(m.F[f].index(x) + 2) % 3] for f in fs}
        a0 = next(iter(nxt))
        ring_ = [a0, nxt[a0], nxt[nxt[a0]], nxt[nxt[nxt[a0]]]]
        for sh in range(4):
            a_, v1, b_, v2 = ring_[sh:] + ring_[:sh]
            be1 = next(f for f in fs if set(m.F[f]) == {x, a_, v1})
            be2 = next(f for f in fs if set(m.F[f]) == {x, b_, v2})
            if be1 not in m.black or be2 not in m.black or m.T.has_edge(v1, v2) or {v1, v2} & set(m.roots):
                continue
            if len(set(m.T[v1]) & set(m.T[v2])) != 3:          # x, a, b only: the merge stays simple
                continue
            faces = [tuple(v1 if w == v2 else w for w in m.F[f]) for f in range(len(m.F)) if x not in m.F[f]]
            try:
                small_ = rooted(faces, m.roots, m.e0)
            except Exception:
                continue
            if len(small_.E) != 3 * len(small_.V) - 6:
                continue
            tms = [z for z in small_.states() if is_tree_matching(small_, z) and any(b0 == z for _, b0 in small_.pairs())]
            if not tms:
                continue
            res = []
            for z in tms:
                ch = dict(zip(small_.A, z))
                lift = {}
                side1 = None
                for t in m.A:
                    if t in (be1, be2):
                        continue
                    key = tuple(v1 if w == v2 else w for w in m.F[t])
                    t2 = next(i for i in small_.A if set(small_.F[i]) == set(key))
                    val = ch[t2]
                    if val == v1:
                        val = v1 if v1 in m.F[t] else v2
                        side1 = (val == v1)
                    lift[t] = val
                if side1:
                    lift[be1], lift[be2] = x, v2
                else:
                    lift[be1], lift[be2] = v1, x
                L = tuple(lift[t] for t in m.A)
                assert m.is_state(L)
                ok = is_tree_matching(m, L)
                rot = None
                if not ok:
                    if side1:
                        g = next(t for t in m.A if {a_, v2} <= set(m.F[t]) and t != be2 and x not in m.F[t])
                        if lift[g] == a_:
                            rot = dict(lift)
                            rot[be1], rot[be2], rot[g] = a_, x, v2
                    else:
                        g = next(t for t in m.A if {b_, v1} <= set(m.F[t]) and t != be1 and x not in m.F[t])
                        if lift[g] == b_:
                            rot = dict(lift)
                            rot[be2], rot[be1], rot[g] = b_, x, v1
                    if rot:
                        rot = tuple(rot[t] for t in m.A)
                        if not (m.is_state(rot) and is_tree_matching(m, rot)):
                            rot = None
                res.append((z, L, ok, rot))
            score = (any(not ok and rot for _, _, ok, rot in res), any(ok for _, _, ok, _ in res))
            if found is None or score > found[0]:
                found = (score, x, (a_, v1, b_, v2), (be1, be2), small_, res)
    assert found, 'no usable degree-4 contraction on the running example'
    score, x, (a_, v1, b_, v2), (be1, be2), sm, res = found
    # the smaller triangulation keeps every surviving vertex as near its old place as the faces allow
    start = {v: xy[v].copy() for v in sm.V}
    start[v1] = (xy[v1] + xy[v2]) / 2
    q2, rad2 = aligned_layout('induction-aligned', sm, start)
    moved = {v: float(np.hypot(*(q2[v] - xy[v]))) for v in sm.V if v != v1}
    drift = max(moved.values())
    nok = sum(ok for _, _, ok, _ in res)
    nrot = sum((not ok) and rot is not None for _, _, ok, rot in res)
    # (a) the vertex and the merge
    names4 = ((v1, 'v_1'), (v2, 'v_2'), (a_, 'a'), (b_, 'b'))
    p = P(U2).base()
    shade_faces(p, [f for f in range(len(m.F)) if x in m.F[f] and f in m.white], 'af tint')
    p.add(rf'\draw[af bold,{{Stealth[length=5pt]}}-{{Stealth[length=5pt]}},shorten <=4pt,shorten >=4pt] {pt(xy[v1])} to[bend left=28] {pt(xy[v2])};')
    p.vertices()
    ring(p, x, '5pt', 'line width=1.3pt')
    for v, nme in names4 + ((x, 'x'),):
        d = xy[v] - xy[x] if v != x else np.array([.0, -1.0])
        p.label(xy[v] + 0.55 * d / np.hypot(*d) if v != x else xy[v] + np.array([.45, -.35]), rf'${nme}$', 'af lab')
    cells = [cell(p.tex(), rf'(a) The vertex $x$ (ringed) has degree four. Remove it and merge $v_1$ with $v_2$: four faces vanish and a triangulation with {len(sm.V)} vertices remains.', 7.1)]
    pick = next((t for t in res if not t[2] and t[3]), None) or next(t for t in res if t[2])
    z, Lf, ok, rot = pick
    p, _ = state_panel(sm, q2, rad2, z, U2)
    p.vertices()
    for v, nme in ((v1, 'v_1{=}v_2'), (a_, 'a'), (b_, 'b')):
        d = q2[v] - q2[v1] if v != v1 else np.array([.0, -1.0])
        p.label(q2[v] + 0.6 * d / np.hypot(*d), rf'${nme}$', 'af lab')
    cells.append(cell(p.tex(), rf'(b) The smaller triangulation with one of its {len(res)} good states. The roots are fixed and the other vertices stay as near their places in (a) as the faces allow.', 7.1))

    p, cyc = state_panel(m, xy, R, Lf, U2)
    ring(p.vertices(), x, '5pt', 'line width=1.3pt')
    if ok:
        cells.append(cell(p.tex(), r'(c) Its lift: the old wedges stay, and the two black faces at $x$ take $x$ and the unused copy of the merged vertex. Here the lift is a good state.', 7.1))
    else:
        cells.append(cell(p.tex(), r'(c) Its lift: the old wedges stay, and the two black faces at $x$ take $x$ and the unused copy of the merged vertex. Here the lift fails: the opposite edges '
                          + ('contain a cycle (heavy dashes).' if cyc else 'no longer hang from the roots as three trees.'), 7.1))
    if rot:
        p, _ = state_panel(m, xy, R, rot, U2)
        diff = [t for t, u_, w_ in zip(m.A, Lf, rot) if u_ != w_]
        p.state(Lf, 'bf r', only=diff)
        ring(p.vertices(), x, '5pt', 'line width=1.3pt')
        cells.append(cell(p.tex(), rf'(d) The repair: rotate three wedges round a white face at $x$ (old positions outlined). The result is a good state.', 7.1))
    else:
        other = next((t for t in res if t[2] and t[1] != Lf), None)
        p, _ = state_panel(m, xy, R, (other or pick)[1], U2)
        cells.append(cell(ring(p.vertices(), x, '5pt', 'line width=1.3pt').tex(), r'(d) Another lift that succeeds.', 7.1))
    CERT['induction'] = dict(x=x, a=a_, v1=v1, b=b_, v2=v2, small_vertices=len(sm.V), tree_matchings_small=len(res), lifts_ok=nok, repaired_by_rotation=nrot,
                             shown=dict(lift_ok=ok, rotation=bool(rot)))
    return grid(cells, 2)


# ---------------------------------------------------------------------------
def relaxed_fs(mod, parts_list, col):
    """For each colour class B: the partitions with a tree whose vertices outside B are pairwise non-adjacent."""
    out = {}
    for B in range(3):
        out[B] = [[S for S in ps if not any(mod.T.has_edge(u, v) for u, v in it.combinations([v for v in S if col[v] != B], 2))] for ps, _ in parts_list]
    return out


@fig('earlier')
def earlier_fig():
    UE = 0.5
    rparts = partitions(m)
    cycles = m.two_factors(1)
    a = cell(P(UE).base().lines(rec['P'], 'bf P').graphG('bf cycle', rec['hamiltonian'], dots=False).vertices(classes=rec['parts']).tex(),
             rf'(a) Stein: two induced trees in $T$ (disks, squares) and the Hamiltonian cycle of $G$ between them. The running example has {len(cycles)} such cycles; the proof produces {len(tree_states)} of them for this root and edge.', 7.1)
    # (b) cycles avoiding each edge
    avoid = {g: sum(und(*g) not in {und(*h_) for h_ in cyc} for cyc in cycles) for g in map(lambda e: und(*e), m.G.edges())}
    assert min(avoid.values()) > 0
    p = P(UE).base(shade=False).graphG(dots=False).dotsG(1.4)
    for g, k in avoid.items():
        te = m.cross[g]
        q = p.mid(*te)
        if m.t0 in g:
            q = q * 0.9
        p.add(rf'\node[font=\footnotesize,fill=white,inner sep=.3pt] at {pt(q)} {{${k}$}};')
    lo_, hi_ = min(avoid.values()), max(avoid.values())
    b = cell(p.tex(), rf'(b) Kelmans: on each edge of $G$, the number of Hamiltonian cycles that avoid it. Every edge can be avoided, here by between {lo_} and {hi_} of the {len(cycles)} cycles.', 7.1)
    # Feder and Subi, relaxed reading. On the running example every cycle passes for every class.
    col = nx.greedy_color(m.T, strategy='DSATUR')
    assert max(col.values()) == 2 and all(col[u] != col[v] for u, v in m.E)
    per = [sum(bool(x) for x in v) for v in relaxed_fs(m, rparts, col).values()]
    assert per == [len(cycles)] * 3
    # (c), (d) the 10-vertex triangulation found by the atlas audit, where the relaxed condition excludes one cycle
    wit = json.loads((ROOT / 'research/2026-11-14_sol_atlas-audit/outputs/fs-witness.json').read_text())
    tg = nx.Graph([tuple(e) for e in wit['edges']])
    assert len(tg) == 10 and tg.number_of_edges() == 24 and nx.check_planarity(tg)[0] and all(d % 2 == 0 for _, d in tg.degree())
    ff = oriented_faces(tg)
    fm = rooted(ff, ff[0])
    q, rad = auto_layout('feder-subi-10', fm)
    fparts = partitions(fm)
    fcol = nx.greedy_color(fm.T, strategy='DSATUR')
    assert max(fcol.values()) == 2 and all(fcol[u] != fcol[v] for u, v in fm.E)
    fs = relaxed_fs(fm, fparts, fcol)
    fper = {B: sum(bool(x) for x in v) for B, v in fs.items()}
    assert len(fparts) == 14 and sorted(fper.values()) == [13, 14, 14]
    B = next(B for B, k in fper.items() if k == 13)
    names = ['circles', 'squares', 'triangles']

    def shapes(p, filled):
        for v in fm.V:
            shape = ['circle', 'rectangle', 'regular polygon,regular polygon sides=3'][fcol[v]]
            p.add(rf'\node[draw,line width=.7pt,fill={"black" if v in filled else "white"},{shape},minimum size={5.5 if fcol[v] < 2 else 7.5}pt,inner sep=0pt] at {pt(q[v])} {{}};')
        return p
    (ps, Pe), ok_ = next((pp_, ok) for pp_, ok in zip(fparts, fs[B]) if ok)
    S = max(ok_, key=len)
    p = P(UE, fm, q, rad).base()
    p.lines([e for e in Pe if e[0] in S and e[1] in S], 'bf P')
    p.lines([e for e in Pe if e[0] not in S], 'bf P,line width=.8pt,draw=black!60')
    c = cell(shapes(p, S).tex(), rf'(c) Feder and Subi, relaxed reading, on a triangulation with 10 vertices. Its three vertex colours are drawn as three shapes. The filled vertices form an induced tree (bold) whose members outside the {names[B]} are pairwise non-adjacent. {fper[B]} of its {len(fparts)} Hamiltonian cycles have such a tree.', 7.1)
    (ps, Pe), = [(ps, Pe) for (ps, Pe), ok in zip(fparts, fs[B]) if not ok]
    bad = [e for e in Pe if fcol[e[0]] != B and fcol[e[1]] != B]
    assert all(any(set(e) <= set(U) for e in bad) for U in ps)
    p = P(UE, fm, q, rad).base()
    p.lines([e for e in Pe if e not in bad], 'bf P')
    p.lines(bad, 'af halo,line width=4.2pt').lines(bad, 'draw=black,line width=2.8pt,dash pattern=on 2.2pt off 1.8pt')
    d = cell(shapes(p, set(ps[0])).tex(), rf'(d) The one cycle without one. Each of its two trees (filled, unfilled) contains an edge between two vertices outside the {names[B]} (heavy dashes). On the running example the relaxed condition excludes nothing: all {len(cycles)} cycles pass for every colour.', 7.1)
    led = (r'\begin{minipage}{14.4cm}\footnotesize\renewcommand{\arraystretch}{1.35}\begin{tabular}{@{}p{2.1cm}p{12.0cm}@{}}\toprule '
           r'\textbf{Earlier idea} & \textbf{What it supplies}\\\midrule '
           r'Stein & the target: two induced trees\\'
           r'Kelmans & a prescribed edge, so that pieces can be glued along small cuts\\'
           r'Feder, Subi & a tree of faces after contracting one colour class, when the other two classes have only short faces. Their tree also needs every omitted vertex of the contracted class to have degree four, which (c) and (d) do not test\\\midrule '
           r'this proof & a good state, from a pair, by cancellation and positivity\\\bottomrule\end{tabular}\end{minipage}')
    CERT['earlier'] = dict(hamiltonian_cycles=len(cycles), avoid_min=lo_, avoid_max=hi_, feder_subi_type_per_class=per, colouring=col,
                           relaxed_example=dict(vertices=10, edges=sorted(map(sorted, tg.edges())), cycles=len(fparts), passing_per_class=fper, excluded_partition=ps, offending_edges=bad))
    return r'\begin{tabular}{@{}c@{}}' + grid([a, b, c, d], 2) + r'\\[3mm]' + led + r'\end{tabular}'

# ---------------------------------------------------------------------------
@fig('produced')
def produced_fig():
    hm, q, rad = prism_model(6, avoiding=4)
    cycles = [sorted(und(*e) for e in c) for c in hm.two_factors(1)]
    assert len(cycles) == 8
    ge0 = hm.dual[hm.e0]
    sts = hm.states()
    prs = hm.pairs(sts)
    tms = [z for z in sts if is_tree_matching(hm, z) and any(b_ == z for _, b_ in prs)]
    images = {tuple(sorted(und(*e) for e in hm.recover(z)['hamiltonian'])): z for z in tms}
    assert len(images) == 2

    def back(cyc):
        """Run the construction backwards: the state read off a cycle that avoids e."""
        Pe = [te for g, te in hm.cross.items() if g not in set(cyc)]
        F = nx.Graph()
        F.add_nodes_from(hm.V)
        F.add_edges_from(e for e in Pe if und(*e) != hm.e0)
        assert nx.is_forest(F) and all(len(set(c) & set(hm.roots)) == 1 for c in nx.connected_components(F))
        z = []
        for t in hm.A:
            e = next(e for e in Pe if und(*e) != hm.e0 and hm.black_face(*e) == t)
            root = next(v for v in hm.roots if nx.has_path(F, v, e[0]))
            d = nx.single_source_shortest_path_length(F, root)
            z.append(e[0] if d[e[0]] > d[e[1]] else e[1])
        z = tuple(z)
        assert hm.is_state(z)
        return z
    u = 0.305
    top, bot, info, reasons = [], [], [], []
    cycles.sort(key=lambda c: (ge0 in c, tuple(c) not in images))
    for cyc in cycles:
        av = ge0 not in cyc
        pr = tuple(cyc) in images
        p = P(u, hm, q, rad).base(shade=False).graphG(dots=False).graphG('bf cycle', cyc, dots=False)
        p.graphG('af bold,dash pattern=on 2pt off 1.5pt', [ge0], dots=False).dotsG(1.3)
        lab = 'avoids $e$, produced' if pr else ('avoids $e$, not produced' if av else 'uses $e$')
        top.append(cell(small(p.tex()), lab, 3.4))
        if av:
            z = back(cyc)
            assert (z in tms) == pr and (not pr or images[tuple(cyc)] == z)
            p, cy = state_panel(hm, q, rad, z, u)
            rp = None if cy else root_path(hm, z)
            assert pr == (not cy and rp is None)
            if rp:
                p.lines(rp, 'af halo,line width=3.4pt').lines(rp, 'bf Q,line width=2.2pt')
            why = 'opposite edges contain a cycle' if cy else 'a path of opposite edges (heavy) joins two roots'
            bot.append(cell(small(p.vertices().tex()), 'good state' if pr else why, 3.4))
            reasons.append(None if pr else why)
        info.append(dict(avoids=av, produced=pr))
    hd = lambda t: r'\begin{minipage}[t]{14.4cm}\centering\footnotesize\textbf{' + t + r'}\end{minipage}\\[2.5mm]'
    # the count as one bar
    n_use = sum(not i_['avoids'] for i_ in info)
    n_pr = sum(i_['produced'] for i_ in info)
    n_miss = sum(i_['avoids'] and not i_['produced'] for i_ in info)
    assert (n_use, n_pr, n_miss) == (4, 2, 2) and n_pr == len(tms)
    wu = 14.0 / len(info)
    L = [rf'\fill[pattern=north east lines,pattern color=black!42] ({n_pr * wu},0) rectangle ({(n_pr + n_miss) * wu},.75);',
         rf'\fill[black!78] (0,0) rectangle ({n_pr * wu},.75);',
         rf'\draw[line width=.8pt] (0,0) rectangle (14,.75);']
    for k in range(1, len(info)):
        L.append(rf'\draw[line width={".8pt" if k in (n_pr, n_pr + n_miss) else ".3pt,black!50"}] ({k * wu},0) -- ({k * wu},{.75 if k in (n_pr, n_pr + n_miss) else .13});')
    L.append(rf'\node[font=\footnotesize,text=white] at ({n_pr * wu / 2},.375) {{{n_pr} produced}};')
    L.append(rf'\node[font=\footnotesize,fill=white,inner sep=1.5pt] at ({(n_pr + n_miss / 2) * wu},.375) {{{n_miss} avoid $e$, not produced}};')
    L.append(rf'\node[font=\footnotesize] at ({(n_pr + n_miss + n_use / 2) * wu},.375) {{{n_use} use $e$}};')
    L.append(rf'\node[font=\footnotesize,anchor=north] at (7,-.12) {{The {len(info)} Hamiltonian cycles of the hexagonal prism, one box each. The proof reaches the {n_pr} dark ones.}};')
    CERT['produced'] = dict(cycles=info, reasons=reasons, faces=hm.F, t0=hm.t0, e0=hm.e0, counts=dict(use_e=n_use, produced=n_pr, avoid_not_produced=n_miss))
    return (r'\begin{tabular}{@{}c@{}}' + hd('The hexagonal prism, drawn inside its dual triangulation: all eight Hamiltonian cycles (purple). The prescribed edge $e$ is the dashed one.')
            + grid(top, 4, colsep='2mm', rowsep='3mm') + r'\\\noalign{\vskip 4mm}'      # \\[len] adds nothing under a deep nested tabular
            + hd('The four cycles that avoid $e$, run backwards: the state each one comes from, with its opposite edges dashed')
            + grid(bot, 4, colsep='2mm') + r'\\\noalign{\vskip 3mm}' + tikz(L) + r'\end{tabular}')

# ---------------------------------------------------------------------------
@fig('hypotheses')
def hypotheses_fig():
    EX = ROOT / 'research/2026-11-14_astra_limits/examples'
    W = 7.1
    # (a) K4: the dual has a vertex of odd degree
    k4 = json.loads((EX / 'K4.json').read_text())
    g = nx.Graph(k4['edges'])
    assert nx.is_isomorphic(g, nx.complete_graph(4)) and not nx.is_bipartite(g) and all(d % 2 == 1 for _, d in nx.Graph(k4['dual_edges']).degree())
    Rr = 3.0
    pts = [Rr * np.array([math.cos(math.radians(t)), math.sin(math.radians(t))]) for t in (210, 330, 90)]
    L = [rf'\fill[bfblack,even odd rule] (0,0) circle[radius={Rr + .35}] (0,0) circle[radius={Rr}];']
    def sector(i, j, style):
        a1, a2 = (210, 330, 90)[i], (210, 330, 90)[j]
        d = (a2 - a1) % 360
        return rf'\path[{style}] (0,0) -- {pt(pts[i])} arc[start angle={a1},end angle={a1 + d},radius={Rr}] -- cycle;'
    L += [sector(0, 1, 'fill=white'), sector(1, 2, 'fill=bfblack'), sector(2, 0, 'pattern=north east lines,pattern color=black!42')]
    L += [rf'\draw[bf edge] (0,0) circle[radius={Rr}];'] + [rf'\draw[bf edge] (0,0) -- {pt(q)};' for q in pts]
    L += [rf'\draw[bf root] {pt(q)} circle[radius=2.3pt];' for q in pts] + [r'\fill (0,0) circle[radius=1.6pt];']
    L += [r'\node[af lab] at (0,-1.5) {white};', r'\node[af lab] at (1.35,.8) {black};', r'\node[af lab] at (-1.35,.8) {?};',
          rf'\path[use as bounding box] (-3.6,-3.6) rectangle (3.6,3.6);']
    a = cell(tikz(L), r'(a) Not bipartite: the tetrahedron. Its dual is again a tetrahedron, with three faces round the middle vertex. Colours must alternate round a vertex, and three cannot.', W)
    # (b) 2-connected: three cubes-minus-an-edge between two terminals
    Gt = nx.Graph()
    pos = {}
    for k in range(3):
        cx = (k - 1) * 2.35
        out = [(cx - .8, .8), (cx + .8, .8), (cx + .8, -.8), (cx - .8, -.8)]
        inn = [(cx - .35, .35), (cx + .35, .35), (cx + .35, -.35), (cx - .35, -.35)]
        for i in range(4):
            pos[k, 'o', i], pos[k, 'i', i] = out[i], inn[i]
            Gt.add_edge((k, 'i', i), (k, 'i', (i + 1) % 4))
            Gt.add_edge((k, 'o', i), (k, 'i', i))
            if i != 3:
                Gt.add_edge((k, 'o', i), (k, 'o', (i + 1) % 4))       # the edge o3-o0 (left side) is removed
        Gt.add_edge('top', (k, 'o', 0))
        Gt.add_edge('bot', (k, 'o', 3))
    pos['top'], pos['bot'] = (0, 2.6), (0, -2.6)
    assert len(Gt) == 26 and all(d == 3 for _, d in Gt.degree()) and nx.is_bipartite(Gt) and nx.check_planarity(Gt)[0]
    assert nx.node_connectivity(Gt) == 2
    Hh = Gt.copy()
    Hh.remove_nodes_from(['top', 'bot'])
    assert nx.number_connected_components(Hh) == 3                       # so no Hamiltonian cycle
    col = nx.bipartite.color(Gt)
    L = [rf'\draw[bf G,line width=.7pt] {pt(pos[u_])} -- {pt(pos[v_])};' for u_, v_ in Gt.edges()]
    L += [rf'\draw[line width=.5pt,fill={"black" if col[v] else "white"}] {pt(pos[v])} circle[radius={"3.2pt" if v in ("top", "bot") else "1.7pt"}];' for v in Gt]
    L += [r'\path[use as bounding box] (-3.6,-3.6) rectangle (3.6,3.6);']
    b = cell(tikz(L), r'(b) Not 3-connected: 26 vertices, cubic, bipartite, planar. Remove the two large vertices and three pieces remain. A Hamiltonian cycle would leave at most two, so there is none.', W)
    # (c) a vertex used twice
    nb = json.loads((EX / 'nonbijective_disk.json').read_text())
    mod = rooted([tuple(f) for f in nb['faces']], nb['faces'][nb['outer']])
    q, rad = auto_layout('nonbijective-9', mod)
    asg = {int(k): v for k, v in nb['assignment'].items()}
    assert set(asg) == set(mod.A) and all(asg[t] in mod.F[t] for t in mod.A)
    cyc = nb['cycle']
    arcs = list(zip(cyc, cyc[1:] + cyc[:1]))
    tails = {}
    for t in mod.A:
        for a_, b_ in arcs:
            if a_ in mod.F[t] and b_ in mod.F[t] and asg[t] == a_:
                tails[a_, b_] = t
    dsum = sum(mod.delta(a_, b_) for a_, b_ in arcs)
    assert dsum == 0 == nb['delta_sum']
    cnt = Counter(asg.values())
    twice = [v for v, c_ in cnt.items() if c_ == 2]
    missed = [v for v in mod.X if v not in cnt]
    assert len(twice) == 1 and len(missed) == 1
    p = P(U2, mod, q, rad).base()
    for t in mod.A:
        p.wedge(t, asg[t], 'bf s')
    p.arrows(arcs).vertices()
    ring(p, twice[0], '5pt', 'line width=1.3pt')
    ring(p, missed[0], '5pt', 'line width=1.1pt,dash pattern=on 2pt off 1.5pt')
    c = cell(p.tex(), r'(c) Not a bijection: the ringed vertex carries two wedges and the dashed-ringed one none. The four arrows form a cycle with black faces twice on the left and twice on the right: sum $0$, not $\pm3$.', W)
    # (d) the torus
    tg = 3
    bl = [((x, y), ((x + 1) % tg, y), ((x + 1) % tg, (y + 1) % tg)) for x in range(tg) for y in range(tg)]
    rr_ = [f[0] for f in bl]
    ss_ = [f[1] for f in bl]
    assert len(set(rr_)) == 9 and len(set(ss_)) == 9 and all(a_ != b_ for a_, b_ in zip(rr_, ss_))
    Q = nx.MultiGraph([tuple(v for v in f if v != z_) for f, z_ in zip(bl, ss_)])
    assert Q.number_of_edges() == 9 and Q.number_of_nodes() == 9 and not nx.is_forest(nx.Graph(Q))
    c_ = 1.85
    L = []
    o = np.array([-2.55, -2.55])
    P_ = lambda x, y: o + c_ * np.array([x, y])
    for x in range(tg):
        for y in range(tg):
            L.append(rf'\fill[bfblack] {pt(P_(x, y))} -- {pt(P_(x + 1, y))} -- {pt(P_(x + 1, y + 1))} -- cycle;')
    for i in range(tg + 1):
        L.append(rf'\draw[bf edge] {pt(P_(i, 0))} -- {pt(P_(i, tg))};\draw[bf edge] {pt(P_(0, i))} -- {pt(P_(tg, i))};')
    for x in range(tg):
        for y in range(tg):
            L.append(rf'\draw[bf edge] {pt(P_(x, y))} -- {pt(P_(x + 1, y + 1))};')
            L.append(rf'\path[bf r] {pt(P_(x, y))} -- ++(0:.42) arc[start angle=0,end angle=45,radius=.42] -- cycle;')
            L.append(rf'\path[bf s] {pt(P_(x + 1, y))} -- ++(90:.42) arc[start angle=90,end angle=180,radius=.42] -- cycle;')
            L.append(rf'\draw[bf Q] {pt(P_(x, y))} -- {pt(P_(x + 1, y + 1))};')
    for x in range(tg + 1):
        for y in range(tg + 1):
            L.append(rf'\fill {pt(P_(x, y))} circle[radius=1.5pt];')
            L.append(rf'\node[font=\footnotesize,anchor=north east,inner sep=2pt] at {pt(P_(x, y))} {{${3 * (x % tg) + (y % tg)}$}};')
    L.append(r'\path[use as bounding box] (-3.6,-3.6) rectangle (3.6,3.6);')
    d = cell(tikz(L), r'(d) On a torus: a grid of 9 vertices whose opposite sides are glued (equal numbers are one vertex). Outlined and solid wedges are two states. The dashed opposite edges of the solid one are 9 edges on 9 vertices, so they contain a cycle.', W)
    CERT['hypotheses'] = dict(K4_dual_degrees_odd=True, theta26=dict(vertices=26, connectivity=2, pieces_without_terminals=3),
                              nonbijective=dict(twice=twice, missed=missed, delta_sum=dsum), torus=dict(Q_edges=9, vertices=9))
    return grid([a, b, c, d], 2)


# ---------------------------------------------------------------------------
def tube(Lr, p_=4):
    g = nx.Graph()
    A_, B_ = p_ * (Lr + 1), p_ * (Lr + 1) + 1
    for j in range(Lr + 1):
        for i in range(p_):
            g.add_edge(j * p_ + i, j * p_ + (i + 1) % p_)
    for j in range(Lr):
        for i in range(p_):
            g.add_edge(j * p_ + i, (j + 1) * p_ + i)
            if i % 2 == 0:
                g.add_edge(j * p_ + i, (j + 1) * p_ + (i + 1) % p_)
            else:
                g.add_edge(j * p_ + (i + 1) % p_, (j + 1) * p_ + i)
    for i in range(p_):
        g.add_edge(A_, i)
        g.add_edge(B_, Lr * p_ + i)
    fs = oriented_faces(g)
    root = {A_, 0, 1} if Lr == 0 else {0, 1, p_ + 1}
    return fs, root


@fig('families')
def families_fig():
    rows = []
    for p_ in (4, 6, 8, 10, 12):
        mod = Model(dual_of_cubic(nx.circular_ladder_graph(p_)), 0)
        ss = mod.states()
        ps = mod.pairs(ss)
        tm = sum(is_tree_matching(mod, z) and any(b_ == z for _, b_ in ps) for z in ss)
        rows.append((p_, len(ss), tm, len(mod.two_factors(1))))
    assert all(r_[1] == r_[0] // 2 and r_[2] == 2 and r_[3] == r_[0] + 2 for r_ in rows)
    trow = []
    for Lr in range(4):
        fs, root = tube(Lr)
        mod = Model(fs, next(i for i, f in enumerate(fs) if set(f) == root))
        ss = mod.states()
        tm = sum(is_tree_matching(mod, z) for z in ss)
        trow.append((Lr, len(mod.V), len(ss), tm))
    assert [t[2:] for t in trow] == [(2, 2), (5, 2), (13, 2), (34, 2)]
    hm, q, rad = prism_model(8)
    z = next(z for z in hm.states() if is_tree_matching(hm, z))
    p, _ = state_panel(hm, q, rad, z, U2)
    a = cell(p.vertices().tex(), rf'(a) The dual of the prism with 8 sides, with one of its two good states. The two hubs have degree 8.', 7.1)
    fs, root = tube(2)
    tm_ = rooted(fs, root)
    q2, rad2 = auto_layout('tube4-2', tm_)
    z = next(z for z in tm_.states() if is_tree_matching(tm_, z))
    p, _ = state_panel(tm_, q2, rad2, z, U2)
    b = cell(p.vertices().tex(), rf'(b) A nanotube of width four with two layers, {len(tm_.V)} vertices, with one of its two good states.', 7.1)

    def chart(title, xs, series, xlabel, x0):
        w, h = 3.9, 3.6
        ymax = max(max(v) for _, v, _ in series)
        top = math.ceil(math.log2(ymax))
        X = lambda i: 0.5 + i * (w - 1.0) / (len(xs) - 1)
        Y = lambda v: h * math.log2(v) / top
        L = [rf'\draw[line width=.5pt] (0,{h}) -- (0,0) -- ({w},0);', rf'\node[font=\footnotesize,anchor=south west,inner sep=1pt] at (0,{h + .25}) {{\textbf{{{title}}}}};']
        for k in range(0, top + 1):
            L.append(rf'\draw[black!25,line width=.3pt] (0,{h * k / top}) -- ({w},{h * k / top});\node[font=\footnotesize,anchor=east] at (-.05,{h * k / top}) {{${2 ** k}$}};')
        for i, xv in enumerate(xs):
            L.append(rf'\node[font=\footnotesize,anchor=north] at ({X(i)},-.05) {{${xv}$}};')
        L.append(rf'\node[font=\footnotesize,anchor=north] at ({w / 2},-.5) {{{xlabel}}};')
        for name, vals, (dash, mark) in series:
            L.append(rf'\draw[line width=1.1pt,{dash}] ' + ' -- '.join(f'({X(i):.3f},{Y(v):.3f})' for i, v in enumerate(vals)) + ';')
            for i, v in enumerate(vals):
                L.append(rf'\node[draw,line width=.8pt,{mark},minimum size=4.5pt,inner sep=0pt] at ({X(i):.3f},{Y(v):.3f}) {{}};')
            L.append(rf'\node[font=\footnotesize,anchor=west,inner sep=2pt] at ({w - .35},{Y(vals[-1]) + (.0)}) {{{name}}};')
        return tikz(L)
    st = [('solid', 'circle,fill=black'), ('dash pattern=on 4pt off 2pt', 'rectangle,fill=white'), ('dash pattern=on 1pt off 1.5pt', 'diamond,fill=white')]
    c1 = chart('Prisms with $2m$ sides', [r_[0] for r_ in rows],
               [('Hamiltonian cycles', [r_[3] for r_ in rows], st[1]), ('states', [r_[1] for r_ in rows], st[0]), ('good states', [r_[2] for r_ in rows], st[2])], 'number of sides $2m$', 0)
    c2 = chart('Nanotubes of width four', [t[0] for t in trow],
               [('states', [t[2] for t in trow], st[0]), ('good states', [t[3] for t in trow], st[2])], 'number of layers', 0)
    CERT['families'] = dict(prisms=[dict(sides=a_, states=b_, tree_matchings=c_, hamiltonian_cycles=d_) for a_, b_, c_, d_ in rows],
                            nanotubes=[dict(layers=a_, vertices=b_, states=c_, tree_matchings=d_) for a_, b_, c_, d_ in trow])
    return (r'\begin{tabular}{@{}c@{}}' + grid([a, b], 2) + r'\\[4mm]' + grid([c1, c2], 2, colsep='4mm')
            + r'\\[1mm]{\footnotesize (c) Counts by direct enumeration, on a doubling scale. The number of good states stays at 2 in both families.}\end{tabular}')


# ---------------------------------------------------------------------------
@fig('open')
def open_fig():
    # (a) evidence ranges. Each number is quoted from the report or referee named in the Sources table; nothing here is recomputed.
    # (statement, largest size with every case checked by two independent programs, by at least one program, largest sampled size)
    bars = [('at least $2^m$ good states, $m$ the fewest cycles of a cover: every root', 22, 22, 100),
            ('the same bound, on triangulations without separating triangles', 16, 24, None),
            ('greedy descent in the lattice reaches a good state', None, 16, 150),
            ('exchange descent on rainbow trees reaches a good state', None, 17, 120),
            ('some contraction keeps a pair', 17, 19, None),
            ('a contraction never has more good states than the original', 17, 18, None)]
    # (statement, size of a known counterexample, True if every smaller case was checked)
    dead = [('the highest state with a partner is good', 12, False), ('an extreme cover has a good orientation', 18, True),
            ('some good state of a contraction lifts directly', 18, True), ('a cover one step from an extreme has one', 24, False),
            ('an extreme or irreducible cover has one', 33, False), ('every maximal chain of covers has one', 33, False),
            ('at least half of all covers have one', 33, False), ('the evict walk never repeats', 38, False)]
    assert all((tw is None or tw <= on) and (sa is None or sa > on) for _, tw, on, sa in bars)
    w = 7.6
    X = lambda v: w * (math.log(v) - math.log(8)) / (math.log(150) - math.log(8))
    L = []
    y = 0
    ybot = -len(bars) * .68 - len(dead) * .5 - .75
    for t in (8, 12, 17, 24, 33, 50, 75, 100, 150):
        L.append(rf'\draw[black!25,line width=.3pt] ({X(t):.3f},.4) -- ({X(t):.3f},{ybot});\node[font=\footnotesize,anchor=south] at ({X(t):.3f},.4) {{${t}$}};')
    L.append(rf'\node[font=\footnotesize,anchor=south west,inner sep=1pt] at (0,.95) {{number of vertices of $T$}};')
    L.append(rf'\node[font=\footnotesize\bfseries,anchor=east,inner sep=1pt] at (-.2,.2) {{open, and tested up to}};')
    for name, tw, on, sa in bars:
        y -= .68
        if sa:
            L.append(rf'\draw[line width=1.5pt,dash pattern=on 3pt off 2pt] ({X(on):.3f},{y}) -- ({X(sa):.3f},{y});\node[font=\footnotesize,fill=white,inner sep=1pt,anchor=west] at ({X(sa) + .05:.3f},{y}) {{${sa}$}};')
        L.append(rf'\draw[line width=.7pt,fill=white] (0,{y - .11}) rectangle ({X(on):.3f},{y + .11});')
        if tw:
            L.append(rf'\fill[black!80] (0,{y - .11}) rectangle ({X(tw):.3f},{y + .11});')
        lab = f'{on}' if tw in (None, on) else f'{tw}, {on}'
        L.append(rf'\node[font=\footnotesize,fill=white,inner sep=1pt,anchor=south west] at ({X(on) + .04:.3f},{y + .08}) {{${lab}$}};')
        L.append(rf'\node[font=\footnotesize,anchor=east,text width=5.7cm,align=right,inner sep=1pt] at (-.2,{y}) {{\hyphenpenalty=10000 {name}}};')
    y -= .72
    L.append(rf'\node[font=\footnotesize\bfseries,anchor=east,inner sep=1pt] at (-.2,{y}) {{refuted, counterexample known at}};')
    for name, v, smallest in dead:
        y -= .5
        L.append(rf'\draw[line width=.4pt,black!55] (0,{y}) -- ({X(v):.3f},{y});\draw[line width=1.6pt] ({X(v) - .1:.3f},{y - .1}) -- ({X(v) + .1:.3f},{y + .1}) ({X(v) - .1:.3f},{y + .1}) -- ({X(v) + .1:.3f},{y - .1});')
        if smallest:
            L.append(rf'\draw[line width=.8pt] ({X(v):.3f},{y}) circle[radius=.19];')
        L.append(rf'\node[font=\footnotesize,inner sep=1pt,anchor=west] at ({X(v) + .25:.3f},{y}) {{${v}$}};')
        L.append(rf'\node[font=\footnotesize,anchor=east,text width=5.7cm,align=right,inner sep=1pt] at (-.2,{y}) {{\hyphenpenalty=10000 {name}}};')
    y -= .75
    x0 = -5.8
    L.append(rf'\fill[black!80] ({x0},{y - .11}) rectangle ({x0 + .8},{y + .11});\node[right,font=\footnotesize] at ({x0 + .8},{y}) {{every case, two programs}};')
    L.append(rf'\draw[line width=.7pt,fill=white] ({x0 + 4.5},{y - .11}) rectangle ({x0 + 5.3},{y + .11});\node[right,font=\footnotesize] at ({x0 + 5.3},{y}) {{every case, one program}};')
    L.append(rf'\draw[line width=1.5pt,dash pattern=on 3pt off 2pt] ({x0 + 9.0},{y}) -- ({x0 + 9.8},{y}) node[right,font=\footnotesize] {{random samples}};')
    L.append(rf'\draw[line width=1.6pt] ({x0 + 12.4},{y - .1}) -- ({x0 + 12.6},{y + .1}) ({x0 + 12.4},{y + .1}) -- ({x0 + 12.6},{y - .1});\draw[line width=.8pt] ({x0 + 12.5},{y}) circle[radius=.19];\node[right,font=\footnotesize] at ({x0 + 12.7},{y}) {{smallest}};')
    chart = tikz(L)
    # (b) the mechanism: a white face whose three black neighbours all point away
    cyc = nx.cycle_basis(m.Q_graph(s))[0]
    y_ = next(f for f in m.white if set(m.F[f]) == set(cyc))
    nb = [m.black_face(a_, b_) for a_, b_ in zip(m.F[y_], m.F[y_][1:] + m.F[y_][:1])]
    assert all(t in m.A for t in nb) and all(s[m.A.index(t)] not in m.F[y_] for t in nb)
    # and conversely on all twelve states: Q_z contains the triangle of a white face iff its three black neighbours point away
    for z in states:
        for f in inner:
            nbf = [m.black_face(a_, b_) for a_, b_ in zip(m.F[f], m.F[f][1:] + m.F[f][:1])]
            away = all(z[m.A.index(t)] not in m.F[f] for t in nbf)
            tri = all(m.Q_graph(z).has_edge(a_, b_) and tuple(sorted((a_, b_))) in {tuple(sorted(e)) for t, e in zip(m.A, m.Q(z)) if t in nbf}
                      for a_, b_ in zip(m.F[f], m.F[f][1:] + m.F[f][:1]))
            assert away == tri
    p = P(0.47).base()
    shade_faces(p, [y_], 'af tint')
    p.state(s, 'bf s', only=nb)
    for t in m.A:
        if t not in nb:
            p.wedge(t, s[m.A.index(t)], 'fill=black!45,draw=black!45')
    p.lines([e for t, e in zip(m.A, m.Q(s)) if t in nb], 'bf Q,line width=2pt').vertices()
    side = (r'\begin{tabular}{@{}c@{\hspace{5mm}}c@{}}' + small(p.tex()) + r' & \begin{minipage}[b][5.4cm][c]{7.6cm}\footnotesize (b) The mechanism behind the failures at the extremes, on the state $s_{' + str(nm[s])
            + r'}$ of the running example. The three black faces round the hatched white face all put their wedge (blue) at the corner away from it, so their opposite edges close a triangle (heavy dashes). '
            r'The 12-vertex counterexample on page ' + pg('canonical') + r' fails through a face of this kind.\end{minipage}\end{tabular}')
    CERT['open'] = dict(open_statements=[dict(statement=a_, every_case_two_programs=b_, every_case_one_program=c_, sampled_to=d_) for a_, b_, c_, d_ in bars],
                        refuted=[dict(statement=a_, counterexample_at=b_, known_smallest=c_) for a_, b_, c_ in dead], quoted_not_recomputed=True, mechanism_face=y_)
    return (r'\begin{tabular}{@{}c@{}}' + chart + r'\\[1mm]\begin{minipage}{14cm}\centering\footnotesize (a) How far each open statement was tested, and where a counterexample to each refuted one is known. Logarithmic scale.\end{minipage}\\[4mm]'
            + side + r'\end{tabular}')

# ---------------------------------------------------------------------------
@fig('random')
def random_fig():
    H = m.spoke_graph()
    nodes = list(H)
    Lap = sp.Matrix(len(nodes), len(nodes), lambda i, j: H.degree(nodes[i]) if i == j else -int(H.has_edge(nodes[i], nodes[j])))
    tau = int(Lap[1:, 1:].det())
    target = {}
    for x in nodes:
        fixed = (x[0] == 't' and x[1] == m.t0) or (x[0] == 'v' and x[1] in m.roots)
        target[x] = H.degree(x) - (0 if fixed else 1)
    good = []
    for z in states:
        Hz = H.copy()
        Hz.remove_edges_from((('t', t), ('v', v)) for t, v in zip(m.A, z))
        if nx.is_tree(Hz):
            assert all(Hz.degree(x) == target[x] for x in nodes)
            good.append(z)
    assert sorted(good) == sorted(tree_states)
    M = len(good)
    assert sum(target.values()) == 2 * (len(nodes) - 1)
    # uniform spanning trees by Wilson's algorithm, fixed seed
    rng = np.random.default_rng(2026)
    nbr = {x: list(H[x]) for x in nodes}

    def wilson():
        root = nodes[0]
        intree = {root}
        par = {}
        for x in nodes:
            u = x
            while u not in intree:
                par[u] = nbr[u][rng.integers(len(nbr[u]))]
                u = par[u]
            u = x
            while u not in intree:
                intree.add(u)
                u = par[u]
        return [(x, par[x]) for x in nodes if x != root]
    N = 4000
    miss = Counter()
    first = None
    for _ in range(N):
        tr = wilson()
        deg = Counter(x for e in tr for x in e)
        k = sum(deg[x] != target[x] for x in nodes)
        miss[k] += 1
        if first is None and k >= 6:
            first = (tr, deg)

    def draw(tree_edges, deg=None):
        p = P(U2).base()
        rr_ = R + draw_ring
        for a_, b_ in H.edges():
            t, v = (a_[1], b_[1]) if a_[0] == 't' else (b_[1], a_[1])
            on = (a_, b_) in tree_edges or (b_, a_) in tree_edges
            st = 'bf kept' if on else 'bf cut'
            if t == m.t0:
                th = ang(xy[v])
                d = (-90 - th + 180) % 360 - 180
                p.add(rf'\draw[{st}] {pt(xy[v])} -- ({th:.2f}:{rr_}) arc[start angle={th:.2f},end angle={th + d:.2f},radius={rr_}];')
            else:
                p.add(rf'\draw[{st}] {pt(p.cen[t])} -- {pt(xy[v])};')
        for t in m.black:
            p.add(rf'\fill {pt(p.cen[t])} ++(-1.7pt,-1.7pt) rectangle ++(3.4pt,3.4pt);')
        p.vertices()
        if deg is not None:
            for x in nodes:
                if deg[x] != target[x]:
                    q = p.cen[x[1]] if x[0] == 't' else xy[x[1]]
                    p.add(rf'\draw[line width=1.1pt] {pt(q)} circle[radius=5pt];')
        return p
    from draw import RING as draw_ring
    z = r
    tz = [e for e in H.edges() if not (e[0][0] == 't' and e[0][1] in m.A and z[m.A.index(e[0][1])] == e[1][1])
          and not (e[1][0] == 't' and e[1][1] in m.A and z[m.A.index(e[1][1])] == e[0][1])]
    assert len(tz) == len(nodes) - 1
    a = cell(draw(set(tz)).tex(), rf'(a) A good state as a spanning tree of the spoke graph (bold). Every black centre keeps two of its three spokes and every non-root vertex loses exactly one. The outer centre and the roots keep all.', 7.1)
    tr, deg = first
    nbad = sum(deg[x] != target[x] for x in nodes)
    b = cell(draw(set(tr), deg).tex(), rf'(b) A spanning tree drawn at random. The {nbad} ringed points have the wrong number of spokes.', 7.1)
    # (c) histogram of the number of wrong points
    ks = list(range(0, max(miss) + 1))
    w, h = 5.4, 3.4
    top = max(miss.values())
    L = [rf'\draw[line width=.5pt] (0,{h}) -- (0,0) -- ({w},0);']
    bw = w / len(ks)
    for i, k in enumerate(ks):
        hh_ = h * miss[k] / top
        L.append(rf'\fill[black!{78 if k == 0 else 45}] ({i * bw + .06},0) rectangle ({(i + 1) * bw - .06},{hh_:.3f});')
        if k % 2 == 0:
            L.append(rf'\node[font=\footnotesize,anchor=north] at ({(i + .5) * bw},-.03) {{${k}$}};')
    L.append(rf'\node[font=\footnotesize,anchor=north] at ({w / 2},-.5) {{points with the wrong number of spokes}};')
    L.append(rf'\node[font=\footnotesize,anchor=south east] at ({w},{h + .05}) {{{N} random spanning trees}};')
    L.append(rf'\node[font=\footnotesize,anchor=south west,inner sep=1pt] at (.0,{h * miss[0] / top + .08}) {{{miss[0]} exact}};')
    c = cell(r'\begin{minipage}[c][6.9cm][c]{7.1cm}\centering ' + tikz(L) + r'\end{minipage}',
             rf'(c) How far random trees fall from the target. Exact hits: {miss[0]} of {N}; the expected number is {N * M / tau:.3f}.', 7.1)
    led = (r'\begin{minipage}[c][6.9cm][c]{7.1cm}\footnotesize\renewcommand{\arraystretch}{1.5}\begin{tabular}{@{}lr@{}}\toprule '
           r'\textbf{Running example} & \\\midrule '
           rf'points of the spoke graph & {len(nodes)}\\ spokes & {H.number_of_edges()}\\ '
           rf'spanning trees & ${tau}$\\ '
           rf'with the prescribed degrees & {M}\\\midrule '
           rf'chance for a random tree & about $1/{round(tau / M)}$\\ '
           rf'chance for a random state & ${M}/{len(states)}$\\\bottomrule\end{{tabular}}\end{{minipage}}')
    CERT['random'] = dict(spanning_trees=tau, prescribed=M, sample=N, seed=2026, wrong_points_histogram=dict(sorted(miss.items())))
    return grid([a, b, c, led], 2)
