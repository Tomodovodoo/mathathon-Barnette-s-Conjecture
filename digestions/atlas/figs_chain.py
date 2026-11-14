"""Figures for the main chain: pages chain, pairs, disk, sum, polynomial,
involutions, heights, recovery, primal. Every drawn object is computed in
lib.py or here, with an assertion next to it."""
import lib
from lib import *

U2 = 0.615          # two panels across: 2 * 11.6 * U2 + gap = 15.3 cm
U4 = 0.25          # four across
DISK = run['disk']
DARCS = list(zip(DISK['cycle'], DISK['cycle'][1:] + DISK['cycle'][:1]))


def pair_panel(a, b, u, q=False, d=True, shade=None):
    p = P(u).base()
    if shade:
        shade_faces(p, shade)
    p.state(a, 'bf r').state(b)
    if q:
        p.lines(m.Q(b), 'bf Q')
    if d:
        p.arrows(m.D(a, b))
    return p.vertices()


def qcycle_face(z):
    """The white face bounded by the cycle of Q_z, if Q_z has one."""
    cyc = nx.cycle_basis(m.Q_graph(z))
    out = []
    for c in cyc:
        f = [i for i in m.white if set(m.F[i]) == set(c)]
        assert len(c) == 3 and len(f) == 1          # on this example every cycle of Q is a white face
        out += f
    return out


# ---------------------------------------------------------------------------
@fig('chain')
def chain():
    u = 0.235
    th = {
        'G': P(u).base(shade=False).graphG(dots=False).graphG('bf cycle', [m.dual[m.e0]], dots=False).dotsG(1.0),
        'T': P(u).base().vertices(),
        'state': P(u).base().state(s).vertices(),
        'pair': P(u).base().state(r, 'bf r').state(s).vertices(),
        'disk': shade_faces(P(u).base(), DISK['white']).arrows(m.D(r, s)).vertices(),
        'forest': P(u).base().state(r).lines(m.Q(r), 'bf Q').vertices(),
        'wtree': P(u).base().white_tree(rec, r).vertices(),
        'trees': P(u).base().lines(rec['P'], 'bf P').vertices(classes=rec['parts']),
        'cycle': P(u).base(shade=False).graphG(dots=False).graphG('bf cycle', rec['hamiltonian'], dots=False),
    }
    names = list(th)
    pre = ''.join(rf'\newsavebox\cb{chr(97 + i)}\sbox\cb{chr(97 + i)}{{{small(th[k].tex())}}}' for i, k in enumerate(names))
    cap = {'G': r'cubic graph $G$,\\root face, edge $e$', 'T': r'its dual $T$,\\faces two-coloured',
           'state': r'a state: one corner\\per black face', 'pair': r'a pair: two states,\\different everywhere',
           'disk': r'the cycles of $D$\\bound disks', 'forest': r'a state whose\\opposite edges are a forest',
           'wtree': r'a tree on\\the white faces', 'trees': r'two induced trees',
           'cycle': r'a Hamiltonian cycle\\avoiding $e$'}
    dx, dy = 4.5, 5.2
    pos = {'G': (0, 0), 'T': (dx, 0), 'state': (2 * dx, 0), 'pair': (2 * dx, -dy), 'disk': (dx, -dy), 'forest': (0, -dy),
           'wtree': (0, -2 * dy), 'trees': (dx, -2 * dy), 'cycle': (2 * dx, -2 * dy)}
    h = 1.36
    L = []
    main = 'line width=2.6pt,draw=black'
    free = 'line width=2.6pt,draw=black,dash pattern=on 5pt off 2.5pt'

    def seg(a, b, style, label, above=True, off=0.0):
        (x1, y1), (x2, y2) = pos[a], pos[b]
        if y1 == y2:
            sgn = 1 if x2 > x1 else -1
            L.append(rf'\draw[{style}] ({x1 + sgn * h},{y1 + off}) -- ({x2 - sgn * h},{y2 + off});')
            L.append(rf'\node[font=\footnotesize,align=center,anchor={"south" if above else "north"}] at ({(x1 + x2) / 2},{y1 + off + (.08 if above else -.08)}) {{{label}}};')
        else:
            L.append(rf'\draw[{style}] ({x1},{y1 - h - .95}) -- ({x2},{y2 + h + .05});')
            L.append(rf'\node[font=\footnotesize,align=left,anchor=west] at ({x1 + .15},{(y1 - h - .95 + y2 + h) / 2}) {{{label}}};')

    seg('G', 'T', main, rf'plane duality')
    seg('T', 'state', free, rf'cut inequality\\page {pg("pairs")}')
    seg('state', 'pair', free, rf'the same inequality\\gives two at once')
    seg('pair', 'disk', main, rf'disk identity\\page {pg("disk")}')
    # the hard step: four parallel lines between the same two stations
    alts = [('sum', 'sum'), ('polynomial', 'polynomial'), ('involutions', 'pairing'), ('determinant', 'matrix')]
    (x1, y1), (x2, y2) = pos['disk'], pos['forest']
    for k, (slug, name) in enumerate(alts):
        y = y1 + 1.05 - k * .7
        L.append(rf'\draw[{free}] ({x1 - h},{y}) -- ({x2 + h},{y});')
        L.append(rf'\node[font=\footnotesize,fill=white,inner sep=1.2pt] at ({(x1 + x2) / 2},{y}) {{{name} {pg(slug)}}};')
    seg('forest', 'wtree', main, rf'delete the chosen\\spokes, page {pg("recovery")}')
    seg('wtree', 'trees', main, r'one side per\\black face')
    seg('trees', 'cycle', main, r'the curve\\between them')
    # the primal reading runs beside the last three steps
    y = pos['wtree'][1] - h - 1.45
    L.append(rf'\draw[line width=1.2pt,draw=black] ({pos["wtree"][0]},{y + .3}) |- ({pos["cycle"][0]},{y}) -- ({pos["cycle"][0]},{y + .3});')
    L.append(rf'\node[font=\footnotesize,fill=white,inner sep=1.5pt] at ({dx},{y}) {{the same steps read inside $G$, page {pg("primal")}}};')
    # open routes from a pair to a forest state: dotted, above the second row
    y = pos['pair'][1] + h + .45
    L.append(rf'\draw[line width=1.2pt,draw=black,dash pattern=on 1.2pt off 2pt] ({pos["pair"][0] - .6},{pos["pair"][1] + h}) |- ({pos["forest"][0] + .0},{y}) -- ({pos["forest"][0]},{pos["forest"][1] + h});')
    L.append(rf'\node[font=\footnotesize,fill=white,inner sep=1.5pt] at ({dx - .3},{y}) {{not proved: exchange moves {pg("rainbow")}, contraction {pg("induction")}}};')
    # refuted shortcuts: dead-end stubs to the right of the pair station
    stubs = [(rf'highest state\\page {pg("canonical")}', 1.11), (rf'two conditions\\of three, page {pg("matroids")}', .37),
             (rf'linear program\\page {pg("lp")}', -.37), (rf'one determinant\\page {pg("determinant")}', -1.11)]
    x0 = pos['pair'][0] + h
    for label, yy in stubs:
        y = pos['pair'][1] + yy
        L.append(rf'\draw[af stub] ({x0},{y}) -- ({x0 + .5},{y});\draw[line width=1.4pt] ({x0 + .5},{y - .13}) -- ({x0 + .5},{y + .13});')
        L.append(rf'\node[font=\footnotesize,anchor=west,align=left,inner sep=1pt] at ({x0 + .6},{y}) {{{label}}};')
    L.append(rf'\node[font=\footnotesize\itshape,anchor=south west,inner sep=1pt] at ({x0 + .1},{pos["pair"][1] + 1.5}) {{refuted shortcuts}};')
    for i, k in enumerate(names):
        x, y = pos[k]
        L.append(rf'\node[inner sep=0pt] at ({x},{y}) {{\usebox\cb{chr(97 + i)}}};')
        L.append(rf'\node[font=\footnotesize,align=center,anchor=north,inner sep=1pt] at ({x},{y - h}) {{\textbf{{{i + 1}}}\ \ {cap[k]}}};')
    # legend
    lx, ly = 2 * dx + h + .15, 1.1
    L.append(rf'\draw[{main}] ({lx},{ly}) -- ++(.7,0) node[right,font=\footnotesize,text width=1.45cm,align=left] {{forced step}};')
    L.append(rf'\draw[{free}] ({lx},{ly - .6}) -- ++(.7,0) node[right,font=\footnotesize,text width=1.45cm,align=left] {{existence step}};')
    return pre + tikz(L)


# ---------------------------------------------------------------------------
@fig('pairs')
def pairs_fig():
    # (a) the cut inequality for one set S on the running example
    S = set(DISK['interior'])
    assert len(S) == 3
    p = P(U2).base()
    tot = 0
    for t in m.A:
        k = min(2, len(set(m.F[t]) & S))
        tot += k
        if k:
            shade_faces(p, [t], 'af tintb')
            facelabel(p, t, rf'${k}$')
    lhs, rhs = m.cut_inequality(S)
    assert (lhs, rhs) == (tot, 2 * len(S)) and lhs >= rhs
    p.vertices()
    for v in S:
        ring(p, v)
    a = cell(p.tex(), rf'(a) $S$ = the three ringed vertices. The marked black faces count ${"+".join(str(min(2, len(set(m.F[t]) & S))) for t in m.A if set(m.F[t]) & S)}={lhs}\geq 2|S|={rhs}$.', 7.1)
    # (b) the two states it yields
    b = cell(P(U2).base().state(r, 'bf r').state(s).vertices().tex(), '(b) Two states that differ at every black face: outlined wedges $r$, solid wedges $s$.', 7.1)
    # (c) the obstruction: a separating triangle with black faces just inside it
    T = gl['T']
    cap = gl['cap']
    inside = [v for v in T.V if v not in oc['model'].V]
    other = [i for i in T.white if not set(T.F[i]) & set(inside) and not set(T.F[i]) <= set(cap)]
    t0 = other[0]
    mod = rooted(T.F, T.F[t0])
    q, rad = auto_layout('glued-black-inner', mod)
    nst = len(mod.states())
    assert len(mod.pairs()) == 0 and nst > 0
    Sin = set(inside)
    p = P(U2, mod, q, rad).base()
    tot = 0
    for t in mod.A:
        k = min(2, len(set(mod.F[t]) & Sin))
        tot += k
        if k:
            shade_faces(p, [t], 'af tintb')
            facelabel(p, t, rf'${k}$')
    assert tot == 5 and 2 * len(Sin) == 6
    capedges = list(zip(cap, cap[1:] + cap[:1]))
    p.lines(capedges, 'af bold').vertices()
    for v in Sin:
        ring(p, v)
    c = cell(p.tex(), rf'(c) Another triangulation: the bold triangle has black faces just inside it. For the ringed set, ${tot}<{2 * len(Sin)}$, so no pair exists, although {nst} single states do.', 7.1)
    CERT['pairs'] = dict(S=sorted(S), lhs=lhs, rhs=rhs, obstruction=dict(faces=mod.F, t0=mod.t0, S=sorted(Sin), lhs=tot, rhs=6, states=nst, pairs=0))
    # (d) the incidence graph with r and s as a 2-factor
    p = P(U2).base().spokes(style='bf spoke', centres=False)
    for t, v in zip(m.A, s):
        p.add(rf'\draw[draw=bfS,line width=1.5pt] {pt(p.cen[t])} -- {pt(p.xy[v])};')
    for t, v in zip(m.A, r):
        p.add(rf'\draw[draw=bfR,line width=1.5pt,dash pattern=on 3pt off 1.6pt] {pt(p.cen[t])} -- {pt(p.xy[v])};')
    for t in m.A:
        p.add(rf'\fill {pt(p.cen[t])} ++(-1.7pt,-1.7pt) rectangle ++(3.4pt,3.4pt);')
    two = nx.Graph([(('t', t), ('v', v)) for z in (r, s) for t, v in zip(m.A, z)])
    assert all(dg == 2 for _, dg in two.degree())
    ncomp = nx.number_connected_components(two)
    p.vertices()
    d = cell(p.tex(), rf'(d) The same pair as spokes from the black centres: $s$ solid, $r$ dashed. Together they cover every centre and every vertex twice, in {ncomp} closed curves.', 7.1)
    return grid([a, b, c, d], 2)


# ---------------------------------------------------------------------------
def disk_base(u, states_=True):
    k = DISK
    p = P(u).base()
    return p, k


@fig('disk')
def disk_fig():
    k = DISK
    # (a) the census
    p = P(U2).base(tint={f: ('bfS!22!bfblack' if f in m.black else 'bfS!9') for f in k['faces']})
    p.state(r, 'bf s', only=k['black'])
    p.arrows(DARCS)
    for a_, b_ in k['inner_black_edges']:
        p.label(p.mid(a_, b_) + 0.0, r'$\ell$', 'af lab')
    p.vertices()
    for v in k['interior']:
        ring(p, v)
    assert k['B'] == k['I'] + k['l'] and k['B'] + k['W'] == 2 * k['I'] + k['h'] - 2 and 3 * (k['B'] - k['W']) == 2 * k['l'] - k['h']
    a = cell(p.tex(), rf'(a) Count. Inside the cycle: $B={k["B"]}$ black faces, $W={k["W"]}$ white faces, $I={k["I"]}$ vertices (ringed). On it: $h={k["h"]}$ edges, $\ell={k["l"]}$ of them with the black face inside. Each black face inside owns one wedge, so $B=I+\ell$.', 7.1)
    # (b) one more white face than black
    p = P(U2).base()
    shade_faces(p, k['white'], 'af tint')
    p.arrows(DARCS)
    for i, f in enumerate(sorted(k['white'], key=lambda f: -p.cen[f][1])):
        facelabel(p, f, rf'$w_{{{i + 1}}}$')
    for i, f in enumerate(sorted(k['black'], key=lambda f: -p.cen[f][1])):
        p.label(p.cen[f], rf'$b_{{{i + 1}}}$', 'inner sep=1pt')
    p.vertices()
    assert k['W'] == k['B'] + 1
    b = cell(p.tex(), rf'(b) Shade. The disk holds white faces $w_1,\dots,w_{{{k["W"]}}}$ and black faces $b_1,\dots,b_{{{k["B"]}}}$. Always $W=B+1$.', 7.1)
    # (c) turning: corner angles in units of 60 degrees
    rr = dict(zip(m.A, r))
    def angle(f, v):
        if f in m.white:
            return 1
        return 5 if rr[f] == v else -1
    turns = {}
    for v in k['cycle']:
        turns[v] = 3 - sum(angle(f, v) for f in k['faces'] if v in m.F[f])
    assert sum(turns.values()) == 6 and all(sum(angle(f, v) for v in m.F[f]) == 3 for f in k['faces'])
    assert all(sum(angle(f, v) for f in range(len(m.F)) if v in m.F[f] and f != m.t0) == 6 for v in k['interior'])
    p = P(U2).base(tint={f: ('bfS!22!bfblack' if f in m.black else 'bfS!9') for f in k['faces']})
    p.state(r, 'bf s', only=k['black'])
    p.arrows(DARCS)
    for f in k['faces']:
        for v in m.F[f]:
            if f in m.white:
                continue                                  # white corners are all 1 and are not written
            if rr[f] != v:
                p.add(rf'\node[font=\footnotesize,inner sep=0pt] at {pt(p.xy[v] + 0.6 * (p.cen[f] - p.xy[v]))} {{$-1$}};')
            else:
                p.add(rf'\node[font=\footnotesize,inner sep=0pt,text=white] at {pt(p.xy[v] + 0.3 * (p.cen[f] - p.xy[v]))} {{$\mathbf 5$}};')
    cen = sum(p.xy[v] for v in k['cycle']) / len(k['cycle'])
    for v in k['cycle']:
        d = p.xy[v] - cen
        p.label(p.xy[v] + 0.62 * d / np.hypot(*d), rf'$\mathbf{{{turns[v]:+d}}}$', 'af lab')
    p.vertices()
    order = [turns[v] for v in k['cycle']]
    ssum = ''.join(f'{t:+d}' for t in order).lstrip('+')
    c = cell(p.tex(), rf'(c) Turn. Unit $60^\circ$. Every white corner is $1$ (not written), a wedge corner is $5$, any other black corner $-1$. Each face sums to $3$ and each inner vertex to $6$, so the disk is flat. The bold numbers are the turns of the boundary: ${ssum}=6$, one full turn.', 7.1)
    led = (r'\begin{minipage}[c][6.9cm][c]{7.1cm}\centering\footnotesize\renewcommand{\arraystretch}{1.5}\begin{tabular}{@{}ll@{}}\toprule '
           r'\multicolumn{2}{@{}l}{\textbf{The same fact, three ways}}\\\midrule '
           rf'count & $3(B-W)=2\ell-h$:\quad $3({k["B"]}-{k["W"]})=2\cdot{k["l"]}-{k["h"]}$\\'
           rf'shade & $W=B+1$:\quad ${k["W"]}={k["B"]}+1$\\'
           rf'turn & total turning $=6\times 60^\circ$\\\midrule '
           r'\multicolumn{2}{@{}p{6.9cm}@{}}{Used later as: walking once round a cycle of $D$, black faces lie on the left three more times than on the right (or three fewer, clockwise). Here the sum is $'
           + str(k['delta_sum']) + r'$.}\\\bottomrule\end{tabular}\end{minipage}')
    CERT['disk'] = dict(B=k['B'], W=k['W'], I=k['I'], h=k['h'], l=k['l'], cycle=k['cycle'], turns=order, delta_sum=k['delta_sum'])
    return grid([a, b, c, led], 2)


# ---------------------------------------------------------------------------
def term_label(a_, b_):
    d = term[a_, b_]
    return rf'$(s_{{{nm[a_]}}},s_{{{nm[b_]}}})$\quad ${expo(d["sign"], d["vol"])}$'


@fig('sum')
def sum_fig():
    w = 11.6 * U4
    ordered = sorted(pairs, key=lambda p_: (m.Q_is_forest(p_[1]), nm[p_[1]], nm[p_[0]]))
    assert not m.Q_is_forest(ordered[0][1]) and ordered[0][1] == ordered[1][1]
    top = []
    for a_, b_ in ordered:
        p = P(U4).base()
        shade_faces(p, qcycle_face(b_))
        p.state(a_, 'bf r').state(b_).lines(m.Q(b_), 'bf Q').vertices()
        top.append(cell(small(p.tex()), term_label(a_, b_)))
    bottom = []
    notes = []
    for i, d in enumerate(group_data):
        g = sorted(d['pairs'], key=lambda p_: term[p_]['vol'])
        for a_, b_ in g:
            p = P(U4).base()
            p.state(b_).arrows(m.D(a_, b_)).vertices()
            bottom.append(cell(small(p.tex()), term_label(a_, b_)))
        fac = ''.join(rf'(1-{"e^{x}" if w_ == 1 else "e^{%dx}" % w_})' for w_ in sorted(d['W'], reverse=True))
        lead = term[g[0]]['sign']
        pre = ('-' if lead < 0 else '') + ('' if d['base'] == 0 else ('e^{x}' if d['base'] == 1 else 'e^{%dx}' % d['base']))
        notes.append(rf'cycle cover $D_{{{i + 1}}}$, its four orientations: the terms add up to ${pre}{fac}$')
    cols = '@{}' + 'c@{\\hspace{2.5mm}}' * 3 + 'c@{}'
    hd = lambda t: r'\multicolumn{4}{@{}l}{\footnotesize\textbf{' + t + r'}}\\[.8mm]'
    note = lambda t: r'\multicolumn{4}{c}{\footnotesize ' + t + r'}\\[2.2mm]'
    brace = (r'\multicolumn{2}{c}{\footnotesize$\underbrace{\hspace{' + f'{2 * w:.2f}' + r'cm}}_{\text{same }s,\ Q_s\text{ has a cycle (shaded): the two terms cancel}}$} & '
             r'\multicolumn{2}{c}{\footnotesize $Q_s$ is a forest: nothing to cancel with}\\[1mm]')
    body = (rf'\begin{{tabular}}{{{cols}}}' + hd('Grouped by the second state $s$ (solid wedges), with its opposite edges $Q_s$ dashed')
            + ' & '.join(top[:4]) + r'\\[.5mm]' + brace + ' & '.join(top[4:]) + r'\\[6mm]'
            + hd('Grouped by the cycle cover $D$ (arrows from the corner of $r$ to the corner of $s$)')
            + ' & '.join(bottom[:4]) + r'\\[.5mm]' + note(notes[0]) + ' & '.join(bottom[4:]) + r'\\[.5mm]' + note(notes[1]).replace(r'\\[2.2mm]', '')
            + r'\end{tabular}')
    return body


# ---------------------------------------------------------------------------
@fig('polynomial')
def polynomial_fig():
    cells = []
    for i, d in enumerate(group_data):
        g = sorted(d['pairs'], key=lambda p_: term[p_]['vol'])
        a_, b_ = g[0]
        p = P(U2).base()
        for k in d['cycles']:
            shade_faces(p, k['white'], 'af tint')
        p.arrows(m.D(a_, b_))
        for k in d['cycles']:
            for j, f in enumerate(sorted(k['white'], key=lambda f: -p.cen[f][1])):
                facelabel(p, f, rf'${j + 1}$')
        p.vertices()
        ws = sorted(d['W'], reverse=True)
        cells.append(cell(p.tex(), rf'({"ab"[i]}) Cycle cover $D_{{{i + 1}}}$. Its two cycles enclose ${ws[0]}$ and ${ws[1]}$ white faces: product ${ws[0] * ws[1]}$.', 7.1))
    # (c) the long cycle slid onto spokes
    k = run['D_cycles'][0]
    cyc = k['ccw_cycle']
    p = P(U2).base()
    shade_faces(p, k['white'], 'af tint')
    p.spokes(centres=False)
    for x, y in zip(cyc, cyc[1:] + cyc[:1]):
        ct = p.cen[m.black_face(x, y)]
        p.add(rf'\draw[bf D,dash pattern=on 2pt off 1.6pt,line width=.8pt] {pt(xy[x])} -- {pt(xy[y])};')
        p.add(rf'\draw[bf detour] {pt(xy[x])} -- {pt(ct)};')
        p.add(rf'\draw[bf detour,shorten >=1.6pt,-{{Stealth[length=4.2pt,width=3.6pt]}}] {pt(ct)} -- {pt(xy[y])};')
    for t in m.A:
        p.add(rf'\fill {pt(p.cen[t])} ++(-1.7pt,-1.7pt) rectangle ++(3.4pt,3.4pt);')
    p.vertices()
    assert abs(k['L_diff'] - k['W']) < 1e-9
    c = cell(p.tex(), rf'(c) Why the count appears. Slide each arrow onto the two spokes through its black centre. The spoke path encloses exactly the shaded white faces, and the weights give each of them circulation one, so reversing the cycle changes the product by ${k["W"]}x$ to first order.', 7.1)
    c2, c3 = Fp.nth(2), Fp.nth(3)
    prods = [math.prod(d['W']) for d in group_data]
    assert abs(c2) == sum(prods)
    led = (r'\begin{minipage}[c][6.9cm][c]{7.1cm}\centering\footnotesize\renewcommand{\arraystretch}{1.6}\begin{tabular}{@{}p{6.9cm}@{}}\toprule '
           r'\textbf{The polynomial}\quad $F(w)=\sum_{(r,s)}\pm\prod_{t}w_{t,s(t)}$,\\ one variable $w_{t,v}$ for each black face $t$ and corner $v$.\\\midrule '
           r'At $w\equiv 1$ the eight signs add up to $0$.\\'
           rf'Put $w_{{t,v}}=1+x\,a_{{t,v}}$ with the weights of (c):\\ $F={sp.latex(c2)}x^2{"+" if c3 > 0 else "-"}{sp.latex(abs(c3))}x^3+\cdots$\\'
           rf'Lowest coefficient: ${prods[0]}+{prods[1]}={sum(prods)}$, the two products in (a) and (b). Both have the same sign, so it cannot vanish.\\\bottomrule\end{{tabular}}\end{{minipage}}')
    CERT['polynomial'] = dict(F=str(Fpoly), products=prods)
    return grid(cells + [c, led], 2)


# ---------------------------------------------------------------------------
@fig('involutions')
def involutions_fig():
    def qp(a_, b_):
        p = P(U2).base()
        shade_faces(p, qcycle_face(b_))
        p.state(a_, 'bf r').state(b_)
        qd = m.Q_directed(a_, b_)
        cyc = m.directed_cycles(qd)[0]
        on = set(zip(cyc, cyc[1:] + cyc[:1]))
        p.lines([e for e in m.Q(b_) if (e[0], e[1]) not in on and (e[1], e[0]) not in on], 'bf Q')
        p.arrows([e for e in qd if e in on], 'bf Qdir')
        return p.vertices()
    assert term[r, s]['sign'] == -term[r2, s]['sign'] and term[r, s]['vol'] == term[r2, s]['vol']
    changed = run['changed']
    a = cell(qp(r, s).tex(), rf'(a) The pair $(s_{{{nm[r]}}},s_{{{nm[s]}}})$, term ${expo(term[r, s]["sign"], term[r, s]["vol"])}$. Dashed arrows: the cycle of $Q_s$, from the corner of $r$ to the third corner.', 7.1)
    b = cell(qp(r2, s).tex(), rf'(b) Move $r$ to the third corner in the {len(changed)} faces on that cycle. The new pair $(s_{{{nm[r2]}}},s_{{{nm[s]}}})$ has the same $s$, the cycle reversed, and term ${expo(term[r2, s]["sign"], term[r2, s]["vol"])}$.', 7.1)
    top = grid([a, b], 2)
    # the two squares of orientations
    sq = []
    for i, d in enumerate(group_data):
        ks = d['cycles']
        g = d['pairs']
        base = min(g, key=lambda p_: term[p_]['vol'])
        def flip(pair_, k):
            a_, b_ = pair_
            on = set(k['cycle'])
            arcs = dict(m.D(a_, b_))
            na = tuple(b0 if a0 in on else a0 for a0, b0 in zip(a_, b_))
            nb = tuple(a0 if a0 in on else b0 for a0, b0 in zip(a_, b_))
            assert (na, nb) in term
            return na, nb
        k_long, k_short = sorted(ks, key=lambda k: -k['h'])
        p00 = base
        p10 = flip(p00, k_long)
        p01 = flip(p00, k_short)
        p11 = flip(p10, k_short)
        assert {p00, p10, p01, p11} == set(g)
        assert term[p00]['sign'] == -term[p10]['sign'] == -term[p01]['sign'] == term[p11]['sign']
        def th(pr):
            a_, b_ = pr
            pp = P(U4).base().state(b_).arrows(m.D(a_, b_)).vertices()
            mark = r'\ \ tree' if m.Q_is_forest(b_) else r'\ \ cyclic'
            return cell(small(pp.tex()), rf'${expo(term[pr]["sign"], term[pr]["vol"])}$' + mark)
        h = r'\footnotesize$\leftrightarrow$'
        v = r'\footnotesize$\updownarrow$'
        sq.append(r'\begin{tabular}{@{}c@{\,}c@{\,}c@{}}' + th(p00) + ' & ' + r'\raisebox{1.6cm}{' + h + '}' + ' & ' + th(p10) + r'\\[-.5mm]' + v + ' & & ' + v + r'\\[-.5mm]'
                  + th(p01) + ' & ' + r'\raisebox{1.6cm}{' + h + '}' + ' & ' + th(p11) + r'\\[1mm]\multicolumn{3}{c}{\footnotesize\begin{minipage}{6.6cm}\centering '
                  + rf'({"cd"[i]}) Cover $D_{{{i + 1}}}$. $\leftrightarrow$ reverses the long cycle (exponent changes by {k_long["W"]}), $\updownarrow$ the short one (by {k_short["W"]}). Each reversal flips the sign.'
                  + r'\end{minipage}}\end{tabular}')
    CERT['involutions'] = dict(first=[[nm[r], nm[s]], [nm[r2], nm[s]]], changed_faces=changed)
    return r'\begin{tabular}{@{}c@{}}' + top + r'\\[3mm]' + grid(sq, 2, colsep='6mm') + r'\end{tabular}'


# ---------------------------------------------------------------------------
@fig('heights')
def heights_fig():
    lo, hi = by_name[0], by_name[len(states) - 1]
    one = next(states[j] for i, j in state_order.edges() if states[i] == lo)
    def hp(z, prev=None):
        p = P(U2).base()
        h = hs[sid[z]]
        shade_faces(p, [w for w, v in zip(inner, h) if v > 0], 'af tint')
        if prev is not None:
            diff = [t for t, a_, b_ in zip(m.A, prev, z) if a_ != b_]
            p.state(prev, 'bf r', only=diff)
        p.state(z)
        for w, v in zip(inner, h):
            facelabel(p, w, rf'$\mathbf{{{v}}}$')
        for w in m.white:
            if w not in inner:
                p.add(rf'\node[font=\footnotesize,text=black!55] at {pt(p.cen[w])} {{$0$}};')
        return p.vertices()
    ndiff = sum(a_ != b_ for a_, b_ in zip(lo, one))
    assert ndiff == 3
    cells = [cell(hp(lo).tex(), rf'(a) The lowest state $s_0$. Height $0$ on every white face.', 7.1),
             cell(hp(one, lo).tex(), rf'(b) One clock move: the three wedges round one white face each step to the next corner (old positions outlined). That face rises to $1$. This is $s_{{{nm[one]}}}$.', 7.1),
             cell(hp(s).tex(), rf'(c) The state $s=s_{{{nm[s]}}}$ of the running pair. Heights add up to its volume ${vol[sid[s]]}$, the exponent in $e^{{{vol[sid[s]]}x}}$.', 7.1),
             cell(hp(hi).tex(), rf'(d) The highest state $s_{{{nm[hi]}}}$, volume ${vol[sid[hi]]}$. Grey zeros: the three white faces on the outer circle never move.', 7.1)]
    CERT['heights'] = dict(lowest=nm[lo], first_move=nm[one], highest=nm[hi], volumes={nm[z]: vol[sid[z]] for z in states})
    return grid(cells, 2)


# ---------------------------------------------------------------------------
@fig('recovery')
def recovery_fig():
    a = cell(P(U2).base().state(r).lines(m.Q(r), 'bf Q').vertices().tex(),
             rf'(a) The state $s_{{{nm[r]}}}$. Its opposite edges (dashed) form a forest: three trees, one hanging from each root.', 7.1)
    b = cell(P(U2).base().spokes(deleted=list(zip(m.A, r)), outer=True).white_tree(rec, r).vertices().tex(),
             r'(b) Delete the chosen spoke in each black face (dotted). The other spokes form a spanning tree (bold), so the curves crossing the deleted spokes form a tree on the white faces. The ringed white face touches $e$.', 7.1)
    p = P(U2).base()
    for t, ch in rec['chosen'].items():
        p.add(r'\draw[bf wtree,line width=.7pt] ' + p.curve_tex(p.white_curves(rec, t, ch['corner'])) + ';')
    p.lines(rec['P'], 'bf P').vertices()
    assert len(rec['P']) == len(m.A) + 1
    c = cell(p.tex(), rf'(c) Each tree edge passes two sides of its black face. Select the side nearer the leaves, and add $e$: {len(rec["P"])} selected edges, one on every face.', 7.1)
    d = cell(P(U2).base().lines(rec['P'], 'bf P').graphG('bf cycle', rec['hamiltonian'], dots=False).vertices(classes=rec['parts']).tex(),
             rf'(d) The selected edges are two trees (disks, squares) through all {len(m.V)} vertices, with no other edge inside either class. The closed curve between them visits all {len(m.F)} faces: a Hamiltonian cycle of $G$.', 7.1)
    CERT['recovery'] = dict(state=nm[r], P=rec['P'], parts=rec['parts'], cycle=rec['cycle_order'])
    return grid([a, b, c, d], 2)


# ---------------------------------------------------------------------------
@fig('primal')
def primal_fig():
    k = DISK
    barrier = {und(a_, b_) for a_, b_ in DARCS}
    cut = [g for g, te in m.cross.items() if und(*te) in barrier]
    assert len(cut) == k['h']
    inside = set(k['faces'])
    assert all((g[0] in inside) != (g[1] in inside) for g in cut)
    # (a) G with its two classes, the root vertex and the edge e
    p = P(U2).base(shade=False).graphG(dots=False).graphG('bf cycle', [m.dual[m.e0]], dots=False).dotsG(2.0)
    p.label(p.cen[m.t0] + np.array([.9, .0]), r'$t_0$', 'inner sep=1pt')
    a = cell(p.tex(), rf'(a) $G$ on the same layout: one vertex per face of $T$, black or white, {m.G.number_of_edges()} edges. The vertex $t_0$ sits in the collar. The purple edge is $e$.', 7.1)
    # (b) a cycle of D is an edge cut; its disk is one shore
    p = P(U2).base(shade=False)
    shade_faces(p, k['faces'], 'af soft')
    p.graphG(dots=False)
    p.graphG('af bold', cut, dots=False).dotsG(2.0)
    nb, nw = sum(f in m.black for f in inside), sum(f in m.white for f in inside)
    assert nw == nb + 1
    b = cell(p.tex(), rf'(b) The long cycle of $D$ is a cut of $G$ with {len(cut)} edges (bold). The shore away from $t_0$ (tinted) holds {nb} black and {nw} white vertices. One more white: the disk identity.', 7.1)
    # (c) the state as a flow: each black vertex sends its unit to a face of G
    p = P(U2).base(shade=False).graphG(dots=False)
    for t, v in zip(m.A, r):
        p.add(rf'\draw[bf D] {pt(p.cen[t])} -- {pt(p.xy[v] + 0.18 * (p.cen[t] - p.xy[v]))};')
    p.dotsG(2.0)
    for v in m.V:
        if v in m.roots:
            p.add(rf'\node[font=\footnotesize,text=black!60] at {pt(p.xy[v] * 0.985)} {{$\circ$}};')
        else:
            p.add(rf'\node[draw=black!70,circle,inner sep=1.3pt,line width=.4pt,fill=white] at {pt(p.xy[v])} {{}};')
    assert sorted(r) == sorted(m.X)
    c = cell(p.tex(), rf'(c) A state inside $G$. Small circles mark the faces of $G$ (vertices of $T$). Each black vertex except $t_0$ points into one of its three faces, and each of the {len(m.X)} faces away from $t_0$ is chosen once.', 7.1)
    # (d) the matching whose removal leaves the cycle
    M = [g for g in m.G.edges() if und(*g) not in {und(*h_) for h_ in rec['hamiltonian']}]
    assert len(M) == len(m.F) // 2 and len({v for g in M for v in g}) == len(m.F) and m.dual[m.e0] in [und(*g) for g in M]
    p = P(U2).base(shade=False).graphG('bf cycle', rec['hamiltonian'], dots=False)
    p.graphG('af half', M, dots=False).dotsG(2.0)
    d = cell(p.tex(), rf'(d) The outcome in $G$: a perfect matching (dashed, {len(M)} edges, $e$ among them) whose removal leaves one cycle through all {len(m.F)} vertices.', 7.1)
    CERT['primal'] = dict(cut_edges=len(cut), shore=dict(black=nb, white=nw), matching=M)
    return grid([a, b, c, d], 2)
